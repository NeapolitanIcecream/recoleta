---
source: hn
url: https://github.com/anma-labs/anma
published_at: '2026-06-21T23:41:02'
authors:
- nxy
topics:
- code-intelligence
- ai-coding-agents
- software-architecture
- ci-governance
- human-ai-interaction
- automated-software-production
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: ANMA, boundary contracts for cheaper AI coding agents

## Summary
## 摘要
ANMA 将 YAML 模块契约转换为 Claude Code 指引、阻止编辑的 hook 和 CI 检查，让成本更低的编码 agent 留在声明的架构边界内。最有力的证据来自 Python 和 TypeScript 中的边界违规测试；Go 的证据较弱，但结果为正向。

## 问题
- 成本更低或速度更快的编码 agent 可能会进行跨越模块边界的编辑，例如添加不允许的导入。
- 架构文档可能与 CI 规则脱节，导致 agent 和人类看到的指令不同于检查实际执行的规则。
- 对于在批量编码工作流中使用 agent 的团队，这会影响模块边界的可靠性，因为他们不能手动审查每一次编辑。

## 方法
- 开发者为每个模块编写纯 YAML 契约，包括公共接口、允许的依赖、负责人和源根目录。
- `anma sync` 会生成 `CLAUDE.md`、每个模块的指引、`.claude/rules`、一个 `PreToolUse` hook、后端配置、CI workflow 文件，以及可选的 `CODEOWNERS` 条目。
- 生成的指引会在 Claude Code 编辑代码前告诉它哪些模块和导入是允许的。
- 生成的 hook 会用退出码 2 阻止拟议的破坏边界的编辑；同一套边界检查也可以在 pre-commit 和 CI 中运行。
- Python 支持模块依赖和公共接口约束；Go 和 TypeScript 目前约束模块到模块的依赖。

## 结果
- 在使用 Claude Haiku 4.5 的受控 Python benchmark 中，普通 repo 在 19 次运行中出现 13 次边界违规；使用 ANMA 后，20 次运行中违规为 0，Fisher 精确检验 p < 0.0001。
- 报告中的 Python 对照组违规率为 68%，使用 ANMA 指引后降至 0%。
- 在预注册的 TypeScript 后续实验中，对照条件在 20 次运行中出现 18 次违规；ANMA 在 20 次运行中违规为 0，Fisher 精确检验 p < 0.00001。
- 在 Go 中，对照组在 30 次运行中出现 10 次违规，ANMA 在 30 次运行中违规为 0，p = 0.0004；作者称这一结果具有提示性，因为对照组违规率低于预注册的 0.40 下限。
- 在报告的研究中，Claude Opus 4.8 在没有 ANMA 的情况下也遵守了 Python 边界，因此所声称的收益主要适用于成本更低的 agent，以及 CI 治理，而不是提升前沿模型本身的能力。
- 该工具被描述为约 800 行代码，没有运行时组件，只有一个必需依赖，并提供可选后端：用于 Python 的 tach、用于 Go 的 go-arch-lint，以及用于 TypeScript 的 dependency-cruiser。

## Problem

## Approach

## Results

## Link
- [https://github.com/anma-labs/anma](https://github.com/anma-labs/anma)
