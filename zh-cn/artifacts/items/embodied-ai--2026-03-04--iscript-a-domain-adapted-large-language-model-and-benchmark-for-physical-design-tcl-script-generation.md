---
source: arxiv
url: http://arxiv.org/abs/2603.04476v1
published_at: '2026-03-04T15:20:35'
authors:
- Ning Xu
- Zhaoyang Zhang
- Senlin Shu
- Lei Qi
- Jiaqi Lv
- Wensuo Wang
- Tianhao Zhao
- Chao Zhang
- Zhaoliang Yang
- Xiangyu Li
- Zhaorui Su
- Jingshan Li
- Xin Geng
topics:
- eda-llm
- tcl-generation
- domain-adaptation
- benchmarking
- code-generation
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# iScript: A Domain-Adapted Large Language Model and Benchmark for Physical Design Tcl Script Generation

## Summary
本文提出面向物理设计 Tcl 脚本生成的领域适配模型 iScript，以及首个对应基准 iScript-Bench。核心贡献是在公开数据稀缺、难以真实执行验证的 EDA 场景下，构建了数据合成、训练和评测的一整套可复现流程。

## Problem
- 物理设计流程高度依赖 Innovus Tcl 脚本，但通用大模型对这类**工具专有、语义强耦合、容错要求高**的脚本生成能力很弱。
- 公开可用的 PD Tcl 数据极少，导致训练数据和统一 benchmark 都缺失，模型之间难以公平比较。
- 真实功能验证通常需要商业 EDA 工具执行，成本高且不可复现；仅做语法检查又不足以判断脚本是否满足设计意图。

## Approach
- 基于 **Qwen3-8B** 做领域适配，提出 iScript，训练采用两阶段：先做 **continued pretraining (CPT)** 学习 Innovus Tcl 语法与词汇，再做带 **Chain-of-Thought** 的 **supervised fine-tuning (SFT)** 学习“需求→脚本”的映射。
- 设计多阶段数据合成流水线：从用户指南、命令手册、论坛与社区收集种子数据，抽取命令与参数组合生成脚本，经 **静态 lint** 过滤，再用 **GPT-4.1** 反推需求并生成 CoT，最终得到 **10,000** 条 `(requirement, CoT, script)` 数据。
- 构建 **iScript-Bench**：覆盖 **5** 个主任务类、**25** 个子类、**3** 个难度等级，共 **116** 个测试任务，用于系统评测自然语言到 PD Tcl 的能力。
- 提出两步验证框架：先在轻量 sandbox 中做**静态语法验证**，再用带官方命令知识增强提示的 LLM 做**功能评估**，以替代昂贵的商业工具执行。

## Results
- 在 **iScript-Bench (116 tasks)** 上，iScript 的 **Pass@1** 总体成绩为：**syntax 59.48% / function 18.97%**；对比第二好的 **Gemini**：**31.03% / 14.66%**，分别高出 **28.45** 和 **4.31** 个百分点。
- 在 **Pass@5** 上，iScript 总体达到 **syntax 91.38% / function 46.55%**；对比 **Gemini 73.28% / 39.66%**，分别提升 **18.10** 和 **6.89** 个百分点。
- 分类别看，iScript 在 **DIQA** 上达到 **Pass@5 syntax 100.00%, function 71.43%**；在 **FA** 上达到 **95.45% / 40.91%**；在 **PAO** 上达到 **100.00% / 33.33%**。但在 **NIAA Pass@1 function** 上仅 **10.00%**，弱于 **Gemini/Claude 的 30.00%**，说明并非所有子任务都全面领先。
- 分难度看，iScript 在 **L1** 的 **Pass@1/5 syntax** 为 **66.67% / 94.44%**，在最难 **L3** 上仍有 **61.54% / 88.46%**；对应 **Pass@1/5 function** 为 **11.54% / 19.23%**，说明复杂逻辑下功能正确性依然困难，但其鲁棒性优于多数通用模型。
- 为验证 LLM 功能评估可靠性，作者从 **784** 个语法正确脚本中随机抽取 **100** 个给工程师复核：LLM 判对 **39** 个，人类判对 **42** 个，且 **LLM 判对的 39 个全部包含在人类判对集合中**，表明其自动评估具有接近完美精度、几乎无假阳性。

## Link
- [http://arxiv.org/abs/2603.04476v1](http://arxiv.org/abs/2603.04476v1)
