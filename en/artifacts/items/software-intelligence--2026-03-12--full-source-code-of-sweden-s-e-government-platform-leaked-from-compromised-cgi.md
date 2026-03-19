---
source: hn
url: https://darkwebinformer.com/full-source-code-of-swedens-e-government-platform-leaked-from-compromised-cgi-sverige-infrastructure/
published_at: '2026-03-12T23:50:16'
authors:
- reimertz
topics:
- cybersecurity-breach
- source-code-leak
- software-supply-chain
- jenkins-compromise
- egovernment
relevance_score: 0.71
run_id: materialize-outputs
language_code: en
---

# Full Source Code of Sweden's E-Government Platform Leaked from Compromised CGI

## Summary
This is not an academic paper, but a cybersecurity incident disclosure: an attacker claims to have stolen and publicly released the complete source code of Sweden's e-government platform from CGI Sverige infrastructure. The incident highlights the systemic risks posed by compromises in critical government software supply chains, CI/CD infrastructure, and credential management.

## Problem
- The core issue is that a critical government digital services platform and its contractor infrastructure were compromised, exposing the **complete source code**, internal system details, and potentially sensitive data.
- This matters because e-government platforms support public services, identity-related processes, and electronic signing capabilities; once source code and access paths are leaked, the risks of follow-on attacks, exploitation, and supply-chain intrusion rise significantly.
- The text also states that citizen PII databases and electronic signing documents were sold separately, indicating that the incident is not only a code leak but may also expand into a privacy and identity security incident.

## Approach
- The "approach" described is not a defensive solution, but the intrusion chain claimed by the attacker: first obtaining **full control of Jenkins**, then using the fact that the Jenkins user belongs to the Docker group to achieve a **Docker escape**.
- The attacker then used **SSH private keys for lateral movement** and analyzed local **.hprof** files for reconnaissance to discover additional system information and exploitable assets.
- It also mentions using **SQL copy-to-program** to gain further pivoting or command execution, ultimately expanding control over the infrastructure.
- The leaked or listed assets include: the complete platform source code, a staff database, an API document signing system, RCE test endpoints, initial foothold details, jailbreak artifacts, and Jenkins SSH pivot credentials.

## Results
- The strongest concrete claim is that the attacker says they leaked the **complete source code of Sweden's e-government platform**, and that it is "not just configuration snippets."
- The text provides no verifiable academic experiments, benchmarks, or performance metrics, so there are **no quantitative research results** to report.
- Specific impact claims include that Sweden's e-government system is described as "the most affected party," while **citizen PII databases** and **electronic signing documents** were allegedly obtained and sold separately.
- The incident also allegedly exposed multiple categories of high-risk internal assets: **Jenkins SSH pivot credentials, RCE test endpoints, staff database, API document signing system, initial foothold details**.
- Key weaknesses named in the intrusion chain include: **1 full Jenkins compromise scenario**, **1 Docker escape scenario (because the Jenkins user is in the Docker group)**, SSH private-key lateral movement, .hprof reconnaissance, and SQL copy-to-program pivoting.

## Link
- [https://darkwebinformer.com/full-source-code-of-swedens-e-government-platform-leaked-from-compromised-cgi-sverige-infrastructure/](https://darkwebinformer.com/full-source-code-of-swedens-e-government-platform-leaked-from-compromised-cgi-sverige-infrastructure/)
