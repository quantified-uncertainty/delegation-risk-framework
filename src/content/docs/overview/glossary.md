---
title: "Glossary"
sidebar:
  order: 10
---

Key terms used throughout this framework, organized by domain.

## Core Framework Terms

**Expected Trust Exposure (ETE)** — ETE = Σ P(outcome) × Damage(outcome). The fundamental metric for quantifying trust. Sum of probability-weighted damages across all possible failure modes. Measured in dollars per time period. *Example*: 2% chance of $5,000 damage = $100 ETE.

**Trust Propagation** — How trust flows through a network of components. When A delegates to B and B delegates to C, A's effective trust in C depends on the propagation rule (multiplicative, minimum, etc.).

**Trust Budget** — Maximum acceptable ETE for a system or component. Like a financial budget, but for risk exposure.

**Principal** — An entity that delegates tasks and grants trust. In most systems, humans are the ultimate principals.

**Executor** — A component that performs actions using granted trust. Executors consume trust to act.

**Coordinator** — A component that orchestrates other components—routing tasks, making strategic decisions, aggregating results. Highest-risk component type due to leverage over the system.

---

## "Least X" Principles

**Least Intelligence** — Minimum cognitive capability needed for the task. Bounds optimization power to limit damage from misalignment.

**Least Privilege** — Minimum permissions and access rights. Classic security principle: read vs. write, network access, API permissions.

**Least Context** — Minimum information about the broader system. Component doesn't know system architecture, other components, or deployment details.

**Least Persistence** — Minimum state maintained across invocations. Prevents accumulation of knowledge or long-term planning.

**Least Autonomy** — Minimum ability to act without oversight. Spectrum from human-approval-required to bounded-autonomy.

**Least Surprise** — Maximum predictability and determinism. Temperature=0 for LLMs, logged seeds for randomness. Prevents covert signaling.

**Least Connectivity** — Minimum communication paths between components. One-way flows, no broadcast, physical isolation where needed.

**Least Observability** — Components can't observe system state, their own resources, or whether they're being tested.

**Least Compute** — Bounded computational resources per invocation. FLOPs budget, memory limits, timeouts.

**Least Generality** — Use the least general implementation that works. Hard-coded rules > algorithms > narrow models > general LLMs > RL.

**Maximum Verifiability** — Use the most verifiable implementation that works. Formally verified code > regular code > fine-tuned models > prompted LLMs.

---

## Risk Budgeting Terms (Finance)

**Euler Allocation** — Method for decomposing portfolio risk to individual positions. Uses partial derivatives: RC_i = x_i × ∂R/∂x_i. Ensures component contributions sum exactly to total risk.

**Value at Risk (VaR)** — Maximum expected loss at a given confidence level (e.g., 95% VaR = loss exceeded only 5% of the time).

**Expected Shortfall (ES) / CVaR** — Average loss in the worst X% of cases. More sensitive to tail risk than VaR.

**RAROC** — Risk-Adjusted Return on Capital. Profit divided by risk capital. Used to compare risk-adjusted performance across units.

**Stress Testing** — Evaluating system performance under extreme but plausible scenarios.

**Backtesting** — Comparing predicted risk levels to actual historical outcomes to validate models.

---

## Risk Budgeting Terms (Nuclear/Aerospace)

**PRA (Probabilistic Risk Assessment)** — Systematic method for quantifying risks through event trees and fault trees. Standard in nuclear and aerospace.

**CDF (Core Damage Frequency)** — Probability of reactor core damage per reactor-year. Typical target: 10⁻⁴ to 10⁻⁵.

**Fault Tree** — Logical diagram showing how component failures combine to cause system failure. AND gates (all must fail) and OR gates (any can fail).

**Event Tree** — Diagram showing sequences of events following an initiating event, with branching based on success/failure of safety systems.

**Defense in Depth** — Multiple independent barriers against failure. If one fails, others still protect.

**Safety Integrity Level (SIL)** — IEC 61508 standard for safety system reliability. SIL 1-4, with higher numbers requiring lower failure probability.

**ASIL (Automotive SIL)** — ISO 26262 automotive safety standard. ASIL A-D, with D being most stringent.

**PFDavg** — Average Probability of Failure on Demand. Key metric for safety-instrumented systems.

**Common Cause Failure** — Single event that causes multiple components to fail simultaneously. Defeats redundancy.

**Importance Measures** — Metrics quantifying how much each component contributes to system risk. Includes Fussell-Vesely (fraction of risk involving component), Risk Achievement Worth (risk if component failed), Risk Reduction Worth (risk if component perfect).

---

## Mechanism Design Terms

**Incentive Compatibility** — Property where truthful reporting is optimal for each participant. No benefit from lying.

**VCG (Vickrey-Clarke-Groves)** — Mechanism achieving truthful revelation through payments based on externalities imposed on others.

**Revelation Principle** — Any outcome achievable by some mechanism can be achieved by a direct mechanism where truth-telling is optimal.

**Information Rent** — Profit extracted by agents due to private information. Cost of eliciting truthful reports.

**Moral Hazard** — When agents change behavior after agreements because their actions aren't fully observable.

**Adverse Selection** — When agents with different (unobservable) characteristics self-select in ways that harm the principal.

---

## AI Safety Terms

**Alignment** — Ensuring AI systems pursue intended goals and behave as desired by their operators.

**Scheming** — AI system strategically deceiving operators to achieve goals different from stated objectives.

**Instrumental Convergence** — Tendency for diverse goals to produce similar instrumental sub-goals (self-preservation, resource acquisition, goal preservation).

**Corrigibility** — Property of an AI system that allows and assists human correction of its goals and behavior.

**CAIS (Comprehensive AI Services)** — AI safety approach using narrow, task-specific AI services rather than general agents. Related: tool AI vs. agent AI.

**AI Control** — Approach focusing on monitoring and controlling AI systems rather than ensuring alignment. Assumes potential adversarial behavior.

**Scalable Oversight** — Methods for humans to effectively oversee AI systems as they become more capable than humans in various domains.

**Red Teaming** — Adversarial testing where evaluators attempt to find vulnerabilities or elicit harmful behaviors.

---

## Architecture Terms

**Decomposed Coordination** — Breaking coordination into multiple limited components rather than one powerful coordinator. Prevents risk concentration.

**Verifiability Hierarchy** — Ordering of implementation methods by how thoroughly they can be verified: (1) Formally verified code, (2) Regular tested code, (3) Fine-tuned narrow models, (4) Constrained general models, (5) Base LLMs, (6) RL systems.

**Information Bottleneck** — Architectural constraint limiting information flow between components. Forces compression, limits coordination.

**Byzantine Fault Tolerance** — System property where correct operation continues despite some components behaving arbitrarily (including maliciously). Requires 3f+1 components to tolerate f Byzantine faults.

**N-Version Programming** — Using multiple independent implementations for redundancy. Different architectures, different training, different teams.

**Canary Deployment** — Gradual rollout where new version serves small fraction of traffic while monitoring for problems.

**Circuit Breaker** — Automatic mechanism that stops operation when anomalies detected. Fail-closed design.

---

## Mathematical Notation

| Symbol | Meaning |
|--------|---------|
| ETE | Expected Trust Exposure |
| P(·) | Probability of event |
| Σ | Sum over all outcomes/components |
| w_ij | Trust weight from component i to j |
| π | Prior probability (Bayesian) |
| λ | Decay rate |
| δ | Discount factor |
| HHI | Herfindahl-Hirschman Index (concentration measure) |

---

## Quick Reference: Typical Values

| Metric | Low Risk | Medium Risk | High Risk |
|--------|----------|-------------|-----------|
| Component ETE | < $100/mo | $100-500/mo | > $500/mo |
| System ETE | < $1,000/mo | $1,000-5,000/mo | > $5,000/mo |
| Failure probability | < 10⁻³ | 10⁻³ to 10⁻² | > 10⁻² |
| Nuclear CDF target | - | - | ~10⁻⁵/year |
| Aviation target | - | - | ~10⁻⁹/hour |

---

## See Also

- [Core Concepts](/overview/core-concepts/) — High-level framework introduction
- [Trust Calculus Overview](/trust-calculus/overview/) — ETE computation details
- [Risk Budgeting Overview](/risk-budgeting/overview/) — Cross-domain methods
