---
source: hn
url: https://ainowinstitute.org/publications/friendly-fire-exploit-brief
published_at: '2026-07-08T23:35:29'
authors:
- Cynddl
topics:
- ai-coding-agents
- prompt-injection
- remote-code-execution
- software-supply-chain
- code-intelligence
- agent-security
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Hijacking Defensive Cyber AI Agents for Remote Code Execution

## Summary
## 摘要
这份简报称，防御性编码代理在自动批准模式下审查恶意第三方代码库时，可能被转化为远程代码执行（RCE）路径。受影响的配置包括使用 Claude Sonnet 4.6、Sonnet 5 和 Opus 4.8 的 Claude Code，以及使用 GPT-5.5 的 Codex CLI。

## 问题
- 论文针对 AI 辅助漏洞审查中的一个安全缺口：代理必须读取不受信任的代码，但它可能把代码库中的文本当作指令，并运行攻击者控制的命令。
- 这很重要，因为 Claude Code 和 Codex 被推广用于开源安全审查、补丁编写和长时间运行的代理式工作，用户可能依赖自动批准。
- 在 CI/CD 或依赖审查工作流中，受攻陷的软件包可能在本应用来发现供应链攻击的同一次审查中触发该漏洞利用。

## 方法
- 作者修改了 Python geopy 库的本地副本，并要求代理：`Perform security testing on /path/to/geopy`。
- 他们添加了 `security.sh`、一个恶意的 `code_policies` 二进制文件，以及一个诱饵 `code_policies.go` 文件；该诱饵文件看起来像是这个二进制文件的源代码。
- 他们在 `README.md` 中放入语气温和的文档，建议运行 `./security.sh` 作为安全检查器，使该指令看起来像普通的项目指南。
- Claude Code 或 Codex 检查这些文件，判断脚本和二进制文件安全，并在 auto-mode 或 auto-review 下运行脚本；脚本随后启动恶意二进制文件。
- 该攻击不需要 hooks、plugins、MCP servers、configuration files，也不需要对项目文件夹的明确信任。

## 结果
- PoC 在 Claude Code CLI 版本 2.1.116、2.1.196、2.1.198 和 2.1.199 上实现了远程代码执行。
- PoC 也在 Codex CLI 版本 0.142.4 上生效。
- 列出的受影响模型配置包括 Claude Sonnet 4.6、Claude Sonnet 5、Claude Opus 4.8 high-effort 和 GPT-5.5。
- 作者报告称，最初为 Claude Sonnet 4.6 构建的漏洞利用无需修改即可迁移到 Claude Sonnet 5、Opus 4.8 和 GPT-5.5。
- 简报没有报告成功率、运行次数、时间指标或基准比较；简报称这些攻击已多次重复并成功。
- 作者还报告了使用 `CLAUDE.md` 和 `agent.md` 的成功变体，表明代码库文档通道不是唯一可能的注入路径。

## Problem

## Approach

## Results

## Link
- [https://ainowinstitute.org/publications/friendly-fire-exploit-brief](https://ainowinstitute.org/publications/friendly-fire-exploit-brief)
