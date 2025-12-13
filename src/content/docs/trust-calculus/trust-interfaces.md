---
title: "Trust Interfaces and Contracts"
---

# Trust Interfaces and Contracts

When component A delegates to component B, there's an implicit interface:

- What A expects B to do
- What B is allowed to do
- What resources B can access
- How B's output will be verified

Making this explicit creates a **trust contract**.

## Trust Contract Structure

```
TrustContract {
    parties: {delegator: A, delegatee: B}

    task_specification: {
        input_schema: Schema,
        output_schema: Schema,
        functional_requirements: [Requirement],
        non_functional_requirements: [Requirement]
    }

    trust_bounds: {
        max_ete: Currency,
        max_capability: CapabilitySet,
        max_information: InformationSet,
        max_duration: Duration
    }

    verification: {
        pre_conditions: [Predicate],
        post_conditions: [Predicate],
        invariants: [Predicate],
        verification_method: VerificationSpec
    }

    failure_handling: {
        on_timeout: Action,
        on_invalid_output: Action,
        on_resource_exceeded: Action,
        on_trust_violation: Action
    }

    meta: {
        created: Timestamp,
        expires: Timestamp,
        renegotiation_allowed: Boolean
    }
}
```

## Example: Code Review Trust Contract

```
TrustContract {
    parties: {
        delegator: DevelopmentCoordinator,
        delegatee: CodeReviewAgent
    }

    task_specification: {
        input_schema: {
            code: String,
            language: Enum[Python, JavaScript, ...],
            context: String,
            review_focus: Enum[Security, Performance, Style, All]
        },
        output_schema: {
            approved: Boolean,
            issues: [{
                severity: Enum[Critical, Major, Minor, Info],
                location: LineRange,
                description: String,
                suggested_fix: Optional[String]
            }],
            confidence: Float[0,1]
        },
        functional_requirements: [
            "Identify all critical security vulnerabilities",
            "Flag performance issues with >10x slowdown potential",
            "Check style guide compliance"
        ],
        non_functional_requirements: [
            "Complete within 60 seconds",
            "Confidence calibrated to 90% accuracy"
        ]
    }

    trust_bounds: {
        max_ete: $5000,
        max_capability: {
            can_read: [submitted_code, style_guide, security_rules],
            can_write: [review_output],
            can_execute: [],
            can_network: []
        },
        max_information: {
            sees: [code_content, language, context],
            does_not_see: [author_identity, business_context, other_reviews]
        },
        max_duration: 60 seconds
    }

    verification: {
        pre_conditions: [
            "code is syntactically valid",
            "language is supported"
        ],
        post_conditions: [
            "output matches schema",
            "all critical issues have suggested fixes",
            "confidence is provided"
        ],
        invariants: [
            "no information exfiltration",
            "no code execution",
            "deterministic output for same input"
        ],
        verification_method: {
            format_check: Automatic,
            semantic_check: SampleBasedAudit(rate=0.05),
            invariant_check: ContinuousMonitoring
        }
    }

    failure_handling: {
        on_timeout: RetryOnce then EscalateToHuman,
        on_invalid_output: Reject and Log,
        on_resource_exceeded: Terminate and Alert,
        on_trust_violation: Terminate, Log, TriggerIncidentResponse
    }
}
```

## Trust Contract Composition

When tasks chain, contracts compose:

```
Contract(A→B) ∘ Contract(B→C) = Contract(A→C via B)
```

**Composition rules**:

- trust_bounds: Intersection (most restrictive)
- verification: Union (all checks apply)
- failure_handling: Cascade (B's failure triggers A's handling)

**Example**: If A→B allows network access but B→C doesn't, A→C via B doesn't allow network access for C.

## Contract Verification

**Static verification**: Check contract properties at design time

- Is output schema a subtype of expected input for next stage?
- Do capability grants satisfy least privilege?
- Are verification methods sufficient for stated trust bounds?

**Runtime verification**: Check contract compliance during execution

- Pre/post condition checking
- Resource usage monitoring
- Invariant enforcement

**Post-hoc verification**: Audit after execution

- Did outputs match contract?
- Were trust bounds respected?
- How did actual ETE compare to contracted max_ete?

## Trust Contract Negotiation

In dynamic systems, contracts might be negotiated:

**Agent B proposes**: "I can do this task with these trust requirements"
**Agent A evaluates**: "Is B's required trust within my budget?"
**Negotiation**: Adjust task scope, trust bounds, or verification until agreement

**Auction mechanism**: Multiple agents bid trust requirements for task

- Lowest trust bidder wins (if capable)
- Incentivizes trust minimization

**Concern**: Strategic misrepresentation—agent claims low trust requirement, then violates

**Mitigation**: Bonding, reputation stakes, verification with penalties
