---
title: "Worked Examples"
description: "Step-by-step analysis of pattern interconnection in real architectures"
sidebar:
  order: 4
---

# Worked Examples

This page walks through complete analyses of interconnection in realistic architectures.

---

## Example 1: Code Review Verification Pipeline

### Initial Architecture

```
Code Review Verification Pipeline
─────────────────────────────────
                    ┌─────────────────┐
                    │  Code Submission │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌────────────┐ ┌────────────┐ ┌────────────┐
       │  Static    │ │  LLM-based │ │  LLM-based │
       │  Analysis  │ │  Security  │ │  Quality   │
       │  (Semgrep) │ │  Review    │ │  Review    │
       │            │ │  (GPT-4)   │ │  (Claude)  │
       └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                     ┌────────────┐
                     │ Aggregator │
                     │ (2/3 pass) │
                     └─────┬──────┘
                           │
                           ▼
                    ┌────────────────┐
                    │ Human Reviewer │
                    │ (for flagged)  │
                    └────────────────┘
```

### Step 1: Identify Apparent Diversity

| Component | Type | Provider | Methodology |
|-----------|------|----------|-------------|
| Static Analysis | Rule-based | Semgrep (open source) | Pattern matching |
| Security Review | LLM | OpenAI (GPT-4) | Natural language |
| Quality Review | LLM | Anthropic (Claude) | Natural language |

**Initial assessment**: Looks diverse! Rule-based + two different LLM providers.

### Step 2: Construct Correlation Matrix

Based on architecture review and red team testing:

| | Static | GPT-4 | Claude |
|------|--------|-------|--------|
| **Static** | 1.0 | 0.1 | 0.1 |
| **GPT-4** | 0.1 | 1.0 | **0.6** |
| **Claude** | 0.1 | **0.6** | 1.0 |

**Red flags identified**:
- GPT-4 and Claude show 0.6 correlation (both miss same novel vulnerability classes)
- Both LLMs trained on similar public code repositories
- Static analysis has low correlation with LLMs—this is actually good

### Step 3: Analyze Hidden Dependencies

Deeper investigation reveals:

```
Hidden dependencies discovered:

┌─────────────────────────────────────────────────────────────┐
│                    Same CI/CD Pipeline                       │
│    (timeout kills all checks if one is slow)                │
└─────────────────────────────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
    ┌─────────┐        ┌─────────┐        ┌─────────┐
    │ Static  │        │  GPT-4  │        │ Claude  │
    └─────────┘        └────┬────┘        └────┬────┘
                            │                  │
                            └────────┬─────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │     Same Prompt Template     │
                      │  (same framing, same blind  │
                      │   spots in task definition)  │
                      └──────────────────────────────┘
                                     │
                                     ▼
                      ┌──────────────────────────────┐
                      │       Same Review Team       │
                      │  (Alice wrote all prompts,   │
                      │   Bob reviews all escalations)│
                      └──────────────────────────────┘
```

**Additional correlations found**:
- Same prompt template: +0.2 to LLM correlation (now 0.8 effective)
- Same team: Organizational blind spots affect all components
- Shared CI infrastructure: Timeout can cause all checks to "pass by default"

### Step 4: Calculate Actual Risk

```
Apparent protection (assuming independence):
- Static: 80% effective at catching bugs
- GPT-4: 70% effective
- Claude: 70% effective
- Independent assumption: 1 - (0.2 × 0.3 × 0.3) = 98.2%

Actual protection (accounting for correlation):
- Static remains ~80% (low correlation with LLMs)
- GPT-4 + Claude effective joint miss rate: ~25% (not 9%)
  (because 0.6-0.8 correlation means they miss together often)
- Combined: 1 - (0.2 × 0.25) = 95%

Correlation tax: (100% - 95%) / (100% - 98.2%) ≈ 2.8×

Actual risk is 2.8× higher than independent model suggests.
```

### Step 5: Identify Interventions

| Intervention | Cost | Correlation Reduced | Priority |
|--------------|------|---------------------|----------|
| Different prompt templates | Low | 0.8 → 0.6 | **High** |
| Add fuzzing-based checker | Medium | Adds orthogonal check | **High** |
| Separate CI pipelines | Medium | Removes cascade risk | Medium |
| Different team for each | High | Removes org correlation | Low |

### Step 6: Redesigned Architecture

```
Improved Pipeline (correlation-aware):

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Static Analysis │  │   LLM Review    │  │  Fuzzing-based  │
│    (Semgrep)    │  │   (GPT-4)       │  │   (AFL/custom)  │
│                 │  │                 │  │                 │
│ Rule-based      │  │ Semantic        │  │ Dynamic         │
│ Deterministic   │  │ understanding   │  │ execution       │
│                 │  │                 │  │                 │
│ Catches:        │  │ Catches:        │  │ Catches:        │
│ - Known vulns   │  │ - Logic issues  │  │ - Edge cases    │
│ - Style issues  │  │ - Design flaws  │  │ - Crashes       │
└─────────────────┘  └─────────────────┘  └─────────────────┘
        │                   │                     │
        │ ρ = 0.1           │ ρ = 0.1             │
        └───────────────────┼─────────────────────┘
                            │
                  ┌─────────▼─────────┐
                  │    Aggregator     │
                  │   (2/3 required)  │
                  └───────────────────┘

Correlation matrix after redesign:
              Static   LLM    Fuzzing
Static         1.0     0.1     0.15
LLM            0.1     1.0     0.1
Fuzzing        0.15    0.1     1.0

New effective protection: ~99%
Correlation tax: ~1.5× (down from 2.8×)
```

### Key Lessons

1. **Different providers ≠ low correlation**: GPT-4 and Claude had high correlation despite different providers
2. **Hidden dependencies matter**: Same prompts, same team created correlation not visible in architecture diagram
3. **Fundamentally different methods are key**: Adding fuzzing (dynamic execution) provided more diversity than adding another LLM
4. **Small interventions can help**: Just using different prompts reduced correlation significantly

---

## Example 2: Healthcare Recommendation System

### Initial Architecture

```
Healthcare Recommendation Pipeline
──────────────────────────────────
                    ┌─────────────────┐
                    │ Patient Query   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Intake LLM    │
                    │  (summarize &   │
                    │   categorize)   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌────────────┐ ┌────────────┐ ┌────────────┐
       │  Medical   │ │   Drug     │ │  Symptom   │
       │  Knowledge │ │   Check    │ │  Severity  │
       │    LLM     │ │    LLM     │ │    LLM     │
       └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                    ┌────────────────┐
                    │   Synthesis    │
                    │      LLM       │
                    └────────┬───────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Recommendation │
                    └────────────────┘
```

### Analysis

**Obvious problem**: All 5 components are LLMs, likely from same provider.

### Correlation Matrix

| | Intake | Medical | Drug | Symptom | Synthesis |
|--|--------|---------|------|---------|-----------|
| **Intake** | 1.0 | 0.7 | 0.7 | 0.7 | 0.8 |
| **Medical** | 0.7 | 1.0 | 0.6 | 0.6 | 0.7 |
| **Drug** | 0.7 | 0.6 | 1.0 | 0.5 | 0.7 |
| **Symptom** | 0.7 | 0.6 | 0.5 | 1.0 | 0.7 |
| **Synthesis** | 0.8 | 0.7 | 0.7 | 0.7 | 1.0 |

**Average correlation: 0.67** — Extremely high!

### Critical Issues

1. **Information flow contamination**: Intake LLM's summary is used by all downstream components. If Intake misunderstands, everything downstream is compromised.

2. **Same-provider homogeneity**: All LLMs share training biases, medical knowledge gaps, and reasoning patterns.

3. **No ground truth checking**: All verification is LLM-based; no connection to verified medical databases.

4. **Synthesis inherits all errors**: Final synthesis sees outputs already filtered through correlated reasoning.

### Stakes Assessment

**Existential**: Healthcare recommendations can affect life and death.

**Matrix lookup**: Existential stakes + High correlation = 🚨 **Stop until resolved**

### Redesigned Architecture

```
Healthcare Recommendation Pipeline (Redesigned)
───────────────────────────────────────────────

                    ┌─────────────────┐
                    │ Patient Query   │
                    │  (raw input)    │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│  LLM Intake    │  │  Rule-based    │  │    Direct      │
│  (summarize)   │  │   Parser       │  │  Keyword       │
│                │  │  (symptoms,    │  │   Extract      │
│                │  │   medications) │  │                │
└───────┬────────┘  └───────┬────────┘  └───────┬────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
         ┌───────────────────────────────────────┐
         │        Independent Verifiers           │
         │                                        │
         │  ┌────────────┐ ┌────────────────────┐│
         │  │   Drug     │ │ Medical Database   ││
         │  │ Interaction│ │   Lookup           ││
         │  │ Database   │ │ (UpToDate, etc.)   ││
         │  │ (verified) │ │ (verified facts)   ││
         │  └────────────┘ └────────────────────┘│
         │                                        │
         │  ┌────────────┐ ┌────────────────────┐│
         │  │  Protocol  │ │  Contraindication  ││
         │  │  Matching  │ │     Checker        ││
         │  │(rule-based)│ │   (rule-based)     ││
         │  └────────────┘ └────────────────────┘│
         └───────────────────┬───────────────────┘
                             │
                             ▼
         ┌───────────────────────────────────────┐
         │          LLM Synthesis                 │
         │  (given verified facts, not guesses)  │
         └───────────────────┬───────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │    ALWAYS      │
                    │ Human Review   │
                    │  (physician)   │
                    └────────────────┘
```

### Key Changes

1. **Multiple intake methods**: LLM + rule-based + direct extraction
2. **Verified databases**: Drug interactions, medical facts from authoritative sources
3. **Rule-based protocol matching**: Deterministic, auditable
4. **LLM only for synthesis**: Given verified facts, not generating facts
5. **Mandatory human review**: Healthcare stakes require physician oversight

### New Correlation Structure

```
Correlation after redesign:

              LLM    Rule   Keyword  DrugDB  MedDB  Protocol
LLM           1.0    0.1     0.1     0.05    0.1     0.05
Rule          0.1    1.0     0.3     0.1     0.1     0.2
Keyword       0.1    0.3     1.0     0.1     0.1     0.1
DrugDB        0.05   0.1     0.1     1.0     0.2     0.1
MedDB         0.1    0.1     0.1     0.2     1.0     0.2
Protocol      0.05   0.2     0.1     0.1     0.2     1.0

Average correlation: 0.13 (down from 0.67)
Correlation tax: ~2× (down from estimated 50×+)
```

---

## Example 3: Financial Trading Safeguards

### Initial Architecture

```
Trading Order Verification
──────────────────────────
                    ┌─────────────────┐
                    │  Trading Order  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Risk Model A   │
                    │   (ML-based)    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Risk Model B   │
                    │   (ML-based)    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Execution     │
                    └─────────────────┘
```

### Quick Analysis

**Problem**: Sequential ML models, both trained on same historical data.

**Correlation estimate**: ~0.7 (both learned same patterns from same data)

**Stakes**: High (financial loss potential)

### Redesigned Architecture

```
Trading Order Verification (Redesigned)
───────────────────────────────────────
                    ┌─────────────────┐
                    │  Trading Order  │
                    └────────┬────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       │                     │                     │
       ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ ML Risk Model│    │ Rule-based   │    │  Position    │
│ (statistical)│    │    Limits    │    │   Limits     │
│              │    │ (hard-coded) │    │(deterministic)│
│ Catches:     │    │              │    │              │
│ - Pattern    │    │ Catches:     │    │ Catches:     │
│   anomalies  │    │ - Size limits│    │ - Exposure   │
│ - Volatility │    │ - Price bands│    │   limits     │
│   signals    │    │ - Asset class│    │ - Concentration
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       │ ρ = 0.1           │ ρ = 0.1           │
       └───────────────────┼───────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  ALL must pass  │
                  │  (conservative) │
                  └────────┬────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
      ┌───────────┐ ┌───────────┐ ┌───────────┐
      │ Normal    │ │  Human    │ │   Block   │
      │ Execution │ │  Review   │ │   Order   │
      │           │ │ (flagged) │ │           │
      └───────────┘ └───────────┘ └───────────┘
```

### Key Changes

1. **Three fundamentally different methods**:
   - ML for pattern recognition
   - Rule-based for hard limits
   - Deterministic position checking

2. **Conservative aggregation**: All must pass (not majority)

3. **No sequential dependency**: All checks run in parallel on same input

4. **Clear escalation**: Disagreement → human review

---

## Analysis Template

Use this template for your own systems:

```
## System: [Name]

### Current Architecture
[Diagram]

### Step 1: Identify Components
| Component | Type | Provider/Source | Methodology |

### Step 2: Build Correlation Matrix
| | A | B | C | ... |
|---|---|---|---|---|

### Step 3: Find Hidden Dependencies
- Infrastructure:
- Information flow:
- Organizational:
- Temporal:

### Step 4: Calculate Risk
- Apparent protection (independent model):
- Actual protection (correlated model):
- Correlation tax:

### Step 5: Stakes Assessment
- Stakes level:
- Matrix recommendation:

### Step 6: Interventions
| Intervention | Cost | Impact | Priority |

### Step 7: Redesigned Architecture
[Diagram]

### Step 8: Verification
- New correlation matrix:
- New correlation tax:
- Remaining risks:
```

---

See also:
- [Modeling Approaches](/applying/patterns/interconnection/modeling/) - Quantification methods
- [Solutions](/applying/patterns/interconnection/solutions/) - Implementation guidance
- [Decision Framework](/applying/patterns/interconnection/decision-framework/) - Prioritization
