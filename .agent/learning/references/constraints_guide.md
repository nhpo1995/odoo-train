# Constraints & Data Integrity (Odoo)

## Overview
Odoo enforces data integrity at two layers:
- **SQL constraints** (`_sql_constraints`) for fast, database-level checks.
- **Python constraints** (`@api.constrains`) for complex business rules that need code logic.

Python constraints raise `ValidationError` when a rule is violated and are triggered on `create`/`write` for the declared fields.

## Key Concepts
- **`@api.constrains`**: decorator for Python validation, triggered only when declared fields appear in `create`/`write`. Dotted field names are ignored.
- **`_sql_constraints`**: list of `(name, sql_def, message)` tuples, enforced by PostgreSQL.
- **Errors**: SQL constraints raise database errors (IntegrityError); Python constraints should raise `ValidationError` for user-friendly messaging.
- **Float safety**: use `float_compare()` / `float_is_zero()` for float validations to avoid precision bugs.
- **Delete protection**:
  - Docs mention `@api.ondelete(at_uninstall=False)` for unlink-time checks.
  - Verify availability in the local codebase; if missing, use `unlink()` override + `UserError`.

## Best Practices
- Use **SQL constraints** for uniqueness and simple ranges (fast, safe).
- Use **Python constraints** for cross-field or cross-record checks.
- Keep constraint methods small and avoid heavy queries.
- Always provide clear, actionable error messages.
- For deletion rules, prefer explicit checks in `unlink()` if `@api.ondelete` is not available.

## Common Pitfalls
- `@api.constrains` ignores dotted field names and only triggers when fields are in `create`/`write`.
- Constraints might not run on imports when fields are not part of the payload.
- Float comparisons with `==` lead to false failures; use float utils.
- SQL constraint errors are less friendly; ensure messages are clear in `_sql_constraints`.
