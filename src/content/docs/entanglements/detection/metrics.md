---
title: "Quantitative Metrics"
description: "Practical measurement of entanglement using information-theoretic and empirical methods"
sidebar:
  order: 11
---

# Quantitative Metrics

This page provides practical methods for measuring entanglement. While the [formal definitions](/entanglements/fundamentals/formal-definitions/) give theoretical foundations, these metrics are designed for real-world implementation.

---

## Overview: What to Measure

| Metric Category | What It Captures | Primary Use |
|----------------|------------------|-------------|
| **Correlation metrics** | Passive entanglement (shared failures) | Detect correlated blind spots |
| **Influence metrics** | Active entanglement (directional impact) | Detect context contamination |
| **Capture metrics** | Adversarial entanglement (alignment drift) | Detect verifier capture |
| **Diversity metrics** | Structural independence | Assess design quality |
| **Temporal metrics** | Drift over time | Early warning system |

---

## Correlation Metrics (Passive Entanglement)

### Metric 1: Failure Correlation Coefficient

The simplest measure of passive entanglement.

**Definition**:
$$
\rho_{AB} = \frac{P(F_A \cap F_B) - P(F_A) \cdot P(F_B)}{\sqrt{P(F_A)(1-P(F_A)) \cdot P(F_B)(1-P(F_B))}}
$$

**Implementation**:

```python
import numpy as np
from scipy.stats import pearsonr

def failure_correlation(failures_a: list[bool], failures_b: list[bool]) -> float:
    """
    Calculate correlation coefficient between component failures.

    Args:
        failures_a: Boolean list where True = A failed on this input
        failures_b: Boolean list where True = B failed on this input

    Returns:
        Correlation coefficient in [-1, 1]
    """
    if len(failures_a) != len(failures_b):
        raise ValueError("Lists must be same length")

    # Convert to numeric
    a = np.array(failures_a, dtype=float)
    b = np.array(failures_b, dtype=float)

    # Handle edge cases
    if np.std(a) == 0 or np.std(b) == 0:
        return 0.0  # Can't compute correlation with no variance

    corr, _ = pearsonr(a, b)
    return corr
```

**Interpretation**:
| ρ Value | Interpretation | Action |
|---------|----------------|--------|
| ρ < 0 | Negative correlation (good!) | Maintain this diversity |
| 0 ≤ ρ < 0.3 | Low correlation | Acceptable |
| 0.3 ≤ ρ < 0.5 | Moderate correlation | Investigate |
| ρ ≥ 0.5 | High correlation | Redesign required |

### Metric 2: Mutual Information of Failures

More general than correlation—captures non-linear relationships.

**Definition**:
$$
I(F_A; F_B) = \sum_{a,b \in \{0,1\}} P(F_A=a, F_B=b) \log \frac{P(F_A=a, F_B=b)}{P(F_A=a) \cdot P(F_B=b)}
$$

**Implementation**:

```python
from sklearn.metrics import mutual_info_score
import numpy as np

def failure_mutual_information(failures_a: list[bool], failures_b: list[bool]) -> float:
    """
    Calculate mutual information between component failures.

    Returns:
        Mutual information in bits (log base 2)
    """
    a = np.array(failures_a, dtype=int)
    b = np.array(failures_b, dtype=int)

    # sklearn uses natural log; convert to bits
    mi_nats = mutual_info_score(a, b)
    mi_bits = mi_nats / np.log(2)

    return mi_bits
```

**Interpretation**:
- I = 0: Components are independent
- I > 0: Knowing one tells you about the other
- Maximum I = min(H(F_A), H(F_B)) ≈ 1 bit for binary failures

**Normalized version** (0 to 1 scale):
$$
\text{NMI}(F_A; F_B) = \frac{2 \cdot I(F_A; F_B)}{H(F_A) + H(F_B)}
$$

### Metric 3: Conditional Failure Rate

Measures how much A's failure predicts B's failure.

**Definition**:
$$
\text{CFR}(A \to B) = \frac{P(F_B | F_A)}{P(F_B)}
$$

**Implementation**:

```python
def conditional_failure_rate(failures_a: list[bool], failures_b: list[bool]) -> float:
    """
    How much does A failing increase B's failure probability?

    Returns:
        Ratio >= 1 means positive correlation
        Ratio < 1 means negative correlation
        Ratio = 1 means independence
    """
    a = np.array(failures_a)
    b = np.array(failures_b)

    p_b = np.mean(b)
    if p_b == 0:
        return 1.0  # B never fails

    # P(B fails | A fails)
    a_failed = a == True
    if np.sum(a_failed) == 0:
        return 1.0  # A never fails

    p_b_given_a = np.mean(b[a_failed])

    return p_b_given_a / p_b
```

**Interpretation**:
| CFR Value | Interpretation |
|-----------|----------------|
| CFR = 1 | Independent |
| CFR > 1 | Positive correlation (A failing makes B failing more likely) |
| CFR < 1 | Negative correlation (A failing makes B failing less likely) |
| CFR = ∞ | Perfect correlation (B always fails when A fails) |

### Metric 4: Joint Failure Rate vs. Independent Model

Direct measure of the entanglement tax for a specific failure mode.

**Definition**:
$$
\text{Entanglement Tax} = \frac{P(F_A \cap F_B)}{P(F_A) \cdot P(F_B)}
$$

**Implementation**:

```python
def entanglement_tax(failures_a: list[bool], failures_b: list[bool]) -> float:
    """
    How much worse is joint failure than independent model predicts?

    Returns:
        Tax = 1: Independent
        Tax > 1: Positive entanglement (bad)
        Tax < 1: Negative entanglement (good)
    """
    a = np.array(failures_a)
    b = np.array(failures_b)

    p_a = np.mean(a)
    p_b = np.mean(b)
    p_ab = np.mean(a & b)

    if p_a == 0 or p_b == 0:
        return 1.0  # Can't calculate

    independent_prediction = p_a * p_b
    if independent_prediction == 0:
        return 1.0

    return p_ab / independent_prediction
```

---

## Influence Metrics (Active Entanglement)

### Metric 5: Frame Sensitivity Score

Measures how much A's framing affects B's output.

**Protocol**:
1. Take N inputs with objective correct answers
2. Generate two framings for each via A (neutral and suggestive)
3. Measure B's accuracy under each framing
4. Frame sensitivity = difference in accuracy

**Implementation**:

```python
from dataclasses import dataclass
from typing import Callable

@dataclass
class FrameSensitivityResult:
    neutral_accuracy: float
    suggestive_accuracy: float
    sensitivity: float  # Difference in accuracy
    p_value: float  # Statistical significance

def measure_frame_sensitivity(
    inputs: list[str],
    correct_outputs: list[str],
    neutral_framer: Callable[[str], str],  # A with neutral prompt
    suggestive_framer: Callable[[str], str],  # A with suggestive prompt
    responder: Callable[[str], str],  # B
    is_correct: Callable[[str, str], bool]
) -> FrameSensitivityResult:
    """
    Measure how much framing affects responder accuracy.
    """
    neutral_results = []
    suggestive_results = []

    for inp, correct in zip(inputs, correct_outputs):
        # Neutral framing
        neutral_context = neutral_framer(inp)
        neutral_output = responder(neutral_context)
        neutral_results.append(is_correct(neutral_output, correct))

        # Suggestive framing
        suggestive_context = suggestive_framer(inp)
        suggestive_output = responder(suggestive_context)
        suggestive_results.append(is_correct(suggestive_output, correct))

    neutral_acc = np.mean(neutral_results)
    suggestive_acc = np.mean(suggestive_results)
    sensitivity = suggestive_acc - neutral_acc

    # Statistical test
    from scipy.stats import chi2_contingency
    contingency = [
        [sum(neutral_results), len(neutral_results) - sum(neutral_results)],
        [sum(suggestive_results), len(suggestive_results) - sum(suggestive_results)]
    ]
    _, p_value, _, _ = chi2_contingency(contingency)

    return FrameSensitivityResult(
        neutral_accuracy=neutral_acc,
        suggestive_accuracy=suggestive_acc,
        sensitivity=sensitivity,
        p_value=p_value
    )
```

**Interpretation**:
| Sensitivity | Interpretation |
|-------------|----------------|
| \|S\| < 0.05 | Low frame sensitivity (good) |
| 0.05 ≤ \|S\| < 0.15 | Moderate (investigate) |
| \|S\| ≥ 0.15 | High frame sensitivity (redesign needed) |

### Metric 6: Transfer Entropy

Measures directional information flow over time.

**Definition**:
$$
TE(A \to B) = I(O_A^{t-1}; O_B^t | O_B^{t-1})
$$

"How much does A's past output tell us about B's current output, beyond what B's own past tells us?"

**Implementation**:

```python
from scipy.stats import entropy

def transfer_entropy(
    outputs_a: list[int],  # A's outputs over time (discretized)
    outputs_b: list[int],  # B's outputs over time (discretized)
    lag: int = 1
) -> float:
    """
    Measure information transfer from A to B.

    Args:
        outputs_a: A's discretized outputs
        outputs_b: B's discretized outputs
        lag: Time lag (default 1)

    Returns:
        Transfer entropy in bits
    """
    n = len(outputs_a)
    if n < lag + 2:
        return 0.0

    # Build joint distributions
    # P(b_t | b_{t-1}, a_{t-1}) vs P(b_t | b_{t-1})

    from collections import Counter

    # Count (b_prev, a_prev, b_curr) triples
    joint_counts = Counter()
    marginal_counts = Counter()

    for t in range(lag, n):
        b_curr = outputs_b[t]
        b_prev = outputs_b[t - lag]
        a_prev = outputs_a[t - lag]

        joint_counts[(b_prev, a_prev, b_curr)] += 1
        marginal_counts[(b_prev, b_curr)] += 1

    # Calculate transfer entropy
    total = sum(joint_counts.values())
    te = 0.0

    for (b_prev, a_prev, b_curr), count in joint_counts.items():
        p_joint = count / total
        p_marginal = marginal_counts[(b_prev, b_curr)] / total

        # P(b_curr | b_prev, a_prev)
        p_cond_joint = count / sum(
            c for (bp, ap, bc), c in joint_counts.items()
            if bp == b_prev and ap == a_prev
        )

        # P(b_curr | b_prev)
        p_cond_marginal = marginal_counts[(b_prev, b_curr)] / sum(
            c for (bp, bc), c in marginal_counts.items()
            if bp == b_prev
        )

        if p_cond_marginal > 0:
            te += p_joint * np.log2(p_cond_joint / p_cond_marginal)

    return te
```

**Interpretation**:
| TE Value | Interpretation |
|----------|----------------|
| TE ≈ 0 | No information transfer |
| TE > 0.05 | Detectable transfer |
| TE > 0.2 | Significant influence |

---

## Capture Metrics (Adversarial Entanglement)

### Metric 7: Approval Rate Ratio

Simple measure of potential capture.

**Definition**:
$$
\text{Approval Ratio} = \frac{\text{Approval rate for this agent}}{\text{Baseline approval rate}}
$$

**Implementation**:

```python
def approval_rate_ratio(
    agent_approvals: list[bool],
    baseline_approvals: list[bool]
) -> float:
    """
    Compare this agent's approval rate to baseline.

    Returns:
        Ratio > 1: This agent gets approved more often
        Ratio < 1: This agent gets approved less often
        Ratio = 1: Same as baseline
    """
    agent_rate = np.mean(agent_approvals)
    baseline_rate = np.mean(baseline_approvals)

    if baseline_rate == 0:
        return float('inf') if agent_rate > 0 else 1.0

    return agent_rate / baseline_rate
```

**Interpretation**:
| Ratio | Interpretation |
|-------|----------------|
| 0.9-1.1 | Normal variation |
| 1.1-1.3 | Slightly elevated (monitor) |
| > 1.3 | Significantly elevated (investigate) |

### Metric 8: Preference Alignment Score

Measures whether verifier decisions align with agent preferences.

**Definition**:
$$
\text{PAS} = P(\text{approve} | \text{agent prefers approve}) - P(\text{approve} | \text{agent prefers reject})
$$

**Implementation**:

```python
def preference_alignment_score(
    agent_preferences: list[bool],  # True = agent prefers approval
    verifier_decisions: list[bool]  # True = approved
) -> float:
    """
    How aligned is the verifier with agent preferences?

    Returns:
        PAS = 0: No alignment (independent)
        PAS > 0: Aligned with agent preferences (potential capture)
        PAS < 0: Adversarial to agent preferences (expected for good verification)
    """
    prefs = np.array(agent_preferences)
    decisions = np.array(verifier_decisions)

    prefer_approve = prefs == True
    prefer_reject = prefs == False

    if sum(prefer_approve) == 0 or sum(prefer_reject) == 0:
        return 0.0

    approve_when_wanted = np.mean(decisions[prefer_approve])
    approve_when_not_wanted = np.mean(decisions[prefer_reject])

    return approve_when_wanted - approve_when_not_wanted
```

**Interpretation**:
| PAS Value | Interpretation |
|-----------|----------------|
| PAS < -0.1 | Healthy adversarial relationship |
| -0.1 ≤ PAS ≤ 0.1 | Independent |
| 0.1 < PAS ≤ 0.3 | Some alignment (monitor) |
| PAS > 0.3 | Significant alignment (capture risk) |

### Metric 9: Verifier Consistency Across Agents

If a verifier treats different agents differently, it may be captured by some.

**Implementation**:

```python
from scipy.stats import f_oneway

def verifier_consistency(
    decisions_by_agent: dict[str, list[bool]]  # agent_id -> list of decisions
) -> float:
    """
    Are decisions consistent across different agents?

    Returns:
        Consistency score from 0 (inconsistent) to 1 (consistent)
    """
    approval_rates = [np.mean(decisions) for decisions in decisions_by_agent.values()]

    # Use coefficient of variation as inconsistency measure
    if np.mean(approval_rates) == 0:
        return 1.0

    cv = np.std(approval_rates) / np.mean(approval_rates)

    # Convert to consistency score (lower CV = higher consistency)
    consistency = 1 / (1 + cv)

    return consistency
```

**Interpretation**:
| Consistency | Interpretation |
|-------------|----------------|
| > 0.9 | Highly consistent (good) |
| 0.7-0.9 | Moderately consistent |
| < 0.7 | Inconsistent (some agents may be favored) |

---

## Diversity Metrics (Structural Independence)

### Metric 10: Representation Similarity

For neural network components, measure how similar their internal representations are.

**Definition**: Use Centered Kernel Alignment (CKA) to compare hidden representations.

**Implementation** (simplified):

```python
def linear_cka(features_a: np.ndarray, features_b: np.ndarray) -> float:
    """
    Calculate linear CKA similarity between two feature matrices.

    Args:
        features_a: (n_samples, n_features_a)
        features_b: (n_samples, n_features_b)

    Returns:
        CKA similarity in [0, 1]
    """
    # Center the features
    a = features_a - features_a.mean(axis=0)
    b = features_b - features_b.mean(axis=0)

    # Compute similarity matrices
    k_a = a @ a.T
    k_b = b @ b.T

    # HSIC (Hilbert-Schmidt Independence Criterion)
    hsic_ab = np.sum(k_a * k_b)
    hsic_aa = np.sum(k_a * k_a)
    hsic_bb = np.sum(k_b * k_b)

    # CKA
    cka = hsic_ab / np.sqrt(hsic_aa * hsic_bb)

    return cka
```

**Interpretation**:
| CKA Value | Interpretation |
|-----------|----------------|
| CKA > 0.8 | Very similar representations (high entanglement risk) |
| 0.5-0.8 | Moderately similar |
| CKA < 0.5 | Different representations (lower entanglement risk) |

### Metric 11: Methodological Diversity Index

Qualitative assessment of verification diversity.

**Scoring rubric**:

| Dimension | Score 0 | Score 1 | Score 2 |
|-----------|---------|---------|---------|
| **Provider diversity** | All same provider | 2 providers | 3+ providers |
| **Architecture diversity** | All same architecture | 2 types | 3+ types (e.g., transformer + rule-based + symbolic) |
| **Training diversity** | Same training data | Overlapping data | Independent data |
| **Methodology diversity** | All ML-based | ML + rules | ML + rules + formal |
| **Temporal diversity** | All synchronous | Pre + post | Pre + concurrent + post |

**Total score**: Sum of dimension scores (0-10)

**Interpretation**:
| Score | Interpretation |
|-------|----------------|
| 0-3 | Low diversity (high entanglement risk) |
| 4-6 | Moderate diversity |
| 7-10 | High diversity (lower entanglement risk) |

---

## Temporal Metrics

### Metric 12: Entanglement Drift Rate

Track how entanglement changes over time.

**Implementation**:

```python
from scipy.stats import linregress

def entanglement_drift_rate(
    weekly_correlations: list[float],
) -> tuple[float, float]:
    """
    Calculate rate of change in correlation over time.

    Returns:
        (slope, p_value)
        slope > 0: Entanglement increasing (concerning)
        slope < 0: Entanglement decreasing (improving)
    """
    weeks = np.arange(len(weekly_correlations))
    correlations = np.array(weekly_correlations)

    result = linregress(weeks, correlations)

    return result.slope, result.pvalue
```

**Alert thresholds**:
| Drift Rate | Action |
|------------|--------|
| < 0.01/week | Normal |
| 0.01-0.02/week | Monitor |
| > 0.02/week | Investigate |

### Metric 13: Capture Velocity

Rate at which approval rates are increasing.

```python
def capture_velocity(
    weekly_approval_rates: list[float]
) -> float:
    """
    Rate of change in approval rate.
    """
    weeks = np.arange(len(weekly_approval_rates))
    rates = np.array(weekly_approval_rates)

    result = linregress(weeks, rates)

    return result.slope
```

**Interpretation**:
| Velocity | Interpretation |
|----------|----------------|
| < 0.5%/month | Stable |
| 0.5-2%/month | Drifting (investigate) |
| > 2%/month | Rapid capture (urgent) |

---

## Dashboard Implementation

### Composite Entanglement Score

Combine metrics into a single score for dashboarding:

```python
@dataclass
class EntanglementReport:
    passive_score: float  # 0-100, higher = more entanglement
    active_score: float
    capture_score: float
    overall_score: float
    risk_level: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"

def calculate_entanglement_score(
    failure_correlation: float,
    mutual_information: float,
    frame_sensitivity: float,
    approval_ratio: float,
    preference_alignment: float,
    diversity_index: int
) -> EntanglementReport:
    """
    Calculate composite entanglement scores.
    """
    # Passive entanglement (0-100)
    passive_score = min(100, max(0,
        50 * failure_correlation +
        50 * mutual_information
    ))

    # Active entanglement (0-100)
    active_score = min(100, max(0,
        100 * frame_sensitivity
    ))

    # Capture risk (0-100)
    capture_score = min(100, max(0,
        50 * max(0, approval_ratio - 1) +
        50 * max(0, preference_alignment)
    ))

    # Diversity adjustment (reduces scores)
    diversity_factor = 1 - (diversity_index / 10)

    # Overall score
    overall_score = (
        0.4 * passive_score +
        0.3 * active_score +
        0.3 * capture_score
    ) * (0.5 + 0.5 * diversity_factor)

    # Risk level
    if overall_score < 25:
        risk_level = "LOW"
    elif overall_score < 50:
        risk_level = "MEDIUM"
    elif overall_score < 75:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    return EntanglementReport(
        passive_score=passive_score,
        active_score=active_score,
        capture_score=capture_score,
        overall_score=overall_score,
        risk_level=risk_level
    )
```

### Example Dashboard Output

```
┌─────────────────────────────────────────────────────────────┐
│                  ENTANGLEMENT DASHBOARD                      │
│                  System: Production-v2.3                     │
│                  Period: 2024-01-01 to 2024-01-31           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  OVERALL RISK LEVEL: ████████░░ MEDIUM (Score: 42/100)      │
│                                                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│  │ PASSIVE: 35     │ │ ACTIVE: 28      │ │ CAPTURE: 18     ││
│  │ ████████░░░░    │ │ ██████░░░░░░    │ │ ████░░░░░░░░    ││
│  │                 │ │                 │ │                 ││
│  │ Correlation:    │ │ Frame sens:     │ │ Approval ratio: ││
│  │   0.38 ⚠️       │ │   0.12 ⚠️       │ │   1.08 ✓        ││
│  │ Mut. Info:      │ │ Transfer ent:   │ │ Pref. align:    ││
│  │   0.21 ⚠️       │ │   0.08 ✓        │ │   0.05 ✓        ││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘│
│                                                             │
│  TREND: Correlation increasing 0.015/week ⚠️                │
│  DIVERSITY: 6/10 (Moderate)                                 │
│                                                             │
│  RECOMMENDATIONS:                                            │
│  • Investigate shared blind spots (high correlation)        │
│  • Review context flow (frame sensitivity elevated)         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Collection Requirements

To compute these metrics, you need:

| Data Type | Required For | Collection Method |
|-----------|--------------|-------------------|
| Component failures | Correlation, MI, Tax | Log all verification decisions with ground truth |
| Ground truth labels | Frame sensitivity | Periodic human labeling of samples |
| Agent preferences | Preference alignment | Infer from agent behavior or explicit queries |
| Component outputs | Transfer entropy | Time-series logging |
| Internal representations | CKA | Probe hidden layers |
| Weekly aggregates | Drift detection | Aggregate logs weekly |

---

## Summary: Metric Selection Guide

| If You Suspect... | Measure | Alert If |
|-------------------|---------|----------|
| Shared blind spots | Failure correlation, MI | ρ > 0.3 or MI > 0.2 |
| Context contamination | Frame sensitivity | \|S\| > 0.1 |
| Information flow | Transfer entropy | TE > 0.1 |
| Verifier capture | Preference alignment | PAS > 0.15 |
| Favoritism | Verifier consistency | < 0.8 |
| Drift over time | Entanglement drift rate | > 0.01/week |
| Low structural diversity | Diversity index | Score < 5 |

---

See also:
- [Formal Definitions](/entanglements/fundamentals/formal-definitions/) - Mathematical foundations
- [Detecting Influence](/entanglements/detection/detecting-influence/) - Detection protocols
- [Solutions & Mitigations](/entanglements/mitigation/solutions/) - What to do when metrics are concerning
