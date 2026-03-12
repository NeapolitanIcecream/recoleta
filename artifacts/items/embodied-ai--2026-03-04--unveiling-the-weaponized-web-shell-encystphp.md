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
---

# Unveiling the Weaponized Web Shell EncystPHP

## Summary
这是一份针对 FreePBX 新型武器化 Web Shell“EncystPHP”的威胁研究，重点分析其投递、持久化、伪装与攻击链。报告的价值在于揭示了利用 CVE-2025-64328 后可形成长期管理员级控制的现实风险。

## Problem
- 该研究解决的问题是：攻击者如何利用 FreePBX Endpoint Manager 的 **CVE-2025-64328** 在受害主机上部署高隐蔽、强持久化的 Web Shell，并实现长期接管。
- 这很重要，因为受影响系统是企业 PBX/通信基础设施；一旦被控，攻击者可获得远程命令执行、管理员权限、SSH 持久化，甚至滥用电话资源发起外呼。
- 报告还试图回答：该活动与谁有关、攻击链如何运作、以及防御方应将其视为多大级别的完全失陷事件。

## Approach
- 核心方法很简单：先利用 **FreePBX 后认证命令注入漏洞 CVE-2025-64328** 投递初始 dropper（`c`），再由其解码并落地 Base64 编码的 PHP Web Shell，伪装成合法的 `ajax.php`。
- 初始 dropper 会先“清场”和加固控制权：修改关键文件权限、读取 `/etc/freepbx.conf`、删除 cron 与多个用户、清除其他可疑 PHP Shell、创建 root 级用户 `newfpbx`、统一重置密码并提权。
- 然后它通过注入 SSH 公钥、保持 22 端口开放、安装多阶段 crontab 下载任务、写入 `license.php` 和执行 `test.sh`，建立 **四阶段持久化**。
- 次级 dropper `k.php` 会把同一个 Web Shell 复制到多个 Web 路径（如 `digium_phones/`、`rest_phones/`、`freepbx/` 等），并伪造时间戳、写入 `.htaccess` 重写规则，以提高隐蔽性和存活率。
- 登录后，Web Shell 通过明文密码经 **MD5** 校验后开放“Ask Master”界面，支持文件枚举、进程查看、Asterisk 通道与 SIP peer 查询、配置文件窃取和任意命令执行。

## Results
- 报告给出了明确受影响范围：**FreePBX Endpoint Manager v17.0.2.36 – v17.0.3**，影响对象为 **任何组织**，总体严重级别为 **High**。
- 观察到的攻击时间为 **去年 12 月初** 开始；样本通过 **45.234.176.202**（域名 `crm.razatelefonia.pro`）投递，已列出多个 IOC，包括 **2 个 URL**、**2 个 IP** 和 **5 个 SHA-256** 哈希。
- 持久化强度具有具体时间粒度：crontab 会以 **每 1 分钟** 下载 `k.php` 到 `/var/lib/asterisk/bin/zen2` 与 `devnull2`，并以 **每 3 分钟** 下载到 `devnull`；另一路还会以 **每 1 分钟** 下载 `c` 和 `k.php` 到额外路径。
- 部署冗余非常明显：`k.php` 会创建至少 **7 个目录**（如 `digium_phones/`、`rest_phones/`、`phones/`、`freepbx/` 等）并将 Shell 复制到多处常见 Web 路径，提高单点清除后的恢复能力。
- 功能层面，研究声称该 Shell 可实现 **远程命令执行、管理员级持久化、日志篡改、SSH 访问维持、配置窃取、Asterisk/FreePBX 信息查询以及电话资源滥用**；但文中**没有提供实验型对比指标**（如检测率提升、时延、覆盖率等量化评测）。
- 防护结果方面，Fortinet 声称其产品已提供具体检测与拦截：杀毒签名 **`PHP/EncystPHP.A!tr`**、**`BASH/EncystPHP.A!tr`**，Web Filtering 阻断 C2，IPS 提供针对 **CVE-2025-64328** 的签名 **59448**。

## Link
- [https://www.fortinet.com/blog/threat-research/unveiling-the-weaponized-web-shell-encystphp](https://www.fortinet.com/blog/threat-research/unveiling-the-weaponized-web-shell-encystphp)
