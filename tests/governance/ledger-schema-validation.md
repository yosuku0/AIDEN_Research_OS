# Ledger Schema Validation Spec

## Scope

Validate ledger entries use LEDGER_SCHEMA and JSON schemas.

## Fixture Inputs

Use abstract safe and unsafe fixtures under fixtures. Fixtures must not contain real credential-looking values.

## Expected Result

Safe cases are accepted for review. Unsafe cases stop promotion, create or update incident-record, and require Human review.

## Evidence

Record reviewed summaries and ledger links only. Do not store raw runtime logs.
