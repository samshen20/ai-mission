# 06 — Traceability Matrix: UC-04 Stories → Outcome Metrics

## Metrics Reference

| ID | Metric | Window | Threshold | Source |
|----|--------|--------|-----------|--------|
| [M-01] | DSAR response time compliance | Rolling quarter | ≥80% fulfilled within 30 calendar days | GDPR Art. 12(3) / 04-canvas.md §3 |
| [M-02] | Consent jurisdiction accuracy | Per deployment | Banner matches visitor's jurisdiction ≥99% of the time | 04-canvas.md §3 (regulatory compliance) |
| [M-03] | Consent signal propagation reliability | Per session | <0.1% of downstream requests receive stale or missing consent headers (p99 ≤100ms propagation) | 04-canvas.md §3 (technical SLA) |
| [M-04] | Google Consent Mode v2 emission correctness | Per tag audit | Zero GCM v2 violations in automated tag audit (ad_storage, ad_user_data, ad_personalization, analytics_storage) | Google Consent Mode v2 spec / 04-canvas.md §9 |
| [M-05] | Compliance audit log completeness | Per regulatory audit | 100% of consent decisions have a verifiable proof record within regulatory retention period | 04-canvas.md §3 / GDPR Art. 7(1) |
| [M-06] | New market integration time | Per new market | ≤4 weeks from configuration submission to go-live | 04-canvas.md §3 |

---

## Story ↔ Metric Mapping

| Story ID | Story Title | Primary Metric | Secondary Metric | Verification Method |
|----------|-------------|----------------|------------------|---------------------|
| US-001 | Geo-Targeted Consent Banner | [M-02] — Jurisdiction accuracy ≥99% | — | Automated geo-test suite (Staging EU/JP/US IP proxies) + Playwright assertion per deployment |
| US-002 | Consent Capture, Storage & Proof | [M-05] — Audit log completeness 100% | — | Database audit query: COUNT(decisions without proof record) / COUNT(total decisions) = 0 |
| US-003 | Consent Signal Propagation | [M-03] — Propagation ≤100ms p99, stale headers <0.1% | [M-02] — Jurisdiction accuracy | API gateway observability (Datadog/New Relic): p99 propagation latency; header-mismatch alert |
| US-004 | Google Consent Mode v2 | [M-04] — Zero GCM v2 violations | [M-03] — Propagation reliability | Automated tag audit (ObservePoint / custom Puppeteer): fires `gtag('consent','default',...)` before any Google tag |
| US-005 | GPC Signal Processing | [M-02] — Jurisdiction accuracy | [M-05] — Audit log completeness | GPC simulator test: Sec-GPC header → confirmed opt-out state + audit record with source="gpc" |
| US-006 | DSAR Automated Fulfillment | [M-01] — ≥80% within 30 days | [M-05] — Audit log completeness | Quarterly DSAR aging report: count(fulfilled ≤30 days) / count(total) ≥0.80 |
| US-007 | Right to Erasure | [M-01] — DSAR response time compliance | [M-05] — Audit log completeness | Deletion certificate audit: every deletion event has ≥1 cert per affected system |
| US-008 | Preference Center | [M-02] — Jurisdiction accuracy | [M-03] — Propagation reliability | Preference change → confirm API header updated within 100ms (Playwright assertion) |
| US-009 | Compliance Dashboard | [M-05] — Audit log completeness | [M-01] — DSAR compliance | Dashboard metric value vs. raw database query: difference = 0 |
| US-010 | New Market Onboarding | [M-06] — ≤4 weeks configuration | [M-02] — Jurisdiction accuracy | Calendar days from config submission to geo-detection go-live |

---

## Metric ↔ Story Mapping (Reverse Lookup)

| Metric | Target | Stories That Drive It | Total Stories |
|--------|--------|---------------------|---------------|
| [M-01] DSAR compliance (≥80% ≤30d) | ≥80% | US-006, US-007 | 2 |
| [M-02] Consent jurisdiction accuracy (≥99%) | ≥99% | US-001, US-005, US-008, US-010 | 4 |
| [M-03] Consent signal propagation (<0.1% stale, ≤100ms p99) | <0.1% stale / ≤100ms | US-003, US-008 | 2 |
| [M-04] GCM v2 correctness (zero violations) | Zero violations | US-004 | 1 |
| [M-05] Audit log completeness (100%) | 100% | US-002, US-005, US-006, US-007, US-009 | 5 |
| [M-06] New market integration (≤4 weeks) | ≤4 weeks | US-010 | 1 |

---

## Coverage Summary

| Measure | Count |
|---------|-------|
| Total stories | 10 |
| Stories with error-path AC | 10/10 (100%) |
| Stories with non-functional AC | 10/10 (100%) |
| Stories tracing to ≥1 metric | 10/10 (100%) |
| Unique outcome metrics | 6 |
| Metrics with ≥1 story linked | 6/6 (100%) |
| In-scope stories | 10 |
| Out-of-scope items listed (06-prd.md) | 5 |
