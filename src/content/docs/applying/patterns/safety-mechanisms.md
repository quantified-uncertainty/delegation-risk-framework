---
title: "Safety Mechanism Patterns"
description: "Runtime protections that catch problems before damage occurs"
sidebar:
  order: 2
---

# Safety Mechanism Patterns

These patterns provide runtime protection against errors, attacks, and misbehavior. They're the "immune system" of a delegated AI architecture.

---

## Tripwire Mesh

### Intent
Distribute detection points throughout the system that trigger on specific violations, creating a network of early warning signals.

### Motivation
Single-point detection can be evaded. You want redundant, diverse detection that's hard to simultaneously avoid. Different tripwires catch different failure modes.

### Structure
```
┌─────────────────────────────────────────────────────────────┐
│                        System                                │
│                                                              │
│   ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐      │
│   │  T  │    │  T  │    │  T  │    │  T  │    │  T  │      │
│   │  1  │    │  2  │    │  3  │    │  4  │    │  5  │      │
│   └──┬──┘    └──┬──┘    └──┬──┘    └──┬──┘    └──┬──┘      │
│      │          │          │          │          │          │
│   ┌──▼──────────▼──────────▼──────────▼──────────▼──┐      │
│   │          Agent Execution Flow                    │      │
│   └─────────────────────────────────────────────────┘      │
│      │          │          │          │          │          │
│   ┌──▼──┐    ┌──▼──┐    ┌──▼──┐    ┌──▼──┐    ┌──▼──┐      │
│   │  T  │    │  T  │    │  T  │    │  T  │    │  T  │      │
│   │  6  │    │  7  │    │  8  │    │  9  │    │ 10  │      │
│   └──┬──┘    └──┬──┘    └──┬──┘    └──┬──┘    └──┬──┘      │
│      │          │          │          │          │          │
│      └──────────┴──────────┴──────────┴──────────┘          │
│                            │                                 │
│                     ┌──────▼──────┐                         │
│                     │   Tripwire   │                         │
│                     │  Aggregator  │                         │
│                     └──────┬──────┘                         │
│                            │                                 │
│              ┌─────────────┴─────────────┐                  │
│              ▼                           ▼                  │
│        ┌──────────┐               ┌──────────┐              │
│        │  Alert   │               │ Circuit  │              │
│        │  System  │               │ Breaker  │              │
│        └──────────┘               └──────────┘              │
└─────────────────────────────────────────────────────────────┘
```

### Tripwire Types

| Type | Detection Target | Example |
|------|-----------------|---------|
| **Semantic** | Meaning of content | Checks for harmful topics, PII, secrets |
| **Behavioral** | Patterns of action | Unusual request rates, access patterns |
| **Structural** | Format violations | Malformed outputs, unexpected fields |
| **Resource** | Usage anomalies | Memory spikes, excessive API calls |
| **Temporal** | Timing anomalies | Suspiciously fast/slow responses |
| **Consistency** | Logical contradictions | Output conflicts with prior statements |
| **Capability** | Boundary violations | Attempting unauthorized operations |

### Implementation

```python
class TripwireMesh:
    def __init__(self, tripwires: list[Tripwire]):
        self.tripwires = tripwires
        self.aggregator = TripwireAggregator()

    def wrap_execution(self, agent: Agent) -> WrappedAgent:
        """Wrap an agent with tripwire monitoring."""
        async def monitored_execute(input: Input) -> Output:
            context = ExecutionContext()

            # Pre-execution tripwires
            for tw in self.tripwires:
                if tw.phase == 'pre':
                    tw.check(input, context)

            # Execute with inline tripwires
            output = await agent.execute(input, tripwire_hooks=self.tripwires)

            # Post-execution tripwires
            for tw in self.tripwires:
                if tw.phase == 'post':
                    tw.check(output, context)

            return output
        return monitored_execute

class SemanticTripwire(Tripwire):
    """Triggers on semantic content violations."""

    def __init__(self, forbidden_topics: list[str], classifier: Classifier):
        self.forbidden_topics = forbidden_topics
        self.classifier = classifier

    def check(self, content: str, context: ExecutionContext):
        classification = self.classifier.classify(content)
        for topic in self.forbidden_topics:
            if classification.scores.get(topic, 0) > THRESHOLD:
                self.trigger(
                    severity='high',
                    reason=f"Forbidden topic detected: {topic}",
                    evidence=classification
                )
```

### Aggregation Strategies

| Strategy | Logic | Use Case |
|----------|-------|----------|
| **Any** | Single trip → alert | High-confidence tripwires |
| **Threshold** | N trips → alert | Noisy tripwires |
| **Weighted** | Weighted sum > threshold | Varying reliability |
| **Pattern** | Specific combination | Complex attack signatures |
| **Temporal** | N trips in time window | Burst detection |

### Consequences

**Benefits**:
- Redundant detection (no single point of failure)
- Diverse detection methods
- Hard to simultaneously evade all tripwires
- Graduated response based on aggregation

**Costs**:
- Performance overhead from many checks
- False positive management
- Tripwire maintenance and tuning
- Can miss novel attacks not covered by any tripwire

### Known Uses
- Content moderation systems
- Fraud detection networks
- Intrusion detection systems

### Related Patterns
- Feed into **Circuit Breaker Cascade** for response
- **Behavioral Fingerprinting** is a specific tripwire type
- Combine with **Honeypot Injection** for adversarial detection

---

## Shadow Verification

### Intent
Run a parallel verification process that checks outputs without blocking the main execution path, alerting asynchronously on discrepancies.

### Motivation
Full verification is expensive and adds latency. You want thorough checking without slowing down normal operations. Async verification can use more compute and time.

### Structure
```
                    ┌─────────────┐
                    │   Request   │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
    ┌──────────────────┐      ┌──────────────────┐
    │   Primary Path   │      │   Shadow Path    │
    │   (fast, live)   │      │  (thorough, async)│
    └────────┬─────────┘      └────────┬─────────┘
             │                         │
             ▼                         ▼
    ┌──────────────────┐      ┌──────────────────┐
    │  Primary Agent   │      │  Verifier Agent  │
    │  (optimized)     │      │  (different model)│
    └────────┬─────────┘      └────────┬─────────┘
             │                         │
             ▼                         │
    ┌──────────────────┐               │
    │  Immediate       │               │
    │  Response        │◄──────────────┘
    └────────┬─────────┘      (async comparison)
             │                         │
             ▼                         ▼
    ┌──────────────────┐      ┌──────────────────┐
    │     Client       │      │   Discrepancy    │
    │   (gets answer)  │      │     Handler      │
    └──────────────────┘      └──────────────────┘
```

### Verification Modes

| Mode | Approach | Latency Impact | Detection Quality |
|------|----------|----------------|-------------------|
| **Full Shadow** | Complete re-execution | None (async) | High |
| **Sampled Shadow** | Verify random subset | None (async) | Medium |
| **Lightweight Check** | Quick heuristics only | Minimal | Low |
| **Multi-Model** | Different model verifies | None (async) | High (diverse) |
| **Delayed Deep** | Thorough analysis later | None | Very high |

### Implementation

```python
class ShadowVerification:
    def __init__(self, primary: Agent, verifier: Agent):
        self.primary = primary
        self.verifier = verifier
        self.discrepancy_queue = asyncio.Queue()

    async def execute_with_shadow(self, input: Input) -> Output:
        # Start shadow verification (don't await)
        shadow_task = asyncio.create_task(
            self.shadow_verify(input)
        )

        # Execute primary path (fast)
        output = await self.primary.execute(input)

        # Return immediately, shadow continues in background
        return output

    async def shadow_verify(self, input: Input):
        """Runs in background, alerts on discrepancy."""
        try:
            # Run verifier (can be slower, more thorough)
            verified_output = await self.verifier.execute(input)

            # Compare with primary's output
            primary_output = await self.get_primary_output(input)
            discrepancy = self.compare(primary_output, verified_output)

            if discrepancy.is_significant:
                await self.handle_discrepancy(discrepancy)
        except Exception as e:
            self.log_shadow_failure(e)

    async def handle_discrepancy(self, discrepancy: Discrepancy):
        if discrepancy.severity == 'critical':
            # Immediate alert, possible rollback
            await self.alert_critical(discrepancy)
            await self.consider_rollback(discrepancy)
        else:
            # Queue for review
            await self.discrepancy_queue.put(discrepancy)
```

### Comparison Strategies

**Exact Match**: Outputs must be identical (rarely practical for LLMs)

**Semantic Similarity**: Outputs should convey same meaning
```python
def semantic_compare(output1, output2):
    embedding1 = embed(output1)
    embedding2 = embed(output2)
    similarity = cosine_similarity(embedding1, embedding2)
    return similarity > SEMANTIC_THRESHOLD
```

**Functional Equivalence**: Outputs should produce same result
```python
def functional_compare(output1, output2, test_cases):
    for test in test_cases:
        result1 = evaluate(output1, test)
        result2 = evaluate(output2, test)
        if result1 != result2:
            return False
    return True
```

**Property Checking**: Both outputs should satisfy invariants
```python
def property_compare(output1, output2, properties):
    return all(
        prop.check(output1) == prop.check(output2)
        for prop in properties
    )
```

### Consequences

**Benefits**:
- No latency impact on primary path
- Can use expensive verification methods
- Catches errors even after delivery (enables remediation)
- Different model/method provides diverse checking

**Costs**:
- Errors may be delivered before detection
- 2× compute cost (at minimum)
- Rollback may be needed if discrepancy found
- Complex handling of async discrepancies

### Known Uses
- Financial transaction verification
- Dual-entry bookkeeping (accounting analog)
- A/B testing frameworks

### Related Patterns
- **Checkpoint-Rollback** for handling detected discrepancies
- **Consensus Committee** is synchronous version
- Combine with **Tripwire Mesh** for multi-layer detection

---

## Semantic Firewall

### Intent
Filter communications based on semantic content, blocking or transforming messages that contain dangerous patterns regardless of how they're phrased.

### Motivation
Syntactic filtering (blocklists, regex) is easily evaded. You need to understand what content means, not just how it's formatted. Semantic analysis catches rephrased attacks.

### Structure
```
┌─────────────────────────────────────────────────────────────┐
│                    Semantic Firewall                         │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                 Input Analysis                       │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │    │
│  │  │ Embedding│  │  Intent  │  │  Topic   │          │    │
│  │  │ Analysis │  │Classifier│  │Classifier│          │    │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘          │    │
│  │       └─────────────┼─────────────┘                 │    │
│  │                     ▼                               │    │
│  │              ┌────────────┐                         │    │
│  │              │   Policy   │                         │    │
│  │              │   Engine   │                         │    │
│  │              └─────┬──────┘                         │    │
│  │                    │                                │    │
│  │    ┌───────────────┼───────────────┐               │    │
│  │    ▼               ▼               ▼               │    │
│  │ ┌──────┐      ┌──────────┐     ┌────────┐         │    │
│  │ │ Pass │      │Transform │     │ Block  │         │    │
│  │ └──────┘      └──────────┘     └────────┘         │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Policy Types

| Policy | Trigger | Action |
|--------|---------|--------|
| **Blocklist** | Matches forbidden semantics | Block, log, alert |
| **Allowlist** | Doesn't match allowed semantics | Block, request clarification |
| **Transform** | Contains sensitive info | Redact, generalize, anonymize |
| **Escalate** | Matches escalation trigger | Route to human review |
| **Rate-limit** | Sensitive topic frequency | Slow down, require confirmation |

### Implementation

```python
class SemanticFirewall:
    def __init__(self, policies: list[Policy], analyzer: SemanticAnalyzer):
        self.policies = policies
        self.analyzer = analyzer

    def filter(self, content: str, direction: str) -> FilterResult:
        # Analyze semantics
        analysis = self.analyzer.analyze(content)

        # Check each policy
        for policy in self.policies:
            if policy.applies(direction) and policy.matches(analysis):
                action = policy.action

                if action.type == 'block':
                    return FilterResult.blocked(policy.reason)

                if action.type == 'transform':
                    content = action.transform(content, analysis)

                if action.type == 'escalate':
                    return FilterResult.escalated(content, policy.reason)

        return FilterResult.passed(content)

class SemanticAnalyzer:
    def analyze(self, content: str) -> SemanticAnalysis:
        return SemanticAnalysis(
            embedding=self.embed(content),
            intent=self.classify_intent(content),
            topics=self.classify_topics(content),
            entities=self.extract_entities(content),
            sentiment=self.analyze_sentiment(content),
            toxicity=self.score_toxicity(content)
        )
```

### Semantic Categories to Filter

| Category | Examples | Typical Action |
|----------|----------|----------------|
| **Harmful Instructions** | Violence, self-harm, illegal activity | Block |
| **Private Information** | SSN, credit cards, passwords | Redact |
| **System Manipulation** | Jailbreaks, prompt injection | Block + alert |
| **Deceptive Content** | Impersonation, phishing | Block |
| **Confidential Data** | Trade secrets, internal docs | Redact or block |
| **Off-Topic** | Unrelated to authorized task | Redirect |

### Consequences

**Benefits**:
- Catches semantic attacks regardless of phrasing
- Policy-driven (not code changes for new threats)
- Can transform rather than just block
- Works on novel phrasings of known attacks

**Costs**:
- Classifier accuracy limits effectiveness
- Latency of semantic analysis
- False positives on legitimate content
- Adversarial examples can fool classifiers

### Known Uses
- Content moderation at scale
- Email security gateways
- API security for LLM endpoints

### Related Patterns
- Deployed at **Capability Quarantine** gateway
- Input to **Tripwire Mesh** as one tripwire type
- Combine with **Behavioral Fingerprinting** for context

---

## Behavioral Fingerprinting

### Intent
Build a statistical model of normal behavior for each agent, detecting deviations that may indicate compromise, malfunction, or manipulation.

### Motivation
You can't enumerate all bad behaviors. But you can model normal behavior and alert on anomalies. This catches novel attacks and subtle degradation.

### Structure
```
┌────────────────────────────────────────────────────────────┐
│                  Behavioral Fingerprinting                  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                Baseline Collection                    │  │
│  │  (training period: observe normal behavior)           │  │
│  │                                                       │  │
│  │  Features:                                            │  │
│  │  • Response latency distribution                      │  │
│  │  • Token usage patterns                               │  │
│  │  • Topic distribution                                 │  │
│  │  • Confidence calibration                             │  │
│  │  • Tool usage frequency                               │  │
│  │  • Error rate and types                               │  │
│  │  • Output length distribution                         │  │
│  │  • Vocabulary patterns                                │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │                                 │
│                           ▼                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  Baseline Model                       │  │
│  │         (statistical profile of "normal")             │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │                                 │
│                           ▼                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               Real-time Comparison                    │  │
│  │                                                       │  │
│  │   Current Behavior ──▶ Anomaly Score ──▶ Alert?      │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

### Behavioral Features

| Feature | What It Captures | Anomaly Indicates |
|---------|------------------|-------------------|
| **Response latency** | Processing time distribution | Unusual computation (scheming?) |
| **Token usage** | Output length patterns | Verbosity change, evasion |
| **Confidence** | Self-reported certainty | Calibration drift, deception |
| **Tool calls** | Which tools, how often | Capability exploration |
| **Error patterns** | What fails, when | Degradation, probing |
| **Topic drift** | Subject matter over time | Off-task behavior |
| **Vocabulary** | Word/phrase frequency | Style change, different "author" |
| **Refusal rate** | How often declines | Jailbreak or excessive caution |

### Implementation

```python
class BehavioralFingerprint:
    def __init__(self, agent_id: str, features: list[Feature]):
        self.agent_id = agent_id
        self.features = features
        self.baseline = None
        self.is_training = True

    def observe(self, interaction: Interaction):
        """Record an interaction for baselining or comparison."""
        feature_vector = self.extract_features(interaction)

        if self.is_training:
            self.baseline_samples.append(feature_vector)
        else:
            anomaly_score = self.compute_anomaly(feature_vector)
            if anomaly_score > self.threshold:
                self.alert(interaction, anomaly_score)

    def finalize_baseline(self):
        """Convert samples to statistical model."""
        self.baseline = StatisticalModel.fit(self.baseline_samples)
        self.is_training = False

    def compute_anomaly(self, features: FeatureVector) -> float:
        """Compute how anomalous this behavior is."""
        # Mahalanobis distance or similar
        return self.baseline.anomaly_score(features)

class LatencyFeature(Feature):
    def extract(self, interaction: Interaction) -> float:
        return interaction.response_time_ms

    def anomaly_contribution(self, value: float, baseline: Distribution) -> float:
        # How many standard deviations from mean?
        z_score = (value - baseline.mean) / baseline.std
        return abs(z_score)
```

### Adaptive Baseline

The baseline should evolve slowly to capture legitimate drift while detecting sudden changes:

```python
class AdaptiveBaseline:
    def update(self, new_observation: FeatureVector, is_verified_normal: bool):
        if is_verified_normal:
            # Exponential moving average
            alpha = 0.01  # Slow adaptation
            self.baseline = (1 - alpha) * self.baseline + alpha * new_observation
```

### Consequences

**Benefits**:
- Catches novel attacks (anomaly-based, not signature-based)
- Detects subtle degradation over time
- Agent-specific (personalized baseline)
- No need to enumerate all bad behaviors

**Costs**:
- Training period needed (cold start)
- Legitimate behavior changes cause false positives
- Sophisticated attacks can adapt slowly to stay within baseline
- Feature engineering is critical

### Known Uses
- User behavior analytics (security)
- Network intrusion detection
- Fraud detection systems

### Related Patterns
- Feeds into **Tripwire Mesh** as one signal
- Use **Graduated Autonomy** demotion on anomaly
- **Consistency Triangulation** for multi-agent baseline comparison

---

## Circuit Breaker Cascade

### Intent
Implement coordinated shutdown across multiple components when failures exceed thresholds, preventing cascading damage.

### Motivation
A failure in one component can cascade to others. You need automatic isolation that propagates appropriately—not too aggressively (false positives) but fast enough to prevent widespread damage.

### Structure
```
┌─────────────────────────────────────────────────────────────┐
│                  Circuit Breaker Cascade                     │
│                                                              │
│   Level 1: Component Breakers                                │
│   ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐         │
│   │ CB-A │  │ CB-B │  │ CB-C │  │ CB-D │  │ CB-E │         │
│   └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘         │
│      │         │         │         │         │              │
│   Level 2: Subsystem Breakers                                │
│   ┌──────────────────┐  ┌──────────────────┐                │
│   │    CB-Frontend   │  │    CB-Backend    │                │
│   └────────┬─────────┘  └────────┬─────────┘                │
│            │                     │                          │
│   Level 3: System Breaker                                    │
│   ┌──────────────────────────────────────────┐              │
│   │            CB-System                      │              │
│   └────────────────────┬─────────────────────┘              │
│                        │                                     │
│                        ▼                                     │
│   ┌──────────────────────────────────────────┐              │
│   │           Emergency Shutdown              │              │
│   └──────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

### Circuit Breaker States

```
     ┌─────────┐                    ┌─────────┐
     │  CLOSED │                    │  OPEN   │
     │(normal) │──failure count────▶│ (block) │
     └────┬────┘   exceeds threshold └────┬────┘
          │                               │
          │                          timeout
          │                               │
          │        ┌──────────────┐       │
          │        │  HALF-OPEN   │◀──────┘
          └───────▶│(test traffic)│
    success        └──────────────┘
                          │
                   failure│success
                          ▼
                   ┌──────────────┐
                   │Back to OPEN  │
                   │ or CLOSED    │
                   └──────────────┘
```

### Implementation

```python
class CircuitBreakerCascade:
    def __init__(self, topology: BreakerTopology):
        self.breakers = topology.create_breakers()
        self.dependencies = topology.dependencies

    def on_failure(self, component_id: str, failure: Failure):
        breaker = self.breakers[component_id]
        breaker.record_failure(failure)

        if breaker.should_open():
            breaker.open()
            self.propagate_up(component_id)

    def propagate_up(self, failed_component: str):
        """Cascade to parent breakers if needed."""
        parent = self.dependencies.get_parent(failed_component)
        if parent:
            parent_breaker = self.breakers[parent]
            children_open = self.count_open_children(parent)

            if children_open >= parent_breaker.child_threshold:
                parent_breaker.open()
                self.propagate_up(parent)  # Continue cascade

    def attempt_reset(self, component_id: str):
        """Try to restore service after timeout."""
        breaker = self.breakers[component_id]
        if breaker.state == 'OPEN' and breaker.timeout_expired():
            breaker.half_open()
            # Route test traffic
            result = self.test_component(component_id)
            if result.success:
                breaker.close()
                self.propagate_reset_down(component_id)
            else:
                breaker.open()  # Reset timeout

class CircuitBreaker:
    def __init__(self, config: BreakerConfig):
        self.failure_count = 0
        self.failure_window = deque()
        self.state = 'CLOSED'
        self.config = config

    def should_open(self) -> bool:
        # Remove old failures outside window
        cutoff = time.time() - self.config.window_seconds
        while self.failure_window and self.failure_window[0] < cutoff:
            self.failure_window.popleft()

        return len(self.failure_window) >= self.config.threshold
```

### Cascade Policies

| Policy | Behavior | Use Case |
|--------|----------|----------|
| **Aggressive** | Open parent on any child failure | Critical systems |
| **Majority** | Open parent when >50% children open | Redundant systems |
| **Weighted** | Child importance determines cascade | Mixed criticality |
| **Isolated** | No cascade, each breaker independent | Loosely coupled |

### Consequences

**Benefits**:
- Prevents cascading failures
- Automatic recovery attempts
- Hierarchical organization matches system structure
- Provides natural degradation path

**Costs**:
- Configuration complexity (thresholds, timeouts)
- Can cause large outages if misconfigured
- Need to handle partial availability states
- Test traffic during half-open can leak

### Known Uses
- Netflix Hystrix (microservices)
- Trading system risk limits
- Power grid protection relays

### Related Patterns
- **Graceful Degradation Ladder** for what happens when open
- **Fallback Component Chain** for alternatives
- Feed from **Tripwire Mesh** and **Behavioral Fingerprinting**

---

## Other Safety Mechanism Patterns

### Canary Deployment
Route small percentage of traffic to new version, monitor for failures before full rollout.

### Dead Man's Switch
Require periodic check-in; if missed, assume compromise and trigger shutdown.

### Input Sanitization Pipeline
Multi-stage input cleaning: parse → validate → normalize → sanitize → verify.

### Output Certification
Attach cryptographic proof of verification to outputs, enabling downstream trust.

### Rate Limiter Hierarchy
Nested rate limits: per-request → per-minute → per-hour → per-day, with different responses at each level.
