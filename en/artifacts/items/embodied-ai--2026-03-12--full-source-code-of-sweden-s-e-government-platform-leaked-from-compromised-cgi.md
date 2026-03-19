---
source: hn
url: https://darkwebinformer.com/full-source-code-of-swedens-e-government-platform-leaked-from-compromised-cgi-sverige-infrastructure/
published_at: '2026-03-12T23:50:16'
authors:
- reimertz
topics:
- cybersecurity-incident
- source-code-leak
- supply-chain-breach
- jenkins-compromise
- government-it
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Full Source Code of Sweden's E-Government Platform Leaked from Compromised CGI

## Summary
This is not a research paper, but a cybersecurity incident bulletin describing the alleged leak of the full source code of Sweden's e-government platform and related sensitive assets from CGI Sverige infrastructure. Its core value lies in revealing the systemic risk that can arise to national-level digital government services after a supply chain/provider compromise.

## Problem
- The issue highlighted by the text is that after a critical e-government platform's third-party IT infrastructure is compromised, sensitive assets such as source code, credentials, test endpoints, employee databases, and citizen PII may be leaked in bulk.
- This matters because such platforms support government digital services, electronic signatures, and citizen data; once compromised, they can lead to national-level service disruption, privacy exposure, and further intrusion risk.
- The text also emphasizes the issue of "attribution of responsibility": the attacker claims the intrusion clearly occurred on the CGI infrastructure side, rather than being simply attributed to the customer side.

## Approach
- The text does not describe a scientific method, but rather an attack chain: the attacker claims to have first obtained full control of Jenkins.
- They then allegedly used the fact that the Jenkins user belonged to the Docker group to achieve Docker escape, moving laterally from a container or restricted environment into a higher-privilege environment.
- They further combined SSH private keys for pivoting, analyzed local `.hprof` files for reconnaissance, and used SQL `copy-to-program`-type techniques to continue lateral movement or execute commands.
- Ultimately, they allegedly collected the full e-government platform source code, along with an employee database, API document signing system, RCE test endpoints, initial foothold details, jailbreak artifacts, and Jenkins SSH credentials.

## Results
- The text claims that the leaked material is the **complete** source code of Sweden's e-government platform, and "not just configuration snippets," but provides no independently verifiable technical evidence or sample scale.
- It also claims that citizen PII databases and electronic signing documents were obtained and are being **sold separately**; however, it does not provide record counts, data volume, or the number of affected users.
- The listed compromised assets include: employee database, API document signing system, RCE test endpoints, initial foothold details, jailbreak artifacts, Jenkins SSH pivot credentials.
- The attack stages mentioned in the text include: **full Jenkins compromise**, **Docker escape**, **SSH private key pivots**, **.hprof reconnaissance**, **SQL copy-to-program pivots**.
- There are no research-style quantitative results: no dataset, experimental setup, baseline methods, success rate, detection metrics, or false positive rate figures are provided.

## Link
- [https://darkwebinformer.com/full-source-code-of-swedens-e-government-platform-leaked-from-compromised-cgi-sverige-infrastructure/](https://darkwebinformer.com/full-source-code-of-swedens-e-government-platform-leaked-from-compromised-cgi-sverige-infrastructure/)
