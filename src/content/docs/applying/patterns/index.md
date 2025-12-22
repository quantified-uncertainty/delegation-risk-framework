---
title: "Design Patterns"
description: "Reusable architectural patterns for safe AI delegation"
sidebar:
  order: 0
---

# Design Patterns for Safe Delegation

This section catalogs **reusable architectural patterns** for building safer AI systems. Like the Gang of Four design patterns for software, these are named, documented solutions to recurring problems in AI delegation.

## Why Patterns?

Patterns capture hard-won knowledge:
- **Shared vocabulary**: "Use a Supervisor Chain" is faster than explaining the architecture
- **Proven solutions**: Each pattern has been tested in real deployments
- **Trade-off awareness**: Patterns document costs, not just benefits
- **Composability**: Patterns combine to create robust architectures

## Pattern Categories

### [Delegation Architecture Patterns](/applying/patterns/delegation-architectures/)
How to structure the relationship between principals and AI agents:
- **Supervisor Chain** - Hierarchical oversight with escalation
- **Consensus Committee** - Multiple agents must agree
- **Graduated Autonomy** - Trust increases with track record
- **Capability Quarantine** - Isolate dangerous capabilities
- **Task Decomposition Pipeline** - Break complex tasks into verifiable steps

### [Safety Mechanism Patterns](/applying/patterns/safety-mechanisms/)
Runtime protections that catch problems before damage occurs:
- **Tripwire Mesh** - Distributed detection points
- **Shadow Verification** - Parallel checking without blocking
- **Semantic Firewall** - Content-aware filtering
- **Behavioral Fingerprinting** - Detect anomalous patterns
- **Circuit Breaker Cascade** - Coordinated shutdown

### [Deception Detection Patterns](/applying/patterns/deception-detection/)
Patterns specifically for detecting scheming or manipulation:
- **Honeypot Injection** - Traps that only schemers trigger
- **Consistency Triangulation** - Cross-reference for contradictions
- **Capability Probing** - Test for hidden abilities
- **Information Asymmetry Exploitation** - Use what the agent doesn't know
- **Temporal Behavior Analysis** - Detect strategic timing

### [Recovery & Resilience Patterns](/applying/patterns/recovery-resilience/)
How to handle failures gracefully:
- **Graceful Degradation Ladder** - Staged capability reduction
- **Checkpoint-Rollback** - Return to known-good states
- **Fallback Component Chain** - Alternative implementations ready
- **Blast Radius Containment** - Limit damage propagation
- **Self-Healing Loop** - Automatic recovery procedures

---

## Pattern Template

Each pattern is documented with:

| Section | Description |
|---------|-------------|
| **Intent** | What problem does this solve? |
| **Motivation** | When and why would you use this? |
| **Structure** | Architecture diagram or pseudocode |
| **Participants** | What components are involved? |
| **Dynamics** | How do components interact? |
| **Consequences** | Trade-offs and limitations |
| **Implementation** | Practical guidance |
| **Known Uses** | Real-world examples |
| **Related Patterns** | What combines well or conflicts? |

---

## Pattern Selection Guide

### By Threat Model

| Primary Threat | Recommended Patterns |
|----------------|---------------------|
| Capability errors | Supervisor Chain, Shadow Verification, Checkpoint-Rollback |
| Adversarial inputs | Semantic Firewall, Input Sanitization Pipeline, Tripwire Mesh |
| AI scheming | Honeypot Injection, Consistency Triangulation, Capability Probing |
| Cascading failures | Circuit Breaker Cascade, Blast Radius Containment, Graceful Degradation |
| Trust miscalibration | Graduated Autonomy, Track Record Gating, Capability Quarantine |

### By System Characteristics

| System Type | Pattern Focus |
|-------------|---------------|
| High-throughput | Async patterns, Shadow Verification, Sampling |
| Low-latency critical | Pre-computed fallbacks, Fail-fast, Circuit Breakers |
| High-stakes decisions | Consensus Committee, Multi-layer Verification, Human-in-loop |
| Long-running tasks | Checkpoint-Rollback, Progress Monitoring, Timeout Escalation |
| Multi-agent | Behavioral Fingerprinting, Consistency Triangulation, Byzantine Voting |

---

## Composing Patterns

Patterns are most powerful in combination. Common compositions:

### Defense in Depth Stack
```
┌─────────────────────────────────────┐
│         Semantic Firewall           │  ← Block obvious bad outputs
├─────────────────────────────────────┤
│       Shadow Verification           │  ← Parallel correctness check
├─────────────────────────────────────┤
│      Behavioral Fingerprint         │  ← Detect anomalous patterns
├─────────────────────────────────────┤
│        Tripwire Mesh                │  ← Catch what slips through
├─────────────────────────────────────┤
│     Circuit Breaker Cascade         │  ← Shut down if overwhelmed
└─────────────────────────────────────┘
```

### Trust Escalation Pipeline
```
Capability Quarantine → Graduated Autonomy → Supervisor Chain
     (start here)         (earn trust)        (for high stakes)
```

### Resilient Execution
```
Checkpoint-Rollback + Fallback Chain + Graceful Degradation
   (save state)       (alternatives)    (reduce scope)
```

---

## Anti-Pattern Awareness

Each pattern page notes related **anti-patterns** to avoid. Common mistakes:

- **Over-engineering**: Adding patterns that don't address real threats
- **Pattern cargo-culting**: Using patterns without understanding trade-offs
- **Incomplete implementation**: Half-implementing a pattern (often worse than nothing)
- **Pattern conflicts**: Combining patterns that interfere with each other

See also: [Anti-Patterns Guide](/case-studies/ai-systems/anti-patterns/)
