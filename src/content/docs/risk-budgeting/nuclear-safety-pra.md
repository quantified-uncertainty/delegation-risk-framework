---
title: "Nuclear Safety: Probabilistic Risk Assessment"
---

# Nuclear Safety: Probabilistic Risk Assessment

Probabilistic Risk Assessment (PRA), developed after Three Mile Island and codified in NRC regulations, demonstrates how a single system-level risk target can be decomposed across thousands of components. U.S. nuclear plants operate to quantified safety goals: **Core Damage Frequency below 10⁻⁴ per reactor-year** and **Large Early Release Frequency below 10⁻⁵ per reactor-year**. Actual performance achieves an order of magnitude better—CDF around **10⁻⁵** and LERF around **10⁻⁶**—demonstrating that aggressive targets coupled with defense-in-depth create substantial safety margins.

## Decomposition Mechanism

The decomposition mechanism uses fault tree and event tree analysis. Fault trees propagate failure probabilities upward: AND gates multiply component probabilities (P_output = Π P_inputs), while OR gates combine them (P_output ≈ Σ P_inputs for rare events). Importance measures then identify which components contribute most to total risk. **Fussell-Vesely importance** quantifies what fraction of total risk comes from cut sets containing a component; **Risk Achievement Worth (RAW)** measures how much risk increases if that component fails (RAW > 2 triggers NRC significance thresholds). These metrics guide resource allocation—components with high RAW receive more redundancy, testing, and maintenance budget.

## Safety Integrity Levels (IEC 61508)

IEC 61508's Safety Integrity Levels provide an even more explicit budget framework. Each SIL corresponds to a Probability of Failure on Demand range: **SIL 4 requires PFD between 10⁻⁵ and 10⁻⁴**, representing a Risk Reduction Factor of 10,000-100,000×. When a Safety Instrumented Function requires SIL 3, its constituent sensor, logic solver, and actuator subsystems each receive allocated PFD targets that sum to the overall requirement: **PFD_system = PFD_sensor + PFD_logic + PFD_actuator**. This additive decomposition for series reliability is the direct analog of Euler allocation for independent failure modes.

## Aerospace Safety (ARP 4761, DO-178C)

Aerospace safety assessment extends this with an inverse relationship between severity and allowable probability. **Catastrophic failures must be "Extremely Improbable" at below 10⁻⁹ per flight hour**; hazardous failures below 10⁻⁷; major below 10⁻⁵. Since a transport aircraft has approximately 100 potential catastrophic failure conditions, the aggregate budget for catastrophic failures is around 10⁻⁷ per flight hour, with each condition allocated a fraction. Design Assurance Levels (A through E) then flow requirements to software and hardware components, with DAL A requiring **71 verification objectives including MC/DC structural coverage**.

## Key Concepts for AI Safety

| Concept | Definition | AI Safety Analog |
|---------|------------|------------------|
| Core Damage Frequency | System-level failure target | Catastrophic harm probability |
| Fault Tree | Logical decomposition of failure modes | Capability/failure decomposition |
| Fussell-Vesely Importance | Component contribution to total risk | Which AI components matter most |
| Risk Achievement Worth | Risk increase if component fails | Impact of component compromise |
| Safety Integrity Level | Quantified reliability requirement | AI capability/trust level |
| Defense in Depth | Multiple independent barriers | Layered AI safety mechanisms |

## Limitations for AI

- Assumes independent random failures
- Historical failure rates inform future predictions
- Components have well-characterized failure modes
- AI exhibits systematic, not random, failures
