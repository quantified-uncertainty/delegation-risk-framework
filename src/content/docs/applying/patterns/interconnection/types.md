---
title: "Types of Correlation"
description: "Understanding different types of failure correlation in safety architectures"
sidebar:
  order: 1
---

# Types of Correlation

Not all correlation is equal. Understanding the type of correlation helps determine the appropriate response and prioritize interventions.

## Correlation Type Matrix

| Type | Description | Example | Implication |
|------|-------------|---------|-------------|
| **Positive failure correlation** | If A fails, B more likely to fail | Same LLM provider for both | Reduces effective redundancy |
| **Negative failure correlation** | If A fails, B more likely to succeed | Adversarial collaboration (A and B have opposed biases) | *Increases* effective redundancy—this is good |
| **Conditional correlation** | Only correlated under certain conditions | Independent normally, but correlated under high load | Must stress-test to detect |
| **Asymmetric correlation** | A's failure predicts B's, but not vice versa | A provides context to B; corrupted A → corrupted B | Direction matters for intervention |
| **Higher-order correlation** | Only manifests when 3+ components interact | A+B fine, B+C fine, A+C fine, but A+B+C fails | Pairwise analysis misses this |

---

## Positive Failure Correlation

The most common and dangerous type. When component A fails, component B is more likely to fail on the same input.

```
Positive Correlation Example:

Input X arrives
    │
    ▼
┌─────────────┐   ┌─────────────┐
│  Checker A  │   │  Checker B  │
│  (GPT-4)    │   │  (Claude)   │
└─────┬───────┘   └─────┬───────┘
      │                 │
      │ MISS            │ MISS
      │                 │
      └────────┬────────┘
               │
        Both miss because both are
        LLMs with similar training
```

**Sources of positive correlation**:
- Shared training data or methodology
- Same underlying infrastructure
- Similar architectural decisions
- Common conceptual blind spots
- Shared failure modes under stress

**Mitigation**: Genuine methodological diversity—not just different providers, but fundamentally different verification approaches (rule-based + statistical + semantic + formal).

---

## Negative Failure Correlation

The rare and valuable case. When A fails, B is more likely to succeed. This is what you *want* in a robust system.

```
Negative Correlation Example:

Input X arrives
    │
    ▼
┌─────────────┐   ┌─────────────┐
│  Checker A  │   │  Checker B  │
│  (Optimist) │   │ (Pessimist) │
└─────┬───────┘   └─────┬───────┘
      │                 │
      │ MISS            │ CATCH!
      │ (too lenient)   │ (catches edge cases)
      │                 │
      └────────┬────────┘
               │
        A's blind spot is
        B's strength
```

**How to create negative correlation**:
- **Adversarial collaboration**: Explicitly opposed incentives
- **Complementary specialization**: One focuses on false positives, another on false negatives
- **Different priors**: One conservative, one permissive
- **Different granularity**: One checks high-level patterns, another checks details

**Example**: A security team with one member who tends toward false positives and another who tends toward false negatives. Their disagreements catch what each would miss.

---

## Conditional Correlation

Components appear independent under normal conditions but become correlated under stress.

```
Normal Operation:               Under Stress:

A: ●●●○○●●●●○  (independent)    A: ○○○○○●○○○○  (correlated)
B: ●○●●●○●●○●  (independent)    B: ○○○○○●○○○○  (correlated)
                                       ↑
                                 Shared failure mode
                                 activated by load
```

**Sources**:
- Shared resource pools that only bottleneck under load
- Timeout cascades that only trigger during delays
- Fallback paths that activate simultaneously
- Cache coherence issues under high write volume

**Detection**: Stress testing is essential. Normal-condition testing won't reveal conditional correlations.

**Mitigation**:
- Separate resource pools
- Staggered timeouts
- Independent fallback mechanisms
- Load shedding that affects components differently

---

## Asymmetric Correlation

A's failure predicts B's failure, but not vice versa. This typically occurs in information flow chains.

```
Asymmetric Correlation:

A fails → B likely to fail (A provides context to B)
B fails → A unaffected   (B doesn't feed back to A)

┌─────────────┐     ┌─────────────┐
│  Component  │────▶│  Component  │
│      A      │     │      B      │
└─────────────┘     └─────────────┘
     │                    │
     │ If A produces      │ B inherits
     │ poisoned context   │ the poison
     │                    │
     ▼                    ▼
 Independent          Dependent on A
```

**Examples**:
- Summarization → analysis pipelines (bad summary → bad analysis)
- Preprocessing → verification (malformed preprocessing → verification on wrong data)
- Context construction → LLM evaluation (manipulated context → manipulated evaluation)

**Implications**:
- Correlation is directional—fixing B won't help if A is the problem
- The earlier component in the chain is more critical
- Later components should not blindly trust earlier outputs

**Mitigation**:
- Independent context construction for verification
- Redundant preprocessing paths
- Validators that don't inherit framing from validated components

---

## Higher-Order Correlation

Failures that only manifest when three or more components interact. Pairwise analysis will miss these entirely.

```
Higher-Order Correlation:

Pairwise tests:       Three-way test:
A + B: PASS           A + B + C: FAIL!
B + C: PASS
A + C: PASS

        A
       / \
      /   \    ← All edges fine
     B─────C

But the triangle creates emergent failure
```

**Examples**:
- Resource contention: A+B fine, B+C fine, A+C fine, but A+B+C exhausts shared pool
- Timing: A finishes before B starts (fine), B finishes before C starts (fine), but A+B+C creates race condition
- Logic: A→approve, B→approve, C→approve independently, but A+B+C together trigger conflicting constraints

**Why pairwise analysis fails**:
- Combinatorial explosion means most teams only test pairs
- Emergent behavior requires specific conditions
- The components may genuinely be independent in pairs

**Detection**:
- Chaos engineering that affects multiple components simultaneously
- Combinatorial testing at critical junctures
- Production monitoring for multi-component failures

**Mitigation**:
- Holistic system testing, not just component testing
- Conservative resource allocation (don't optimize for pairwise-safe maximums)
- Explicit documentation of assumed independence

---

## Success Correlation vs. Failure Correlation

**Critical distinction**: We care about **failure correlation**, not general correlation.

```
Good correlation:              Bad correlation:
All detect threat X            All miss threat Y

    A ──detect──┐                  A ──miss──┐
    B ──detect──┼── ALERT          B ──miss──┼── NO ALERT
    C ──detect──┘                  C ──miss──┘

Redundancy confirms           Redundancy provides
the detection                 false confidence
```

If all your detectors agree on true positives, that's *good*—they're correctly identifying threats. High correlation in successful detection is fine.

The problem is when they agree on **false negatives** (all missing the same threats) or when they **cascade into failure together**.

**Implications for measurement**:
- Don't measure overall correlation; measure failure correlation specifically
- A system with high detection agreement AND low miss agreement is ideal
- The correlation matrix should focus on "given that at least one component missed, did others miss too?"

---

## Measuring Correlation Type

### Quick Assessment

| Observation | Likely Type |
|-------------|-------------|
| Components fail on similar input patterns | Positive (conceptual) |
| Components fail during same time periods | Conditional (resource-based) |
| Downstream components fail when upstream fails | Asymmetric (information flow) |
| Pairs work but triples fail | Higher-order |
| Opposite-tendency components catch each other's misses | Negative (designed correctly) |

### Correlation Coefficient Interpretation

For a pair of components, calculate:

```
ρ (failure correlation) = P(both fail | one fails) / P(either fails)

ρ < 0.3:  Low correlation (acceptable)
ρ 0.3-0.5: Moderate correlation (investigate)
ρ > 0.5:  High correlation (redesign required)
ρ < 0:    Negative correlation (good—maintain this)
```

### Testing for Correlation Type

1. **For positive correlation**: Find inputs that cause Component A to fail. Do they also cause Component B to fail?

2. **For conditional correlation**: Repeat tests under stress. Does correlation increase?

3. **For asymmetric correlation**: Test both directions. If A→B correlation differs from B→A, it's asymmetric.

4. **For higher-order correlation**: Test triples and quadruples, not just pairs.

---

## Implications for Architecture

| Correlation Type | Architectural Response |
|------------------|----------------------|
| Positive | Add fundamentally different verification methods |
| Negative | Preserve and strengthen this diversity |
| Conditional | Separate resource pools; stress test regularly |
| Asymmetric | Isolate information flows; verify contexts independently |
| Higher-order | Holistic testing; conservative resource allocation |

---

See also:
- [Challenge Categories](/applying/patterns/interconnection/challenges/) - Sources of correlation
- [Modeling Approaches](/applying/patterns/interconnection/modeling/) - Quantifying correlation
- [Solutions](/applying/patterns/interconnection/solutions/) - Reducing correlation
