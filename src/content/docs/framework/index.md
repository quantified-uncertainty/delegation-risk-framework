---
title: The Framework
description: The quantitative foundation for measuring, decomposing, and managing delegation risk.
---

This section contains the core intellectual contribution: a rigorous framework for quantifying delegation risk.

## Prerequisites

Before diving in, you should understand:
- [Core Concepts](/getting-started/core-concepts/) — The key ideas without mathematical formalism
- [Introduction](/getting-started/introduction/) — Why this problem matters

## Reading Order

These pages build on each other. Read in sequence:

1. **[Overview](/framework/overview/)** — The core formula and how pieces fit together
2. **[Walkthrough: The $1,000 Delivery](/framework/walkthrough/)** — Complete worked example
3. **[Delegation Accounting](/framework/delegation-accounting/)** — Balance sheet view of delegation
4. **[Risk Decomposition](/framework/risk-decomposition/)** — Accidents vs. defection: two types of harm
5. **[Exposure Cascade](/framework/exposure-cascade/)** — How risk compounds through delegation chains
6. **[The Insurer's Dilemma](/framework/insurers-dilemma/)** — Moral hazard and pricing delegation risk

## Section Contents

| Page | Key Question | Builds On |
|------|--------------|-----------|
| [Overview](/framework/overview/) | How do we quantify delegation risk? | Core Concepts |
| [Walkthrough](/framework/walkthrough/) | What does this look like in practice? | Overview |
| [Delegation Accounting](/framework/delegation-accounting/) | How do we track risk like finances? | Overview |
| [Risk Decomposition](/framework/risk-decomposition/) | What types of harm can occur? | Overview |
| [Exposure Cascade](/framework/exposure-cascade/) | How does risk flow through chains? | Accounting, Decomposition |
| [Insurer's Dilemma](/framework/insurers-dilemma/) | How do we price and bound exposure? | All above |

## The Core Formula

The framework centers on one equation:

```
Delegation Risk = Σ P(failure mode) × Damage(failure mode)
```

Where failure modes decompose into:
- **Accident Risk** — Bugs, errors, capability limits (non-goal-directed)
- **Defection Risk** — Scheming, deception, misalignment (goal-directed)

The [Overview](/framework/overview/) explains this in detail with worked examples.

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
