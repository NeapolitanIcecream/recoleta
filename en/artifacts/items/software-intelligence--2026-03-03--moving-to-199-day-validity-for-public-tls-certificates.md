---
source: hn
url: https://knowledge.digicert.com/alerts/public-tls-certificates-199-day-validity
published_at: '2026-03-03T23:54:39'
authors:
- thread_id
topics:
- tls-certificates
- certificate-lifecycle
- pki-operations
- security-automation
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Moving to 199-day validity for public TLS certificates

## Summary
This is an industry change notice about the shortening validity period for public TLS certificates, not an academic paper. It explains that DigiCert will reduce the maximum certificate validity from 397 days to 199 days on February 24, 2026, and advises enterprises to transition to automated certificate lifecycle management as soon as possible.

## Problem
- The maximum validity period for public TLS certificates will be reduced from **397 days** to **199 days**, and this is the first stage toward a later move to approximately **47/46 days** validity.
- Shorter validity periods will significantly increase the frequency of renewals, reissues, duplicates, and validation maintenance, making **manual certificate lifecycle management** increasingly impractical.
- If an enterprise's domain validation, organization validation, or API call logic is not adapted in advance, it may lead to insufficient time for certificate issuance, interrupted renewal workflows, or increased operational burden.

## Approach
- Starting **2026-02-24**, DigiCert plans to uniformly limit the maximum validity of newly issued public TLS certificates to **199 days**.
- In **CertCentral**, the available validity options will then become: **199 days**, a **custom expiration date not exceeding 199 days**, and a **custom duration not exceeding 199 days**.
- For the **CertCentral Services API**, if requests are still submitted with longer terms such as **1 year**, the system will **automatically adjust them to 199 days** to avoid request errors.
- Certificates issued before the deadline with validity periods greater than 199 days will **remain valid until expiration**; however, any **renewal, reissue, or duplicate issuance** after the deadline must comply with the new **199-day limit**.
- The document explicitly recommends that organizations complete domain/organization validation in advance and adopt automation solutions such as **ACME** and **Trust Lifecycle Manager** to prepare for a further reduction to **46 days** in the future.

## Results
- Key change date: starting **2026-02-24**, the maximum validity of DigiCert public TLS certificates will be reduced from **397 days to 199 days**.
- Long-term roadmap: this is the first stage of the transition toward **47-day** certificate validity; by **2029**, the maximum validity period will be reduced to **46 days**.
- Impact on existing issued certificates: certificates issued **before 2026-02-24** with validity greater than **199 days** **will not be invalidated early**, but will remain trusted until their natural expiration.
- Impact on reissue/duplicate issuance: **before 2026-02-24**, reissue/duplicate of 365/397-day certificates can still go up to **397 days**; **on and after that date**, the limit becomes **199 days**.
- Impact on renewals: renewals can still begin **90 days** before expiration, but starting **2026-02-24**, newly issued certificates will have a maximum validity of only **199 days**.
- The text does not provide experiments, benchmarks, or performance metrics; the strongest concrete claims are that API requests will be **automatically rewritten to 199 days** to reduce errors, and that future **46-day** validity will make manual CLM “impractical.”

## Link
- [https://knowledge.digicert.com/alerts/public-tls-certificates-199-day-validity](https://knowledge.digicert.com/alerts/public-tls-certificates-199-day-validity)
