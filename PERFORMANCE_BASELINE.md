# Performance Baseline

Measured with Django `CaptureQueriesContext` against the seeded SQLite database after Phase 1 runtime fixes.

## Query Counts

| Page | URL | HTTP status | Before | After |
|------|-----|-------------|--------|-------|
| Homepage | `/` | 200 | 0 | 0 |
| Product list | `/products/` | 200 | 19 | 1 |
| Product detail | `/products/products/1/detail` | 200 | 6 | 5 |
| Search results | `/products/?nome=Carta%20politenata&material=politenata` | 200 | 4 | 1 |
| Forum thread list | `/forum/list/` | 200 | 9 | 1 |
| Forum detail | `/forum/forum/3/discussione/` | 200 | 4 | 2 |
| Cart detail with 3 items | `/cart/` | 200 | 4 | 4 |
| Owner product list | `/products/gestioneprodotti` | 200 | 18 | 3 |

## Notes

- The original plan's sample URLs were adjusted to the routes that exist in this project.
- Query counts were measured with Django's `CaptureQueriesContext` instead of manual browser toolbar reads so the numbers are reproducible.
- The SQLite WAL step from the plan was skipped because Django 4.2's SQLite backend does not support `init_command` or `transaction_mode` in `DATABASES["default"]["OPTIONS"]`.
