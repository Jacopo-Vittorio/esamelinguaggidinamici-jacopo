# Performance Baseline

Measured with Django `CaptureQueriesContext` against the seeded SQLite database after Phase 1 runtime fixes.

## Before ORM Optimizations

| Page | URL | HTTP status | Query count |
|------|-----|-------------|-------------|
| Homepage | `/` | 200 | 0 |
| Product list | `/products/` | 200 | 19 |
| Product detail | `/products/products/1/detail` | 200 | 6 |
| Search results | `/products/?nome=Carta%20politenata&material=politenata` | 200 | 4 |
| Forum thread list | `/forum/list/` | 200 | 9 |
| Forum detail | `/forum/forum/3/discussione/` | 200 | 4 |
| Cart detail with 3 items | `/cart/` | 200 | 4 |
| Owner product list | `/products/gestioneprodotti` | 200 | 18 |
