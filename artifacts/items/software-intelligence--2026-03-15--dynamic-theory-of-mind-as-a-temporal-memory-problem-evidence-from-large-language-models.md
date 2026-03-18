---
source: arxiv
url: http://arxiv.org/abs/2603.14646v1
published_at: '2026-03-15T22:54:03'
authors:
- Thuy Ngoc Nguyen
- Duy Nhat Phan
- Cleotilde Gonzalez
topics:
- theory-of-mind
- temporal-memory
- llm-evaluation
- human-ai-interaction
- belief-tracking
relevance_score: 0.74
run_id: materialize-outputs
---

# Dynamic Theory of Mind as a Temporal Memory Problem: Evidence from Large Language Models

## Summary
本文将动态心智理论（ToM）重新定义为一个**时间记忆与检索**问题，而不只是某一时刻的静态信念判断。作者提出 DToM-Track 基准，发现大语言模型通常更擅长判断**当前信念**，却难以回忆**更新前的旧信念**。

## Problem
- 现有 ToM 评测大多聚焦静态的“此刻某人相信什么”，忽视了真实交互中信念会随时间被维护、更新和回忆。
- 这很重要，因为在人机长期互动中，系统不仅要理解用户当前想法，还要追踪其过去想法、何时改变、为何改变。
- 作者关注的核心难点是：LLM 是否能表示并检索**信念轨迹**，而不只是根据最新上下文推断当前状态。

## Approach
- 提出 **DToM-Track**：一个用于多轮对话中时序信念推理的评测框架，专门测试三类动态能力：**pre-update**（更新前信念回忆）、**post-update**（更新后当前信念推断）、**update-detection**（识别信念何时改变）。
- 使用受控的 **LLM-LLM 对话生成**：代理在每轮发言前有隐藏的 inner speech（内心表征），从而制造信息不对称，模拟 ToM/错误信念场景。
- 在预定轮次显式注入信念更新，并用 belief tracker 记录信念类型、来源轮次、是否被覆盖、更新前内容，以构造时间敏感问题。
- 通过多阶段 LLM 过滤验证：检查计划中的信念更新是否真的在对话中实现、问答是否可回答且选项质量合格，得到最终数据集。
- 在 6 个模型上进行 zero-shot 多项选择评测，覆盖 3B–70B、开源与闭源模型。

## Results
- 最终 **DToM-Track** 数据集包含 **5,794** 道题，覆盖 **6** 类问题与 **5** 类心理状态；其中 temporal **1,807 (31.2%)**、false belief **1,761 (30.4%)**、second-order **768 (13.3%)**、update detection **591 (10.2%)**、post-update **527 (9.1%)**、pre-update **340 (5.9%)**。
- 总体准确率范围为 **35.7%–63.3%**，均高于四选一随机基线 **25%**；最佳模型是 **LLaMA 3.3-70B: 63.3%**，最低是 **LLaMA 3.2-3B: 35.7%**，GPT-4o-mini 为 **55.1%**。
- 按题型平均表现：**update-detection 67.5%** 最高，**post-update 63.9%** 次之，但 **pre-update 27.7%** 显著最低，说明模型能抓住“现在信什么”，却难回忆“之前信什么”。
- 与标准 ToM 任务相比，动态回忆更难：**pre-update 27.7%** 明显低于 **false belief 44.7%**，表明“追踪信念演化”是不同于经典错误信念推理的独立挑战。
- 具体模型上也存在明显“近因偏置”：例如 **GPT-4o-mini** 的 post-update / pre-update 为 **68.5% / 27.6%**，**LLaMA 3.3-70B** 为 **71.3% / 40.9%**，**LLaMA 3.1-8B** 为 **57.9% / 12.1%**。
- 作者的最强主张是：这种“当前信念强、旧信念弱”的不对称现象跨模型家族和规模都存在，符合认知科学中的**recency bias** 与**interference**解释，说明动态 ToM 受限于时间表征与记忆检索，而不只是模型参数规模。

## Link
- [http://arxiv.org/abs/2603.14646v1](http://arxiv.org/abs/2603.14646v1)
