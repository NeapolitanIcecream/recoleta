---
source: arxiv
url: https://arxiv.org/abs/2606.26924v1
published_at: '2026-06-25T12:02:18'
authors:
- Padmaraj Madatha
topics:
- llm-coding-agents
- code-governance
- agent-configuration
- software-supply-chain
- ide-agents
- human-ai-interaction
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# A Deterministic Control Plane for LLM Coding Agents

## Summary
## 摘要
论文提出了 Rel(AI)Build，一个用于 LLM 编码代理配置的确定性控制平面。它把提示词、权限和工作流状态作为受管理的工件处理，使用哈希、锁文件、审计日志、工具调用前检查和面向目标的编译器。

## 问题
- LLM 编码代理可以读写文件并运行 shell 命令，但其规则文件、代理定义和 IDE markdown 配置通常缺少来源信息、权限边界和可追踪的变更历史。
- 对 10,008 个公开 GitHub 仓库的研究发现，代理配置存在重复且维护较弱的问题。这一点影响较大，因为这些文件会引导拥有高影响访问权限的代理。
- 代理能力与 Claude Code、Cursor、Copilot、Aider、Codex 和 Windsurf 等工具特定方言绑定，使团队之间难以维护共享策略。

## 方法
- Rel(AI)Build 在现有 IDE 编码工具链之上添加一个控制平面。它不替代模型推理、代码索引或编辑循环。
- 它用 SHA-256 对代理资源进行内容寻址，写入带 HMAC 戳的锁文件，并在哈希链式 JSONL 审计日志中记录变更。
- 它为每个代理分配权限层级，在安装或转换前检查工具允许列表，并在工具执行前阻止高风险命令和写入路径。
- 它通过一个阶段状态机管控工作，生成需求、文件和测试跟踪工件。跟踪链接依赖代理配合，并在事后接受审计。
- 它将一个规范的 Markdown+YAML 代理定义编译为七个 IDE 目标，并用 Jaccard 相似度检测提示词漂移。

## 结果
- 在包含 6,145 个代理配置文件的 10,008 个公开 GitHub 仓库中，经 fork 调整后，10.1% 的已跟踪配置路径是完全重复项；该结果用 SHA-256 测量。
- 在重复克隆对中，75.5% 跨越组织边界，支持了代理配置作为未声明共享组件传播这一说法。
- 58% 的代理配置文件只有一次提交。按存在时间归一化后，代理配置平均为 0.4 次提交/月，同一批仓库中的 CI/CD 工作流为 0.6 次提交/月。
- 少于 1% 的代理配置文件声明了权限边界，而 GitHub Actions 工作流的比例为 33%。论文将这一结果标为脆弱，因为解析器只找到 31 个真阳性。
- 语料库显示出 3.18% 的凭据模式命中，以及六种代理配置方言。
- 在 N=10、N=15 和 N=20 注入违规的符合性测试确认，该实现会执行其声明的不变量。论文没有声称能提升开发者生产力；受控的开发者结果属于未来工作。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.26924v1](https://arxiv.org/abs/2606.26924v1)
