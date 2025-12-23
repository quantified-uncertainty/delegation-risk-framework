---
title: The Framework
description: The quantitative foundation for measuring delegation risk and capability.
---

This section contains the core intellectual contribution: a rigorous framework for quantifying both **what we want to maximize** (capability) and **what we want to minimize** (risk).

## Prerequisites

Before diving in, you should understand:
- [Core Concepts](/getting-started/core-concepts/) — The key ideas without mathematical formalism
- [Introduction](/getting-started/introduction/) — Why this problem matters

## The Fundamental Optimization Problem

The framework addresses one central question:

$$\max \text{Capability} \quad \text{subject to} \quad \text{DelegationRisk} \leq \text{Budget}$$

This requires formalizing both sides:
- **Capability** = Power × Agency (what the system can accomplish)
- **Delegation Risk** = Σ P(harm) × Damage (what could go wrong)

## Reading Order

These pages build on each other. Read in sequence:

### Formalizing Capability (The Positive Side)
1. **[Agent, Power, and Authority](/framework/capability/agent-power-formalization/)** — What makes something an agent? How do we measure power?
2. **[Worked Examples: Agency and Power](/framework/capability/agency-power-examples/)** — Concrete calculations for real systems
3. **[The Strong Tools Hypothesis](/framework/capability/strong-tools-hypothesis/)** — Can we have high capability with low agency?

### Formalizing Risk (The Negative Side)
4. **[Delegation Risk Overview](/framework/risk/overview/)** — The core formula for quantifying risk
5. **[Walkthrough: The $1,000 Delivery](/framework/risk/walkthrough/)** — Complete worked example
6. **[Risk Decomposition](/framework/risk/risk-decomposition/)** — Accidents vs. defection: two types of harm

### Managing Delegation
7. **[Delegation Accounting](/framework/risk/delegation-accounting/)** — Balance sheet view of delegation
8. **[Exposure Cascade](/framework/risk/exposure-cascade/)** — How risk compounds through delegation chains
9. **[The Insurer's Dilemma](/framework/risk/insurers-dilemma/)** — Moral hazard and pricing delegation risk

## Section Contents

| Page | Key Question |
|------|--------------|
| [Agent, Power, Authority](/framework/capability/agent-power-formalization/) | How do we formalize capability? |
| [Agency/Power Examples](/framework/capability/agency-power-examples/) | What do these metrics look like for real systems? |
| [Strong Tools Hypothesis](/framework/capability/strong-tools-hypothesis/) | Can we get capability without dangerous agency? |
| [Delegation Risk Overview](/framework/risk/overview/) | How do we quantify delegation risk? |
| [Walkthrough](/framework/risk/walkthrough/) | What does this look like in practice? |
| [Risk Decomposition](/framework/risk/risk-decomposition/) | What types of harm can occur? |
| [Delegation Accounting](/framework/risk/delegation-accounting/) | How do we track risk like finances? |
| [Exposure Cascade](/framework/risk/exposure-cascade/) | How does risk flow through chains? |
| [Insurer's Dilemma](/framework/risk/insurers-dilemma/) | How do we price and bound exposure? |

## The Core Equations

### Capability Side

```
Effective Capability = Power × Agency

Where:
- Power = ability to achieve diverse goals
- Agency = coherence of goal-pursuit (0 = tool, 1 = perfect optimizer)
```

### Risk Side

```
Delegation Risk = Σ P(harm mode) × Damage(harm mode)

Where harm modes decompose into:
- Accident Risk — Bugs, errors, capability limits (non-goal-directed)
- Defection Risk — Scheming, deception, misalignment (goal-directed)
```

### Combined

```
RACAP (Risk-Adjusted Capability) = Capability / Risk

Higher RACAP = more efficient system design
```

## Key Insight

**High power + low agency may be optimal.**

"Strong tools" provide capability without coherent optimization pressure. A search engine is extremely powerful but not an agent. If we can build AGI-level capability with tool-like agency, we may sidestep the alignment problem for many applications.

See [The Strong Tools Hypothesis](/framework/capability/strong-tools-hypothesis/) for analysis.

## How This Section Connects

```
                    [Getting Started]
                          ↓
                    ┌─────────────┐
                    │  FRAMEWORK  │ ← You are here
                    └─────────────┘
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
  [Applying]        [Case Studies]    [Deep Dives]
  (practical)       (examples)        (theory)
```

## Next Steps

After understanding the framework:
- **Apply it** → [Applying the Framework](/applying/) for design principles and tools
- **See examples** → [Case Studies](/case-studies/) for real-world applications
- **Go deeper** → [Deep Dives](/deep-dives/) for theoretical foundations
