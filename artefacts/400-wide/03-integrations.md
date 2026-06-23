# 03-integrations.md — POS Cart Lookup Contract

**Integration:** POS Client → Apollo GraphQL Gateway
**Operation:** Look up a customer's active online cart at the POS by scanning
their loyalty QR code
**Date:** 2026-06-22
**Status:** Phase 1 contract — pilot country

---

## API Style

**GraphQL mutation** over HTTPS. The Apollo Gateway federates the request
across Identity, Cart, and Inventory Read Cache services. The POS Client sees
a single endpoint; the Gateway handles composition, error aggregation, and
partial-failure semantics.

## Named Resource

```
POST https://api.meridian.com/graphql
```

| Attribute | Value |
|-----------|-------|
| **HTTP verb** | `POST` |
| **Resource** | `/graphql` (single GraphQL endpoint — no REST resource-per-entity) |
| **Content-Type** | `application/json` |
| **Mutation** | `lookupCustomerCart` |

## Auth

| Attribute | Value |
|-----------|-------|
| **Method** | Bearer token — associate session JWT issued by Auth0 at POS login |
| **Header** | `Authorization: Bearer <associate-session-token>` |
| **Token claims required** | `sub` (associate ID), `store_id` (assigned store), `permissions: ["pos:cart:read"]` |
| **Token validation** | Gateway validates token signature + expiry, then calls Identity Service `validateAssociateSession` to confirm the session is still active and the associate is assigned to the store in the request |
| **Expiry** | Token expires 8 hours after POS login (one shift). Refresh via POS re-login, not silent refresh |

## Request Payload

```graphql
mutation LookupCustomerCart($input: LookupCustomerCartInput!) {
  lookupCustomerCart(input: $input) {
    customer {
      customerId
      givenName
      loyaltyTier
      loyaltyQrCode
    }
    cart {
      cartId
      state
      lastUpdatedAt
      items {
        sku
        name
        imageUrl
        requestedQty
        unitPrice {
          amount
          currency
        }
        availability {
          status
          qtyOnShelf
          sellThroughToday
          freshness
          source
        }
      }
      itemCount
      total {
        amount
        currency
      }
    }
    alternatives {
      sku
      storeName
      storeId
      qtyOnShelf
      distanceKm
    }
  }
}
```

### Variables

```json
{
  "input": {
    "qrCode": "MRD-LOY-8421-A3F9",
    "storeId": "high-st-01"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `qrCode` | `String!` | Yes | Loyalty QR payload scanned at POS. Format: `MRD-LOY-<customerId>-<checksum>`. |
| `storeId` | `String!` | Yes | Store identifier where the associate is currently signed in. Must match the `store_id` claim in the associate's session token. |

## Response Payload (Happy Path)

```json
{
  "data": {
    "lookupCustomerCart": {
      "customer": {
        "customerId": "cust-8421",
        "givenName": "Alex",
        "loyaltyTier": "gold",
        "loyaltyQrCode": "MRD-LOY-8421-A3F9"
      },
      "cart": {
        "cartId": "cart-9f3a",
        "state": "active",
        "lastUpdatedAt": "2026-06-22T10:29:00Z",
        "items": [
          {
            "sku": "LMP-100",
            "name": "Smart Lamp E27",
            "imageUrl": "https://cdn.meridian.com/pim/LMP-100/hero-2x.jpg",
            "requestedQty": 1,
            "unitPrice": { "amount": "49.00", "currency": "EUR" },
            "availability": {
              "status": "available",
              "qtyOnShelf": 4,
              "sellThroughToday": 8,
              "freshness": "checked-12-min-ago",
              "source": "inventory-cache"
            }
          },
          {
            "sku": "TRL-X9-42",
            "name": "Trail Runner X9 — Men's 42",
            "imageUrl": "https://cdn.meridian.com/pim/TRL-X9-42/hero-2x.jpg",
            "requestedQty": 1,
            "unitPrice": { "amount": "149.00", "currency": "EUR" },
            "availability": {
              "status": "available-sap-confirmed",
              "qtyOnShelf": 2,
              "sellThroughToday": null,
              "freshness": "sap-physical-count-0915-utc",
              "source": "sap-ecc-realtime"
            }
          },
          {
            "sku": "LMP-200",
            "name": "Smart Lamp E14",
            "imageUrl": "https://cdn.meridian.com/pim/LMP-200/hero-2x.jpg",
            "requestedQty": 2,
            "unitPrice": { "amount": "34.00", "currency": "EUR" },
            "availability": {
              "status": "available",
              "qtyOnShelf": 2,
              "sellThroughToday": 5,
              "freshness": "checked-8-min-ago",
              "source": "inventory-cache"
            }
          }
        ],
        "itemCount": 3,
        "total": { "amount": "232.00", "currency": "EUR" }
      },
      "alternatives": []
    }
  }
}
```

### Availability status values

| `status` | `source` | Meaning | POS treatment |
|----------|----------|---------|---------------|
| `available` | `inventory-cache` | Stock confirmed from Inventory Read Cache (batch SAP data, ≤30 min old) | Green ✓ — show quantity + freshness |
| `available-sap-confirmed` | `sap-ecc-realtime` | Stock confirmed via real-time SAP ECC fallback after cache miss (+400ms penalty) | Amber ⚠ — show quantity + "SAP-confirmed" label |
| `unavailable` | `inventory-cache` | No stock record in cache; SAP fallback not attempted or not configured | Red ✗ — "Not available at this store" |
| `unavailable-sap-confirmed` | `sap-ecc-realtime` | Cache miss → SAP fallback → SAP confirms no stock at this location | Red ✗ — "Confirmed unavailable — source-of-truth has no record" |
| `stale` | `inventory-cache` | Stock data exists in cache but `lastSync` exceeds staleness threshold (>30 min) | Amber — quantity hidden, "Availability uncertain" + "Call store" CTA |

---

## Error-Code Mapping

All errors follow the GraphQL `errors` array convention. The Gateway returns
HTTP 200 even on application errors; partial failures (one item unavailable)
are NOT errors — they use the `availability.status` field on the item.

### Error 1: Unknown loyalty QR code

**Condition:** The scanned QR code does not resolve to a known customer in
Identity Service.

```json
{
  "errors": [
    {
      "message": "Loyalty QR code does not match any registered customer.",
      "extensions": {
        "code": "LOYALTY_QR_UNKNOWN",
        "qrCode": "MRD-LOY-9999-X1Y2",
        "httpStatus": 404
      }
    }
  ],
  "data": { "lookupCustomerCart": null }
}
```

| Field | Value |
|-------|-------|
| **Error code** | `LOYALTY_QR_UNKNOWN` |
| **HTTP status** | 200 (GraphQL layer); `extensions.httpStatus` signals 404 to the POS Client |
| **POS behaviour** | Display "Customer not found — check the QR code or look up by name/email." Do NOT retry automatically (QR may be damaged or from another retailer's loyalty program). |
| **Retry?** | No — manual intervention required. Associate should offer name/email lookup as fallback. |

### Error 2: Cart not found

**Condition:** The customer is known but has no active online cart (never added
items, or cart expired/abandoned >30 days).

```json
{
  "errors": [
    {
      "message": "Customer cust-8421 has no active cart.",
      "extensions": {
        "code": "CART_NOT_FOUND",
        "customerId": "cust-8421",
        "httpStatus": 404,
        "suggestion": "create-pos-cart"
      }
    }
  ],
  "data": {
    "lookupCustomerCart": {
      "customer": {
        "customerId": "cust-8421",
        "givenName": "Alex",
        "loyaltyTier": "gold",
        "loyaltyQrCode": "MRD-LOY-8421-A3F9"
      },
      "cart": null,
      "alternatives": []
    }
  }
}
```

| Field | Value |
|-------|-------|
| **Error code** | `CART_NOT_FOUND` |
| **HTTP status** | 200; `extensions.httpStatus` signals 404 |
| **POS behaviour** | Display "Alex has no active online cart. Start a new in-store order?" Offer a single-tap "New POS cart" action that creates a cart anchored to the associate's store. |
| **Retry?** | No — cart creation is the recovery path. The `suggestion: "create-pos-cart"` field tells the POS Client which recovery action to surface. |
| **Partial data** | The `customer` object is still returned (identity resolved successfully) — the POS can greet the customer by name even when the cart is empty. |

### Error 3: Inventory-cache miss with SAP fallback failure

**Condition:** One or more cart items have no stock record in the Inventory Read
Cache AND the real-time SAP ECC fallback also fails (SAP timeout, connection
refused, or SAP returns an error). This is NOT a GraphQL error — the mutation
succeeds with partial availability data. The item is marked with an
`availability` status that signals the double-failure to the POS.

```json
{
  "data": {
    "lookupCustomerCart": {
      "customer": { "customerId": "cust-8421", "givenName": "Alex", "loyaltyTier": "gold" },
      "cart": {
        "cartId": "cart-9f3a",
        "state": "active",
        "items": [
          {
            "sku": "TRL-X9-42",
            "name": "Trail Runner X9 — Men's 42",
            "availability": {
              "status": "unknown",
              "qtyOnShelf": null,
              "sellThroughToday": null,
              "freshness": null,
              "source": null,
              "failureReason": "inventory-cache-miss-and-sap-unreachable"
            }
          }
        ]
      },
      "alternatives": []
    }
  },
  "extensions": {
    "warnings": [
      {
        "message": "Inventory cache miss for SKU TRL-X9-42 at store high-st-01. SAP ECC fallback timed out after 400ms. Availability could not be determined.",
        "code": "AVAILABILITY_UNKNOWN",
        "sku": "TRL-X9-42",
        "storeId": "high-st-01"
      }
    ]
  }
}
```

| Field | Value |
|-------|-------|
| **Warning code** | `AVAILABILITY_UNKNOWN` |
| **Availability status** | `"unknown"` |
| **POS behaviour** | Display "⚠ Can't check stock right now — ask a manager or call the store." Grey out the "reserve" action for this item. Do NOT block the rest of the cart — other items with valid availability remain actionable. |
| **Retry?** | Manual retry only — the associate can tap "Retry stock check" which re-invokes `lookupCustomerCart` for the single SKU. Automatic retry would compound the SAP timeout. |
| **Monitoring** | The Gateway emits a `AvailabilityLookupFailed` metric with tags `sku`, `storeId`, `failureReason`. A >5% failure rate on this metric triggers a P2 incident (SAP ECC or Inventory Cache degraded). |

### Error 4: Unauthorized associate session

**Condition:** The associate's session token is expired, revoked, or lacks the
`pos:cart:read` permission.

```json
{
  "errors": [
    {
      "message": "Associate session is not authorized for this operation.",
      "extensions": {
        "code": "UNAUTHORIZED",
        "httpStatus": 401,
        "detail": "token-expired"
      }
    }
  ],
  "data": { "lookupCustomerCart": null }
}
```

| Field | Value |
|-------|-------|
| **Error code** | `UNAUTHORIZED` |
| **HTTP status** | 200; `extensions.httpStatus` signals 401 |
| **POS behaviour** | Redirect to POS login screen. Do NOT show partial data. |
| **Retry?** | Yes — after re-authentication. |

---

## Webhook Idempotency (Stripe → Checkout Service)

The Checkout Service webhook handler for Stripe events SHALL enforce
idempotency on `stripe_event_id`. Before processing any Stripe webhook, the
handler SHALL check the `processed_stripe_events` table in Order Database for
the `stripe_event_id`. If the event ID exists, the handler SHALL return HTTP
200 without processing the event. If the event ID does not exist, the handler
SHALL insert it in the same transaction as the event processing — a duplicate
delivery after the insert commits will find the ID and no-op.

| Attribute | Value |
|-----------|-------|
| **Idempotency key** | `stripe_event_id` from the webhook payload (e.g., `evt_1AbCdEfGhIjKlMn`) |
| **Idempotency store** | `processed_stripe_events` table in Order Database (PostgreSQL) |
| **Retention** | 30 days — Stripe does not redeliver webhooks older than 3 days |
| **Duplicate behavior** | Return HTTP 200, log at DEBUG level, emit `StripeWebhookDuplicate` metric |
| **CI contract test** | Replay an identical webhook payload; assert second processing is a no-op (no state change in Order Database, no SendGrid dispatch) |

---

## p95 Latency Budget

| Scenario | p95 | Dominant cost |
|----------|-----|---------------|
| All items in cache | ≤ 250ms | Store WiFi + TLS (2×80ms) |
| 1 item cache miss → SAP fallback | ≤ 650ms | SAP IDoc sync (+400ms) |
| 3 items all cache miss → 3× SAP | ≤ 1,450ms | 3 sequential SAP calls |

The POS Client SHALL set a socket timeout of 2,000ms. Requests exceeding
this timeout SHALL be surfaced as `AVAILABILITY_UNKNOWN` for all items and the
associate SHALL be offered a manual retry.

---

## Contract Governance

| Attribute | Value |
|-----------|-------|
| **Schema registry** | Apollo GraphOS — `lookupCustomerCart` mutation, schema version `v1` |
| **Breaking change policy** | Removing a field or changing a field type = major version bump. Adding a nullable field = minor. Adding an `availability.status` enum value = minor (POS Clients must treat unknown enum values as `"unknown"`). |
| **Deprecation** | Fields deprecated with `@deprecated(reason:)` for one minor version before removal. |
| **Owner** | Cart Service team owns the `lookupCustomerCart` resolver composition. Identity Service owns `customer` sub-resolver. |
| **SLA** | 99.9% availability during store operating hours (06:00–22:00 local). p95 latency targets measured per-scenario above. |
