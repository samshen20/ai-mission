# 04 — User Stories & Acceptance Criteria: UC-04 Multi-Region Consent Management Platform

> **Traceability Key:** Each story's metric link is shown as [M#] — see 06-traceability.md for the full mapping.

---

## US-001: Geo-Targeted Consent Banner

**As a** visitor to any Meridian digital property,
**I want** to see a consent banner tailored to my jurisdiction's legal requirements (EU opt-in, US opt-out, JP opt-in + notice),
**So that** my rights under local privacy law are respected before any non-essential data processing begins.

**Metric link:** [M-02]

### Acceptance Criteria

**AC-1 (Happy path — EU visitor):**
Given a visitor geolocates to an EU/EEA member state
When they land on any Meridian webpage, mobile app, or PWA
Then a consent banner is displayed with: (a) a clear "Accept All" button, (b) an equally prominent "Reject All" button, (c) a "Customize / Preferences" link, (d) a link to the privacy policy
And no non-essential cookies or tracking scripts load before the visitor makes a selection.

**AC-2 (Happy path — US visitor):**
Given a visitor geolocates to the United States
When they land on any Meridian digital property
Then a consent banner is displayed with: (a) a "Do Not Sell or Share My Personal Information" link, (b) a "Your Privacy Choices" notice, (c) a link to the privacy policy
And no assumption of consent is made (implied opt-out model — processing begins unless visitor opts out).

**AC-3 (Happy path — Japan visitor):**
Given a visitor geolocates to Japan
When they land on any Meridian digital property
Then a consent banner is displayed with: (a) opt-in consent for each processing purpose, (b) notice of data use purpose in Japanese language, (c) cross-border transfer notice if data will leave Japan, (d) a link to the privacy policy
And no processing occurs for purposes not explicitly consented to.

**AC-4 (Error path — geo-detection failure):**
Given the CMP cannot determine the visitor's jurisdiction (geo-IP lookup fails or returns unknown)
When the page loads
Then the banner defaults to the strictest regime (EU GDPR opt-in) as the safe default
And the incident is logged to the compliance audit trail with the visitor's IP prefix and timestamp.

**AC-5 (Non-functional — page load impact):**
Given a first-time visitor to any Meridian property
When the consent banner script loads
Then the page's Largest Contentful Paint (LCP) increases by no more than 200ms compared to the same page without the CMP
And the banner is interactive within 1.5 seconds of page load.

---

## US-002: Consent Capture, Storage & Proof

**As a** Meridian compliance operations analyst,
**I want** every consent decision to be captured with a verifiable proof record (timestamp, jurisdiction, consent state, version of banner shown),
**So that** Meridian can demonstrate compliance to a regulator on demand.

**Metric link:** [M-05]

### Acceptance Criteria

**AC-1 (Happy path — consent recorded):**
Given a visitor makes a consent choice on a Meridian property
When the choice is submitted
Then the following fields are persisted in the consent record: (a) anonymized visitor identifier, (b) ISO timestamp of decision (±1s accuracy), (c) jurisdiction code (EU/JP/US), (d) the exact consent state (all_accepted / all_rejected / custom — one per purpose), (e) version identifier of the banner shown, (f) the IP-country used for geo-detection
And the record is stored in the CMP's immutable audit log within 500ms.

**AC-2 (Error path — storage failure):**
Given a visitor submits a consent choice but the CMP audit log write fails
When the write attempt returns an error
Then the consent decision is buffered locally in the browser's localStorage
And is retried on the next page load or within 60 seconds, whichever comes first
And the failed write is escalated to the compliance monitoring dashboard within 5 minutes.

**AC-3 (Non-functional — audit log retention):**
Given any consent record is created
When the record is stored
Then the retention period is no less than the statute of limitations of the strictest applicable jurisdiction
And records are queryable by regulator without assistance from engineering.

---

## US-003: Consent Signal Propagation to Downstream Services

**As a** downstream service (loyalty, cart, personalization, analytics, ad platform),
**I want** real-time consent signals to be propagated via the API gateway,
**So that** I can honor the visitor's consent choices for data processing.

**Metric link:** [M-03]

### Acceptance Criteria

**AC-1 (Happy path — consent propagated):**
Given a visitor has made a consent decision on a Meridian property
When any downstream API call is made for that visitor's session
Then the HTTP request includes consent-preference headers: (a) `X-Consent-Marketing` (true/false), (b) `X-Consent-Analytics` (true/false), (c) `X-Consent-Personalization` (true/false), (d) `X-Consent-Jurisdiction` (EU/JP/US), (e) `X-Consent-Timestamp`
And services receiving these headers enforce consent before processing — rejected purposes return 403 with a `ConsentDenied` error body.

**AC-2 (Error path — consent expired / missing):**
Given a downstream service receives an API request with no consent headers or an expired timestamp (>24 hours old)
When the request is processed
Then the service assumes no consent has been given (default reject for marketing, analytics, personalization purposes)
And returns a 403 `ConsentRequired` response for any marketing/analytics/personalization operation
And the absence is logged with the caller identity and requested operation.

**AC-3 (Non-functional — propagation latency):**
Given a visitor changes their consent preference
When the change is submitted
Then all in-flight requests within 2 seconds receive the updated consent signal
And the propagation delay (consent change → header available at API gateway) is ≤100ms p99.

---

## US-004: Google Consent Mode v2 Integration

**As a** Meridian marketing operations lead,
**I want** the CMP to emit Google Consent Mode v2 commands (`ad_storage`, `ad_user_data`, `ad_personalization`, `analytics_storage`),
**So that** Google Ads and Google Analytics behave in compliance with EU user consent.

**Metric link:** [M-04]

### Acceptance Criteria

**AC-1 (Happy path — GCM v2 emitted):**
Given a visitor lands on a Meridian property with geolocation = EU
When the consent banner is displayed
Then the CMP sets the following default ` gtag('consent', 'default', ...)` values before any Google tag fires: `ad_storage='denied'`, `ad_user_data='denied'`, `ad_personalization='denied'`, `analytics_storage='denied'`
And when the visitor explicitly grants a purpose, the corresponding ` gtag('consent', 'update', ...)` call fires within 200ms.

**AC-2 (Error path — Google tag fires before consent):**
Given a race condition where a Google tag begins loading before `gtag('consent', 'default', ...)` has been set
When the tag execution is detected
Then the CMP console-logged a `ConsentModeError` with the tag ID
And no data is sent to Google endpoints for that session
And the event is captured in the compliance audit trail.

**AC-3 (Non-functional — Google tags blocked until consent):**
Given any Meridian page in the EU
When the page is loading
Then no Google Ads conversion linker, Google Analytics tag, or Floodlight tag fires until the consent default state is established
And this is verified by automated tag audit scanning every deployment.

---

## US-005: Global Privacy Control (GPC) Signal Processing

**As a** US-based visitor who has enabled GPC in my browser,
**I want** Meridian to recognize and honor the GPC signal as a valid opt-out request,
**So that** I don't need to interact with the consent banner to exercise my CCPA right to opt-out.

**Metric link:** [M-02]

### Acceptance Criteria

**AC-1 (Happy path — GPC honored):**
Given a visitor with geolocation = US arrives with the `Sec-GPC` header set to `1` and/or the `navigator.globalPrivacyControl` property is `true`
When the page loads
Then Meridian treats this as a valid opt-out request for the purposes of sale/sharing of personal information
And the consent banner shows a confirming state "You have opted out via your browser's privacy setting" rather than requesting any interaction
And the GPC signal is recorded in the audit log as a consent record with source="gpc".

**AC-2 (Error path — conflicting GPC + banner interaction):**
Given a visitor with GPC enabled later manually accepts all via the consent banner
When the manual choice is submitted
Then the most recent explicit choice overrides the GPC signal (consent record shows manual acceptance with original GPC signal preserved as "previously_opted_out")
And the audit trail captures both the GPC signal and the subsequent override with timestamps that demonstrate the correct sequence.

**AC-3 (Non-functional — GPC detection all browsers):**
Given any modern browser supported by Meridian (Chrome, Safari, Firefox, Edge, mobile WebView)
When the page loads
Then GPC signal is detected via both HTTP header and JavaScript API
And detection is verified in the CI pipeline via Playwright tests for each supported browser.

---

## US-006: Data Subject Access Request (DSAR) — Automated Fulfillment

**As a** data subject (customer),
**I want** to submit a DSAR via a self-service portal and receive my data within the required statutory period (≤30 days for GDPR),
**So that** I can exercise my right of access without contacting customer support.

**Metric link:** [M-01]

### Acceptance Criteria

**AC-1 (Happy path — DSAR fulfilled):**
Given a verified customer submits a DSAR via the self-service portal
When the request is received
Then an automated process identifies and collects the customer's personal data across (a) the CIAM/identity layer, (b) the commerce/cart service, (c) the loyalty engine, (d) the CMP consent audit log, (e) associated analytics profiles
And the data is compiled into a machine-readable format (JSON) and a human-readable format (PDF) within 48 hours
And both files are delivered via a secure, time-limited download link sent to the customer's verified email address.

**AC-2 (Error path — data source unavailable):**
Given a DSAR is triggered but one of the data sources returns an error or timeout
When the automated collection completes
Then the DSAR response includes the partial data set with a clear annotation listing which sources were unavailable and why
And the unavailable source is flagged in the compliance dashboard for manual follow-up within 24 hours.

**AC-3 (Non-functional — response time SLA):**
Given a DSAR is submitted
When the statutory clock starts
Then ≥80% of DSARs are fully fulfilled within 30 calendar days (GDPR requirement)
And ≥95% within 45 days
And the DPO receives a weekly DSAR aging report showing outstanding requests and time remaining.

---

## US-007: Right to Erasure / Data Deletion

**As a** data subject,
**I want** to request deletion of my personal data across all Meridian systems,
**So that** my right to erasure ("right to be forgotten") under GDPR and APPI is honored.

**Metric link:** [M-01]

### Acceptance Criteria

**AC-1 (Happy path — deletion propagated):**
Given a verified customer submits a deletion request via the DSAR portal
When the request is verified (identity confirmed + no legal hold exemption applies)
Then the deletion command is sent to all registered downstream services (CIAM, cart, loyalty, analytics, marketing automation, CMP audit log) within 1 hour
And each service confirms deletion or returns a documented exemption reason
And the customer receives a confirmation email listing each system where data was deleted and any exemptions with their legal basis.

**AC-2 (Error path — legal hold exemption):**
Given a deletion request is received but the customer has an active transaction, open return, or pending chargeback
When legal hold status is checked
Then the deletion is deferred for the specific data elements needed for the legal hold period
And the customer is notified: "We have begun deleting your data. Some records are retained under [legal basis] until [expected date]. You will receive a final confirmation on [date]."
And the hold reason, basis, and expiration are logged in the compliance audit trail.

**AC-3 (Non-functional — deletion audit trail):**
Given any data deletion event
When the deletion is executed
Then a deletion certificate is generated for each affected system (system name, data scope, deletion timestamp, operator/automation ID)
And certificates are retained for no less than 6 years for EU operations.

---

## US-008: Consent Preference Center — Granular Controls

**As a** visitor who has already made a consent choice,
**I want** to access a "Preference Center" to review and change my consent decisions at any time,
**So that** I can exercise ongoing control over my data.

**Metric link:** [M-02]

### Acceptance Criteria

**AC-1 (Happy path — preference center accessible):**
Given any visitor on any Meridian property
When they click the persistent "Cookie Preferences" or "Privacy Settings" link/icon (always visible in the page footer)
Then the preference center loads showing: (a) all consent purposes (marketing, analytics, personalization, functional), (b) current state per purpose with a toggle, (c) last-updated timestamp, (d) jurisdiction identifier
And toggles respond within 500ms and save the new state immediately upon interaction.

**AC-2 (Error path — preference center fails to load):**
Given a visitor clicks "Cookie Preferences" but the preference center JavaScript fails to load
When the error is detected
Then a static fallback is displayed with the same options using server-rendered HTML
And the error is logged to the monitoring dashboard.

**AC-3 (Non-functional — persistence of choice):**
Given a visitor makes a consent choice (via banner or preference center)
When they return to any Meridian property within 12 months
Then the previous consent choice is honored without re-prompting
Unless the privacy policy or consent purposes have materially changed (prompt shown once with "What's changed" summary).

---

## US-009: Compliance Monitoring Dashboard for Privacy Operations

**As a** Meridian DPO / privacy operations lead,
**I want** a compliance monitoring dashboard showing real-time consent metrics, DSAR pipeline status, and regulatory risk indicators,
**So that** I can demonstrate oversight and respond to incidents before they become fines.

**Metric link:** [M-05]

### Acceptance Criteria

**AC-1 (Happy path — dashboard operational):**
Given a DPO or privacy analyst logs into the compliance dashboard
When the dashboard loads
Then it displays: (a) total consent records captured (today / 7-day / 30-day), (b) consent opt-in rate by jurisdiction (EU opt-in %, US opt-out %, JP opt-in %), (c) DSAR pipeline (received / in-progress / completed / overdue), (d) compliance incidents in the last 7 days (geo-failures, propagation failures, storage failures), (e) top 3 data sources with unavailability incidents
And all metrics refresh at most every 60 seconds.

**AC-2 (Error path — data source for dashboard unavailable):**
Given the compliance dashboard attempts to pull metrics from one of the downstream services
When that service is unreachable
Then the dashboard shows the metric as "—" (unavailable) with a timestamp of the last successful data point
And an amber alert is shown: "Data source [service name] unreachable since [timestamp]. Metrics incomplete."

**AC-3 (Non-functional — dashboard access control):**
Given any user accessing the compliance dashboard
When they attempt to view the page
Then access is restricted to users with the "privacy_operations" role
And all dashboard views are audit-logged with user identity, timestamp, and filters applied.

---

## US-010: New Market Onboarding — Configure, Don't Rebuild

**As a** Meridian engineering lead,
**I want** to onboard a new country/market into the CMP by adding configuration (not writing code),
**So that** adding Meridian's 23rd country takes ≤4 weeks instead of a custom integration.

**Metric link:** [M-06]

### Acceptance Criteria

**AC-1 (Happy path — new market configured):**
Given Meridian decides to enter a new country with privacy regulation "CountryX"
When the privacy team provides the CMP configuration parameters (consent model, accepted/non-accepted purposes, banner text translations, legal notice links, data retention period, cross-border transfer rules)
Then the new market is live on the CMP with geo-detection activated within 4 weeks from configuration submission
And no code changes to the core CMP integration are required.

**AC-2 (Error path — country has an unhandled consent model):**
Given the new country's regulation requires a consent model not yet supported by the CMP (e.g., a novel "pay-for-privacy" model)
When feasibility assessment is run
Then the CMP identifies the gap with specific details: which purposes, which processing activities, which notification requirements are not covered
And the task is escalated to the product team as a feature request, not a configuration change.

**AC-3 (Non-functional — configuration-driven architecture):**
Given any new market onboarding
When the configuration is deployed
Then 100% of the market-specific behavior is driven by the configuration payload (no conditional code branches by country)
And this is verified by a CI check that fails any pull request containing a country-specific `if`/`switch` statement.

---

## Story Summary

| ID | Title | Error-Path AC | NFR | Metric Link |
|----|-------|---------------|-----|-------------|
| US-001 | Geo-Targeted Consent Banner | AC-4 (geo-detection failure → strictest default) | AC-5 (LCP +200ms max, interactive ≤1.5s) | [M-02] |
| US-002 | Consent Capture, Storage & Proof | AC-2 (storage failure → local fallback + retry) | AC-3 (retention ≥statute of limitations in strictest jurisdiction) | [M-05] |
| US-003 | Consent Signal Propagation | AC-2 (missing/expired consent → 403 + default reject) | AC-3 (propagation ≤100ms p99; in-flight update ≤2s) | [M-03] |
| US-004 | Google Consent Mode v2 | AC-2 (race: tag fires before consent default) | AC-3 (no Google tags fire until default state) | [M-04] |
| US-005 | GPC Signal Processing | AC-2 (GPC → manual override sequence) | AC-3 (GPC detection in all supported browsers, CI-tested) | [M-02] |
| US-006 | DSAR Automated Fulfillment | AC-2 (data source unavailable → partial response + 24h flag) | AC-3 (≥80% within 30 days, ≥95% within 45 days) | [M-01] |
| US-007 | Right to Erasure | AC-2 (legal hold exemption → deferred + notification) | AC-3 (deletion certificate retained ≥6 years) | [M-01] |
| US-008 | Preference Center | AC-2 (JS fails → server-rendered fallback) | AC-3 (choice persists 12 months unless material change) | [M-02] |
| US-009 | Compliance Dashboard | AC-2 (data source unavailable → amber alert) | AC-3 (role-based access + audit logging) | [M-05] |
| US-010 | New Market Onboarding | AC-2 (unhandled model → escalate as feature request) | AC-3 (100% config-driven; CI blocks country-specific code branches) | [M-06] |
