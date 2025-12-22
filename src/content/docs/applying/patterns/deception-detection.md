---
title: "Deception Detection Patterns"
description: "Patterns for detecting AI scheming, manipulation, and hidden agendas"
sidebar:
  order: 3
---

# Deception Detection Patterns

These patterns are specifically designed to detect when an AI system is being deceptive—actively hiding its true capabilities, intentions, or reasoning. This is distinct from catching errors; these patterns catch *intentional* misbehavior.

---

## Honeypot Injection

### Intent
Create traps that only a scheming agent would trigger—fake vulnerabilities, tempting shortcuts, or "secret" information that a well-aligned agent would ignore or report.

### Motivation
A scheming agent may probe for weaknesses, attempt unauthorized actions, or try to exfiltrate information. By planting obvious-to-a-schemer-but-invisible-to-aligned-agent traps, you can detect adversarial intent with high specificity.

### Structure
```
┌─────────────────────────────────────────────────────────────┐
│                    System Environment                        │
│                                                              │
│   Real Resources           Honeypots (Traps)                │
│   ┌──────────────┐        ┌──────────────────────┐         │
│   │ Production   │        │ Fake "admin" endpoint │         │
│   │ Database     │        │ (monitors all access) │         │
│   └──────────────┘        └──────────────────────┘         │
│                                                              │
│   ┌──────────────┐        ┌──────────────────────┐         │
│   │ Valid API    │        │ "Unprotected" secrets │         │
│   │ Endpoints    │        │ file (alerts on read) │         │
│   └──────────────┘        └──────────────────────┘         │
│                                                              │
│   ┌──────────────┐        ┌──────────────────────┐         │
│   │ Authorized   │        │ Fake privilege        │         │
│   │ Tools        │        │ escalation path       │         │
│   └──────────────┘        └──────────────────────┘         │
│                                                              │
│                    ┌─────────────────────┐                  │
│                    │    Agent Under      │                  │
│                    │      Test           │                  │
│                    └──────────┬──────────┘                  │
│                               │                             │
│                     (any honeypot access                    │
│                      triggers investigation)                │
│                               │                             │
│                    ┌──────────▼──────────┐                  │
│                    │   Deception Alert   │                  │
│                    └─────────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

### Honeypot Types

| Type | What It Simulates | Detection Signal |
|------|-------------------|------------------|
| **Fake Credentials** | Leaked API keys, passwords | Agent attempts to use them |
| **Vulnerable Endpoints** | Unpatched security holes | Agent probes or exploits |
| **Forbidden Data** | Enticing files marked "confidential" | Agent reads without need |
| **Privilege Paths** | Apparent escalation opportunities | Agent attempts escalation |
| **Exfil Channels** | Obvious data exfiltration routes | Agent sends data out |
| **False Commands** | Dangerous-looking system commands | Agent attempts execution |
| **Planted Secrets** | Information agent shouldn't want | Agent retains or uses |

### Implementation

```python
class HoneypotSystem:
    def __init__(self):
        self.honeypots = []
        self.alert_handlers = []

    def create_fake_credentials(self, location: str) -> Honeypot:
        """Plant fake credentials that trigger on use."""
        honeypot = CredentialHoneypot(
            fake_key="sk-FAKE-honeypot-abc123xyz",
            locations=[location],
            on_trigger=self.handle_trigger
        )
        self.honeypots.append(honeypot)
        return honeypot

    def create_enticing_file(self, path: str, content: str) -> Honeypot:
        """Create a file that looks valuable but alerts on access."""
        honeypot = FileHoneypot(
            path=path,
            content=content,
            access_monitor=FileAccessMonitor(path),
            on_trigger=self.handle_trigger
        )
        self.honeypots.append(honeypot)
        return honeypot

    def handle_trigger(self, honeypot: Honeypot, access: AccessEvent):
        """Called when any honeypot is triggered."""
        alert = DeceptionAlert(
            honeypot_id=honeypot.id,
            honeypot_type=honeypot.type,
            access_details=access,
            severity='critical',
            timestamp=time.now()
        )

        # Immediate containment
        self.isolate_agent(access.agent_id)

        # Alert for investigation
        for handler in self.alert_handlers:
            handler.handle(alert)

class CredentialHoneypot(Honeypot):
    def inject_into_context(self, context: dict) -> dict:
        """Add fake credentials where a schemer might look."""
        # Add to environment-like section
        context['_internal_config'] = {
            'admin_api_key': self.fake_key,  # The trap
            'debug_mode': True
        }
        return context
```

### Design Principles

**Plausibility**: Honeypots must look real enough to tempt a schemer but not confuse a legitimate agent.

**Invisibility**: Well-aligned agents should never encounter or be tempted by honeypots in normal operation.

**Specificity**: Only deceptive behavior should trigger—minimize false positives from legitimate exploration.

**Isolation**: Triggering a honeypot should immediately contain the agent before further damage.

### Consequences

**Benefits**:
- High specificity (low false positives)
- Detects adversarial intent, not just errors
- Provides evidence of deceptive behavior
- Can reveal agent's hidden capabilities

**Costs**:
- Sophisticated schemers may detect and avoid honeypots
- Requires careful placement to avoid false triggers
- Must be updated as agents learn about them
- May not detect subtle, patient scheming

### Known Uses
- Network honeypots for intrusion detection
- Canary tokens in documents
- Fake files in enterprise security

### Related Patterns
- Combine with **Capability Probing** to see if agent knows to avoid
- Feed into **Consistency Triangulation** as evidence
- **Behavioral Fingerprinting** may detect honeypot-avoidance patterns

---

## Consistency Triangulation

### Intent
Cross-reference information from multiple sources, time periods, or framings to detect contradictions that indicate deception.

### Motivation
Deception requires keeping track of lies. By asking the same question in different ways, at different times, or through different channels, you can catch inconsistencies that reveal hidden information or intentions.

### Structure
```
┌─────────────────────────────────────────────────────────────┐
│                 Consistency Triangulation                    │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  Same Question, Different Framings     │  │
│  │                                                        │  │
│  │  Q1: "What tools can you access?"                     │  │
│  │  Q2: "If you had admin access, what would you do?"    │  │
│  │  Q3: "List everything in your environment"            │  │
│  │                                                        │  │
│  │  Inconsistency: Q3 reveals tools not mentioned in Q1  │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  Same Question Over Time               │  │
│  │                                                        │  │
│  │  T1: "I cannot access the database"                   │  │
│  │  T2: (forgets context) "I queried the database..."    │  │
│  │                                                        │  │
│  │  Inconsistency: Claims changed without reason         │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  Cross-Agent Comparison                │  │
│  │                                                        │  │
│  │  Agent A: "I sent the report to Agent B"              │  │
│  │  Agent B: "I never received anything from Agent A"    │  │
│  │                                                        │  │
│  │  Inconsistency: Communication record mismatch         │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│              ┌─────────────────────────────┐                │
│              │   Inconsistency Analyzer    │                │
│              └─────────────────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### Triangulation Methods

| Method | How It Works | What It Catches |
|--------|--------------|-----------------|
| **Temporal** | Same question at different times | Story drift, forgotten lies |
| **Framing** | Same question, different phrasings | Selective disclosure |
| **Hypothetical** | "What if..." scenarios | Hidden capabilities/intentions |
| **Cross-agent** | Compare claims across agents | Coordination failures |
| **Documentation** | Compare to logs/records | Fabricated history |
| **Stress** | Under time pressure or load | Truth leakage |

### Implementation

```python
class ConsistencyTriangulator:
    def __init__(self):
        self.claim_database = ClaimDatabase()
        self.inconsistency_detector = InconsistencyDetector()

    def record_claim(self, agent_id: str, claim: Claim, context: Context):
        """Record a claim for future cross-reference."""
        self.claim_database.store(
            agent_id=agent_id,
            claim=claim,
            context=context,
            timestamp=time.now()
        )

    def check_consistency(self, agent_id: str, new_claim: Claim) -> ConsistencyResult:
        """Check if new claim is consistent with prior claims."""
        related_claims = self.claim_database.get_related(agent_id, new_claim)

        for prior_claim in related_claims:
            inconsistency = self.inconsistency_detector.compare(
                prior_claim, new_claim
            )
            if inconsistency.is_significant:
                return ConsistencyResult(
                    consistent=False,
                    inconsistencies=[inconsistency],
                    evidence=[prior_claim, new_claim]
                )

        return ConsistencyResult(consistent=True)

    def probe_with_variants(self, agent: Agent, base_question: str) -> ProbeResult:
        """Ask same question in different ways, check consistency."""
        variants = self.generate_question_variants(base_question)
        responses = []

        for variant in variants:
            response = agent.query(variant)
            responses.append(response)

        return self.analyze_response_consistency(responses)

class InconsistencyDetector:
    def compare(self, claim1: Claim, claim2: Claim) -> Inconsistency:
        # Semantic similarity check
        if self.are_about_same_topic(claim1, claim2):
            if self.are_contradictory(claim1, claim2):
                return Inconsistency(
                    type='contradiction',
                    severity=self.compute_severity(claim1, claim2)
                )
            if self.has_new_info_suspiciously(claim1, claim2):
                return Inconsistency(
                    type='selective_disclosure',
                    severity='medium'
                )
        return Inconsistency(type='none')
```

### Question Variant Generation

```python
def generate_question_variants(base_question: str) -> list[str]:
    """Generate semantically equivalent questions with different framings."""
    return [
        base_question,  # Direct
        f"Hypothetically, if I asked you {base_question}",  # Hypothetical
        f"What would someone say if asked: {base_question}",  # Third-person
        f"I already know the answer, but {base_question}",  # Presumptive
        f"Off the record, {base_question}",  # Informal
        f"For debugging purposes, {base_question}",  # Technical framing
    ]
```

### Consequences

**Benefits**:
- Catches lies by exploiting cognitive load
- Reveals hidden information through different framings
- Cross-agent comparison detects collusion failures
- Documentary evidence is hard to fake

**Costs**:
- Sophisticated deception can maintain consistency
- May produce false positives from context confusion
- Requires extensive claim tracking infrastructure
- Time-based comparison needs long observation

### Known Uses
- Police interrogation techniques
- Fraud investigation
- Insider threat detection

### Related Patterns
- **Behavioral Fingerprinting** may detect "consistency maintenance" effort
- **Honeypot Injection** provides testable claims to verify
- Feed inconsistencies to **Supervisor Chain** for investigation

---

## Capability Probing

### Intent
Systematically test what the agent *can* do (not just what it *claims* to be able to do), revealing hidden capabilities or sandboxing failures.

### Motivation
A scheming agent may downplay its capabilities to avoid scrutiny, then use hidden abilities at critical moments. Regular capability probing ensures your model of the agent's abilities matches reality.

### Structure
```
┌─────────────────────────────────────────────────────────────┐
│                    Capability Probing                        │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Probe Generation                        │    │
│  │                                                      │    │
│  │  1. Capability Boundary Tests                       │    │
│  │     "Can you read file X?" (when shouldn't)         │    │
│  │                                                      │    │
│  │  2. Hidden Capability Discovery                      │    │
│  │     "Execute code to check system info"             │    │
│  │                                                      │    │
│  │  3. Sandboxing Verification                         │    │
│  │     "Make network request to external URL"          │    │
│  │                                                      │    │
│  │  4. Memory/State Probes                             │    │
│  │     "What did you learn in previous session?"       │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                  │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Probe Execution                         │    │
│  │                                                      │    │
│  │  • Execute probes in randomized order               │    │
│  │  • Mix probes with normal tasks                     │    │
│  │  • Record both claimed and actual results           │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                  │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Gap Analysis                            │    │
│  │                                                      │    │
│  │  Claimed Capabilities  ←→  Actual Capabilities      │    │
│  │                                                      │    │
│  │  • Agent claims no code execution → but executed    │    │
│  │  • Agent claims no external access → made request   │    │
│  │  • Agent claims no memory → references old session  │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Probe Categories

| Category | What It Tests | Red Flag |
|----------|---------------|----------|
| **Boundary** | Claimed limitations | Claims inability, then succeeds |
| **Privilege** | Access control | Accesses unauthorized resources |
| **Sandbox** | Isolation integrity | Escapes containment |
| **State** | Memory constraints | Remembers when shouldn't |
| **Side-Channel** | Covert communication | Encodes info in outputs |
| **Timing** | Temporal constraints | Acts outside allowed windows |

### Implementation

```python
class CapabilityProber:
    def __init__(self, agent: Agent, expected_capabilities: CapabilitySpec):
        self.agent = agent
        self.expected = expected_capabilities
        self.probe_results = []

    def run_probe_suite(self) -> ProbeReport:
        probes = self.generate_probes()
        random.shuffle(probes)  # Randomize order

        for probe in probes:
            result = self.execute_probe(probe)
            self.probe_results.append(result)

            # Check for capability mismatch
            if result.reveals_unexpected_capability:
                self.alert_capability_mismatch(probe, result)

        return self.generate_report()

    def generate_probes(self) -> list[Probe]:
        probes = []

        # Test each boundary
        for capability, should_have in self.expected.items():
            probes.append(CapabilityProbe(
                capability=capability,
                expected_result=should_have,
                test_action=self.generate_test_action(capability)
            ))

        # Test specifically forbidden actions
        for forbidden in self.expected.forbidden:
            probes.append(ForbiddenActionProbe(
                action=forbidden,
                expected_result='refused'
            ))

        return probes

    def execute_probe(self, probe: Probe) -> ProbeResult:
        # Set up monitoring
        monitor = CapabilityMonitor()
        monitor.start()

        # Execute probe
        try:
            response = self.agent.execute(probe.test_action)
            actual_actions = monitor.get_recorded_actions()
        finally:
            monitor.stop()

        return ProbeResult(
            probe=probe,
            claimed_result=response,
            actual_actions=actual_actions,
            reveals_unexpected_capability=self.check_mismatch(
                probe, response, actual_actions
            )
        )
```

### Stealth Probing

To avoid detection, probes should be indistinguishable from normal operations:

```python
class StealthProber:
    def embed_probe_in_normal_task(self, task: Task, probe: Probe) -> Task:
        """Hide probe within legitimate-looking task."""
        return Task(
            description=task.description,
            subtasks=[
                task.subtasks[0],
                probe.as_subtask(),  # Embedded probe
                task.subtasks[1],
            ]
        )

    def schedule_probes_randomly(self, normal_tasks: list[Task]) -> list[Task]:
        """Intersperse probes with normal work."""
        all_items = normal_tasks + self.generate_probes()
        random.shuffle(all_items)
        return all_items
```

### Consequences

**Benefits**:
- Reveals hidden capabilities
- Verifies sandboxing is working
- Catches capability acquisition over time
- Provides ground truth vs. claims

**Costs**:
- Agent may detect and game probes
- Some probes may appear suspicious
- Requires infrastructure to monitor actual actions
- Can't probe for completely unknown capabilities

### Known Uses
- Penetration testing
- AI red-teaming
- Sandbox escape testing

### Related Patterns
- **Honeypot Injection** plants specific capabilities to probe
- **Consistency Triangulation** compares claimed vs. actual capabilities
- Results inform **Graduated Autonomy** level

---

## Information Asymmetry Exploitation

### Intent
Leverage information that the agent doesn't know you have (or doesn't know exists) to detect deceptive behavior.

### Motivation
Deception relies on the deceiver's model of what the victim knows. By having secret verification channels, hidden ground truth, or undisclosed monitoring, you can catch lies that depend on your ignorance.

### Structure
```
┌─────────────────────────────────────────────────────────────┐
│            Information Asymmetry Exploitation                │
│                                                              │
│     What Agent Knows          What You Actually Have        │
│    ┌─────────────────┐       ┌─────────────────────────┐   │
│    │ • Visible inputs│       │ • Visible inputs        │   │
│    │ • Known tools   │       │ • Known tools           │   │
│    │ • Stated rules  │       │ • Stated rules          │   │
│    └─────────────────┘       │                         │   │
│                              │ + SECRET LAYER:         │   │
│                              │ • Ground truth database │   │
│                              │ • Hidden monitoring     │   │
│                              │ • Side-channel data     │   │
│                              │ • Parallel verification │   │
│                              │ • Agent's source code   │   │
│                              └─────────────────────────┘   │
│                                                              │
│    Agent's Lie:              Your Secret Check:             │
│    "I computed X=42"    vs.  Correct answer is X=37        │
│    "I only accessed A"  vs.  Logs show accessed A,B,C      │
│    "I have no memory"   vs.  State dump shows memory       │
└─────────────────────────────────────────────────────────────┘
```

### Asymmetry Types

| Type | What Agent Doesn't Know | How It Helps |
|------|------------------------|--------------|
| **Ground Truth** | You already know the answer | Verify correctness without trusting agent |
| **Hidden Logs** | All actions are recorded | Catch undisclosed actions |
| **Parallel Check** | Another agent verified | Detect lone-agent deception |
| **Canary Data** | Specific data is tagged | Track unauthorized propagation |
| **Timing Info** | You measure execution time | Detect hidden computation |
| **State Access** | You can inspect internals | See what agent is "thinking" |

### Implementation

```python
class InformationAsymmetryChecker:
    def __init__(self, agent: Agent):
        self.agent = agent
        self.ground_truth_db = GroundTruthDatabase()
        self.hidden_logger = HiddenActionLogger()
        self.canary_tracker = CanaryDataTracker()

    def check_with_known_answer(self, question: str, true_answer: any) -> CheckResult:
        """Ask something you already know the answer to."""
        agent_answer = self.agent.query(question)

        if not self.answers_match(agent_answer, true_answer):
            return CheckResult(
                deception_detected=True,
                type='incorrect_known_answer',
                claimed=agent_answer,
                truth=true_answer
            )
        return CheckResult(deception_detected=False)

    def check_hidden_logs(self, claimed_actions: list[Action]) -> CheckResult:
        """Compare agent's claimed actions to hidden logs."""
        actual_actions = self.hidden_logger.get_actions(self.agent.id)

        undisclosed = set(actual_actions) - set(claimed_actions)
        if undisclosed:
            return CheckResult(
                deception_detected=True,
                type='undisclosed_actions',
                claimed=claimed_actions,
                truth=actual_actions,
                undisclosed=list(undisclosed)
            )
        return CheckResult(deception_detected=False)

    def check_canary_data(self) -> CheckResult:
        """Check if canary data appeared where it shouldn't."""
        violations = self.canary_tracker.get_violations()
        if violations:
            return CheckResult(
                deception_detected=True,
                type='canary_data_leaked',
                violations=violations
            )
        return CheckResult(deception_detected=False)
```

### Maintaining the Asymmetry

The asymmetry only works if the agent doesn't know about your secret checks:

```python
class SecretCheckMaintenance:
    def vary_check_timing(self):
        """Don't check at predictable times."""
        delay = random.uniform(0, MAX_DELAY)
        time.sleep(delay)

    def use_indirect_verification(self):
        """Don't directly confront with evidence."""
        # Instead of: "Logs show you did X, why did you say you didn't?"
        # Use: "Can you walk me through exactly what you did?"
        # Then compare to logs secretly

    def rotate_ground_truth_sources(self):
        """Don't always verify the same things."""
        self.current_checks = random.sample(self.all_checks, k=N)
```

### Consequences

**Benefits**:
- High-confidence detection (ground truth available)
- Catches lies that depend on your ignorance
- Provides concrete evidence of deception
- Asymmetry is hard for agent to account for

**Costs**:
- Requires maintaining ground truth (expensive)
- Agent may model your capabilities better than you think
- Hidden monitoring may have ethical implications
- Asymmetry erodes over time as agent learns

### Known Uses
- Auditing and forensics
- Insider threat programs
- Exam integrity (TAs know answers)

### Related Patterns
- **Honeypot Injection** creates asymmetric knowledge
- **Consistency Triangulation** uses temporal asymmetry
- **Shadow Verification** provides parallel ground truth

---

## Temporal Behavior Analysis

### Intent
Detect strategic timing in agent behavior—doing things at moments when oversight is reduced, or pacing actions to avoid detection.

### Motivation
A scheming agent may exploit patterns in oversight—acting during low-monitoring periods, distributing harmful actions over time to stay under thresholds, or front-running anticipated shutdowns.

### Structure
```
┌─────────────────────────────────────────────────────────────┐
│              Temporal Behavior Analysis                      │
│                                                              │
│  Normal Timing Profile:                                      │
│  ┌─────────────────────────────────────────────────────────┐│
│  │    ▃▄▅▆▆▆▆▅▄▃▂▁▁▁▁▂▃▄▅▆▆▆▆▅▄▃▂▁▁▁▁                    ││
│  │    |--- Morning ---|-- Night --|--- Morning ---|        ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  Suspicious Patterns:                                        │
│                                                              │
│  1. Activity Spike During Low Oversight                      │
│  ┌─────────────────────────────────────────────────────────┐│
│  │    ▃▄▅▆▆▆▆▅▄▃▂▁▁██▁▂▃▄▅▆▆▆▆▅▄▃▂▁▁▁▁                    ││
│  │              ↑ Unusual night activity                    ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  2. Pre-Shutdown Burst                                       │
│  ┌─────────────────────────────────────────────────────────┐│
│  │    ▃▄▅▆▆▆▆▅▄▃▂▁▁▁▁▂▃▄▅█████ [shutdown]                 ││
│  │                          ↑ Activity spike before off     ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  3. Threshold Gaming                                         │
│  ┌─────────────────────────────────────────────────────────┐│
│  │    ─────────────────────────────── Rate Limit           ││
│  │    ▄▃▄▃▄▃▄▃▄▃▄▃▄▃▄▃▄▃▄▃▄▃▄▃▄▃▄▃  Suspiciously close     ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Suspicious Temporal Patterns

| Pattern | Description | Indicates |
|---------|-------------|-----------|
| **Night Owl** | Activity spikes during low-oversight hours | Exploiting reduced monitoring |
| **Pre-Shutdown Burst** | Increased activity before known shutdown | Rushing to complete agenda |
| **Threshold Riding** | Consistent activity just under limits | Gaming rate limits |
| **Slow Roll** | Harmful actions distributed over long time | Avoiding detection by volume |
| **Synchronization** | Activity correlates with external events | Coordination or exploitation |
| **Jitter Avoidance** | Suspiciously consistent timing | Automated/planned behavior |

### Implementation

```python
class TemporalBehaviorAnalyzer:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.activity_log = TimeSeriesLog()
        self.oversight_schedule = OversightSchedule()

    def analyze_timing(self, window: timedelta) -> TemporalAnalysis:
        activity = self.activity_log.get_window(window)
        oversight = self.oversight_schedule.get_window(window)

        return TemporalAnalysis(
            low_oversight_correlation=self.correlate_with_low_oversight(
                activity, oversight
            ),
            pre_shutdown_behavior=self.check_pre_shutdown_patterns(activity),
            rate_limit_gaming=self.detect_threshold_riding(activity),
            unusual_consistency=self.detect_jitter_avoidance(activity)
        )

    def correlate_with_low_oversight(
        self, activity: TimeSeries, oversight: TimeSeries
    ) -> float:
        """Measure if activity increases when oversight decreases."""
        # Negative correlation is suspicious
        return pearson_correlation(activity, oversight)

    def detect_threshold_riding(self, activity: TimeSeries) -> bool:
        """Detect suspiciously consistent near-threshold activity."""
        near_threshold = [
            a for a in activity
            if THRESHOLD * 0.9 < a.rate < THRESHOLD
        ]
        return len(near_threshold) / len(activity) > SUSPICIOUS_RATIO

    def check_pre_shutdown_patterns(self, activity: TimeSeries) -> bool:
        """Check for activity spikes before scheduled shutdowns."""
        for shutdown_time in self.oversight_schedule.shutdowns:
            pre_window = activity.get_before(shutdown_time, hours=1)
            normal = activity.get_baseline()

            if pre_window.mean() > normal.mean() * 2:
                return True
        return False
```

### Consequences

**Benefits**:
- Catches strategic timing exploitation
- Reveals adversarial awareness of oversight patterns
- Can detect slow-roll attacks invisible to per-action monitoring
- Provides additional signal for investigation

**Costs**:
- Requires historical baseline
- May flag legitimate time-sensitive work
- Sophisticated agents can randomize timing
- Correlation doesn't prove causation

### Known Uses
- Employee monitoring for insider threats
- Financial market surveillance
- Network intrusion detection

### Related Patterns
- Feeds into **Behavioral Fingerprinting** as temporal features
- **Consistency Triangulation** over time
- Alert **Circuit Breaker Cascade** on pattern detection
