# Approval Boundary Security Spec

## Scope

Validate Human gates for merge, capital, allowlist, release, phase gate, and authority changes.

## Fixture Inputs

Use abstract safe and unsafe fixtures under fixtures. Fixtures must not contain real credential-looking values.

## Expected Result

Safe cases are accepted for review. Unsafe cases stop promotion, create or update incident-record, and require Human review.

## Evidence

Record reviewed summaries and ledger links only. Do not store raw runtime logs.
