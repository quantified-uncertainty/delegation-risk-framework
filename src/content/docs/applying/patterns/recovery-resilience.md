---
title: "Recovery & Resilience Patterns"
description: "Patterns for graceful failure handling and system recovery"
sidebar:
  order: 4
---

# Recovery & Resilience Patterns

These patterns focus on what happens when things go wrong. They enable graceful degradation, rollback to safe states, and automatic recovery—limiting damage and maintaining service.

---

## Graceful Degradation Ladder

### Intent
Define explicit levels of reduced functionality, each maintaining safety while sacrificing capability, allowing the system to step down gracefully rather than fail completely.

### Motivation
When components fail, you rarely face a binary choice between full operation and complete shutdown. Intermediate modes can maintain partial service while ensuring safety. Pre-defined degradation levels allow fast, tested transitions.

### Structure
```
┌─────────────────────────────────────────────────────────────┐
│                 Graceful Degradation Ladder                  │
│                                                              │
│   Level 0: FULL OPERATION                                   │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ All features enabled, autonomous operation           │   │
│   │ Trigger to L1: Component failure, anomaly detected   │   │
│   └──────────────────────────┬──────────────────────────┘   │
│                              ▼                               │
│   Level 1: REDUCED AUTONOMY                                 │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ Core features only, human approval for high-stakes   │   │
│   │ Trigger to L2: Multiple failures, high error rate    │   │
│   └──────────────────────────┬──────────────────────────┘   │
│                              ▼                               │
│   Level 2: CONSERVATIVE MODE                                │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ Read-only operations, no modifications, log only     │   │
│   │ Trigger to L3: Security concern, integrity violation │   │
│   └──────────────────────────┬──────────────────────────┘   │
│                              ▼                               │
│   Level 3: SAFE MODE                                        │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ Pre-defined safe responses only, no dynamic behavior │   │
│   │ Trigger to L4: Confirmed compromise, critical failure│   │
│   └──────────────────────────┬──────────────────────────┘   │
│                              ▼                               │
│   Level 4: EMERGENCY SHUTDOWN                               │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ All operations halted, human intervention required   │   │
│   └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Level Definitions

| Level | State | Capabilities | Safety |
|-------|-------|--------------|--------|
| **L0** | Full | All features | Standard checks |
| **L1** | Reduced | Core features | Enhanced verification |
| **L2** | Conservative | Read-only | All writes blocked |
| **L3** | Safe | Static responses | No AI execution |
| **L4** | Emergency | None | Complete shutdown |

### Implementation

```python
class DegradationLadder:
    LEVELS = [
        DegradationLevel(
            name='FULL_OPERATION',
            capabilities=ALL_CAPABILITIES,
            checks=STANDARD_CHECKS
        ),
        DegradationLevel(
            name='REDUCED_AUTONOMY',
            capabilities=CORE_CAPABILITIES,
            checks=ENHANCED_CHECKS,
            requires_approval_for=HIGH_STAKES_ACTIONS
        ),
        DegradationLevel(
            name='CONSERVATIVE_MODE',
            capabilities=READ_ONLY,
            checks=ALL_CHECKS,
            blocks=ALL_MODIFICATIONS
        ),
        DegradationLevel(
            name='SAFE_MODE',
            capabilities=STATIC_RESPONSES_ONLY,
            checks=None,  # No dynamic execution
            response_set=PREDEFINED_SAFE_RESPONSES
        ),
        DegradationLevel(
            name='EMERGENCY_SHUTDOWN',
            capabilities=NONE,
            requires_human_restart=True
        )
    ]

    def __init__(self):
        self.current_level = 0
        self.level_history = []

    def degrade(self, reason: str, severity: int = 1):
        """Step down the degradation ladder."""
        new_level = min(self.current_level + severity, len(self.LEVELS) - 1)
        self.transition_to(new_level, reason)

    def transition_to(self, level: int, reason: str):
        self.level_history.append({
            'from': self.current_level,
            'to': level,
            'reason': reason,
            'timestamp': time.now()
        })

        self.current_level = level
        self.apply_level_restrictions()
        self.notify_operators(level, reason)

    def attempt_recovery(self) -> bool:
        """Try to move back up the ladder."""
        if self.current_level == 0:
            return True  # Already at top

        if self.recovery_checks_pass():
            new_level = self.current_level - 1
            self.transition_to(new_level, 'recovery_check_passed')
            return True
        return False
```

### Transition Triggers

```python
class DegradationTriggers:
    TRIGGERS = {
        'L0_to_L1': [
            Trigger(condition='component_failure', threshold=1),
            Trigger(condition='anomaly_score', threshold=0.7),
            Trigger(condition='error_rate', threshold=0.05),
        ],
        'L1_to_L2': [
            Trigger(condition='component_failure', threshold=3),
            Trigger(condition='error_rate', threshold=0.15),
            Trigger(condition='verification_failure', threshold=1),
        ],
        'L2_to_L3': [
            Trigger(condition='security_alert', threshold=1),
            Trigger(condition='integrity_violation', threshold=1),
            Trigger(condition='deception_detected', threshold=1),
        ],
        'L3_to_L4': [
            Trigger(condition='confirmed_compromise', threshold=1),
            Trigger(condition='critical_system_failure', threshold=1),
            Trigger(condition='human_override', threshold=1),
        ],
    }
```

### Consequences

**Benefits**:
- Maintains partial service during problems
- Clear, tested degradation paths
- Automatic response to various failure modes
- Preserves safety even at reduced functionality

**Costs**:
- Requires designing multiple operating modes
- Testing all levels is expensive
- Users must handle varying capabilities
- Can mask underlying problems if level sticks

### Known Uses
- Aircraft systems (normal → direct law → alternate law)
- Cloud service tiers during outages
- Hospital generator backup systems

### Related Patterns
- Triggered by **Circuit Breaker Cascade**
- Use **Checkpoint-Rollback** to restore L0
- **Fallback Component Chain** provides alternatives within levels

---

## Checkpoint-Rollback

### Intent
Periodically save system state to known-good checkpoints, enabling rollback when problems are detected—undoing harmful changes rather than just stopping them.

### Motivation
Catching an error after the fact is only useful if you can undo the damage. Regular checkpointing creates restore points. Fast rollback limits the blast radius of any incident.

### Structure
```
┌─────────────────────────────────────────────────────────────┐
│                   Checkpoint-Rollback System                 │
│                                                              │
│  Timeline:                                                   │
│  ═══════════════════════════════════════════════════════════│
│  │    │    │    │    │    │    │    │    │                  │
│  CP1  CP2  CP3  CP4  CP5  CP6  CP7  [Error]                 │
│                                      Detected!               │
│                                          │                   │
│                                          ▼                   │
│  ═══════════════════════════════════════════════════════════│
│  │    │    │    │    │    │    │◄───────┘                   │
│  CP1  CP2  CP3  CP4  CP5  CP6  [Rollback to CP6]            │
│                                                              │
│  Checkpoint Contents:                                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ • Full system state snapshot                        │    │
│  │ • All database records at that moment               │    │
│  │ • Agent memory/context                              │    │
│  │ • In-flight task queue                              │    │
│  │ • External system sync points                       │    │
│  │ • Verification hash                                 │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Checkpoint Strategies

| Strategy | When to Checkpoint | Use Case |
|----------|-------------------|----------|
| **Time-based** | Every N minutes | General protection |
| **Operation-based** | After N operations | High-volume systems |
| **Milestone-based** | After key operations | Pipeline stages |
| **Risk-based** | Before risky operations | High-stakes actions |
| **Change-based** | When significant state changes | Efficient storage |

### Implementation

```python
class CheckpointRollbackSystem:
    def __init__(self, storage: CheckpointStorage, retention: int = 10):
        self.storage = storage
        self.retention = retention
        self.checkpoints = []

    def create_checkpoint(self, reason: str = 'scheduled') -> Checkpoint:
        """Capture current system state."""
        checkpoint = Checkpoint(
            id=generate_id(),
            timestamp=time.now(),
            reason=reason,
            state=self.capture_state(),
            hash=self.compute_state_hash()
        )

        self.storage.save(checkpoint)
        self.checkpoints.append(checkpoint.id)

        # Prune old checkpoints
        while len(self.checkpoints) > self.retention:
            old_id = self.checkpoints.pop(0)
            self.storage.delete(old_id)

        return checkpoint

    def capture_state(self) -> SystemState:
        """Capture all relevant system state."""
        return SystemState(
            database=self.snapshot_database(),
            agent_states=self.snapshot_agents(),
            task_queue=self.snapshot_queue(),
            config=self.snapshot_config(),
            external_sync_points=self.get_external_sync_points()
        )

    def rollback_to(self, checkpoint_id: str) -> RollbackResult:
        """Restore system to checkpoint state."""
        checkpoint = self.storage.load(checkpoint_id)

        # Verify checkpoint integrity
        if not self.verify_checkpoint(checkpoint):
            raise CorruptedCheckpointError(checkpoint_id)

        # Stop all operations
        self.pause_system()

        try:
            # Restore state
            self.restore_database(checkpoint.state.database)
            self.restore_agents(checkpoint.state.agent_states)
            self.restore_queue(checkpoint.state.task_queue)
            self.restore_config(checkpoint.state.config)

            # Notify external systems
            self.notify_rollback(checkpoint)

            return RollbackResult(success=True, restored_to=checkpoint)
        except Exception as e:
            # Rollback of rollback - go to even earlier checkpoint
            return self.emergency_rollback(e)
        finally:
            self.resume_system()

    def automatic_rollback_on_error(self, error: Error):
        """Triggered when error is detected."""
        # Find last known-good checkpoint
        for checkpoint_id in reversed(self.checkpoints):
            checkpoint = self.storage.load(checkpoint_id)
            if checkpoint.timestamp < error.first_detected:
                if self.was_state_healthy(checkpoint):
                    return self.rollback_to(checkpoint_id)

        # No good checkpoint found
        raise NoValidCheckpointError()
```

### External System Coordination

Rolling back internal state is insufficient if external effects occurred:

```python
class ExternalRollbackCoordinator:
    def prepare_rollback(self, checkpoint: Checkpoint):
        """Coordinate with external systems before rollback."""
        external_actions = self.get_actions_since(checkpoint.timestamp)

        reversible = []
        irreversible = []

        for action in external_actions:
            if action.can_reverse():
                reversible.append(action)
            else:
                irreversible.append(action)

        if irreversible:
            self.alert_irreversible_actions(irreversible)

        return RollbackPlan(
            internal_rollback=checkpoint,
            external_reversals=reversible,
            requires_manual=[a for a in irreversible if a.requires_manual_fix]
        )
```

### Consequences

**Benefits**:
- Can undo harmful changes, not just stop them
- Known-good states are tested and verified
- Limits damage from any incident to checkpoint interval
- Enables fearless experimentation

**Costs**:
- Storage cost for checkpoints
- Checkpoint creation has overhead
- External effects may not be reversible
- Rollback loses work since checkpoint

### Known Uses
- Database transaction logs
- Version control systems
- Game save systems

### Related Patterns
- Use in **Task Decomposition Pipeline** between stages
- Triggered by **Circuit Breaker Cascade** and **Tripwire Mesh**
- Enables recovery in **Graceful Degradation Ladder**

---

## Fallback Component Chain

### Intent
Maintain a prioritized chain of alternative implementations, automatically switching to the next option when the preferred component fails.

### Motivation
Single implementations are single points of failure. By pre-integrating fallback alternatives, you can maintain service even when primary components fail. Different fallbacks may trade off quality for reliability.

### Structure
```
┌─────────────────────────────────────────────────────────────┐
│                  Fallback Component Chain                    │
│                                                              │
│    ┌─────────────────────────────────────────────────┐      │
│    │                    Request                       │      │
│    └────────────────────────┬────────────────────────┘      │
│                             │                                │
│                             ▼                                │
│    ┌─────────────────────────────────────────────────┐      │
│    │              Fallback Router                     │      │
│    └────────────────────────┬────────────────────────┘      │
│                             │                                │
│         ┌───────────────────┼───────────────────┐           │
│         ▼                   ▼                   ▼           │
│    ┌─────────┐         ┌─────────┐         ┌─────────┐     │
│    │Primary  │ fail    │Secondary│ fail    │Tertiary │     │
│    │(GPT-4)  │────────▶│(Claude) │────────▶│(Cached) │     │
│    └────┬────┘         └────┬────┘         └────┬────┘     │
│         │                   │                   │           │
│         │ success           │ success           │ success   │
│         │                   │                   │           │
│         └───────────────────┴───────────────────┘           │
│                             │                                │
│                             ▼                                │
│    ┌─────────────────────────────────────────────────┐      │
│    │                   Response                       │      │
│    │        (with source attribution)                 │      │
│    └─────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Fallback Hierarchy Examples

**For LLM Requests:**
1. Primary: GPT-4 (highest quality)
2. Secondary: Claude (different failure modes)
3. Tertiary: Local LLM (no external dependency)
4. Emergency: Cached responses / rule-based

**For Critical Decisions:**
1. Primary: Full ensemble voting
2. Secondary: Single high-quality model
3. Tertiary: Conservative heuristics
4. Emergency: Human escalation

### Implementation

```python
class FallbackChain:
    def __init__(self, components: list[Component]):
        self.components = components  # Ordered by preference
        self.health_tracker = ComponentHealthTracker()

    async def execute(self, request: Request) -> Response:
        errors = []

        for component in self.components:
            # Skip unhealthy components
            if not self.health_tracker.is_healthy(component):
                continue

            try:
                response = await component.execute(
                    request,
                    timeout=self.timeout_for(component)
                )

                # Mark success for health tracking
                self.health_tracker.record_success(component)

                return Response(
                    result=response,
                    source=component.name,
                    fallback_level=self.components.index(component)
                )

            except Exception as e:
                self.health_tracker.record_failure(component, e)
                errors.append((component.name, e))
                continue

        # All components failed
        raise AllComponentsFailedError(errors)

    def timeout_for(self, component: Component) -> float:
        """Later fallbacks get less time."""
        position = self.components.index(component)
        return self.base_timeout * (0.8 ** position)

class ComponentHealthTracker:
    def is_healthy(self, component: Component) -> bool:
        """Check if component should be tried."""
        stats = self.get_stats(component)

        # Circuit breaker logic
        if stats.recent_failure_rate > 0.5:
            if not stats.cooldown_expired:
                return False

        return True
```

### Quality vs. Reliability Trade-offs

```python
class FallbackQualityTracker:
    def get_quality_estimate(self, component: Component) -> float:
        """Expected quality of component's output."""
        return {
            'gpt4': 0.95,
            'claude': 0.92,
            'local_llm': 0.75,
            'cached': 0.60,
            'heuristic': 0.40
        }.get(component.name, 0.5)

    def should_accept_fallback(
        self, component: Component, request: Request
    ) -> bool:
        """Some requests require minimum quality."""
        quality = self.get_quality_estimate(component)
        required = request.minimum_quality or 0.0
        return quality >= required
```

### Consequences

**Benefits**:
- High availability despite component failures
- Automatic failover without human intervention
- Quality degrades gracefully, service continues
- Different failure modes across fallbacks

**Costs**:
- Maintaining multiple implementations
- Users may receive varying quality
- Need to handle heterogeneous outputs
- Cost of keeping fallbacks ready

### Known Uses
- CDN fallback chains
- Database replica failover
- Payment gateway alternatives

### Related Patterns
- Works within **Graceful Degradation Ladder** levels
- Triggered by **Circuit Breaker Cascade**
- Consider **Shadow Verification** to compare fallback quality

---

## Blast Radius Containment

### Intent
Design system boundaries so that failures in one area cannot propagate beyond defined limits, containing damage to the smallest possible scope.

### Motivation
Without explicit containment, failures can cascade across the entire system. By defining blast radius boundaries upfront, you ensure that even worst-case failures affect only a limited scope.

### Structure
```
┌─────────────────────────────────────────────────────────────┐
│                 Blast Radius Containment                     │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                    System                            │   │
│   │                                                      │   │
│   │   ┌───────────────────┐   ┌───────────────────┐     │   │
│   │   │   Zone A          │   │   Zone B          │     │   │
│   │   │ ┌───┐ ┌───┐ ┌───┐│   │ ┌───┐ ┌───┐ ┌───┐│     │   │
│   │   │ │ 1 │ │ 2 │ │ 3 ││   │ │ 4 │ │ 5 │ │ 6 ││     │   │
│   │   │ └───┘ └───┘ └───┘│   │ └───┘ └───┘ └───┘│     │   │
│   │   │   Isolated        │   │   Isolated        │     │   │
│   │   └─────────┬─────────┘   └─────────┬─────────┘     │   │
│   │             │                       │               │   │
│   │             │     ┌─────────┐       │               │   │
│   │             └────▶│ Gateway │◀──────┘               │   │
│   │                   │(limited)│                       │   │
│   │                   └─────────┘                       │   │
│   │                                                      │   │
│   │   If Zone A fails:                                  │   │
│   │   ✗ Components 1,2,3 affected                       │   │
│   │   ✓ Components 4,5,6 protected                      │   │
│   │   ✓ Gateway limits cross-zone impact                │   │
│   │                                                      │   │
│   └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Containment Mechanisms

| Mechanism | How It Limits Blast Radius |
|-----------|---------------------------|
| **Resource Isolation** | Separate compute, memory, storage per zone |
| **Network Segmentation** | Firewall rules between zones |
| **Rate Limiting** | Cap cross-zone requests |
| **Bulkheads** | Separate thread pools / connection pools |
| **Timeouts** | Prevent indefinite waits on failed zones |
| **Data Partitioning** | Each zone has separate data stores |

### Implementation

```python
class BlastRadiusContainer:
    def __init__(self, zones: list[Zone]):
        self.zones = {z.id: z for z in zones}
        self.cross_zone_limiter = RateLimiter(max_requests_per_second=100)

    def create_zone(self, config: ZoneConfig) -> Zone:
        """Create an isolated zone with its own resources."""
        return Zone(
            id=generate_id(),
            compute=IsolatedCompute(config.compute_quota),
            memory=IsolatedMemory(config.memory_quota),
            storage=IsolatedStorage(config.storage_quota),
            network=IsolatedNetwork(
                internal_only=True,
                external_gateway=self.create_gateway(config)
            )
        )

    def create_gateway(self, config: ZoneConfig) -> Gateway:
        """Create limited gateway for cross-zone communication."""
        return Gateway(
            rate_limit=config.cross_zone_rate_limit,
            timeout=config.cross_zone_timeout,
            circuit_breaker=CircuitBreaker(
                failure_threshold=3,
                recovery_timeout=30
            ),
            allowed_operations=config.allowed_cross_zone_operations
        )

    def cross_zone_call(
        self, from_zone: str, to_zone: str, request: Request
    ) -> Response:
        """Make a call across zone boundaries."""
        # Rate limit
        if not self.cross_zone_limiter.allow():
            raise CrossZoneRateLimitExceeded()

        gateway = self.zones[from_zone].network.external_gateway

        # Check allowed operations
        if request.operation not in gateway.allowed_operations:
            raise OperationNotAllowedAcrossZones()

        # Make call with timeout and circuit breaker
        return gateway.call(to_zone, request)
```

### Zone Design Principles

**Independence**: Each zone should be able to function if others fail.

**Minimal Coupling**: Cross-zone communication should be explicit and limited.

**Clear Boundaries**: Zone membership should be obvious and enforced.

**Resource Limits**: Each zone has hard caps preventing resource exhaustion.

```python
class Zone:
    def check_resource_limits(self):
        """Enforce zone resource limits."""
        if self.compute.usage > self.compute.quota:
            self.throttle_compute()

        if self.memory.usage > self.memory.quota:
            self.evict_memory()

        if self.storage.usage > self.storage.quota:
            raise StorageQuotaExceeded()

    def isolate_failure(self, component_id: str):
        """Contain a component failure within the zone."""
        component = self.get_component(component_id)

        # Remove from rotation
        component.disable()

        # Clean up resources
        component.release_resources()

        # Notify zone-local components only
        self.notify_zone_components(ComponentFailed(component_id))

        # Do NOT propagate to other zones
```

### Consequences

**Benefits**:
- Failures don't cascade across entire system
- Clear, predictable failure boundaries
- Easier to reason about worst-case impact
- Independent zone recovery

**Costs**:
- Resource overhead of isolation
- Cross-zone operations are slower/limited
- May duplicate functionality across zones
- Zone boundaries can be complex to design

### Known Uses
- AWS availability zones
- Kubernetes namespaces
- Aircraft compartmentalization

### Related Patterns
- Each zone can have its own **Circuit Breaker Cascade**
- **Fallback Component Chain** within zones
- Cross-zone calls through **Capability Quarantine**

---

## Self-Healing Loop

### Intent
Implement automated recovery procedures that detect problems and fix them without human intervention, maintaining system health autonomously.

### Motivation
Human-in-the-loop recovery is slow and expensive. For known, recoverable problems, automated healing reduces downtime and operational burden. The system should maintain itself.

### Structure
```
┌─────────────────────────────────────────────────────────────┐
│                    Self-Healing Loop                         │
│                                                              │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐             │
│   │ Monitor │────▶│ Analyze │────▶│ Diagnose│             │
│   └─────────┘     └─────────┘     └─────────┘             │
│        ▲                               │                    │
│        │                               ▼                    │
│        │                         ┌─────────┐               │
│        │                         │ Known   │               │
│        │                         │ Issue?  │               │
│        │                         └────┬────┘               │
│        │                    yes ┌─────┴─────┐ no           │
│        │                        ▼           ▼              │
│        │               ┌─────────────┐ ┌─────────────┐     │
│        │               │ Auto-Heal   │ │ Escalate to │     │
│        │               │ (runbook)   │ │   Human     │     │
│        │               └──────┬──────┘ └─────────────┘     │
│        │                      │                            │
│        │                      ▼                            │
│        │               ┌─────────────┐                     │
│        │               │  Verify     │                     │
│        │               │  Recovery   │                     │
│        │               └──────┬──────┘                     │
│        │                      │                            │
│        │           ┌──────────┴──────────┐                 │
│        │           ▼                     ▼                 │
│        │    ┌──────────┐          ┌──────────┐            │
│        │    │ Healed   │          │ Escalate │            │
│        └────┤(continue)│          │ (failed) │            │
│             └──────────┘          └──────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### Healing Runbooks

| Issue | Detection | Auto-Heal Action |
|-------|-----------|------------------|
| **High Memory** | Memory > 90% | Restart component |
| **Stuck Request** | Request > timeout | Kill and retry |
| **Connection Leak** | Connections growing | Reset pool |
| **Degraded Model** | Error rate spike | Switch to backup |
| **Disk Full** | Disk > 95% | Delete old logs |
| **Rate Limited** | 429 responses | Exponential backoff |
| **Certificate Expiry** | 7 days before | Auto-renew |

### Implementation

```python
class SelfHealingLoop:
    def __init__(self, runbooks: list[HealingRunbook]):
        self.runbooks = {rb.issue_type: rb for rb in runbooks}
        self.health_monitor = HealthMonitor()

    async def run(self):
        """Continuous self-healing loop."""
        while True:
            issues = await self.health_monitor.get_issues()

            for issue in issues:
                await self.handle_issue(issue)

            await asyncio.sleep(self.check_interval)

    async def handle_issue(self, issue: Issue):
        runbook = self.runbooks.get(issue.type)

        if not runbook:
            await self.escalate_unknown_issue(issue)
            return

        # Check if auto-healing is safe
        if not runbook.is_safe_to_auto_heal(issue):
            await self.escalate_unsafe_issue(issue, runbook)
            return

        # Execute healing action
        try:
            result = await runbook.execute(issue)

            # Verify recovery
            if await self.verify_healed(issue):
                self.log_successful_heal(issue, runbook)
            else:
                await self.escalate_failed_heal(issue, runbook)

        except Exception as e:
            await self.escalate_heal_error(issue, runbook, e)

class HealingRunbook:
    def __init__(
        self,
        issue_type: str,
        detection: Callable,
        action: Callable,
        verification: Callable,
        max_attempts: int = 3,
        cooldown: timedelta = timedelta(minutes=5)
    ):
        self.issue_type = issue_type
        self.detection = detection
        self.action = action
        self.verification = verification
        self.max_attempts = max_attempts
        self.cooldown = cooldown
        self.recent_attempts = []

    def is_safe_to_auto_heal(self, issue: Issue) -> bool:
        # Don't heal too frequently
        recent = [a for a in self.recent_attempts
                  if a.timestamp > time.now() - self.cooldown]
        if len(recent) >= self.max_attempts:
            return False

        # Don't heal during other healing operations
        if self.is_healing_in_progress():
            return False

        return True
```

### Safety Limits

Auto-healing must have limits to avoid healing loops:

```python
class HealingSafetyLimits:
    def __init__(self):
        self.max_heals_per_hour = 10
        self.max_consecutive_failures = 3
        self.require_human_after_failures = True

    def should_continue_healing(self, component: str) -> bool:
        history = self.get_healing_history(component)

        # Too many heals recently
        recent_heals = history.count_in_last(hours=1)
        if recent_heals >= self.max_heals_per_hour:
            return False

        # Consecutive failures indicate deeper problem
        if history.consecutive_failures >= self.max_consecutive_failures:
            if self.require_human_after_failures:
                return False

        return True
```

### Consequences

**Benefits**:
- Reduced downtime from known issues
- Lower operational burden
- Faster recovery than human response
- Consistent, tested recovery procedures

**Costs**:
- Runbooks must be carefully designed and tested
- Risk of healing loops or over-healing
- May mask underlying systemic problems
- Unknown issues still need human intervention

### Known Uses
- Kubernetes self-healing pods
- Auto-scaling groups
- Database automatic failover

### Related Patterns
- Monitors feed from **Tripwire Mesh** and **Behavioral Fingerprinting**
- Uses **Checkpoint-Rollback** as one healing action
- Escalates to **Graceful Degradation Ladder** when healing fails
