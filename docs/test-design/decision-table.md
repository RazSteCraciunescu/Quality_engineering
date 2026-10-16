# Registration decision table

`Y` = true, `N` = false, `–` = not relevant after an earlier rejection.

| Rule | Event published | Input valid | Meets age | Consent | Active duplicate | Place available | Outcome |
|---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| 1 | N | – | – | – | – | – | 404, no record |
| 2 | Y | N | – | – | – | – | 422 validation, no record |
| 3 | Y | Y | N | – | – | – | 422 age rule, no record |
| 4 | Y | Y | Y | N | – | – | 422 consent rule, no record |
| 5 | Y | Y | Y | Y | Y | – | 409 conflict, no record |
| 6 | Y | Y | Y | Y | N | Y | Create `confirmed` |
| 7 | Y | Y | Y | Y | N | N | Create `waitlisted` |

Idempotent replay is evaluated before duplicate detection: an existing valid key returns the original successful record.
