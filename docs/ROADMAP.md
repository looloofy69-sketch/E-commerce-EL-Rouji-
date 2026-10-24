# Roadmap and Delivery Gates

This roadmap is a proposed sequence, not a promise of delivery dates or evidence that features are implemented.

## Phase 0 — Product decisions
- Choose single-merchant storefront versus marketplace.
- Confirm market, languages, currency, product types, customer identity, and guest checkout.
- Validate payment/shipping provider eligibility and commercial terms.
- Define price, discount, tax, invoice, return, cancellation, and refund policies.
- Decide data retention, privacy obligations, support, and operational ownership.
- Approve a written MVP and acceptance criteria.

**Exit gate:** no unresolved business-model decision that would invalidate the data model, tenant model, or payment architecture.

## Phase 1 — Engineering foundation
- Select stack and deployment platform.
- Establish repository structure, environments, CI, secret handling, and database migration workflow.
- Define auth/RBAC and tenant model.
- Implement product, variant, media, category, and inventory primitives.
- Add schema validation, logs, unit/contract-test framework, and API error conventions.

**Exit gate:** source builds reproducibly, access boundaries are tested, and no payment secrets or customer data are committed.

## Phase 2 — Catalog and cart
- Build responsive catalog and product detail.
- Implement search/filter/pagination.
- Add cart operations and server-side price/stock recalculation.
- Build merchant product and inventory management with audit history.

**Exit gate:** published catalog, unavailable products, price changes, and concurrent stock changes behave correctly in automated tests.

## Phase 3 — Checkout and orders
- Create idempotent checkout and immutable order snapshots.
- Implement the agreed payment method/provider adapter.
- Verify webhooks, duplicate events, amount/currency matching, and reconciliation.
- Implement order history, authorized order detail, cancellation/refund/return policy workflows.
- Implement shipping/fulfillment integration or a documented manual process.

**Exit gate:** end-to-end test order and failure/recovery scenarios pass in the provider's test environment.

## Phase 4 — Production hardening
- Complete security and privacy review.
- Test accessibility, mobile, language, and localization behavior.
- Test data backups/restoration and deployment rollback.
- Configure monitoring, alerts, support process, and reconciliation jobs.
- Perform realistic load and failure testing.
- Resolve or formally risk-accept dependency/security findings.

**Exit gate:** accountable release owner approves the release checklist with evidence.

## Phase 5 — Optional enhancements
Only after the core commerce path is stable:
- Customer loyalty or wishlists.
- Recommendations and product discovery improvements.
- Merchant reports and export workflows.
- Optional EL-Rouji AI assistance for product-copy drafts or support summarization, with human approval and privacy review.
- Multi-vendor marketplace features if explicitly selected.
- Additional payment, shipping, and notification integrations.

## Release discipline

Do not mark a roadmap item complete from a code merge alone. Attach relevant build/QA/security evidence and identify the deployed version. Keep dates out of the roadmap until resource, provider, and acceptance constraints are known.
