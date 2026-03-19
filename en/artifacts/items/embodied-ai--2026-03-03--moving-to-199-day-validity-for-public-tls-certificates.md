---
source: hn
url: https://knowledge.digicert.com/alerts/public-tls-certificates-199-day-validity
published_at: '2026-03-03T23:54:39'
authors:
- thread_id
topics:
- tls-certificates
- certificate-lifecycle-management
- pkis
- acme
- security-operations
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Moving to 199-day validity for public TLS certificates

## Summary
This is an industry change notice about shortening the validity period of public TLS certificates, not an academic research paper. Starting on February 24, 2026, DigiCert will reduce the maximum validity of public TLS certificates from 397 days to 199 days, and indicates that it will later transition further to around 47/46 days.

## Problem
- The problem it addresses is that the industry is tightening the maximum validity period for public TLS certificates. If organizations do not adjust their procurement, renewal, and operations processes in advance, they may encounter disruptions during certificate issuance, renewal, and reissuance.
- This matters because TLS certificates are the foundation for establishing trust and encrypted communication for websites and online services; shorter validity periods will significantly increase the frequency of certificate lifecycle management.
- The article explicitly states that by 2029 the maximum validity period will be reduced to **46 days**, at which point manual certificate lifecycle management will be “impractical,” making automation necessary.

## Approach
- The core mechanism is simple: starting on **2026-02-24**, DigiCert will enforce a **199-day maximum validity** limit for newly issued public TLS certificates, replacing the current **397-day** cap.
- When ordering in CertCentral, only three options will be available: **199 days**, a **custom expiration date not exceeding 199 days**, and a **custom duration up to 199 days**.
- For the CertCentral Services API, requests for public TLS certificates originally submitted for **1 year** will be **automatically adjusted to 199 days** to avoid request errors and keep processing successful.
- Existing certificates that were already issued before the deadline and have validity periods longer than 199 days are **not affected** and will remain trusted until their natural expiration; however, renewals, reissuance, or duplicate issue after the deadline will be subject to the **199-day** maximum.
- To address even shorter future cycles, the article recommends adopting automation solutions such as **ACME**, CertCentral automation capabilities, and Trust Lifecycle Manager.

## Results
- Key change in numbers: the maximum validity of public TLS certificates will drop from **397 days** to **199 days**, effective **2026-02-24**.
- This is the first step in a multi-phase transition; the article says the future is moving toward **47-day** TLS certificates, while the “Prepare for the future” section states that by **2029** the maximum validity will be reduced to **46 days**.
- Immediate API-level result: starting on **2026-02-24**, requests for **1-year** public TLS certificates submitted through the CertCentral Services API will be **automatically rewritten to 199 days** to reduce “unexpected errors.”
- The renewal window is unchanged: certificates can still be renewed **90 days** before expiration, but starting on **2026-02-24**, newly issued renewal certificates can be valid for no more than **199 days**.
- Reissuance/duplicate impact: **before 2026-02-24**, reissuance or duplicate issue of 365/397-day certificates can still reach **397 days**; **on and after that date**, the cap becomes **199 days**.
- The article **does not provide experiments, benchmark datasets, or performance metrics**; its strongest concrete claim is that this policy can help avoid API request failures and that future short validity periods will make manual CLM no longer feasible.

## Link
- [https://knowledge.digicert.com/alerts/public-tls-certificates-199-day-validity](https://knowledge.digicert.com/alerts/public-tls-certificates-199-day-validity)
