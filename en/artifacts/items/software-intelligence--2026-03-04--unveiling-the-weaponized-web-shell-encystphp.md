---
source: hn
url: https://www.fortinet.com/blog/threat-research/unveiling-the-weaponized-web-shell-encystphp
published_at: '2026-03-04T23:41:27'
authors:
- WeaklingOra
topics:
- web-shell
- freepbx-security
- threat-intelligence
- persistence
- vulnerability-exploitation
relevance_score: 0.12
run_id: materialize-outputs
language_code: en
---

# Unveiling the Weaponized Web Shell EncystPHP

## Summary
This report analyzes the persistent web shell “EncystPHP” targeting FreePBX, explaining how attackers exploit CVE-2025-64328 to obtain long-term administrator-level control. Its value lies in revealing a real, active attack chain: delivery, disguise, persistence, trace removal, and redundant multi-location deployment.

## Problem
- The problem addressed is: identifying and dissecting a persistent web shell deployed via the **FreePBX Endpoint Manager v17.0.2.36–v17.0.3** vulnerability **CVE-2025-64328**, along with its full attack behavior.
- This matters because once exploitation succeeds, remote attackers can gain high-privilege control of the victim PBX system, creating risks of long-term residence, unauthorized administrative access, and abuse of telephony resources.
- The report also attempts to show this activity’s association with the known threat actor **INJ3CTOR3**, helping defenders with threat attribution and detection hardening.

## Approach
- The core mechanism is straightforward: the attacker first exploits a post-authentication command injection vulnerability in the FreePBX administrative interface, then downloads and executes droppers (`c` and `k.php`), and finally decodes a Base64-encoded PHP web shell, writes it to disk, and disguises it as the legitimate file `ajax.php`.
- The web shell provides an interactive interface through hardcoded MD5 password verification, can execute arbitrary commands, enumerate files and processes, read FreePBX/Elastix configurations, and abuse the PBX context to initiate outbound calls.
- To maintain long-term control, the malware creates a root-level user `newfpbx`, resets multiple account passwords, injects SSH public keys, keeps port 22 open, and repeatedly re-delivers droppers through multiple crontab entries every **1 minute** or **3 minutes**.
- For stealth and resistance to removal, the sample deletes other web shells, tampers with logs, falsifies timestamps, removes the endpoint module, writes `.htaccess` for route hiding, and copies the same web shell to multiple common web paths.

## Results
- The report confirms the affected platform is **FreePBX Endpoint Manager v17.0.2.36–v17.0.3**, the vulnerability is **CVE-2025-64328**, the impact level is labeled **High**, and attacks were observed as early as **early December 2024**.
- Observed delivery infrastructure includes **45.234.176.202**; sample download paths include `hxxp://45[.]234[.]176[.]202/new/c` and `hxxp://45[.]234[.]176[.]202/new/k.php`; the attack source initially came from **Brazil**, and the target environment was managed by an **Indian** cloud and communications technology company.
- The persistence mechanism is broken down into **4 stages**: cron jobs can download `k.php` every **1 minute** to `/var/lib/asterisk/bin/zen2` and `/var/lib/asterisk/bin/devnull2`, and every **3 minutes** to `/var/lib/asterisk/bin/devnull`.
- The dropper creates at least **7 directories** (such as `digium_phones/`, `rest_phones/`, `phones/`, `freepbx/`, etc.) and copies `ajax.php` across multiple web paths to improve survivability; it also deletes at least **8** account entries associated with FreePBX usernames, such as `ampuser`, `svc_freepbx`, and `freepbx_svc`.
- The report does not provide standard academic benchmarks or quantitative evaluation results such as detection rates; the strongest concrete conclusion is that this sample has remote command execution, SSH persistence, log clearing, multi-location deployment, and telephony-system abuse capabilities, allowing a single vulnerability exploit to escalate into “**complete compromise**.”
- On the defensive side, actionable results are provided: Fortinet claims its AV can detect **`PHP/EncystPHP.A!tr`** and **`BASH/EncystPHP.A!tr`**, and provides IPS signature **59448** for **CVE-2025-64328** along with Web/IP blocking for related C2 infrastructure.

## Link
- [https://www.fortinet.com/blog/threat-research/unveiling-the-weaponized-web-shell-encystphp](https://www.fortinet.com/blog/threat-research/unveiling-the-weaponized-web-shell-encystphp)
