---
source: arxiv
url: http://arxiv.org/abs/2603.11076v1
published_at: '2026-03-10T20:54:23'
authors:
- Aili Chen
- Chi Zhang
- Junteng Liu
- Jiangjie Chen
- Chengyu Du
- Yunji Li
- Ming Zhong
- Qin Wang
- Zhengmao Zhu
- Jiayuan Song
- Ke Ji
- Junxian He
- Pengyu Zhao
- Yanghua Xiao
topics:
- tool-use-agents
- synthetic-data
- ood-generalization
- multi-agent-training
- software-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# DIVE: Scaling Diversity in Agentic Task Synthesis for Generalizable Tool Use

## Summary
DIVE研究如何让工具使用型LLM在陌生任务和陌生工具集上更稳健泛化。核心思想是先真实执行多样化工具收集证据，再从执行轨迹反推可验证、可执行的任务，从而把“多样性”与“数据可靠性”同时做大。

## Problem
- 现有agent任务合成多偏向固定任务族和固定工具集，虽然能提升分布内表现，但在任务分布或工具集变化时容易脆弱，甚至出现负迁移。
- 想提升泛化，训练数据不仅要多，还要在**工具类型、工具组合、工具使用模式**上足够多样；但多样化后又容易出现任务不可执行、不可验证的问题。
- 这很重要，因为真实部署中的agent要面对开放世界工具使用：从通用搜索到金融、医疗、生物、软件工程等专用工具，失败会直接限制实际可用性。

## Approach
- DIVE采用**evidence-first**的反向合成流程：不是先编任务再验证，而是**先运行真实工具**，拿到真实输出和轨迹后，再反推出被这些证据严格蕴含的问答任务。
- 这样做的核心机制很简单：**先有事实证据，再出题**。因此任务天然可执行（因为轨迹已经执行过）且可验证（答案直接来自工具输出）。
- 为了扩大结构多样性，方法沿两个轴扩展：**tool-pool coverage**（更广的工具池）与**per-task toolset variety**（每个任务使用更丰富的工具组合）。
- 作者构建了3类解耦资源池：373个经过验证的真实工具、各领域种子概念池、以及只提供任务形式先验的query exemplars；每轮随机采样工具集、种子和示例。
- 在Evidence Collection–Task Derivation循环中，证据收集器最多执行6步工具调用、循环K=3轮，逐步累积证据并诱导多步工具使用模式；随后用这些任务对Qwen3-8B做48k SFT和3.2k RL训练。

## Results
- 在**9个OOD基准**上，基于DIVE训练的**Qwen3-8B**平均提升**+22分**；并且相对“最强8B基线”声称**提升+68%**。
- 数据规模上，训练使用**48k SFT轨迹 + 3.2k RL任务**；合成来源包含**114k任务池**和另一组**38k任务池**，工具池覆盖**373个工具、5个领域**。
- 相比基座Qwen3-8B，Dive-8B (RL) 在多个OOD基准显著提升：**GAIA 22.4→61.2（+38.8）**，**HLE 6.4→17.8（+11.4）**，**BrowseComp 1.3→16.4（+15.1）**，**Xbench-DS 24.0→58.1（+34.1）**。
- 在专用工具OOD基准上也有明显增益：**Finance Agent Benchmark 2.0→34.0（+32.0）**，**MedAgentBench 38.4→57.3（+18.9）**，**SWE-bench Verified 10.8→18.3（+7.5）**，**Toolathlon 0.9→8.3（+7.4）**。
- 相比自家SFT模型，RL继续带来提升：例如**Dive-Eval 35.4→42.5**，**GAIA 49.3→61.2**，**FinSearchComp-T3 33.0→37.3**，**FAB 28.0→34.0**。
- 论文还声称：在OOD泛化上，**扩展多样性优于单纯扩展数量**，即使数据量少**4×**，多样性扩展仍更有效；这是其最重要的机制性结论之一。

## Link
- [http://arxiv.org/abs/2603.11076v1](http://arxiv.org/abs/2603.11076v1)
