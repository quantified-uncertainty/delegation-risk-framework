---
title: "Euler Allocation: The Fundamental Aggregation Problem"
---

# Euler Allocation: The Fundamental Aggregation Problem

```mermaid
flowchart TB
    TR["Total Risk (R)"]
    TR -->|decompose| C1["Component 1: RC1"]
    TR -->|decompose| C2["Component 2: RC2"]
    TR -->|decompose| C3["Component 3: RC3"]
    C1 --> Sum["Sum: RC1 + RC2 + RC3 = R"]
    C2 --> Sum
    C3 --> Sum
```

Each component's risk contribution is: **RC_i = x_i × (∂R/∂x_i)** — weight times marginal impact.

The mathematical foundation for hierarchical risk decomposition comes from financial risk budgeting, where **Euler's theorem for homogeneous functions** enables perfect additive decomposition of total risk into component contributions. For any risk measure R(x) that is homogeneous of degree 1 in portfolio weights, total risk equals the sum of each component's marginal contribution multiplied by its weight: **R(x) = Σᵢ xᵢ · ∂R(x)/∂xᵢ**.

:::tip[Why This Matters]
This Euler decomposition guarantees that allocated risks "add up" exactly to total risk—a property called full allocation that no ad-hoc method achieves.
:::

## Practical Implementation

The practical implementation uses Component VaR (CoVaR) for Value at Risk or Expected Shortfall contributions. Component VaR for position i equals **CoVaR_i = x_i · β_i · VaR**, where β_i is the position's beta to the portfolio. The crucial property: **Σᵢ CoVaR_i = Total VaR** exactly, accounting for diversification benefits. Banks cascade these budgets from board-level risk appetite through business units to trading desks, with each level receiving explicit risk limits derived from the aggregate. The Financial Stability Board's 2013 Risk Appetite Framework established this as regulatory standard, requiring quantitative risk tolerances that flow hierarchically through organizations.

## Application to AI Safety

This approach directly transfers to AI safety: if system-level harm probability is the risk measure, and subsystem contributions can be computed via marginal impacts, Euler allocation provides mathematically principled decomposition. The challenge lies in defining appropriate homogeneous risk measures for AI systems—current approaches like Anthropic's AI Safety Levels provide tiers but lack the continuous differentiability Euler allocation requires.

## Key Properties

- **Full allocation**: Component risks sum exactly to total
- **Marginal contribution**: Each component's share reflects its impact on total risk
- **Diversification accounting**: Correlations between components are handled correctly
- **Hierarchical cascading**: Budgets flow from top-level to components

:::caution[Limitations for AI]
Requires continuous, differentiable risk measures. Assumes risks can be meaningfully quantified. Historical data may not predict future AI behavior. Independence assumptions may fail for correlated AI failures.
:::
