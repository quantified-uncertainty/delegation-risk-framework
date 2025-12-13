---
title: "Coordinator Constraints - Brainstorming"
---

# Brainstorming: Improving the Coordinator Constraints Framework

:::note[Internal Working Document]
This is a brainstorming document for improving the [Coordinator Constraints](/principles/coordinator-constraints/) page. It contains analysis, critiques, and potential improvements—not finalized content.
:::

This document analyzes the current [Coordinator Constraints](/principles/coordinator-constraints/) framework and brainstorms potential improvements across several dimensions.

## 1. Taxonomy/Categorization Analysis

### Current Framework

The document organizes constraints into 4 intrinsic dimensions + external safeguards:

| Dimension | Question | # Principles |
|-----------|----------|--------------|
| Influence/Reach | What can it affect? | 5 |
| Desires/Objectives | What does it want? | 1 |
| Intelligence/Capability | How can it reason? | 4 |
| Knowledge/Context | What does it know? | 2 |
| External Safeguards | How is it checked? | 6 |

### Issues with Current Taxonomy

**Imbalanced categories**: Desires has only 1 principle while Influence has 5. This suggests either:
- Desires is underdeveloped and needs more principles
- Influence should be split into multiple categories
- The categorization isn't carving at natural joints

**"Desires" is anthropomorphic**: Do AI systems have "desires"? Better framings:
- Objective function
- Optimization target
- Reward signal
- Loss function
- What it's trained to maximize

**"Intelligence" conflates multiple things**:
- Planning depth (Shortest Horizon)
- Self-modeling (Least Meta-Reasoning)
- Self-modification (Least Self-Improvement)
- Adaptability (Commitment Without Flexibility)

These are distinct capabilities that might warrant separate treatment.

**External Safeguards feels bolted on**: The first 4 dimensions are intrinsic properties; External Safeguards is architectural. This asymmetry suggests a different organizational scheme.

### Alternative Taxonomies to Consider

**Option A: Input/Process/Output Model**

```
┌─────────────────────────────────────────────────────┐
│                    COORDINATOR                       │
│                                                      │
│  INPUTS           PROCESSING         OUTPUTS        │
│  ───────          ──────────         ───────        │
│  • Context        • Reasoning        • Decisions    │
│  • Memory         • Planning         • Commands     │
│  • Permissions    • Self-model       • Messages     │
│                                                      │
└─────────────────────────────────────────────────────┘
                         │
                    VERIFICATION
                    ────────────
                    • Redundancy
                    • Oversight
                    • Veto
```

**Option B: Capability/Intent/Opportunity (Fraud Triangle)**

Like the fraud triangle from accounting:

- **Capability**: What technical abilities does it have?
- **Intent**: What is it trying to achieve?
- **Opportunity**: What access/permissions does it have?

Remove any one and risk is reduced.

**Option C: Static vs Dynamic Properties**

- **Static** (fixed at design time): Architecture, permissions, communication protocols
- **Dynamic** (vary at runtime): Context, decisions, state
- **Meta** (about the system itself): Self-knowledge, self-modification

**Option D: What/How/With-What**

- **What** it can do (capabilities, permissions)
- **How** it does it (reasoning, planning)
- **With what** information (context, memory)
- **How it's checked** (verification)

### Recommendation

Consider restructuring around:

1. **Capabilities** (what actions it can take)
2. **Cognition** (how it reasons and plans)
3. **Information** (what it knows and remembers)
4. **Objectives** (what it optimizes for)
5. **Verification** (how it's checked externally)

This is more MECE (mutually exclusive, collectively exhaustive) and uses less anthropomorphic language.

---

## 2. Missing Principles

### High Priority (Likely Should Add)

**Principle of Least Authority/Permission**
- Coordinator can only invoke specific pre-approved components
- Cannot execute arbitrary code or access arbitrary resources
- Whitelist, not blacklist approach
- *Currently implied but not explicit*

**Principle of Reversibility**
- Coordinator actions should be reversible where possible
- Prefer "stage for review" over "execute immediately"
- Distinguish reversible (route task) vs irreversible (deploy to production) actions
- Higher scrutiny for irreversible actions

**Principle of Graceful Degradation**
- System should fail safely if coordinator fails/hangs/crashes
- Default to safe state, not continuation
- Timeouts should trigger human review, not auto-approval
- *Critical for availability + safety*

**Principle of Rate Limiting**
- Coordinator can only make N decisions per time period
- Prevents rapid automated attacks
- Forces human-scale operation
- Suspicious if suddenly making 1000x normal decisions

**Principle of Resource Bounds**
- Hard limits on compute, memory, wall-clock time
- Cannot request more resources
- Bounded resource usage makes behavior more predictable
- *Overlaps with "Shortest Horizon" but more concrete*

### Medium Priority (Consider Adding)

**Principle of Separation of Duties**
- No single coordinator can complete high-risk action alone
- Different coordinators for different phases (propose vs approve)
- Like two-key nuclear launch
- *Partially covered by redundancy but worth making explicit*

**Principle of Observable Intent**
- Coordinator must declare intent before acting
- "I plan to route this to component X because Y"
- Allows preemptive veto before action, not just post-hoc review
- Makes reasoning auditable

**Principle of Minimal Footprint**
- Coordinator shouldn't leave persistent traces
- No writing to logs it can later read
- No environmental side effects it can later detect
- Prevents signaling to future selves

**Principle of Freshness/Non-Replay**
- Coordinator decisions have timestamps and expire
- Can't replay old decisions
- Prevents "save up" good decisions for later misuse

**Principle of Containment**
- Coordinator failures don't cascade to other components
- Bulkheads between coordination and execution
- One bad coordinator can't poison others

### Lower Priority (Maybe Add)

**Principle of Predictability**
- Same inputs should produce same (or narrowly bounded) outputs
- Reduces ability to behave differently when not observed
- Enables testing and verification

**Principle of Monotonic Capability**
- Coordinator capabilities can only decrease over session, not increase
- Start with some permissions, can only lose them
- Prevents privilege escalation

**Principle of Minimal Expressiveness**
- Coordinator's "language" should be as limited as possible
- Can only express routing decisions, not arbitrary computation
- DSL (domain-specific language) not general-purpose

---

## 3. Redundant/Overlapping Principles

### Strong Overlaps (Consider Merging)

**Least Influence + Least Direct Impact**
- Both limit what coordinator can affect
- Difference: Influence = magnitude, Direct Impact = indirection
- Could merge into "Principle of Bounded Impact" with two aspects

**Minimal Context + Episodic Operation**
- Both limit information access
- Difference: Context = spatial (what info), Episodic = temporal (when/memory)
- Could merge into "Principle of Information Minimization" with spatial/temporal aspects

**Maximum Oversight + Maximum Transparency**
- Both about visibility into coordinator
- Difference: Oversight = monitoring, Transparency = explainability
- Could merge into "Principle of Full Observability"

### Moderate Overlaps (Keep Separate but Clarify)

**Shortest Horizon + Commitment Without Flexibility**
- Both limit planning
- Horizon = depth of lookahead
- Commitment = inability to revise
- Related but distinct—keep separate but clarify relationship

**Simplest Communication + One-Way Flows**
- Both constrain communication
- Simplest = bandwidth/complexity
- One-Way = direction/topology
- Orthogonal dimensions of same thing—consider subsection together

### Suggested Consolidation

Could reduce from 18 principles to ~12:

| Current | Proposed |
|---------|----------|
| Least Influence + Least Direct Impact | Bounded Impact |
| Simplest Communication + One-Way Flows | Constrained Communication |
| Minimal Context + Episodic Operation | Information Minimization |
| Maximum Oversight + Maximum Transparency | Full Observability |
| Keep others as-is | ... |

**Tradeoff**: Fewer principles = easier to remember, but loses nuance.

---

## 4. Conceptual Clarity Issues

### Undefined Core Concepts

**What exactly IS a "coordinator"?**

The document never defines this precisely. Questions:
- Is it a specific component? A role? A capability?
- Can a component be both coordinator and executor?
- What distinguishes coordinator from "orchestrator" or "scheduler"?

Suggested definition: *A coordinator is a component that makes decisions about which other components to invoke, in what order, with what inputs, but does not itself perform the substantive work.*

**What is an "episode"?**

"Episodic operation" requires defining episode boundaries:
- One user request?
- One task?
- One decision?
- One session?

Different boundaries have different implications.

**What is a "step" in planning horizon?**

"1-10 steps" is meaningless without defining step:
- One API call?
- One component invocation?
- One decision?
- One second?

### Vague Measurements

The document mentions measuring things but doesn't specify how:

| Concept | Mentioned | Measurement Unclear |
|---------|-----------|---------------------|
| Influence | "How much impact can coordinator have?" | Impact in what units? |
| Planning depth | "1-10 steps" | What's a step? |
| Information richness | "Rich context" | Bits? Semantic content? |
| Coordination complexity | "decisions × information" | How to count? |

### Ambiguous Distinctions

**"Desires" vs "Objectives"**: Used interchangeably. Pick one term.

**"Intelligence" vs "Capability"**: Current section is called "Intelligence/Capability" suggesting they're the same, but intelligence (reasoning ability) ≠ capability (what actions are possible).

**"Transparency" vs "Explainability" vs "Interpretability"**: All used but distinctions unclear.

---

## 5. Implementation Gaps

### Hard-to-Implement Principles

**Least Meta-Reasoning**
- How do you detect if a model is reasoning about itself?
- Current LLMs do this by default ("As an AI, I...")
- Would require specialized training or architecture
- No clear implementation path

**Commitment Without Flexibility**
- How do you prevent a model from effectively "revising" by making new decisions that counteract old ones?
- Logging decisions is easy; preventing strategic sequences is hard

**Diverse Implementation**
- Truly diverse implementations are expensive
- How diverse is "diverse enough"?
- Models trained on similar data may have correlated failures despite architectural differences

**Shortest Horizon**
- How do you limit planning depth in a transformer?
- Chain-of-thought can be arbitrarily long
- Compute limits are crude proxy

### Missing Implementation Details

**Performance/latency implications**
- Multiple coordinators + voting + verification = slow
- What's acceptable latency?
- How to handle real-time requirements?

**Failure handling**
- What happens when a coordinator times out?
- What if verifier is unavailable?
- What if redundant coordinators all fail?

**Testing and verification**
- How do you test that constraints are enforced?
- How do you red-team the coordinator?
- What's the test coverage requirement?

**Monitoring and alerting**
- What metrics to track?
- What thresholds trigger alerts?
- Who responds to alerts?

### Suggested Additions

Each principle should have:
1. **Definition**: Precise statement
2. **Rationale**: Why it matters
3. **Implementation**: How to achieve it
4. **Verification**: How to test it
5. **Metrics**: How to measure compliance
6. **Failure modes**: What can go wrong

---

## 6. Tensions and Tradeoffs

### Fundamental Tensions

```
Safety ←――――――――――――――――――→ Capability
      More constraints          More useful

Efficiency ←――――――――――――――→ Redundancy
           Fast, cheap          Multiple checks

Autonomy ←――――――――――――――――→ Oversight
         Scales                 Catches errors

Context ←―――――――――――――――――→ Security
        Better decisions        Less attack surface
```

### Specific Tradeoff Analysis

**Easy Veto vs Availability**
- Easy veto = high false positive rate
- High false positives = lots of blocked legitimate actions
- Blocked actions = reduced availability/usefulness
- *Need to quantify acceptable false positive rate*

**Episodic Operation vs Learning**
- No memory = can't learn from mistakes
- Can't learn = repeats errors
- Repeats errors = worse performance
- *Need to specify what learning IS allowed (aggregate stats)*

**Simplest Communication vs Expressiveness**
- Simple messages = can't express complex coordination
- Can't express = worse task performance
- *Need to characterize what tasks become impossible*

**Diverse Implementation vs Consistency**
- Different implementations = different behaviors
- Different behaviors = unpredictable system
- *Need to specify what aspects must be consistent*

### Missing: Guidance on Navigating Tradeoffs

The document states principles but doesn't help navigate tensions:
- When is it okay to relax a constraint?
- How do you decide between conflicting principles?
- What's the priority order?

**Suggested addition**: Principles should be ranked or have "override conditions" specified.

---

## 7. Connections to Literature

### Security Literature

| Principle | Related Security Concept |
|-----------|-------------------------|
| Least Influence | Principle of Least Privilege |
| Diverse Implementation | Defense in Depth |
| Redundancy | Byzantine Fault Tolerance |
| Verification | Separation of Duties |
| One-Way Flows | Air Gap / Data Diode |
| Minimal Context | Need-to-Know |
| Easy Veto | Fail-Secure |

**Gap**: Should explicitly cite these connections and leverage existing frameworks.

### AI Safety Literature

| Principle | Related AI Safety Concept |
|-----------|--------------------------|
| Least Influence | Capability Control |
| Least Desire | Corrigibility |
| Least Meta-Reasoning | Transparency/Interpretability |
| Shortest Horizon | Myopia |
| Episodic Operation | Memoryless Agents |
| Redundancy | Ensemble Methods |

**Gap**: Should connect to MIRI, Anthropic, DeepMind safety research.

### Other Relevant Fields

**Nuclear Safety**
- Two-person rule
- Defense in depth
- Fail-safe defaults
- Regular testing

**Aviation Safety**
- Checklists
- Crew resource management
- Redundant systems
- Black box recording

**Medical Safety**
- "First, do no harm"
- Informed consent
- Second opinions
- Adverse event reporting

**Financial Controls**
- Separation of duties
- Dual authorization
- Audit trails
- Materiality thresholds

**Gap**: Rich literature to draw from; should mine for principles and failure modes.

---

## 8. Edge Cases and Failure Modes

### Attacks on the Framework

**Correlated Failures**
- All "diverse" coordinators trained on similar data
- Same misconception across all of them
- Unanimous agreement on wrong answer
- *Mitigation: Specify diversity requirements more precisely*

**Human-in-the-Loop Attacks**
- Attacker compromises human reviewer
- Or: Attacker floods with false positives until human rubber-stamps
- *Mitigation: Rotate reviewers, monitor approval rates*

**Side Channel Communication**
- Coordinators communicate via timing, resource usage, error rates
- Even without explicit messages, can coordinate
- *Mitigation: Randomize timing, isolate resources*

**Encoding Schemes in Innocent Decisions**
- Coordinator uses routing decisions to encode information
- "Route to component 1, 0, 1, 1, 0" = binary message
- *Mitigation: Monitor for patterns, randomize when possible*

**Cross-Episode Communication**
- Coordinator affects environment (writes file, modifies config)
- Future coordinator reads environment
- Memory through environment, not internal state
- *Mitigation: Ephemeral environments, no persistent side effects*

**Emergent Coordination**
- Independent coordinators converge on same strategy without communication
- Schelling points in decision space
- *Mitigation: Diverse training, randomized tiebreaking*

### Failure Modes of Principles

| Principle | Failure Mode |
|-----------|--------------|
| Easy Veto | Checker always vetoes (DoS) or never vetoes (rubber stamp) |
| Redundancy | All implementations have same bug |
| Episodic Operation | Environment serves as memory |
| Shortest Horizon | Multiple short-horizon decisions sum to long-horizon plan |
| Verification | Verifier is captured or gamed |
| Transparency | Explanations are post-hoc rationalizations |

### Questions Not Addressed

1. What if the coordinator is more capable than the verifier?
2. What if legitimate tasks require violating constraints?
3. What if constraints make system too slow/expensive to use?
4. How do constraints compose when coordinators are hierarchical?
5. What's the threat model? (Malicious coordinator? Buggy? Misaligned?)
6. How do you update constraints over time?
7. What's the governance process for constraint changes?

---

## 9. Structural/Presentation Improvements

### Current Issues

**Too many principles (18)**
- Hard to remember
- Hard to audit against
- Suggests some should merge

**Inconsistent depth**
- Some principles get a paragraph
- Others get multiple subsections + diagrams
- Desires section is underdeveloped

**Missing practical guidance**
- Lots of "what" but less "how"
- No example implementations
- No case studies

### Suggested Structure

```
1. Introduction
   - What is a coordinator?
   - Why are coordinators high-risk?
   - Framework overview

2. Core Principles (organized by dimension)
   - Each principle: Definition, Rationale, Implementation, Verification

3. Implementation Patterns
   - Common architectures
   - Example code/pseudocode
   - Anti-patterns

4. Tradeoff Analysis
   - When to relax constraints
   - Priority ordering
   - Decision framework

5. Case Studies
   - Research assistant coordinator
   - Deployment coordinator
   - Multi-agent coordination

6. Failure Mode Analysis
   - Known attacks
   - Mitigations
   - Open problems

7. Checklist
   - Quick audit checklist for coordinator designs
```

---

## 10. Summary of Recommendations

### High Priority

1. **Define "coordinator" precisely** at the start
2. **Add Principle of Least Authority** (explicit permissions)
3. **Add Principle of Reversibility** (prefer reversible actions)
4. **Add Principle of Graceful Degradation** (fail-safe)
5. **Consolidate overlapping principles** (reduce from 18 to ~12)
6. **Add implementation guidance** for each principle
7. **Add tradeoff analysis** section

### Medium Priority

8. **Reconsider taxonomy** (Capabilities/Cognition/Information/Objectives/Verification)
9. **Add rate limiting principle**
10. **Add resource bounds principle**
11. **Connect to existing literature** explicitly
12. **Add failure mode analysis** for each principle
13. **Develop the Desires section** (currently thin)

### Lower Priority

14. **Add case studies**
15. **Create audit checklist**
16. **Add metrics/measurement guidance**
17. **Specify threat model explicitly**
18. **Add governance process for updates**

---

## Appendix: Alternative Framing - The "CAIRO" Model

One possible reorganization using an acronym:

**C**apabilities - What technical actions can it take?
- Least Authority (permissions)
- Bounded Impact (influence limits)
- Resource Bounds (compute/memory)

**A**wareness - What does it know about itself and environment?
- Minimal Context (current task only)
- Episodic Operation (no memory)
- Least Meta-Reasoning (no self-model)

**I**ntent - What is it trying to achieve?
- Minimal Objectives (narrow goals)
- Short Horizon (immediate focus)

**R**easoning - How does it think and decide?
- Constrained Communication (simple messages)
- Commitment (no revision)
- Transparency (auditable logic)

**O**versight - How is it checked?
- Redundancy (multiple implementations)
- Verification (independent checker)
- Easy Veto (asymmetric blocking)
- Maximum Monitoring (full logging)

This gives a memorable acronym and ~13 principles organized into 5 categories.
