---
source: hn
url: https://www.fortinet.com/blog/threat-research/unveiling-the-weaponized-web-shell-encystphp
published_at: '2026-03-04T23:41:27'
authors:
- WeaklingOra
topics:
- web-shell
- freepbx
- cve-2025-64328
- persistence
- threat-intelligence
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Unveiling the Weaponized Web Shell EncystPHP

## Summary
This is a threat research report on a new weaponized web shell for FreePBX called "EncystPHP," focusing on its delivery, persistence, disguise, and attack chain. The value of the report lies in revealing the real risk that exploiting CVE-2025-64328 can lead to long-term administrator-level control.

## Problem
- The problem this research addresses is: how attackers can use **CVE-2025-64328** in FreePBX Endpoint Manager to deploy a highly stealthy, strongly persistent web shell on victim hosts and achieve long-term takeover.
- This matters because the affected systems are enterprise PBX/communications infrastructure; once compromised, attackers can gain remote command execution, administrator privileges, SSH persistence, and even abuse telephony resources to place outbound calls.
- The report also seeks to answer: who this activity is associated with, how the attack chain operates, and to what extent defenders should treat it as a full-compromise incident.

## Approach
- The core method is straightforward: first exploit the **post-authentication command injection vulnerability CVE-2025-64328 in FreePBX** to deliver the initial dropper (`c`), which then decodes and writes a Base64-encoded PHP web shell to disk, disguising it as a legitimate `ajax.php`.
- The initial dropper first "cleans house" and hardens control: it modifies permissions on key files, reads `/etc/freepbx.conf`, deletes cron jobs and multiple users, removes other suspicious PHP shells, creates a root-level user `newfpbx`, resets passwords in a coordinated way, and escalates privileges.
- It then establishes **four-stage persistence** by injecting an SSH public key, keeping port 22 open, installing multi-stage crontab download tasks, writing `license.php`, and executing `test.sh`.
- The secondary dropper `k.php` copies the same web shell to multiple web paths (such as `digium_phones/`, `rest_phones/`, `freepbx/`, etc.), forges timestamps, and writes `.htaccess` rewrite rules to improve stealth and survivability.
- After login, the web shell exposes the "Ask Master" interface after validating a plaintext password with **MD5**, supporting file enumeration, process viewing, Asterisk channel and SIP peer queries, configuration theft, and arbitrary command execution.

## Results
- The report provides a clear affected scope: **FreePBX Endpoint Manager v17.0.2.36 – v17.0.3**, impacting **any organization**, with an overall severity level of **High**.
- The observed attacks began in **early December last year**; the sample was delivered via **45.234.176.202** (domain `crm.razatelefonia.pro`), and multiple IOCs are listed, including **2 URLs**, **2 IPs**, and **5 SHA-256** hashes.
- The persistence strength is described with specific timing granularity: crontab downloads `k.php` to `/var/lib/asterisk/bin/zen2` and `devnull2` **every 1 minute**, and downloads it to `devnull` **every 3 minutes**; another path also downloads `c` and `k.php` to additional locations **every 1 minute**.
- The deployment redundancy is very clear: `k.php` creates at least **7 directories** (such as `digium_phones/`, `rest_phones/`, `phones/`, `freepbx/`, etc.) and copies the shell to many common web paths, improving recovery after single-point removal.
- Functionally, the research claims the shell enables **remote command execution, administrator-level persistence, log tampering, sustained SSH access, configuration theft, Asterisk/FreePBX information queries, and abuse of telephony resources**; however, the article **does not provide experimental comparative metrics** (such as improved detection rate, latency, coverage, or other quantitative evaluations).
- On the protection side, Fortinet states that its products already provide specific detection and blocking: antivirus signatures **`PHP/EncystPHP.A!tr`** and **`BASH/EncystPHP.A!tr`**, Web Filtering blocks C2, and IPS provides signature **59448** for **CVE-2025-64328**.

## Link
- [https://www.fortinet.com/blog/threat-research/unveiling-the-weaponized-web-shell-encystphp](https://www.fortinet.com/blog/threat-research/unveiling-the-weaponized-web-shell-encystphp)
