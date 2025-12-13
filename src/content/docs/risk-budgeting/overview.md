---
title: "Quantified Risk Budgeting: A Cross-Domain Framework for AI Safety"
---

# Quantified Risk Budgeting: A Cross-Domain Framework for AI Safety

The most promising path toward a risk budgeting framework for AI safety lies in combining **Euler allocation** from finance, **Safety Integrity Levels** from nuclear/aerospace, and **mechanism design** from economics—three domains with decades of operational experience managing quantified risk hierarchically. Finance has proven that risks can be decomposed additively across portfolios using the formula RC_i = x_i · ∂R/∂x_i; nuclear safety has demonstrated that system-level failure probability targets like **10⁻⁹ per flight hour** can flow down to components through fault trees; and mechanism design has established that truthful risk reporting can be made incentive-compatible through VCG-style payments. The critical insight across all domains is that successful risk budgeting requires not just quantification, but compositional guarantees that component risks aggregate predictably and incentive structures that make honest reporting optimal.

## Five Essential Characteristics

This cross-domain analysis reveals that mature risk budgeting frameworks share five essential characteristics that any AI safety adaptation must incorporate.

**1. Mathematically principled allocation mechanisms**—Euler decomposition in finance, fault tree propagation in nuclear, Shapley values in cooperative games—ensure that component risk budgets sum correctly to system-level totals. Ad-hoc allocation creates either gaps (total risk exceeds sum of budgets) or waste (budgets exceed actual risk capacity). For AI systems, this requires developing risk measures that are homogeneous of degree 1 in component contributions, enabling the partial derivative computations Euler allocation requires.

**2. Explicit compositional guarantees** must specify how risks combine. Nuclear safety's fault tree semantics (AND gates multiply, OR gates sum) and ISO 26262's ASIL decomposition rules with independence verification provide templates. AI safety needs analogous formal semantics for how component capabilities, failure modes, and safety properties combine across architectural boundaries.

**3. Incentive-compatible reporting mechanisms** address the information asymmetry between those closest to risks and those setting budgets. VCG payments, RAROC-based compensation, and third-party verification all serve this function. For AI safety, this might involve safety-contingent procurement, independent red teams with authority to block deployment, or liability frameworks making development teams financially responsible for safety failures.

**4. Verification and audit infrastructure** must match framework sophistication. Nuclear's three lines of defense, aviation's MC/DC coverage requirements at DAL A, finance's backtesting with green/yellow/red zones, and carbon markets' MRV systems all provide independent confirmation that claimed risk levels match reality. AI safety verification remains the weakest link—current red-teaming and evaluation approaches lack the mathematical guarantees of formal verification and the operational track record of industrial safety audits.

**5. Conservative safety margins** buffer against model uncertainty and unknown unknowns. Pharmacology's 100-1000× uncertainty factors, nuclear's defense-in-depth with multiple independent barriers, and robust optimization's explicit "budget of uncertainty" all acknowledge that precise probability estimates are often unavailable. Rather than pretending to precision, effective frameworks embed substantial conservatism while enabling graduated response as uncertainties resolve.

## The Gap for AI Safety

The most significant gap between existing frameworks and AI safety needs lies in handling systematic failures rather than random hardware faults. Nuclear PRA, reliability allocation, and SIL calculations fundamentally assume independent random failures with known probability distributions. AI systems exhibit systematic failures—emergent capabilities, adversarial vulnerabilities, distributional shift—where independence assumptions fail and historical failure rates may not predict future behavior. Addressing this gap requires extending compositional verification methods, developing importance measures for systematic rather than random failures, and potentially adopting defense-in-depth architectures with diverse AI systems and human oversight as independent barriers rather than relying solely on quantified probabilities.

The theoretical apparatus exists: linear logic for consumable risk budgets, mechanism design for truthful reporting, Shapley allocation for principled distribution, Markov categories for compositional probability. The engineering challenge is instantiating these theories in practical frameworks with appropriate conservatism for the profound uncertainties inherent in novel AI systems.

## Detailed Domain Analyses

- [Euler Allocation (Finance)](euler-allocation.md)
- [Nuclear Safety & Probabilistic Risk Assessment](nuclear-safety-pra.md)
- [Mechanism Design for Truthful Reporting](mechanism-design.md)
- [Attack Surface & Capability Metrics](attack-surface-metrics.md)
- [Carbon Budgets & Large-Scale Allocation](carbon-budgets.md)
- [Linear Logic & Type Systems](linear-logic-types.md)
- [ASIL Decomposition (Automotive)](asil-decomposition.md)
- [Chance Constraints & Robust Optimization](chance-constraints.md)
- [Safety Factors (Pharmacology)](safety-factors.md)
- [Historical Failures](lessons-from-failures.md)
- [Emerging AI Safety Frameworks](emerging-ai-frameworks.md)
- [Compositional Safety Properties](compositional-safety.md)
