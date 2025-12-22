---
title: "Delegation Architecture Patterns"
description: "Patterns for structuring oversight and control in AI delegation"
sidebar:
  order: 1
---

# Delegation Architecture Patterns

These patterns define how to structure the relationship between principals (humans or trusted systems) and AI agents. They determine who makes decisions, how oversight works, and how trust is calibrated.

---

## Supervisor Chain

### Intent
Create hierarchical oversight where each level can only delegate to less-privileged levels, with escalation paths for uncertainty.

### Motivation
You need AI assistance but can't have a single point of failure. Different decisions require different levels of authority. You want to catch errors before they propagate.

### Structure
```
┌─────────────────────────────────────────────────┐
│                 Human Principal                  │
│            (final authority, rare)               │
└────────────────────┬────────────────────────────┘
                     │ escalate
┌────────────────────▼────────────────────────────┐
│              Senior Supervisor                   │
│     (high-stakes decisions, occasional)          │
└────────────────────┬────────────────────────────┘
                     │ escalate
┌────────────────────▼────────────────────────────┐
│             Junior Supervisor                    │
│      (routine oversight, frequent)               │
└────────────────────┬────────────────────────────┘
                     │ delegate
┌────────────────────▼────────────────────────────┐
│              Worker Agents                       │
│        (task execution, continuous)              │
└─────────────────────────────────────────────────┘
```

### Key Dynamics

**Downward delegation**: Each level can only delegate tasks within its authority. A junior supervisor cannot grant a worker permission to make high-stakes decisions.

**Upward escalation**: Uncertainty or high stakes trigger escalation. Workers escalate to junior supervisors; junior supervisors escalate to senior.

**Authority attenuation**: Each delegation step reduces available capabilities. Workers have fewer permissions than their supervisors.

### Implementation

```python
class SupervisorChain:
    def __init__(self, levels: list[Supervisor]):
        self.levels = levels  # Ordered from worker to principal

    def process_task(self, task: Task, level: int = 0):
        supervisor = self.levels[level]

        # Check if this level can handle the task
        if task.stakes > supervisor.max_stakes:
            return self.escalate(task, level)

        if supervisor.confidence(task) < supervisor.min_confidence:
            return self.escalate(task, level)

        # Execute with bounded permissions
        result = supervisor.execute(
            task,
            permissions=self.attenuate(supervisor.permissions, level)
        )

        # Log for audit
        self.audit_log.record(task, result, level)
        return result

    def escalate(self, task: Task, current_level: int):
        if current_level >= len(self.levels) - 1:
            return self.human_fallback(task)
        return self.process_task(task, current_level + 1)
```

### Consequences

**Benefits**:
- Clear authority hierarchy
- Natural escalation paths
- Defense in depth (multiple review layers)
- Matches organizational structures

**Costs**:
- Latency increases with escalation depth
- Requires well-defined escalation criteria
- Can create bottlenecks at upper levels
- Complex to tune thresholds

### Known Uses
- Customer service bots with human escalation
- Automated code review with senior engineer approval
- Trading systems with risk manager oversight

### Related Patterns
- Combines with **Graduated Autonomy** (escalation frequency decreases over time)
- Use **Circuit Breaker** at each level to prevent cascade failures
- **Consensus Committee** can replace single supervisors at critical levels

---

## Consensus Committee

### Intent
Require agreement among multiple independent agents before taking action, preventing any single point of failure or corruption.

### Motivation
High-stakes decisions shouldn't depend on a single AI. You want robustness against both errors and adversarial manipulation. Different models may catch different failure modes.

### Structure
```
                    ┌─────────────┐
                    │   Request   │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
    ┌─────────┐       ┌─────────┐       ┌─────────┐
    │ Agent A │       │ Agent B │       │ Agent C │
    │ (GPT-4) │       │ (Claude)│       │(Gemini) │
    └────┬────┘       └────┬────┘       └────┬────┘
         │                 │                 │
         ▼                 ▼                 ▼
    ┌─────────────────────────────────────────────┐
    │              Consensus Protocol              │
    │  (unanimous / majority / weighted / veto)    │
    └─────────────────────┬───────────────────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
        ┌──────────┐            ┌──────────┐
        │ Approved │            │ Rejected │
        │  Action  │            │(escalate)│
        └──────────┘            └──────────┘
```

### Voting Schemes

| Scheme | Rule | Use Case |
|--------|------|----------|
| **Unanimous** | All must agree | Safety-critical, irreversible actions |
| **Majority** | >50% agree | Routine decisions with some risk |
| **Supermajority** | ≥2/3 agree | Important but not critical |
| **Weighted** | Weighted by trust/accuracy | When agents have different track records |
| **Veto** | Any can block | When false negatives are much worse than false positives |

### Implementation

```python
class ConsensusCommittee:
    def __init__(self, agents: list[Agent], scheme: VotingScheme):
        self.agents = agents
        self.scheme = scheme

    def decide(self, proposal: Proposal) -> Decision:
        # Collect votes in parallel (prevent information leakage)
        votes = asyncio.gather(*[
            agent.vote(proposal, isolated=True)
            for agent in self.agents
        ])

        # Apply voting scheme
        result = self.scheme.aggregate(votes)

        # If disagreement, collect reasoning for analysis
        if result.has_dissent:
            self.log_dissent(votes, proposal)

            # Option: request reconciliation
            if self.scheme.allows_reconciliation:
                return self.reconcile(votes, proposal)

        return result

class VetoScheme(VotingScheme):
    """Any agent can block an action."""
    def aggregate(self, votes: list[Vote]) -> Decision:
        if any(v.is_veto for v in votes):
            return Decision.BLOCKED
        if all(v.is_approve for v in votes):
            return Decision.APPROVED
        return Decision.NEEDS_REVIEW
```

### Diversity Requirements

Consensus only helps if agents fail independently. Maximize diversity in:

| Dimension | Why It Matters |
|-----------|----------------|
| **Model family** | Different architectures have different blind spots |
| **Training data** | Correlated data → correlated errors |
| **Fine-tuning** | Same RLHF → same biases |
| **Prompting** | Different framings catch different issues |
| **Temperature** | Deterministic vs. stochastic responses |

### Consequences

**Benefits**:
- Robust against single-point failures
- Catches errors that any individual agent might miss
- Provides natural confidence signal (degree of agreement)
- Resistant to adversarial manipulation of single agent

**Costs**:
- N× inference cost
- Latency of slowest agent (or timeout handling)
- Correlated failures reduce benefit
- Reconciling disagreements is non-trivial

### Known Uses
- Code review requiring multiple AI reviewers
- Content moderation with multiple classifiers
- Autonomous vehicle decisions (sensor fusion analogy)

### Related Patterns
- **N-Version Programming** is the implementation approach
- **Byzantine Fault Tolerance** for adversarial robustness
- Combine with **Supervisor Chain** for escalation on disagreement

---

## Graduated Autonomy

### Intent
Start with heavy oversight and systematically reduce it as the agent demonstrates reliability, matching trust to track record.

### Motivation
New agents shouldn't be trusted like proven ones. You want to give autonomy efficiently—more oversight than necessary is expensive, less is dangerous. Trust should be earned, not assumed.

### Structure
```
Trust Level:    Probation → Supervised → Trusted → Autonomous
                    │            │           │          │
Oversight:      100% review  Sampling    Exceptions   Audit only
                    │            │           │          │
Permissions:    Read-only    Write-limited  Write     Full access
                    │            │           │          │
Escalation:     Always       On uncertainty Rarely    Emergency only
```

### Trust Level Transitions

```python
class GraduatedAutonomy:
    LEVELS = ['probation', 'supervised', 'trusted', 'autonomous']

    def __init__(self, agent: Agent):
        self.agent = agent
        self.level = 'probation'
        self.track_record = TrackRecord()

    def should_promote(self) -> bool:
        level_requirements = {
            'probation': {
                'min_tasks': 50,
                'success_rate': 0.98,
                'max_severity': 'low',
                'time_in_level': timedelta(days=7)
            },
            'supervised': {
                'min_tasks': 200,
                'success_rate': 0.995,
                'max_severity': 'medium',
                'time_in_level': timedelta(days=30)
            },
            'trusted': {
                'min_tasks': 1000,
                'success_rate': 0.999,
                'max_severity': 'medium',
                'time_in_level': timedelta(days=90)
            }
        }
        reqs = level_requirements.get(self.level)
        return self.track_record.meets(reqs)

    def should_demote(self) -> bool:
        # Any high-severity failure → immediate demotion
        if self.track_record.recent_high_severity_failures > 0:
            return True
        # Degraded performance → gradual demotion
        if self.track_record.recent_success_rate < 0.95:
            return True
        return False
```

### Asymmetric Trust Updates

**Promotion** should be slow and evidence-based:
- Require statistical significance
- Multiple criteria (not just success rate)
- Time-in-level minimums
- No skipping levels

**Demotion** should be fast and precautionary:
- Single severe failure can trigger
- Performance degradation detected quickly
- Can skip levels downward
- Automatic on anomaly detection

### Level-Specific Oversight

| Level | Review Rate | Permissions | Escalation Trigger |
|-------|-------------|-------------|-------------------|
| **Probation** | 100% | Read-only, sandbox | Always (learning mode) |
| **Supervised** | 20% random + all flagged | Limited write | Uncertainty > 0.3 |
| **Trusted** | 5% random + anomalies | Standard write | Uncertainty > 0.7 |
| **Autonomous** | Audit log only | Full access | Critical only |

### Consequences

**Benefits**:
- Trust matches evidence
- Efficient—autonomy increases as warranted
- Catches degradation before serious damage
- Clear, objective criteria for autonomy

**Costs**:
- Requires robust track record tracking
- Initial period is expensive (heavy oversight)
- Criteria can be gamed if agent is adversarial
- Level boundaries are somewhat arbitrary

### Known Uses
- Employee probationary periods (human analog)
- Automated trading system deployment
- Self-driving car testing phases

### Related Patterns
- Use **Supervisor Chain** during lower trust levels
- **Behavioral Fingerprinting** enables demotion detection
- **Checkpoint-Rollback** provides safety during transitions

---

## Capability Quarantine

### Intent
Isolate dangerous capabilities so they can only be invoked through heavily-monitored, restricted pathways.

### Motivation
Some capabilities (code execution, external API calls, financial transactions) are inherently risky. You want most of the system to operate freely while constraining access to dangerous functions.

### Structure
```
┌─────────────────────────────────────────────────────────┐
│                    Normal Operations                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │ Agent 1 │  │ Agent 2 │  │ Agent 3 │  │ Agent 4 │    │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘    │
│       │            │            │            │          │
│       └────────────┼────────────┼────────────┘          │
│                    │            │                       │
│              ┌─────▼─────┐      │                       │
│              │  Request  │      │                       │
│              │  Router   │◄─────┘                       │
│              └─────┬─────┘                              │
│                    │                                    │
└────────────────────┼────────────────────────────────────┘
                     │ (restricted channel)
┌────────────────────▼────────────────────────────────────┐
│              QUARANTINE ZONE                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │               Capability Gateway                  │  │
│  │  • Authentication required                       │  │
│  │  • Rate limited                                  │  │
│  │  • Full audit logging                            │  │
│  │  • Anomaly detection                             │  │
│  │  • Human approval queue (optional)               │  │
│  └──────────────────────────────────────────────────┘  │
│                         │                               │
│        ┌────────────────┼────────────────┐             │
│        ▼                ▼                ▼             │
│   ┌─────────┐     ┌──────────┐     ┌─────────┐        │
│   │ Execute │     │ External │     │Financial│        │
│   │  Code   │     │   APIs   │     │  Txns   │        │
│   └─────────┘     └──────────┘     └─────────┘        │
└─────────────────────────────────────────────────────────┘
```

### Quarantine Mechanisms

| Mechanism | Purpose | Implementation |
|-----------|---------|----------------|
| **Authentication** | Only authorized agents can request | Cryptographic tokens with short expiry |
| **Rate Limiting** | Prevent rapid exploitation | Token bucket, hierarchical budgets |
| **Audit Logging** | Forensics and detection | Immutable append-only log |
| **Anomaly Detection** | Catch unusual patterns | Behavioral baseline + ML classifier |
| **Approval Queue** | Human checkpoint | Async approval for high-stakes |
| **Sandboxing** | Contain execution | Containers, VMs, network isolation |

### Implementation

```python
class CapabilityQuarantine:
    def __init__(self, capability: DangerousCapability):
        self.capability = capability
        self.rate_limiter = TokenBucket(tokens_per_hour=10)
        self.anomaly_detector = BehavioralBaseline()
        self.audit_log = ImmutableLog()

    async def invoke(self, request: CapabilityRequest) -> Result:
        # 1. Authenticate
        if not self.verify_token(request.auth_token):
            raise UnauthorizedError()

        # 2. Rate limit
        if not self.rate_limiter.allow():
            raise RateLimitExceeded()

        # 3. Anomaly check
        anomaly_score = self.anomaly_detector.score(request)
        if anomaly_score > ANOMALY_THRESHOLD:
            return await self.escalate_to_human(request, anomaly_score)

        # 4. Log before execution
        log_entry = self.audit_log.record_request(request)

        # 5. Execute in sandbox
        try:
            result = await self.capability.execute_sandboxed(
                request,
                timeout=MAX_EXECUTION_TIME,
                resource_limits=SANDBOX_LIMITS
            )
            self.audit_log.record_result(log_entry, result)
            return result
        except Exception as e:
            self.audit_log.record_failure(log_entry, e)
            raise
```

### Consequences

**Benefits**:
- Dangerous capabilities are heavily monitored
- Normal operations remain fast and unconstrained
- Clear security boundary
- Blast radius limited by rate limiting and sandboxing

**Costs**:
- Latency for quarantined operations
- Complexity of maintaining gateway
- Must correctly classify capabilities (false negatives are dangerous)
- Can be circumvented if classification is wrong

### Known Uses
- Production database access through approval workflows
- External API calls through rate-limited proxies
- Code execution in containerized environments

### Related Patterns
- **Semantic Firewall** at the gateway for content filtering
- **Circuit Breaker** if quarantined capability has failures
- Works within **Supervisor Chain** structure

---

## Task Decomposition Pipeline

### Intent
Break complex tasks into smaller, verifiable steps where each step can be independently validated before proceeding.

### Motivation
Large tasks are hard to verify atomically. Errors compound across steps. You want to catch problems early and enable partial rollback.

### Structure
```
┌──────────────────────────────────────────────────────────┐
│                     Original Task                         │
│            "Analyze data and update report"               │
└────────────────────────┬─────────────────────────────────┘
                         │ decompose
                         ▼
┌──────────────────────────────────────────────────────────┐
│                   Decomposer Agent                        │
│              (identifies sub-tasks)                       │
└────────────────────────┬─────────────────────────────────┘
                         │
    ┌────────────────────┼────────────────────┐
    ▼                    ▼                    ▼
┌────────┐          ┌────────┐          ┌────────┐
│ Step 1 │ ──────▶  │ Step 2 │ ──────▶  │ Step 3 │
│ Fetch  │ verify   │Analyze │ verify   │ Write  │
│ Data   │    ✓     │ Data   │    ✓     │ Report │
└────────┘          └────────┘          └────────┘
    │                    │                    │
    ▼                    ▼                    ▼
┌────────┐          ┌────────┐          ┌────────┐
│Verifier│          │Verifier│          │Verifier│
│   1    │          │   2    │          │   3    │
└────────┘          └────────┘          └────────┘
```

### Decomposition Strategies

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **Sequential** | Steps have dependencies | Data pipeline: fetch → clean → analyze |
| **Parallel** | Independent sub-tasks | Multiple file processing |
| **Hierarchical** | Recursive structure | Document: sections → paragraphs → sentences |
| **Iterative** | Refinement needed | Draft → review → revise → review |

### Verification Points

Each step should have:

1. **Pre-conditions**: What must be true before starting
2. **Post-conditions**: What must be true after completion
3. **Invariants**: What must remain true throughout
4. **Output validation**: Is the output well-formed and plausible

```python
class VerifiedStep:
    def execute(self, input: StepInput) -> StepOutput:
        # Check pre-conditions
        assert self.check_preconditions(input), "Preconditions failed"

        # Execute step
        output = self.agent.process(input)

        # Check post-conditions
        assert self.check_postconditions(output), "Postconditions failed"

        # Validate output format and plausibility
        assert self.validator.validate(output), "Output validation failed"

        # Independent verification (different agent/method)
        verification = self.verifier.verify(input, output)
        if not verification.passed:
            raise VerificationFailed(verification.reason)

        return output
```

### Consequences

**Benefits**:
- Early error detection (fail fast)
- Partial rollback possible
- Each step is simpler to verify
- Natural checkpointing
- Enables parallel verification

**Costs**:
- Decomposition overhead
- More total operations
- Requires defining verification for each step
- May not suit highly interdependent tasks

### Known Uses
- Multi-step code refactoring
- Research workflows (search → read → synthesize → write)
- Data processing pipelines

### Related Patterns
- **Checkpoint-Rollback** at each step boundary
- **Supervisor Chain** for step-level oversight
- Each step can use **Consensus Committee** for high stakes

---

## Other Notable Patterns

### Human-on-the-Loop
Like human-in-the-loop, but human monitors rather than approves each action. Agent acts autonomously; human intervenes when anomalies detected.

### Reversibility Requirement
Only allow actions that can be undone. Irreversible actions require escalation.

### Staged Deployment
Canary → limited rollout → full deployment, with metrics gates between stages.

### Temporal Separation
Proposal and execution happen at different times, allowing for cooling-off period and review.

### Buddy System
Two agents must coordinate to perform sensitive actions (like two-person integrity in nuclear systems).
