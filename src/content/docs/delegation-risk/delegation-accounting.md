---
title: "Delegation Accounting: A Balance Sheet View"
sidebar:
  order: 2
---

# Delegation Accounting: A Balance Sheet View

:::note[TL;DR]
**Net Delegation Value = Receivable - Exposure - Costs**. What you expect to get, minus what could go wrong, minus what it costs.
:::

---

## The Setup

**Alice** has a gem worth $1,000. A buyer will pay on delivery. Alice can't deliver it herself, so she hires **Bob** for a **$50 fee**.

| Item | Type | Value |
|------|------|-------|
| Buyer's payment | Receivable | $1,000 |
| Bob's fee | Cost | $50 |

**Naive calculation**: $1,000 - $50 = $950.

But this ignores what could go wrong.

---

## Exposures

An **exposure** is a potential cost. Unlike Bob's $50 fee (certain), exposures are probability-weighted.

| Exposure | What happens | Probability | Damage | Expected Loss |
|----------|--------------|-------------|--------|---------------|
| **Loss** | Bob loses the gem | 2% | $1,000 | $20 |
| **Theft** | Bob steals the gem | 1% | $1,000 | $10 |
| **Total Expected Loss** | | | | **$30** |

---

## The Balance Sheet

| | Value |
|---|------|
| **Receivable** | $1,000 |
| **Cost** (Bob's fee) | -$50 |
| **Exposure** (expected) | -$30 |
| **Net Delegation Value** | **$920** |

This is Alice's expected profit after accounting for what could go wrong.

---

## Bob's Perspective

What does this look like from Bob's side? When Bob accepts the gem, he has two **options**. Each is its own balance sheet.

**Option A: Attempt Delivery**

| | Value |
|---|------|
| **Receivable** (fee if successful) | $50 |
| **Exposure** (2% loss, $1,000 penalty) | -$20 |
| **Net Value** | **$30** |

**Option B: Steal**

| | Value |
|---|------|
| **Receivable** (gem) | $1,000 |
| **Contingent Liability** (80% caught, $2,000 penalty) | -$1,600 |
| **Net Value** | **-$600** |

Bob chooses **Attempt Delivery** because $30 > -$600.

:::note[Exposure vs. Contingent Liability]
**Exposure** = accidental risk (Option A). Something might happen *to* Bob.
**Contingent Liability** = consequence of choice (Option B). Bob deliberately takes on this risk, and the penalty only materializes if he's caught.

Stealing has negative value because the contingent liability (-$1,600) outweighs the asset ($1,000).
:::

---

## Delegation Chains

Now Alice is running a large operation. She doesn't deal with couriers directly—she has **Xavier**, a manager.

Alice tasks Xavier with getting the gem delivered. Xavier then hires Bob.

### Three Balance Sheets

When the gem changes hands, **all three parties** take on exposure simultaneously.

**Alice's Balance Sheet**

| | Value |
|---|------|
| **Receivable** | $1,000 |
| **Cost** (Xavier's fee) | -$100 |
| **Exposure** (Xavier fails or steals) | -$33 |
| **Net Delegation Value** | **$867** |

Alice's exposure is now to *Xavier*, not Bob. She doesn't know or care who Xavier uses.

**Xavier's Balance Sheet**

| | Value |
|---|------|
| **Receivable** (fee from Alice) | $100 |
| **Cost** (Bob's fee) | -$50 |
| **Exposure** (Bob fails → Xavier owes Alice) | -$30 |
| **Net Value** | **$20** |

Xavier earns $50 margin but takes on $30 expected exposure. If Bob loses the gem, Xavier is responsible to Alice.

**Bob's Balance Sheet**

| | Value |
|---|------|
| **Receivable** (fee if successful) | $50 |
| **Exposure** (2% loss, $1,000 penalty) | -$20 |
| **Net Value** | **$30** |

Bob's balance sheet is unchanged—he doesn't know or care that Xavier has a boss.

### The Key Insight

When Xavier accepts the delegation, he **takes on personal exposure** for Bob's potential failures. The exposure doesn't disappear—it transfers from Alice to Xavier.

| Party | Exposed To | Expected Exposure |
|-------|-----------|-------------------|
| Alice | Xavier | $33 |
| Xavier | Bob | $30 |
| Bob | Accidents | $20 |

:::note[Exposure Flows Downward]
Each delegator is exposed to their immediate delegate, not the full chain. Alice trusts Xavier. Xavier trusts Bob. The chain of trust creates a chain of exposure.
:::

---

## Insurance

Alice can **externalize** her exposure by buying insurance from **Carol**.

Carol charges a **$40 premium** (the $30 expected exposure + margin). If Bob fails, Carol pays Alice.

| | Without Insurance | With Insurance |
|---|------------------|----------------|
| Receivable | $1,000 | $1,000 |
| Costs | $50 | $90 |
| Exposure | $30 | $0 |
| **NDV** | **$920** | **$910** |
| Worst case | Lose $1,000 | Lose $90 |

:::note[The Trade-off]
Insurance costs $10 in expected value. But it eliminates the worst case. Alice trades expected value for certainty.
:::

---

## Summary

```
Net Delegation Value = Receivable - Exposure - Costs
                     = $1,000 - $30 - $50
                     = $920
```

| Term | Meaning |
|------|---------|
| **Receivable** | What you expect to get |
| **Cost** | Certain expenses |
| **Exposure** | Potential losses (probability × damage) |
| **NDV** | Expected profit after accounting for risk |
