---
source: arxiv
url: http://arxiv.org/abs/2603.11103v1
published_at: '2026-03-11T09:23:20'
authors:
- Zhiyuan Zeng
- Yichi Zhang
- Yong Shan
- Kai Hua
- Siyuan Fang
- Zhaiyu Liu
- Jiaheng Liu
- Haozhe Wang
- Yining Zheng
- Ming Ding
- Ke Shen
- Ge Zhang
- Wenhao Huang
- Xipeng Qiu
topics:
- code-pretraining
- synthetic-trajectories
- multi-agent-simulation
- software-engineering
- long-context
- code-llm
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Understanding by Reconstruction: Reversing the Software Development Process for LLM Pretraining

## Summary
本文提出“通过重建来理解”的预训练范式：不再只看代码仓库的最终结果，而是合成其背后的规划、读取、编写与调试轨迹来训练模型。作者表明，用这种重建出的多智能体软件开发轨迹继续预训练 Llama-3-8B，可提升长上下文理解、代码生成和部分代理能力。

## Problem
- 现有代码预训练主要使用**静态仓库快照**，只包含最终代码，丢失了需求分析、架构规划、调试和迭代等关键推理过程。
- 这导致模型更容易学到“表面代码模式”，却难以获得**复杂软件工程所需的长程、因果式推理能力**。
- 该问题重要，因为真实软件开发依赖跨文件依赖、长期上下文和分步决策，决定了代码智能体与自动化软件生产的上限。

## Approach
- 用一个**多智能体模拟框架**把现成高质量仓库“反向展开”为开发轨迹：主智能体先生成项目需求与文件级实现计划，再让子智能体逐文件完成实现。
- 子智能体通过简单的 **Read / Write 工具调用**模拟开发：先读已实现文件获取上下文，再写当前文件代码；整条轨迹包含 Think、Action、Observation。
- 为减少幻觉，方法将**仓库真实结构注入模拟过程**，包括文件树、跨文件依赖图、以及文件内部 AST 结构；并用真实仓库内容替换 Read/Write 的观测与最终代码。
- 进一步用**基于搜索的 CoT 优化**逐步改写推理步骤：若某个替代思维链能降低目标真值代码的困惑度，就保留该改写，从而最大化 \(\log p(x|z)\)。
- 最后把分层多智能体轨迹压平成单个长序列做**持续预训练**，并对 Observation token 做 loss masking，只训练模型预测 Think 和 Action，强化“推理到行动”的因果学习。

## Results
- 数据与训练规模：从约 **300k GitHub 仓库**生成约 **4B token** 的合成轨迹；对 **Llama3-8B-Instruct** 进行 **20B token** 持续预训练，使用 **64k** 上下文窗口。
- 长上下文理解：在 **Ruler 65,536** 上，**Repo2Agent-Search 61.80**，优于 **Raw-Repos 61.00** 和 **Prolong 57.10**；在 **Helmet 32,768** 上，**62.65**，优于 **Raw-Repos 60.98** 与 **Prolong 61.57**。
- 代码能力：在 **HumanEval** 上，**Repo2Agent-Search 37.20**，高于 **Raw-Repos 34.76** 和 **Prolong 16.46**；在 **LongCodeBench-32k** 上，**36.46**，高于 **Raw-Repos 34.16** 与 **Prolong 29.38**。
- 长代码任务并非全面领先：在 **LongCodeBench-64k** 上，**Repo2Agent 31.05** 最好，超过 **Repo2Agent-Search 30.26**、**Prolong 30.52** 与 **Raw-Repos 27.37**，说明搜索优化并非对所有超长代码场景都最优。
- 推理迁移：在 **BBH** 上，**Repo2Agent-Search 67.03**，略高于 **Prolong 66.69** 和 **Raw-Repos 66.27**；在 **MATH** 上，**3.76** 高于 **Repo2Agent 3.72**、**Raw-Repos 2.18** 和 **Prolong 1.64**；但 **GSM-8k** 上未超过 Raw-Repos（**60.96 vs 61.94**）。
- 代理/软件工程基础能力：在 **APTBench Overall Average** 上，**Repo2Agent 30.10** 优于 **Repo2Agent-Search 29.65** 和 **Raw-Repos 29.02**；例如 **Issue-Fix Average 34.84 vs 33.72**，表明未搜索优化的原始轨迹在部分 agentic 软件任务上更强。

## Link
- [http://arxiv.org/abs/2603.11103v1](http://arxiv.org/abs/2603.11103v1)
