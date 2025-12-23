---
title: "Pattern Interconnection"
description: "Understanding correlated failures in composed safety architectures"
sidebar:
  order: 10
---

# Pattern Interconnection Challenges

When composing multiple safety patterns, it's tempting to assume they operate **independently**—that stacking five 90%-effective layers yields 99.999% protection. In practice, patterns in a complex architecture are often interconnected in ways that create **correlated failure modes**, dramatically changing the risk profile.

Understanding and modeling these interconnections is one of the hardest problems in delegation architecture design.

## The Independence Illusion

Consider a "Defense in Depth Stack":

```
Independent Model (Idealized):
┌─────────────────────────┐
│  Layer 1: 90% effective │ → 10% pass through
├─────────────────────────┤
│  Layer 2: 90% effective │ → 1% pass through
├─────────────────────────┤
│  Layer 3: 90% effective │ → 0.1% pass through
└─────────────────────────┘
Combined: 99.9% effective
```

But if layers share failure modes:

```
Correlated Model (Reality):
┌─────────────────────────┐
│  Layer 1: 90% effective │─┐
├─────────────────────────┤ │ Shared blind spot:
│  Layer 2: 90% effective │─┤ 5% of threats evade
├─────────────────────────┤ │ ALL layers together
│  Layer 3: 90% effective │─┘
└─────────────────────────┘
Combined: 95% effective (not 99.9%)
```

The gap between perceived and actual protection can be enormous—often 10× to 100× worse than the independent model predicts.

## Why This Matters

**False confidence**: Teams believe they have robust multi-layer protection when they actually have multiple implementations of the same protection.

**Resource misallocation**: Adding more layers of the same type provides diminishing returns while consuming resources that could go toward genuinely diverse approaches.

**Adversarial vulnerability**: Sophisticated attackers specifically look for correlated weaknesses—one "master key" input that defeats all your defenses simultaneously.

**Audit failures**: Security reviews that examine each component independently will miss systemic vulnerabilities in how components interact.

## The Correlation Tax

We define the **Correlation Tax** as the ratio of actual risk to perceived risk:

```
Correlation Tax = Actual_Delegation_Risk / Perceived_Delegation_Risk
```

In the example above:
- Perceived risk: 0.1% (99.9% protection)
- Actual risk: 5% (95% protection)
- Correlation tax: 50×

**Your actual risk is 50× higher than your independent model suggests.**

This "tax" compounds with system complexity. Organizations with many composed patterns and high assumed protection levels may be paying correlation taxes of 100× or more.

## Section Contents

This section provides frameworks for understanding, measuring, and mitigating pattern interconnection:

### [Types of Correlation](/applying/patterns/interconnection/types/)
Not all correlation is equal. Learn to distinguish:
- Positive vs. negative failure correlation
- Conditional and asymmetric correlations
- Higher-order effects that pairwise analysis misses

### [Challenge Categories](/applying/patterns/interconnection/challenges/)
Nine categories of interconnection challenges:
1. Shared infrastructure dependencies
2. Correlated detection blind spots
3. Information flow contamination
4. Cascading failure dynamics
5. Adversarial exploitation
6. Emergent coupling over time
7. Measurement gaps
8. Organizational correlation
9. Fundamental/irreducible correlation

### [Modeling Approaches](/applying/patterns/interconnection/modeling/)
Quantitative tools for measuring interconnection:
- Delegation Risk formulas
- Correlation matrices and heatmaps
- Dependency graphs with risk edges
- Swiss cheese and risk surface visualizations

### [Worked Examples](/applying/patterns/interconnection/examples/)
Step-by-step analysis of real architectures:
- Code review verification pipeline
- Healthcare decision system
- Financial trading safeguards

### [Solutions & Mitigations](/applying/patterns/interconnection/solutions/)
Seven approaches to reducing correlation:
1. Architectural diversity requirements
2. Explicit correlation audits
3. Stress testing for coupling
4. Isolation boundaries
5. Correlation-aware risk budgeting
6. Circuit breakers for correlation
7. Regular independence verification

### [Decision Framework](/applying/patterns/interconnection/decision-framework/)
When is diversity worth the cost?
- Stakes × correlation decision matrix
- Costs of diversity
- When to accept vs. reject correlation

---

## Quick Diagnostic

Before reading further, assess your current architecture:

| Question | Yes = Higher Risk |
|----------|-------------------|
| Do multiple verification layers use the same LLM provider? | Shared infrastructure |
| Were all safety patterns designed by the same team? | Organizational correlation |
| Do later stages use context from earlier stages? | Information flow contamination |
| Has the architecture been "optimized" for performance? | Emergent coupling |
| Can your red team find inputs that evade multiple layers? | Correlated blind spots |
| Do your dashboards only show per-component metrics? | Measurement gaps |

If you answered "yes" to 3+ questions, pattern interconnection is likely a significant source of unrecognized risk in your system.

---

## Key Takeaways

1. **Independence is the exception, not the rule.** Assume correlation until proven otherwise.

2. **Diversity must be intentional.** Different providers ≠ different failure modes. Different teams ≠ different assumptions. Genuine diversity requires explicit effort.

3. **Correlation is measurable.** Use the tools in this section to quantify your correlation tax rather than guessing.

4. **Some correlation is irreducible.** At the limit, all AI verification of AI may share fundamental blind spots. Know where those limits are.

5. **The honest answer is sometimes "we can't verify this."** Better to know your limitations than to believe in illusory protection.

---

See also:
- [Channel Integrity Patterns](/applying/patterns/channel-integrity/) - Active boundary violations (complements this section's focus on passive correlations)
- [Composing Patterns](/applying/patterns/#composing-patterns) - How to combine patterns
- [Anti-Pattern Awareness](/applying/patterns/#anti-pattern-awareness) - Common mistakes
- [Defense in Depth](/applying/patterns/structural/#defense-in-depth) - Layered security architectures
