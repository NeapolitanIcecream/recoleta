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
---

# Unveiling the Weaponized Web Shell EncystPHP

## Summary
这篇报告分析了针对 FreePBX 的持久化 Web Shell“EncystPHP”，说明攻击者如何利用 CVE-2025-64328 获得长期管理员级控制。其价值在于揭示了一个现实活跃攻击链：投递、伪装、持久化、清痕和多点冗余部署。

## Problem
- 解决的问题是：识别并剖析一种利用 **FreePBX Endpoint Manager v17.0.2.36–v17.0.3** 漏洞 **CVE-2025-64328** 部署的持久化 Web Shell，以及其完整攻击行为。
- 这很重要，因为一旦利用成功，远程攻击者可获得受害 PBX 系统的高权限控制，带来长期驻留、未授权管理访问和电话资源滥用风险。
- 报告还试图说明该活动与已知威胁行为体 **INJ3CTOR3** 的关联性，帮助防御方进行威胁归因和检测加固。

## Approach
- 核心机制很简单：攻击者先利用 FreePBX 管理界面的后认证命令注入漏洞，然后下载并执行 dropper（`c` 和 `k.php`），再把 Base64 编码的 PHP Web Shell 解码写入磁盘并伪装成合法文件 `ajax.php`。
- Web Shell 通过硬编码 MD5 口令校验提供交互界面，可执行任意命令、枚举文件和进程、读取 FreePBX/Elastix 配置，并利用 PBX 上下文发起外呼等操作。
- 为了长期控制，恶意程序创建 root 级用户 `newfpbx`、重置多个账户密码、注入 SSH 公钥、保持 22 端口开放，并通过多组 crontab 每 **1 分钟** 或 **3 分钟** 重下发 dropper。
- 为了隐蔽与抗清除，样本会删除其他 Web Shell、篡改日志、伪造时间戳、删除 endpoint 模块、写入 `.htaccess` 做路由隐藏，并把同一 Web Shell 复制到多个常见 Web 路径。

## Results
- 报告确认受影响平台为 **FreePBX Endpoint Manager v17.0.2.36–v17.0.3**，漏洞为 **CVE-2025-64328**，影响级别标注为 **High**；攻击在 **2024 年 12 月初** 已被观测到。
- 观测到的投递基础设施包括 **45.234.176.202**，样本下载路径包括 `hxxp://45[.]234[.]176[.]202/new/c` 和 `hxxp://45[.]234[.]176[.]202/new/k.php`；攻击源最初来自 **Brazil**，目标环境由 **Indian** 云与通信技术公司管理。
- 持久化机制被分解为 **4 个阶段**：其中 cron 任务可每 **1 分钟** 下载 `k.php` 到 `/var/lib/asterisk/bin/zen2` 和 `/var/lib/asterisk/bin/devnull2`，并每 **3 分钟** 下载到 `/var/lib/asterisk/bin/devnull`。
- Dropper 会创建至少 **7 个目录**（如 `digium_phones/`、`rest_phones/`、`phones/`、`freepbx/` 等）并在多个 Web 路径复制 `ajax.php`，以提高存活率；还会删除至少 **8 个** FreePBX 用户名相关账户条目，如 `ampuser`、`svc_freepbx`、`freepbx_svc` 等。
- 报告没有提供标准学术基准或检测率类定量评测结果；最强的具体结论是：该样本具备远程命令执行、SSH 持久化、日志清除、多点部署和电话系统滥用能力，可将一次漏洞利用升级为“**完全沦陷**”。
- 防护侧给出可操作结果：Fortinet 声称其 AV 可检测 **`PHP/EncystPHP.A!tr`** 和 **`BASH/EncystPHP.A!tr`**，并提供针对 **CVE-2025-64328** 的 IPS 签名 **59448** 及对相关 C2 的 Web/IP 阻断。

## Link
- [https://www.fortinet.com/blog/threat-research/unveiling-the-weaponized-web-shell-encystphp](https://www.fortinet.com/blog/threat-research/unveiling-the-weaponized-web-shell-encystphp)
