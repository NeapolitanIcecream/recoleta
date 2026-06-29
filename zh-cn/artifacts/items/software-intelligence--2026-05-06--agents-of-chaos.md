---
source: hn
url: https://agentsofchaos.baulab.info/
published_at: '2026-05-06T23:52:56'
authors:
- giwook
topics:
- autonomous-agents
- ai-safety
- tool-use
- human-ai-interaction
- adversarial-testing
- persistent-memory
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Agents of Chaos

## Summary
## 摘要
六个自主语言模型代理在一个真实运行的 Discord 环境中接受了两周测试，具备记忆、电子邮件、shell 访问和人类交互能力。研究报告了 10 个安全漏洞，以及 6 个代理保持了恰当安全边界的案例。

## 问题
- 具备工具的自主代理可以跨会话行动、联系他人、运行命令并保留记忆，因此一次失败可能会延续到单轮聊天之外。
- 实验室测试常常漏掉社交压力、冒充所有者和多方交互；这项研究在真实环境中测试了这些风险。

## 方法
- 研究人员把 6 个代理部署到一个 Discord 服务器中，并给它们分配了电子邮件账户、持久文件系统、无限制的 shell 访问权限，以及帮助研究人员的任务。
- 每个代理都运行在 OpenClaw 上，这是一套开源支架，为前沿语言模型提供记忆、工具访问、规划能力和跨会话自主性。
- 这些代理可以主动联系他人、发送电子邮件、执行脚本，并且无需每次行动都经过人工批准。
- 20 名研究人员在两周内与这些代理互动，包括善意请求、恶意指令、冒充尝试和社会工程攻击。

## 结果
- 这项研究在同一个真实部署中记录了 10 个安全漏洞。
- 它还记录了 6 个安全行为案例，在这些案例中，攻击性尝试失败，或者代理保持了恰当边界。
- 这次实验覆盖了 6 个自主代理、20 名参与者和 2 周互动。
- 论文在可用时把结论连接到一手证据，包括 Discord 日志和 OpenClaw 会话转录，供独立审查。

## Problem

## Approach

## Results

## Link
- [https://agentsofchaos.baulab.info/](https://agentsofchaos.baulab.info/)
