# Promotion launch log

This is the append-only ledger for external promotion attempts. There have been
no external submissions in this sprint yet.

## Metric definitions

- `T0 evaluation`: an external user inspects the bundled demo or live fleet.
- `T1 qualified activation`: a non-project user generates a new artifact from
  non-bundled input and voluntarily reports or publishes it.
- `T2 retained`: the same opted-in external identity produces a new artifact
  for four consecutive calendar weeks.
- `R independent reference`: an external user or organization controls a public
  reference based on actual use.

Downloads, pulls, clones, stars, page views, bot traffic, maintainer runs, CI,
and the bundled demo are not `T1`.

## Attempt ledger

| ID | Date | Channel | Destination | Material | Operator | Status | Attributable T0 | T1 | T2 | R | Decision |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| — | — | — | — | — | — | not started | 0 | 0 | 0 | 0 | Wait for release gates |

## Receipt ledger

Record only public or explicitly consented evidence. Do not copy private
configuration, source material, email, organization identity, or machine paths
into this file.

| Receipt | First artifact date | Source channel | Public evidence | Consecutive weeks | Classification | Notes |
| --- | --- | --- | --- | ---: | --- | --- |
| — | — | — | — | 0 | none | No external receipts yet |

## Update procedure

1. Add an attempt row before submitting.
2. Add the public submission URL and result after submitting.
3. Check attributable receipts at 24 hours, 7 days, and 28 days.
4. Keep rejection and zero-result rows.
5. Pause a repeatable channel after 28 days or four policy-compliant attempts
   with zero attributable `T1`.
