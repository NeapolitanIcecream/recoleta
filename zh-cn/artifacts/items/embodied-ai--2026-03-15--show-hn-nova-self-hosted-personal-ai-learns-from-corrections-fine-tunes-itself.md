---
source: hn
url: https://github.com/HeliosNova/nova
published_at: '2026-03-15T23:18:18'
authors:
- heliosnova
topics:
- self-hosted-ai
- continual-learning
- dpo-fine-tuning
- personal-memory
- knowledge-graph
- agentic-system
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Nova–Self-hosted personal AI learns from corrections &fine-tunes itself

## Summary
Nova 是一个可自托管的个人 AI 助手，核心卖点是从用户纠正中持续记忆、检索并在积累足够样本后自动进行 DPO 微调。它强调本地运行、数据不出机，以及围绕记忆、知识图谱、工具调用和安全机制构建的完整自改进管线。

## Problem
- 现有助手通常**不会把用户纠正转化为持久能力提升**，同样错误可能反复出现，这影响长期可用性与个性化体验。
- 个人 AI 若依赖云端，会带来**隐私、数据主权和部署控制**问题；对希望本地掌控数据的用户尤其重要。
- 单次对话式问答缺少**系统化学习闭环**：纠错、记忆、知识更新、训练、评估、部署往往彼此割裂。

## Approach
- 核心机制很简单：**用户纠正一次，系统就把“错什么/对什么”存成 lesson，并在后续相似问题时优先检索出来**，从而实现“记住教训”。
- 每次纠正还会自动生成 **DPO 训练对** `{query, chosen, rejected}`，当样本积累到一定规模后，触发**自动微调 → A/B 评估 → 部署**的闭环。
- 系统将对话后的学习拆成多个模块：**纠错检测（regex 预筛 + LLM 确认）**、事实抽取、reflexion 失败反思、curiosity 知识缺口发现、success patterns 正样本收集。
- 为支持长期记忆与检索，Nova 组合使用**会话历史、事实、lessons、skills、时间型知识图谱**，并通过 **ChromaDB 向量检索 + SQLite FTS5 + Reciprocal Rank Fusion** 进行文档召回。
- 工程上它是一个**本地优先、提供商无关**的异步 Python/FastAPI 系统，支持工具循环、MCP 客户端/服务器、自动模型路由和多层安全防护。

## Results
- 文中给出的最具体“效果”是**定性示例**：首次把“澳大利亚首都”答成 Sydney，经用户纠正为 Canberra 后，**3 个月后**再次询问可回答 **Canberra**，说明其声称具备持久记忆能力。
- 资源与部署指标：本地 GPU 模式建议 **NVIDIA GPU 20GB+ VRAM**；量化模式声称可适配 **16GB VRAM**；也支持**无 GPU 的 cloud mode**。
- 工程规模指标：系统提供 **21 个工具**、工具循环最多 **5 轮**、有 **14 个主动监控器**、知识图谱含 **20 个规范谓词**、环境配置 **75+ 项**。
- 测试覆盖指标：作者声称有 **1,443 个测试**，分布于 **57 个文件**，覆盖 brain pipeline、learning loop、tools、security、stress/concurrency、behavioral 和 e2e。
- 安全与架构具体声明：支持 **4 类 prompt injection 检测**、**4 层访问控制**，并默认启用 **HMAC-SHA256 skill signing**。
- **未提供标准基准上的定量模型效果**：没有给出准确率、胜率、A/B 提升幅度、训练后相对基线提升等可复现实验数字，因此其“比其他开源项目独特/更强”的主张目前主要是产品与系统设计层面的声明。

## Link
- [https://github.com/HeliosNova/nova](https://github.com/HeliosNova/nova)
