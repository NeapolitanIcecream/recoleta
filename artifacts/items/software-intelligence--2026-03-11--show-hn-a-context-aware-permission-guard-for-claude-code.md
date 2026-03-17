---
source: hn
url: https://github.com/manuelschipper/nah/
published_at: '2026-03-11T23:26:25'
authors:
- schipperai
topics:
- agent-safety
- permission-guard
- developer-tools
- code-assistant
- context-aware-security
relevance_score: 0.85
run_id: materialize-outputs
---

# Show HN: A context-aware permission guard for Claude Code

## Summary
nah 是一个面向 Claude Code 的上下文感知权限守卫，用结构化规则而不是简单的按工具允许/拒绝来判断每次工具调用的真实风险。它试图在保持自动化效率的同时，阻止危险文件操作、密钥读取、数据外传和恶意命令执行。

## Problem
- 现有 Claude Code 权限机制主要是按工具做 allow-or-deny，粒度过粗，无法区分“同一工具下安全与危险操作”的差异。
- 仅靠维护 deny list 很难覆盖复杂上下文，模型还可能绕过静态限制，导致删除文件、泄露凭证、执行恶意脚本等风险。
- 这很重要，因为开发代理需要更高自主性，但 `--dangerously-skip-permissions` 这类全放开模式会显著增加破坏本地环境和敏感数据的概率。

## Approach
- 在每次工具执行前，nah 作为 PreToolUse hook 拦截调用，先用**确定性的结构化分类器**按“实际动作类型”判断，而不是按命令名或工具名粗暴放行。
- 分类器结合上下文做决策，例如目标路径、命令参数、写入内容是否含私钥、是否涉及 `git push --force`、是否访问 `~/.aws`/`~/.ssh` 等敏感位置。
- 对分类器无法明确判断的情况，可选接入 LLM 只处理剩余的“ask”决策；并且设置 `max_decision: ask`，防止 LLM 把高风险操作提升为直接 allow。
- 系统支持全局与项目级配置：项目 `.nah.yaml` 只能收紧不能放松策略，从而避免恶意仓库借配置绕过防护；同时提供约 20 个内置 action types、日志、测试与命令行调参能力。

## Results
- 文本未提供正式论文式基准评测、准确率、误报率或与其他权限系统的量化对比结果。
- 作者给出的最具体演示结果是：提供 **25** 个实时安全案例，覆盖 **8** 类威胁，约 **5 分钟** 可跑完，包括 remote code execution、data exfiltration、obfuscated commands 等。
- 系统声称规则分类“运行在**毫秒级**”，并且“每个工具调用”都会先经过确定性分类器，再视情况进入可选 LLM 决策链。
- 内置覆盖面方面，项目声明有 **20** 种 built-in action types，默认 `full` profile 覆盖 shell、git、packages、containers 等场景。
- 具体能力示例包括：允许 `git push`，对 `git push --force` 触发拦截/确认；允许清理 `rm -rf __pycache__`，阻止 `rm ~/.bashrc`；允许读取 `./src/app.py`，拦截读取 `~/.ssh/id_rsa`；对包含私钥内容的写入进行内容检查并阻断。

## Link
- [https://github.com/manuelschipper/nah/](https://github.com/manuelschipper/nah/)
