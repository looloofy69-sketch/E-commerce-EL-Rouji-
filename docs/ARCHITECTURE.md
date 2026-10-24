# Proposed E-commerce Architecture

**Status:** design proposal; no implementation or deployment is claimed.

## 1. Logical components

```text
Customer storefront / Merchant admin
                 |
                 v
        Commerce API / BFF
                 |
     +-----------+-----------+----------------+
     |           |           |                |
     v           v           v                v
 Catalog      Cart/Order   Identity/RBAC   Admin/Audit
 service      service        boundary       records
                  |
          +-------+--------+
          |                |
          v                v
     Payment adapter   Fulfillment adapter
          |                |
          v                v
    Payment provider   Carrier/merchant process
          |
          v
  Verified webhook handler
          |
          v
 Order/payment state transition
```

This is a logical proposal only. The technology stack, deployment platform, database, and provider integrations are not yet selected.

## 2. Architectural principles

### Source of truth
- Catalog and inventory are server-owned.
- The browser's cart is a convenience state; the server must recalculate all commercial totals.
- The order stores immutable snapshots of SKU, title, variant, quantity, unit price, discount allocation, and currency accepted at checkout.
- Payment provider status and commerce order status are distinct state machines.
- Delivery state is tracked separately from payment state.

### Security boundaries
- All customer-owned resources are scoped to the authenticated customer or a secure guest-order credential.
- Merchant/admin operations require explicit role and tenant scope.
- Payment secrets remain server-side.
- Webhook signatures and event identifiers must be verified before processing.
- Do not trust client-supplied price, discount eligibility, shipping fee, payment status, role, or owner ID.

### Reliability
- Use idempotency keys for checkout and any operation that can create financial or fulfillment side effects.
- Persist webhook event IDs to reject duplicate processing.
- Use an outbox/queue or another reliable mechanism for side effects that occur after a transaction, if the chosen stack supports it.
- Retry only recoverable errors with bounded backoff.
- Record failed integration attempts without exposing secrets or private payloads.

## 3. Suggested module boundaries

- `catalog`: products, categories, variants, media references, publication.
- `inventory`: stock on hand, reservations, adjustments, low-stock controls.
- `cart`: selected items and quantities; never authoritative for final price.
- `checkout`: address/fulfillment choice, server-side validation, order creation.
- `orders`: order lifecycle, customer-visible status, cancellation and returns.
- `payments`: provider-neutral payment intent/reference, webhooks, reconciliation.
- `fulfillment`: shipping quote, dispatch, tracking, delivery/failed-delivery events.
- `identity`: authentication, sessions, role and tenant boundaries.
- `admin`: restricted catalog/order operations and audit trail.
- `notifications`: transactional email/SMS/other channels after provider and consent decisions.
- `analytics`: minimized operational metrics without unnecessary personal content.

These modules can initially live in a modular monolith. Do not introduce microservices until measured scale or team boundaries justify the added operational complexity.

## 4. Proposed technology selection process

No stack is prescribed by this document. Before implementation, choose and document:
- Frontend framework and accessibility strategy.
- Backend runtime/API framework.
- Transactional database and migration approach.
- Image storage/CDN and media moderation process.
- Payment and delivery providers actually available to the merchant.
- Queue/worker/notification service, if asynchronous workflows are required.
- Secret manager, logs/metrics, monitoring, backups, and deployment environments.

Selection criteria should include provider eligibility, data-location requirements, costs, reliability, developer skill, support, exit/migration paths, and testability.

## 5. Suggested transactional boundaries

Order creation should atomically validate cart lines, calculate totals, reserve/decrement available stock according to a documented strategy, and persist order snapshots. If stock reservation and order persistence span systems, document reconciliation and compensation behavior.

A payment callback should not directly mutate arbitrary order fields. It should:
1. Verify authenticity and provider/event identity.
2. Reject or safely ignore duplicates.
3. Match the provider reference to a known order/payment attempt.
4. Validate the expected amount and currency.
5. Apply only an allowed state transition.
6. Persist an audit event and trigger downstream actions idempotently.

## 6. Relationship to EL-Rouji

EL-Rouji may later supply optional AI-assisted product description drafts, catalog summarization, or analytics explanations. These are optional integrations, not a dependency of checkout. The commerce platform must remain functional if an AI provider is unavailable. AI output must not set price, stock, tax, payment status, or legal policy.

## 7. Open architecture decisions

- Single merchant or multi-vendor marketplace?
- Hosted storefront or self-hosted deployment?
- Database and transaction model?
- Supported payment methods and eligible provider?
- Shipping calculation/tracking integration?
- Customer account vs guest checkout?
- Product variants, downloadable items, or services?
- Localization, currency, taxes, and invoice requirements?
- Required availability, support, recovery, and performance targets?
