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
- tool-use-llm
- synthetic-data
- ood-generalization
- agent-training
- task-synthesis
relevance_score: 0.41
run_id: materialize-outputs
---

# DIVE: Scaling Diversity in Agentic Task Synthesis for Generalizable Tool Use

## Summary
Dive是一种用于训练工具使用型LLM的数据合成方法，核心思想是先真实调用工具收集证据，再从执行轨迹反向生成任务，从而同时提升多样性与可验证性。论文表明，在广泛OOD基准上，增加“任务/工具多样性”比单纯增加数据量更能提升泛化。

## Problem
- 现有工具使用LLM的后训练常依赖合成任务，但这些任务通常局限于固定任务族和固定工具集，导致模型在新任务、新工具集下泛化差，甚至出现负迁移。
- 想提升泛化，训练数据必须既**多样**，又要**可执行、可验证**；但越追求多样性，越容易生成不可解或不可验证的任务。
- 现有方案要么依赖昂贵的专用流水线抽取数据，要么依赖不稳定的模拟工具，要么采用“先写任务再验真”的流程，都会带来质量与扩展性的瓶颈。

## Approach
- 提出**evidence-first**合成：不是先写问题，而是先在真实工具上执行，收集真实返回结果，再只从这些证据中反推可回答的问题与标准答案，因此“可执行、可验证”是由构造保证的。
- 通过三个解耦资源池扩大多样性：**373个已验证工具**（覆盖通用+4个专家领域）、每个领域约**5,000个seed实体**、以及来自多种任务家族的query-only exemplars。
- 每轮合成随机采样一个配置：seed、**15–50个工具**组成的工具子集、以及**3–5个示例**；随后运行“证据收集—任务推导”闭环，最多进行**K=3**轮迭代，以诱导多步、异构的工具使用模式。
- 训练上采用两阶段：先用合成任务做SFT冷启动，再在有参考答案的任务上做RL；论文使用**Qwen3-8B**为骨干，SFT数据为**48k**轨迹，RL数据为**3.2k**前沿任务。

## Results
- 论文宣称：用Dive数据训练**Qwen3-8B**后，在**9个OOD基准**上的平均成绩提升**+22分**，并且相对“最强8B基线”取得**+68%**的优势（来自摘要的总体结论）。
- 具体看主结果表，**Qwen3-8B (base)** 到 **Dive-8B (RL)** 的提升显著：GAIA **22.4→61.2**（+38.8），HLE **6.4→17.8**（+11.4），BrowseComp **1.3→16.4**（+15.1），Xbench-DS **24.0→58.1**（+34.1）。
- 在领域/专用工具OOD上也有提升：FinSearchComp-T2 **28.6→67.3**（+38.7），T3 **7.1→37.3**（+30.2），Finance Agent Benchmark **2.0→34.0**（+32.0），MedAgentBench **38.4→57.3**（+18.9），SWE-bench Verified **10.8→18.3**（+7.5），Toolathlon **0.9→8.3**（+7.4）。
- 与8B基线比较，Dive-8B (RL) 在多数基准上明显更强，例如对 **WebExplorer-8B**：GAIA **61.2 vs 50.0**，FinSearchComp-T2 **67.3 vs 35.9**，Finance Agent Benchmark **34.0 vs 4.0**；对 **EnvScaler-8B**：GAIA **61.2 vs 25.8**，SWE **18.3 vs 11.5**，Toolathlon **8.3 vs 2.2**。
- SFT到RL也进一步带来增益：Dive-8B从SFT到RL在Dive-Eval **35.4→42.5**，GAIA **49.3→61.2**，HLE **13.8→17.8**，MedAgentBench **50.2→57.3**，说明多样化数据还能放大RL收益。
- 摘要还给出一个关键分析结论：**多样性扩展优于数量扩展**，即使数据量少**4×**，在OOD泛化上仍优于单纯堆更多数据；但摘录中未提供该分析的更细颗粒数值。

## Link
- [http://arxiv.org/abs/2603.11076v1](http://arxiv.org/abs/2603.11076v1)
