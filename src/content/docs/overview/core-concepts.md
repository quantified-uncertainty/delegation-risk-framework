---
title: "Core Concepts"
---

# Core Concepts

This page introduces the key ideas without mathematical formalism. For the quantitative details, see [Trust Calculus](/trust-calculus/overview/).

## Framework Overview

How all the pieces fit together:

```mermaid
flowchart TB
    subgraph Foundation["Foundation: What We're Managing"]
        TRUST["Trust as Resource<br/>ETE = Σ P(harm) × Damage"]
    end

    subgraph Principles["Principles: How We Constrain"]
        LEASTX["Least X Principles<br/>Intelligence, Privilege, Context..."]
        COORD["Coordinator Constraints<br/>Decomposed, stateless, verified"]
    end

    subgraph Architecture["Architecture: How We Build"]
        DECOMP["Decomposed Components<br/>Narrow, specialized, isolated"]
        SAFETY["Safety Mechanisms<br/>Tripwires, circuit breakers, gates"]
        VERIFY["Verification Layers<br/>Multi-method, diverse, redundant"]
    end

    subgraph Operations["Operations: How We Run"]
        BUDGET["Risk Budgeting<br/>Allocate, monitor, enforce"]
        MONITOR["Continuous Monitoring<br/>Behavioral fingerprints, anomalies"]
    end

    TRUST --> LEASTX
    TRUST --> COORD
    LEASTX --> DECOMP
    COORD --> DECOMP
    DECOMP --> SAFETY
    DECOMP --> VERIFY
    SAFETY --> BUDGET
    VERIFY --> BUDGET
    BUDGET --> MONITOR
    MONITOR -.->|feedback| BUDGET
```

**Reading the diagram**: Trust is the resource we're managing. Principles constrain how we use it. Architecture implements those constraints. Operations ensure they hold over time.

## Trust as a Resource

When you delegate a task to an AI system, you're extending **trust**. Trust isn't abstract—it's the potential for harm if the system fails or misbehaves.

**[Expected Trust Exposure (ETE)](/overview/glossary/#core-framework-terms)** is a way to quantify this: for each component, sum over all possible bad outcomes, weighted by their probability. A component with access to your bank account has higher ETE than one that can only read public web pages.

:::tip
Trust is finite and should be budgeted. Just as organizations allocate compute and money, they should allocate trust—tracking how much they're extending, to which components, for what purposes.
:::

## Decomposition Over Monoliths

A single powerful AI agent is dangerous because it concentrates capability, context, and control. If it fails or schemes, the damage is unbounded.

**Decomposed coordination** breaks this pattern:
- Split tasks across many specialized components
- Each component has limited capability and context
- No single component can cause catastrophic harm
- Components can't easily coordinate against the system

Think of it like [separation of powers](https://en.wikipedia.org/wiki/Separation_of_powers) in government, or [microservices](https://en.wikipedia.org/wiki/Microservices) in software architecture. The coordinator itself is decomposed—strategy, tactics, verification, and aggregation handled by different components with different implementations.

### Before and After: Monolithic vs Decomposed

```mermaid
flowchart TB
    subgraph Before["❌ BEFORE: Monolithic Agent"]
        direction TB
        M["GPT-4 Agent<br/>────────────<br/>• Full context access<br/>• All capabilities<br/>• Unbounded autonomy<br/>• Single point of failure"]
        M --> OUT1[Any Output]
    end

    subgraph After["✅ AFTER: Decomposed System"]
        direction TB
        subgraph Coord["Coordination (Code)"]
            R[Router]
        end
        subgraph Workers["Narrow Components"]
            W1["Searcher<br/>Read-only"]
            W2["Summarizer<br/>Text only"]
            W3["Analyzer<br/>No actions"]
        end
        subgraph Safety["Safety Layer"]
            V[Verifier]
            G[Human Gate]
        end
        R --> W1 & W2 & W3
        W1 & W2 & W3 --> V
        V --> G
        G --> OUT2[Verified Output]
    end
```

| Aspect | Monolithic | Decomposed |
|--------|------------|------------|
| **Single point of failure** | Yes—one bad output, system fails | No—failure isolated to component |
| **Attack surface** | Entire model capability | Only exposed component interfaces |
| **Verification** | Must verify everything the model can do | Verify narrow, specific behaviors |
| **Blast radius** | Unlimited—model can do anything | Bounded—each component has limits |
| **Coordination risk** | Model coordinates with itself | Components can't easily collude |

## The "Least X" Principles

Security engineering has the [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege): give each component minimum necessary access. We extend this across multiple dimensions (see [full definitions](/overview/glossary/#least-x-principles)):

- **[Least Intelligence](/overview/glossary/#least-x-principles)**: Minimum cognitive capability needed
- **[Least Privilege](/overview/glossary/#least-x-principles)**: Minimum permissions and access rights
- **[Least Context](/overview/glossary/#least-x-principles)**: Minimum information about the broader system
- **[Least Persistence](/overview/glossary/#least-x-principles)**: Minimum state maintained across invocations
- **[Least Autonomy](/overview/glossary/#least-x-principles)**: Minimum ability to act without oversight
- **[Least Connectivity](/overview/glossary/#least-x-principles)**: Minimum communication paths between components
- **[Least Compute](/overview/glossary/#least-x-principles)**: Bounded computational resources

Each principle bounds a different attack surface. Applied together, they create components that are limited in what they can do, know, remember, and coordinate.

<details>
<summary>Why each principle matters</summary>

| Principle | What it limits | Attack surface bounded |
|-----------|---------------|----------------------|
| Least Intelligence | Optimization power | Ability to find exploits or deceptive strategies |
| Least Privilege | Access rights | Direct damage from compromised component |
| Least Context | System knowledge | Strategic planning against the system |
| Least Persistence | Memory across calls | Long-term scheming, accumulating leverage |
| Least Autonomy | Unsupervised action | Scope of damage before human intervention |
| Least Connectivity | Communication paths | Coordination between components |
| Least Compute | Processing resources | Brute-force attacks, complex planning |

</details>

## Verifiability Hierarchy

Not all implementations are equally trustworthy:

1. **Provably secure code** — Mathematical guarantees of correctness
2. **Regular code** — Auditable, testable, deterministic
3. **Fine-tuned narrow models** — Predictable within a specific domain
4. **Constrained general models** — LLMs with extensive prompting and evaluation
5. **Base LLMs** — General capability, harder to verify
6. **RL systems** — Learned policies, least predictable

:::note[Design Principle]
Use the most verifiable implementation that achieves the required functionality. Don't use a frontier LLM for tasks that can be done with code or a narrow model.
:::

```mermaid
graph TB
    subgraph "Most Verifiable"
        A[Provably Secure Code]
    end
    A --> B[Regular Code]
    B --> C[Fine-tuned Narrow Models]
    C --> D[Constrained General Models]
    D --> E[Base LLMs]
    E --> F[RL Systems]
    subgraph "Least Verifiable"
        F
    end
```

<details>
<summary>When to use each level</summary>

| Level | Use when... | Example |
|-------|-------------|---------|
| Provably secure code | Correctness is critical, logic is simple | Access control checks, rate limiters |
| Regular code | Behavior is fully specifiable | Data transformation, API routing |
| Fine-tuned narrow models | Task is well-defined, training data exists | Sentiment classification, entity extraction |
| Constrained general models | Judgment needed, outcomes recoverable | Draft generation, summarization |
| Base LLMs | Maximum flexibility needed, heavy oversight | Creative tasks, complex reasoning |
| RL systems | Learning from feedback is essential | Rarely recommended for safety-critical paths |

</details>

## Trust Propagation

When components delegate to other components, [trust relationships](/overview/glossary/#core-framework-terms) form networks. If A trusts B with weight 0.8, and B trusts C with weight 0.7, how much should A trust C?

Different rules give different answers:
- **Multiplicative**: 0.8 × 0.7 = 0.56 (each stage is independent risk)
- **Minimum**: min(0.8, 0.7) = 0.7 (chain is only as strong as weakest link)
- **Discounted**: More complex models accounting for path length

The right rule depends on what "trust" means in your context. The framework provides formal tools for reasoning about these relationships.

```mermaid
graph LR
    A((A)) -->|"0.8"| B((B))
    B -->|"0.7"| C((C))
    A -.->|"0.56 mult / 0.7 min"| C
```

<details>
<summary>Choosing a propagation rule</summary>

| Rule | Formula | Best when... |
|------|---------|--------------|
| **Multiplicative** | T(A→C) = T(A→B) × T(B→C) | Each delegation is independent risk; default choice |
| **Minimum** | T(A→C) = min(T(A→B), T(B→C)) | Chain only as strong as weakest link |
| **Discounted** | T(A→C) = T(A→B) × T(B→C) × δⁿ | Longer paths inherently less trustworthy |
| **Maximum path** | T(A→C) = max over all paths | Any valid route suffices |

Most systems should start with **multiplicative** propagation—it's intuitive, conservative, and composes well.

</details>

:::note[Related: Social Choice Theory]
Trust aggregation across multiple components relates to [social choice theory](https://en.wikipedia.org/wiki/Social_choice_theory)—how to combine individual inputs into collective outcomes. [Arrow's impossibility theorem](https://en.wikipedia.org/wiki/Arrow%27s_impossibility_theorem) has implications for trust aggregation: no perfect rule exists.
:::

## Risk Budgeting

Borrowed from finance and nuclear safety: set a total acceptable risk level for the system, then allocate [trust budgets](/overview/glossary/#core-framework-terms) to components.

Key requirements:
- **Compositional guarantees**: Component risks must aggregate predictably
- **Principled allocation**: Methods like [Euler allocation](/overview/glossary/#risk-budgeting-terms-finance) ensure budgets sum correctly
- **[Incentive-compatible](/overview/glossary/#mechanism-design-terms) reporting**: Mechanisms that make honest risk reporting optimal
- **Verification infrastructure**: Independent confirmation that claimed levels match reality
- **Conservative margins**: Buffer for uncertainty and unknown unknowns

:::note
This isn't theoretical—nuclear plants operate at 10⁻⁹ failure probability per flight hour by flowing system targets down to component budgets through fault trees.
:::

```mermaid
flowchart TD
    S[System Risk Target<br/>e.g. 10⁻⁶] --> A[Subsystem A<br/>Budget: 10⁻⁷]
    S --> B[Subsystem B<br/>Budget: 10⁻⁷]
    S --> C[Subsystem C<br/>Budget: 10⁻⁷]
    A --> V[Verification Layer]
    B --> V
    C --> V
```

## Architectural Safety

The central claim: safety can be a property of system architecture, not just individual component behavior.

If you can't guarantee an AI system is aligned, you can still:
- Limit what it can access (least privilege)
- Limit what it knows (least context)
- Limit what it can coordinate (decomposition)
- Limit how much damage it can cause (trust budgets)
- Verify its behavior matches claims (verification layers)

:::caution
These structural constraints provide defense in depth. They don't replace alignment research—they buy time and bound damage while we work on deeper solutions.
:::

## What This Framework Provides

1. **Vocabulary**: Precise terms for discussing trust, delegation, and containment
2. **Principles**: Actionable design constraints (the "Least X" family)
3. **Formal tools**: Mathematics for trust propagation and optimization
4. **Architectural patterns**: Decomposed coordination, forecasting-based navigation
5. **Cross-domain wisdom**: Adapted methods from finance, nuclear safety, security engineering

The goal is infrastructure for safely deploying AI at scale—not a complete solution to AI safety, but a foundation for managing risk as systems become more capable.

---

## Key Takeaways

:::note[Key Takeaways]
1. **ETE quantifies trust**: Expected Trust Exposure = Σ P(outcome) × Damage(outcome)
2. **Decompose, don't centralize**: Many limited components are safer than one powerful agent
3. **Apply "Least X" principles**: Minimize intelligence, privilege, context, persistence, autonomy, connectivity
4. **Use the most verifiable implementation**: Code > narrow models > general LLMs > RL
5. **Propagate trust conservatively**: Multiplicative rule is safest default
6. **Budget risk like finance/nuclear**: Allocate, verify, and enforce trust limits
:::

## See Also

- [Introduction](/overview/introduction/) — The full problem statement and approach
- [Least X Principles](/principles/least-x-principles/) — Deep dive into each principle
- [Trust Calculus Overview](/trust-calculus/overview/) — The math behind ETE
- [Quick Start](/implementation/quick-start/) — Apply these concepts step-by-step
