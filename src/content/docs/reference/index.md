---
title: "Technical Reference"
sidebar:
  order: 0
---

# Technical Reference

:::note[Reference Documentation]
Technical specifications and catalogs for the delegation risk framework. These documents provide precise definitions, formulas, and implementation details.
:::

---

## Documents

### [Protocol Catalog](./protocol-catalog/)

Complete catalog of containment protocols with:
- Exposure multipliers (empirically calibrated)
- Implementation requirements
- Verification methods
- Protocol combinations

### [Insurance Bot Specification](./insurance-bot-spec/)

Technical specification for the automated pricing engine:
- Calculation pipeline
- Database schemas
- API specification
- Calibration process
- Failure modes

---

## Quick Reference

**Exposure Formula:**
```
FinalExposure = BaseExposure × Π(protocol_multipliers) × TrackRecordModifier
```

**Risk-Adjusted Cost:**
```
RiskAdjustedCost = Price + (ExposureScore × PrincipalRiskPremium)
```

---

## Related

- [Delegation Accounting](/framework/delegation-accounting/) — Core framework
- [The Anomaly Chronicles](/case-studies/anomaly-chronicles/) — System in practice
