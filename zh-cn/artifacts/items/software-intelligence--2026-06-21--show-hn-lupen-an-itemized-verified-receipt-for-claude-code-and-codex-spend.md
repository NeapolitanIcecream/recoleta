---
source: hn
url: https://github.com/momoraul/Lupen
published_at: '2026-06-21T23:32:03'
authors:
- momoraul
topics:
- ai-coding-tools
- cost-accounting
- code-agent-logs
- local-verification
- developer-tooling
relevance_score: 0.63
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Lupen – an itemized, verified receipt for Claude Code and Codex spend

## Summary
## 摘要
Lupen 是一个 macOS 应用和 CLI，可根据本地 JSONL 日志逐项列出 Claude Code 和 Codex 开销。它用 token 数和公开价格表重新计算成本，让用户把开销追溯到会话、轮次、步骤和子代理。

## 问题
- 每日 AI 编码开销总额看不出是哪家提供商、哪个会话、哪个轮次、哪个工具循环或哪个子代理产生了成本；当一个失控会话的成本超过当天其余部分时，这一点很关键。
- Claude Code 和 Codex 会写入详细的本地日志，但原始 JSONL 文件很难手动查看。
- 提示词、文件路径、图片和 URL 都很敏感，所以成本分析需要在不上传日志的情况下运行。

## 方法
- 读取 Claude Code 的本地会话文件 `~/.claude/projects/**/*.jsonl`，以及 Codex 的 `~/.codex/sessions/**/rollout-*.jsonl` 或 `$CODEX_HOME/sessions/**/rollout-*.jsonl`。
- 构建本地索引，把活动按 Session → Turn → Step → SkillGroup → SubAgent 分组，并为 Claude Code 和 Codex 提供按提供商区分的模式。
- 使用 Anthropic `stop_reason` 字段设置轮次边界，把工具使用循环保留在同一轮次内。
- 根据原始 token 数和公开价格重新计算每项成本，然后将结果与上报总额做差异比较。
- 在同一个本地索引上提供 CLI，用于报告、搜索、恢复命令、预算检查和验证。

## 结果
- 摘录没有给出基准测试、准确性研究或用户研究结果。
- 声称的成本粒度：按 Session、Turn、Step、SkillGroup 和 SubAgent 统计，并在首个公开版本中提供 4 类 token 拆分。
- 示例提供商总额：`$50 today · Claude Code · 12 sessions · 84 turns`。
- 验证会检查 Claude Code 的逐请求总额和 Codex `token_count` rollout 事件；发生成本漂移时，`lupen verify` 以代码 `4` 退出。
- 预算自动化支持 `lupen budget --over 20 --last 7d` 等门槛；超出预算时同样以代码 `4` 退出。
- 限额跟踪会根据过去 7 天的 5 小时限额使用量估算 `$ per 1%`，菜单栏阈值为 70%、90% 和 100%。

## Problem

## Approach

## Results

## Link
- [https://github.com/momoraul/Lupen](https://github.com/momoraul/Lupen)
