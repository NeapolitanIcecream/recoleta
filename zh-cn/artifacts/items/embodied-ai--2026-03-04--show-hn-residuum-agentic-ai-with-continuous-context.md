---
source: hn
url: https://github.com/Grizzly-Endeavors/residuum
published_at: '2026-03-04T23:40:51'
authors:
- BearFlinn
topics:
- agent-framework
- continuous-memory
- personal-agent
- multi-channel
- task-scheduling
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Residuum | Agentic AI with continuous context

## Summary
Residuum 是一个“无会话边界”的个人 AI 代理框架，主张让同一个代理在所有渠道中持续保留上下文与记忆。其核心卖点是持续上下文记忆、跨渠道单线程交互，以及将定时主动任务从 LLM 推理中剥离出来以降低成本。

## Problem
- 现有 AI agent 框架通常以**会话**为单位工作：新对话需要重复提供背景，长期连续协作体验差。
- 一些系统用 RAG 或固定记忆文件补丁式解决，但模型仍把每次对话视作孤立事件，导致旧上下文依赖“是否想起来去搜”。
- 主动式 agent 常通过周期性触发完整 LLM 轮次检查待办，造成不必要的 token 消耗和调度开销。

## Approach
- 用**连续线程**替代会话：一个 agent 在 CLI、Discord、webhooks 等所有渠道共享同一条对话主线。
- 将历史对话压缩成始终保留在上下文中的**dense observation log**，近期历史无需检索即可直接被模型利用。
- 对更久远的内容提供**混合检索**（BM25 + 向量嵌入），只在需要完整细节时再回查旧 episode。
- 用**YAML pulse scheduling**定义“检查什么、何时检查、结果发到哪里”，把定时逻辑移出 LLM；仅在任务到期时触发模型，且可用更便宜模型执行。
- 采用文件优先与模块化设计：状态存于可读文件，Memory、Projects、Pulses、Skills 独立组合，并兼容 OpenClaw 技能格式。

## Results
- 文本**未提供正式实验或基准测试结果**，没有数据集、评测指标、消融实验或统计显著性数字。
- 明确的系统性主张包括：**无需会话切换**，同一 agent 可在 CLI、Discord、webhooks 间持续共享上下文。
- 相比 OpenClaw，作者声称其解决了“**两天后上下文记忆悬崖**”问题：旧上下文不会仅因不触发搜索而丢失到工作流之外。
- 相比每 30 分钟触发一次完整 LLM heartbeat 的方案，Residuum 声称通过**结构化 pulse 调度**避免为调度逻辑持续消耗 frontier-model 调用，但**未给出具体 token/成本下降数字**。
- 提供的工程事实包括：支持 Linux（x86_64、aarch64）与 macOS（Apple Silicon），支持 Anthropic、OpenAI、Google、Ollama，并带有 provider failover。

## Link
- [https://github.com/Grizzly-Endeavors/residuum](https://github.com/Grizzly-Endeavors/residuum)
