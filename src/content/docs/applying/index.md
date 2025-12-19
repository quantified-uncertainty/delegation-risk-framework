---
title: Applying the Framework
description: Practical guidance for designing safe AI systems using delegation risk principles.
---

This section bridges theory and practice. It covers design principles, architecture patterns, worked examples, and interactive tools.

## Prerequisites

Before applying the framework, understand:
- [Core Concepts](/getting-started/core-concepts/) — The key ideas
- [Framework Overview](/framework/overview/) — The quantitative foundation

## Section Organization

### Foundations
Start here to understand the design principles:

| Page | Purpose |
|------|---------|
| [Principles to Practice](/applying/principles-to-practice/) | How abstract principles become concrete implementations |
| [Least-X Principles](/applying/least-x-principles/) | The core constraints: least capability, privilege, context, etc. |

### Architecture
How to structure AI systems for safety:

| Page | Purpose |
|------|---------|
| [Decomposed Coordination](/applying/decomposed-coordination/) | Breaking monolithic systems into bounded components |
| [Coordinator Constraints](/applying/coordinator-constraints/) | Special constraints for high-risk coordinator components |
| [Safety Mechanisms](/applying/safety-mechanisms/) | Circuit breakers, tripwires, verification layers |
| [Forecasting & Navigation](/applying/forecasting-navigation/) | Handling uncertainty and planning |

### Worked Examples
Complete implementations showing principles in practice:

| Example | Domain | Risk Level |
|---------|--------|------------|
| [Research Assistant](/applying/examples/research-assistant-example/) | Knowledge work | Medium |
| [Code Deployment](/applying/examples/code-deployment-example/) | Software engineering | High |
| [Healthcare Bot](/applying/examples/healthcare-bot-example/) | Medical decisions | Very High |
| [Trading System](/applying/examples/trading-system-example/) | Finance | High |

### Tools & Guides
Interactive tools and practical checklists:

| Tool | Purpose |
|------|---------|
| [Quick Start](/applying/tools/quick-start/) | Step-by-step application checklist |
| [Decision Guide](/applying/tools/decision-guide/) | Choosing implementations based on risk |
| [Delegation Risk Calculator](/applying/tools/delegation-risk-calculator/) | Compute risk for your system |
| [Risk Inheritance](/applying/tools/trust-propagation/) | Model risk flow through delegation chains |
| [Tradeoff Frontier](/applying/tools/tradeoff-frontier/) | Explore capability vs. safety tradeoffs |
| [Cost-Benefit Analysis](/applying/tools/cost-benefit/) | ROI of safety investments |
| [Empirical Tests](/applying/tools/empirical-tests/) | Validating the framework |

## Suggested Reading Paths

### For Implementers
1. [Quick Start](/applying/tools/quick-start/) — Get oriented
2. [Least-X Principles](/applying/least-x-principles/) — Understand constraints
3. [Research Assistant Example](/applying/examples/research-assistant-example/) — See it in practice
4. [Decision Guide](/applying/tools/decision-guide/) — Make choices for your system

### For Architects
1. [Decomposed Coordination](/applying/decomposed-coordination/) — Architecture patterns
2. [Coordinator Constraints](/applying/coordinator-constraints/) — Managing high-risk components
3. [Safety Mechanisms](/applying/safety-mechanisms/) — Defense in depth
4. [Code Deployment Example](/applying/examples/code-deployment-example/) — High-stakes implementation

### For Evaluators
1. [Principles to Practice](/applying/principles-to-practice/) — Theory-practice mapping
2. [Delegation Risk Calculator](/applying/tools/delegation-risk-calculator/) — Quantify risk
3. [Cost-Benefit Analysis](/applying/tools/cost-benefit/) — ROI analysis
4. [Empirical Tests](/applying/tools/empirical-tests/) — Validation approach

## How This Section Connects

```
[Framework] → [Applying] → [Case Studies]
                  ↓
         ┌───────┴───────┐
         ↓               ↓
   [Principles]    [Architecture]
         ↓               ↓
         └───────┬───────┘
                 ↓
            [Examples]
                 ↓
             [Tools]
```

## Next Steps

- **See real applications** → [Case Studies](/case-studies/)
- **Understand the theory** → [Deep Dives](/deep-dives/)
- **Learn from other fields** → [Cross-Domain Methods](/cross-domain-methods/)
