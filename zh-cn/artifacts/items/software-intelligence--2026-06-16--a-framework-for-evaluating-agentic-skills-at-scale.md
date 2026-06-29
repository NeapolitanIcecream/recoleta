---
source: arxiv
url: https://arxiv.org/abs/2606.17819v1
published_at: '2026-06-16T11:46:56'
authors:
- Maksim Shaposhnikov
- Nicolas Fortuin
- Simon Stipcich
- Maria I. Gorinova
- Amy Heineike
- Rob Willoughby
topics:
- agent-evaluation
- agent-skills
- code-intelligence
- software-agents
- llm-benchmarks
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# A Framework for Evaluating Agentic Skills at Scale

## Summary
## 摘要
论文提出了一种可扩展方法，用于测试 agent 技能是否能在真实编码任务中改善 LLM agent 的行为。该方法从每个技能生成任务和隐藏评分细则，然后比较安装技能与未安装技能时的 agent 运行结果。

## 问题
- Agent 技能用于编码工作流、API 模式、编码约定和领域规则，但作者缺少一种可复用方法来测试单个技能是否改善 agent 输出。
- 现有 agent 基准主要测试通用任务求解、工具使用或编码能力；它们未衡量特定技能如何改变不同模型的行为。
- 这一点会影响生产 agent 系统中的指令遵循、目标完成、成本和模型选择。

## 方法
- 该方法读取一个技能，推断真实使用场景，构建可执行任务，并为目标完成度和指令遵循度创建隐藏评分细则。
- 一个环境工程 agent 会检查所需工具、运行时、凭据、网络访问、代码库、数据库、UI 访问和其他依赖项。
- 一个任务生成 agent 会创建任务描述、输入文件、执行设置和评分细则；一个验证 agent 会移除缺少输入、环境损坏或评分细则泄露的任务。
- 每个任务会求解两次：一次不使用技能，另一次安装相关技能并告知 agent 可用。
- 一个评判模型，即 Claude Code 中的 Sonnet 4.6，会根据 100 分制的指令遵循和 100 分制的目标完成评分细则，对求解器输出打分。

## 结果
- 研究使用了约 500 个真实技能、约 1,000 个生成任务、19 种 agent-模型配置，以及约 38,000 条有效轨迹。
- 访问相关技能会使总体分数提高 5.5 到 22 分，具体幅度取决于模型；大部分增益来自指令遵循。
- 在使用技能时的指令遵循上，报告的最高分为 Opus 4.8 的 88.0、Opus 4.7 的 87.7、Sonnet 4.6 的 85.9、GLM 5.1 的 85.0、Gemini 3.5 Flash 的 81.6，以及 Gemini 3.1 Pro Preview 的 81.5。
- 开放权重模型 GLM 5.1 在指令遵循上达到 85.0，接近顶级专有模型；Kimi K2.6、MiniMax 2.7、Qwen3-Coder-Next 和 Gemini 3.1 Flash Lite 集中在 57–60 左右。
- Nemotron Nano 30B 在使用技能时的指令遵循得分为 25.2，Nemotron Super 120B 得分为 46.8，是报告中最弱的结果。
- 对于 Opus 4.8，指令遵循从 59.8 升至 88.0，目标完成度从 93.3 升至 97.5，总体分数从 76.6 升至 92.7，技能带来的增量为 +16.2；每个场景的成本从 2.66 美元增至 3.26 美元。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.17819v1](https://arxiv.org/abs/2606.17819v1)
