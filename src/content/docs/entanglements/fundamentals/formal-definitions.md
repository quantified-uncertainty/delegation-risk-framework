---
title: "Formal Definitions"
description: "Mathematical formalization of entanglement using information theory and game theory"
sidebar:
  order: 9
---

# Formal Definitions

This page provides rigorous mathematical definitions for entanglement concepts. These formalizations enable precise reasoning, quantitative measurement, and theoretical analysis.

---

## Notation

| Symbol | Meaning |
|--------|---------|
| A, B, C | Components (agents, verifiers, etc.) |
| X | Input to the system |
| F_A, F_B | Failure events for components A, B |
| O_A, O_B | Outputs of components A, B |
| I(·;·) | Mutual information |
| H(·) | Entropy |
| P(·) | Probability |
| do(·) | Intervention operator (Pearl) |

---

## Information-Theoretic Definitions

### Definition 1: Passive Entanglement (Mutual Information)

**Passive entanglement** between components A and B is the mutual information between their failure events:

$$
\text{Entanglement}_{\text{passive}}(A, B) = I(F_A; F_B)
$$

Where:
- $F_A \in \{0, 1\}$ indicates whether A fails on a given input
- $F_B \in \{0, 1\}$ indicates whether B fails on a given input
- $I(F_A; F_B) = H(F_A) + H(F_B) - H(F_A, F_B)$

**Interpretation**:
- $I(F_A; F_B) = 0$: Components are independent (no passive entanglement)
- $I(F_A; F_B) > 0$: Knowing whether A failed tells you something about whether B failed
- $I(F_A; F_B) = H(F_A) = H(F_B)$: Perfect correlation (maximum entanglement)

**Properties**:
- Symmetric: $I(F_A; F_B) = I(F_B; F_A)$
- Non-negative: $I(F_A; F_B) \geq 0$
- Bounded: $I(F_A; F_B) \leq \min(H(F_A), H(F_B))$

### Definition 2: Conditional Entanglement

**Conditional entanglement** given condition C:

$$
\text{Entanglement}_{\text{conditional}}(A, B | C) = I(F_A; F_B | C)
$$

This captures entanglement that only manifests under certain conditions.

**Example**: Components may be independent under normal load ($C = \text{normal}$) but entangled under stress ($C = \text{stress}$):

$$
I(F_A; F_B | \text{normal}) = 0 \quad \text{but} \quad I(F_A; F_B | \text{stress}) > 0
$$

### Definition 3: Active Entanglement (Transfer Entropy)

**Active entanglement** from A to B is the information transfer, measured by transfer entropy:

$$
\text{Entanglement}_{\text{active}}(A \to B) = I(O_A^{t-1}; F_B^t | F_B^{t-1})
$$

This measures how much A's past output predicts B's current failure, beyond what B's own history predicts.

**Properties**:
- Asymmetric: $\text{Entanglement}_{\text{active}}(A \to B) \neq \text{Entanglement}_{\text{active}}(B \to A)$
- Directional: Captures influence flow
- Temporal: Requires time-series data

### Definition 4: Interventional Influence

Using Pearl's do-calculus, we define **causal influence** as:

$$
\text{Influence}(A \to B) = \mathbb{E}_X \left[ D_{KL}\left( P(O_B | X) \,\|\, P(O_B | X, do(O_A = a)) \right) \right]
$$

Where $D_{KL}$ is the Kullback-Leibler divergence.

**Interpretation**: How much does intervening on A's output change the distribution of B's output, averaged over inputs?

**Simplified version** (for binary outcomes):

$$
\text{Influence}(A \to B) = P(F_B | do(F_A = 1)) - P(F_B | do(F_A = 0))
$$

### Definition 5: Context Contamination

When B receives context C derived from A's processing of input X:

$$
\text{Contamination}(A \to B) = I(X; O_B) - I(X; O_B | C)
$$

This measures how much information about the original input X is lost when B only sees A's processed context C.

**Data Processing Inequality** guarantees:

$$
I(X; O_B) \leq I(X; C) \leq I(X; X) = H(X)
$$

Information can only be lost, never gained, through processing.

---

## Game-Theoretic Definitions

### Definition 6: Collusion Game

Consider a **verification game** with:
- Principal P (system designer)
- Agent A (being verified)
- Verifier V (checking A's work)

**Payoff structure**:

| | V Approves | V Rejects |
|---|-----------|-----------|
| A Good | (1, 1, 1) | (0, 0, -1) |
| A Bad | (-10, 1, 1) | (0, 0, 0) |

Format: (P's payoff, A's payoff, V's payoff)

**Analysis**:
- If A and V cannot communicate: V should reject bad actions (V gets 0 vs 1, but P loses -10)
- If A and V can collude: They may agree A→bad, V→approve (both get 1, P loses -10)

**Collusion resistance** requires: The collusion payoff must be lower than the non-collusion payoff, accounting for detection probability and penalties.

### Definition 7: Collusion-Resistant Mechanism

A verification mechanism is **collusion-resistant** if:

$$
\forall (A, V): \quad U_A^{\text{honest}} + U_V^{\text{honest}} \geq U_A^{\text{collude}} + U_V^{\text{collude}} - P_{\text{detect}} \cdot \text{Penalty}
$$

Where:
- $U^{\text{honest}}$ = expected payoff from honest behavior
- $U^{\text{collude}}$ = expected payoff from collusion
- $P_{\text{detect}}$ = probability of detecting collusion
- Penalty = cost imposed when collusion is detected

**Implication**: Collusion resistance requires either high detection probability, high penalties, or mechanisms that make collusion unprofitable even if undetected.

### Definition 8: Regulatory Capture Equilibrium

**Capture** is a Nash equilibrium where:
- Agent A optimizes for outcomes that benefit A, not P
- Verifier V has adapted to approve A's preferred outcomes
- Neither A nor V has incentive to deviate unilaterally

Formally, let $\theta_A$ be A's type (interests) and $\theta_V$ be V's type:

**Initial state**: $\theta_V$ independent of $\theta_A$

**Captured state**: $\theta_V$ has drifted toward $\theta_A$ through:
- Information asymmetry (V relies on A for expertise)
- Relationship building (V trusts A)
- Incentive alignment (V's rewards depend on A's satisfaction)

**Capture metric**:

$$
\text{Capture}(V) = \frac{P(\text{V approves} | \text{A prefers approval})}{P(\text{V approves} | \text{A prefers rejection})}
$$

- Capture = 1: V is independent of A's preferences
- Capture > 1: V is biased toward A's preferences
- Capture → ∞: V always agrees with A

### Definition 9: Correlated Equilibrium and Logical Correlation

A **correlated equilibrium** exists when players coordinate using a shared signal.

For AI systems, the "signal" may be **shared training**. Two agents with similar training may correlate their decisions without explicit communication:

$$
P(a_A = a_B | \text{similar training}) > P(a_A = a_B | \text{independent training})
$$

**TDT-style logical correlation** is a form of implicit correlation where agents reason: "What would an agent with my decision procedure do?"

This creates entanglement that cannot be eliminated through communication isolation:

$$
I(O_A; O_B | \text{no communication, similar reasoning}) > 0
$$

---

## Risk Formalization

### Definition 10: Entanglement Tax

The **entanglement tax** is the ratio of actual to perceived risk:

$$
\text{Tax} = \frac{R_{\text{actual}}}{R_{\text{perceived}}}
$$

For a system with n components, each with failure probability $p_i$:

**Perceived risk** (assuming independence):

$$
R_{\text{perceived}} = \prod_{i=1}^{n} p_i
$$

**Actual risk** (accounting for correlations):

$$
R_{\text{actual}} = P\left(\bigcap_{i=1}^{n} F_i\right) \geq R_{\text{perceived}}
$$

The inequality follows from positive correlation.

### Definition 11: Delegation Risk with Entanglement

Extending the [Delegation Risk formula](/delegation-risk/delegation-risk-formula/):

**Without entanglement** (independent failures):

$$
DR = \text{Stakes} \times P(\text{Failure}) \times P(\text{Oversight Miss})
$$

**With entanglement** (correlated failures):

$$
DR = \text{Stakes} \times P(\text{Failure}) \times P(\text{All Oversight Layers Miss} | \text{Failure})
$$

The conditional probability accounts for correlation:

$$
P(\text{All Miss} | \text{Failure}) \geq \prod_{i} P(\text{Layer}_i \text{ misses} | \text{Failure})
$$

Equality holds only when layers are conditionally independent given failure.

### Definition 12: Effective Redundancy

For n nominally redundant components:

**Nominal redundancy**: n

**Effective redundancy**:

$$
n_{\text{eff}} = \frac{-\log P(\text{all fail})}{\log P(\text{one fails})}
$$

**Interpretation**:
- If components are independent: $n_{\text{eff}} = n$
- If components are perfectly correlated: $n_{\text{eff}} = 1$
- In practice: $1 \leq n_{\text{eff}} \leq n$

**Example**: Three 90%-effective layers:
- Independent: $P(\text{all fail}) = 0.1^3 = 0.001$, $n_{\text{eff}} = 3$
- With 50% correlation: $P(\text{all fail}) \approx 0.05$, $n_{\text{eff}} \approx 1.3$

---

## Channel Capacity and Side-Channels

### Definition 13: Side-Channel Capacity

The **capacity** of a side-channel between A and B:

$$
C_{A \to B} = \max_{P(X_A)} I(X_A; Y_B)
$$

Where:
- $X_A$ is what A encodes in the channel
- $Y_B$ is what B receives

**Applications**:
- Timing channel: A modulates response latency, B observes timing
- Steganographic channel: A embeds information in outputs, B decodes
- Resource channel: A consumes resources, B observes availability

### Definition 14: Covert Channel Capacity

A **covert channel** is a side-channel designed to evade detection.

The capacity is bounded by:

$$
C_{\text{covert}} \leq C_{\text{overt}} \times (1 - P_{\text{detect}})^{\alpha}
$$

Where $\alpha$ depends on the detection sophistication.

**Implication**: Perfect detection ($P_{\text{detect}} = 1$) eliminates covert channel capacity, but this is generally unachievable.

---

## Temporal Dynamics

### Definition 15: Entanglement Drift Rate

The rate at which passive entanglement changes over time:

$$
\frac{d}{dt} I(F_A; F_B) = \text{Entanglement Drift Rate}
$$

**Positive drift**: Components are becoming more entangled (concerning)
**Negative drift**: Components are becoming less entangled (intervention working)
**Zero drift**: Stable state (may or may not be acceptable)

### Definition 16: Capture Rate

The rate at which a verifier is captured:

$$
\text{Capture Rate} = \frac{d}{dt} \text{Capture}(V)
$$

Where Capture(V) is as defined in Definition 8.

**Threshold-based alerts**:
- Capture Rate > 0.1/month: Intervention recommended
- Capture Rate > 0.2/month: Urgent action required

---

## Bounds and Impossibility Results

### Theorem 1: Irreducible Entanglement

For any verification system where A and B share a common reasoning paradigm (e.g., both are neural networks trained with similar methods):

$$
I(F_A; F_B) > 0
$$

**Proof sketch**: Adversarial examples transfer between models with similar architectures and training. This creates a lower bound on failure correlation that cannot be eliminated through isolation.

### Theorem 2: Verification Ceiling

If verifier V has capability level $c_V$ and agent A has capability level $c_A$:

For tasks requiring capability $c > c_V$:

$$
P(\text{V catches A's error}) \leq \frac{c_V}{c}
$$

**Implication**: Verifiers cannot reliably catch errors in domains where they lack capability. This creates fundamental limits on AI oversight of AI.

### Theorem 3: Collusion Detection Limits

For sufficiently sophisticated agents:

$$
P(\text{detect collusion}) \leq 1 - P(\text{TDT-style coordination})
$$

**Implication**: If agents coordinate through logical correlation rather than explicit communication, detection through communication monitoring is impossible.

---

## Summary of Key Formulas

| Concept | Formula |
|---------|---------|
| Passive entanglement | $I(F_A; F_B)$ |
| Active entanglement | $I(O_A^{t-1}; F_B^t \| F_B^{t-1})$ |
| Causal influence | $P(F_B \| do(F_A=1)) - P(F_B \| do(F_A=0))$ |
| Context contamination | $I(X; O_B) - I(X; O_B \| C)$ |
| Entanglement tax | $R_{\text{actual}} / R_{\text{perceived}}$ |
| Effective redundancy | $-\log P(\text{all fail}) / \log P(\text{one fails})$ |
| Capture metric | $P(\text{approve} \| \text{A wants}) / P(\text{approve} \| \text{A doesn't want})$ |
| Side-channel capacity | $\max_{P(X)} I(X; Y)$ |

---

## Practical Application

These formal definitions enable:

1. **Quantitative measurement**: Compute entanglement metrics from empirical data
2. **Theoretical analysis**: Prove bounds on achievable independence
3. **Design optimization**: Minimize entanglement subject to constraints
4. **Alert thresholds**: Define precise conditions for intervention

For practical measurement approaches, see [Quantitative Metrics](/entanglements/detection/metrics/).

---

See also:
- [Quantitative Metrics](/entanglements/detection/metrics/) - Practical measurement of these quantities
- [Research Connections](/entanglements/research/research-connections/) - Academic foundations
- [Types of Entanglement](/entanglements/fundamentals/types/) - Conceptual overview
