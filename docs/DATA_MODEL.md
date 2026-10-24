# Proposed E-commerce Data Model

**Status:** conceptual model only; not an existing database schema or migration.

## 1. Core entities

| Entity | Key fields (proposed) | Notes |
|---|---|---|
| User | id, email/phone identifier, status, createdAt | Store only necessary identity/contact data; exact sign-in model TBD |
| Role/Grant | subjectId, role, scopeId | Must be enforced server-side; supports tenant scope only if marketplace approved |
| Address | id, ownerId, recipient, delivery fields | Minimize retention; use a validated address model appropriate to the target market |
| Product | id, slug, title, description, status, categoryId | Draft/published/archived lifecycle |
| ProductVariant | id, productId, sku, option values, price, currency | Price and currency validated server-side |
| ProductMedia | id, productId, storageKey, altText, order | Store controlled media references, not untrusted arbitrary file paths |
| Inventory | variantId, availableQty, reservedQty, updatedAt | Concurrency control required |
| Cart | id, customerId or secure guest token, updatedAt | Never authoritative for final commercial total |
| CartLine | cartId, variantId, quantity | Price should be re-read at checkout |
| Order | id, customerId, status, currency, itemSubtotal, discountTotal, shippingTotal, taxTotal, grandTotal, createdAt | Monetary totals stored as integer minor units or exact decimal according to currency rules |
| OrderLine | orderId, product/variant snapshots, quantity, unitPrice, lineTotal | Purchase-time immutable snapshots |
| PaymentAttempt | id, orderId, provider, providerReference, amount, currency, status | No raw card details or secret tokens |
| PaymentEvent | providerEventId, paymentAttemptId, eventType, receivedAt, verification status | Unique provider event ID prevents duplicate processing |
| Fulfillment | id, orderId, carrier/reference, status, dispatchedAt, deliveredAt | Provider integration TBD |
| Refund/Return | id, orderId, amount, reasonCode, status | Authorized transitions and audit trail required |
| AuditEvent | id, actorId, action, resourceType, resourceId, timestamp, safeMetadata | Exclude secrets and unnecessary personal content |

## 2. Money and inventory

- Never use binary floating-point as the sole representation for order totals.
- Choose a currency-aware monetary representation and rounding rule with the accounting/payment provider.
- Store currency alongside each commercial amount.
- Recalculate discounts and delivery fees server-side; store the resulting order snapshot.
- Define behavior for simultaneous checkouts, stock reservation timeouts, cancelled payments, and failed delivery.
- Prevent negative stock unless the merchant explicitly chooses an approved back-order model.

## 3. Order state model

A preliminary state model could be:

```text
PENDING_CONFIRMATION
    ├──► CONFIRMED
    ├──► CANCELLED
    └──► EXPIRED

CONFIRMED ─► PROCESSING ─► FULFILLING ─► COMPLETED
     │             │            │
     └─────────────┴────────────┴──► CANCELLATION/RETURN REVIEW
```

This diagram is intentionally incomplete: the final transitions depend on payment method, COD support, shipping provider, cancellation cutoff, and return/refund policy. Define allowed transitions and actor permissions before code is written. Do not collapse payment state and fulfillment state into a single status field.

## 4. Payment state model

Suggested states include `NOT_REQUIRED`, `PENDING`, `AUTHORIZED`, `PAID`, `FAILED`, `CANCELLED`, `REFUND_PENDING`, `PARTIALLY_REFUNDED`, and `REFUNDED`, depending on the selected provider and payment methods.

Only verified provider results or explicitly documented authorized manual flows may change financial status. Browser redirects are not authoritative evidence of payment.

## 5. Deletion and retention

Define retention separately for customer profiles, addresses, orders/invoices, payment references, provider event records, support records, and audit logs. Some transaction records may require retention for accounting or dispute obligations; that must be determined from the applicable law and advice, not guessed by application code. Remove or anonymize personal fields where legally and operationally appropriate without breaking required record integrity.

## 6. Migration policy

- Version all schema migrations.
- Apply migrations in a reviewed, repeatable process.
- Test migration and rollback/recovery on representative data.
- Do not edit production data manually without an auditable runbook.
- Treat state-machine changes as backward-compatibility and operational changes, not just enum edits.
