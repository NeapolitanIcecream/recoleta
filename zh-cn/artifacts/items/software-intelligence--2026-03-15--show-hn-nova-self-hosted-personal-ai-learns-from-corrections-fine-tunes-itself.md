---
source: hn
url: https://github.com/HeliosNova/nova
published_at: '2026-03-15T23:18:18'
authors:
- heliosnova
topics:
- self-hosted-ai
- continual-learning
- dpo-finetuning
- personal-assistant
- knowledge-graph
- agentic-systems
relevance_score: 0.8
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Nova–Self-hosted personal AI learns from corrections &fine-tunes itself

## Summary
Nova 是一个可自托管的个人 AI 助手，核心卖点是把用户纠错转化为持久记忆、训练样本和自动微调，从而在本地持续变聪明。它将检索、工具调用、知识图谱、反思与安全机制整合为一条端到端学习闭环。

## Problem
- 现有助手通常**不会从用户纠错中永久学习**，同样错误会反复出现，这降低了长期个人化与可靠性。
- 云端助手常要求数据外发；对重视隐私、主权和本地控制的个人/开发者，这很重要。
- 个人 AI 若要真正可用，不仅要回答问题，还要能积累记忆、发现知识缺口、并在足够数据后自我改进。

## Approach
- Nova 把一次对话后的“纠错”转成多种可复用资产：**lesson 存储**、**DPO 训练对**、以及知识图谱更新；以后遇到相似问题先检索这些学习结果。
- 推理流水线是工程化的：加载历史/事实/lesson/KG，上层用**规则做意图分类**，再用 **ChromaDB 向量检索 + SQLite FTS5 + Reciprocal Rank Fusion** 召回信息，拼装提示后生成回答，并可进入最多 5 轮工具循环。
- 它在回答后继续做“后台学习”：**correction detection**、**fact extraction**、**reflexion**（静默失败检测）、**curiosity engine**（发现不知道/工具失败并排队研究）、**success patterns**（高分回答正强化）。
- 当积累足够多 DPO 样本后，系统会触发**自动微调**，并在部署前进行 **A/B evaluation**；模型层是 provider-agnostic，可在本地模型或云模型间切换。
- 系统强调自主可控与安全：本地部署、MCP client/server 双角色、动态工具接入、4 类 prompt injection 检测、SSRF 防护、训练数据投毒防护、签名技能与 Docker 加固等。

## Results
- 文中**没有提供标准基准数据集上的定量效果**，也没有给出诸如准确率、胜率、延迟或成本的系统性实验结果。
- 最具体的效果声明是行为示例：被纠正“澳大利亚首都是堪培拉”后，**3 个月后**再次被问同一问题时可回答正确，表明其声称具备**持久学习**能力。
- 项目宣称具备完整自动改进闭环：每次纠错会生成 **1 组 DPO training pair**（`query, chosen, rejected`），并在样本足够后自动执行 **train -> eval -> deploy**。
- 工程规模上，作者给出 **~74 个 async Python 文件**、**21 个工具**、**最多 5 轮工具循环**、**14 个主动监控任务**、**20 个 canonical predicates** 的时序知识图谱，以及 **75+ 配置项**。
- 测试方面，项目声称包含 **1,443 个测试**、覆盖 **57 个文件**，涵盖 brain pipeline、learning loop、tools、channels、security、stress/concurrency、behavioral 与 e2e。
- 部署要求上，完整本地主模型方案需 **NVIDIA GPU 20GB+ VRAM**；同时也声称支持**云模式无 GPU**与**16GB VRAM 的量化模式**。

## Link
- [https://github.com/HeliosNova/nova](https://github.com/HeliosNova/nova)
