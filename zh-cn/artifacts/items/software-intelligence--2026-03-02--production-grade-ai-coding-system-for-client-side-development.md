---
source: arxiv
url: http://arxiv.org/abs/2603.01460v1
published_at: '2026-03-02T05:17:55'
authors:
- Ruihan Wang
- Chencheng Guo
- Guangjing Wang
topics:
- ai-coding
- client-side-development
- design-to-code
- prd-understanding
- multi-stage-pipeline
- code-generation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Production-Grade AI Coding System for Client-Side Development

## Summary
本文提出一个面向真实客户端开发的生产级 AI 编码系统，把 Figma 设计稿、自然语言 PRD 和企业工程规范转成可审计的中间产物，再分阶段生成代码。核心价值在于它不是“一次性写代码”，而是把需求理解、规划、执行拆开，从而更稳定地满足生产要求。

## Problem
- 要把 **设计稿 + PRD + 企业规范** 一起转成可上线的客户端代码很难；现有 design-to-code 往往只重视觉翻译或单次生成，难以可靠实现交互逻辑。
- PRD 是非结构化、含糊且不完整的，而 Figma 只描述 UI 结构和样式、不包含行为语义；两者脱节会导致代码与产品需求不一致。
- 客户端开发还有平台碎片化、深层代码库、调试慢、运行时可观测性差等工程约束，所以生成错误的代价比很多 web/server 场景更高。

## Approach
- 采用 **多阶段、产物驱动** 的流水线：先做上下文规范化，再做任务规划，最后做可恢复的执行编排；每一步都产出持久化 artifact，便于人工审核、追踪和失败恢复。
- 将 Figma 转成设计 IR，将 PRD 转成“requirement understanding”结构化产物，并注入企业知识库中的组件使用规范、间距/资源等工程规则。
- 把 **PRD 理解建模为类似 NER 的 UI 组件实体抽取问题**：先识别 PRD 中涉及的 UI 组件，再把对应逻辑锚定到具体组件上，减少开放式推理带来的偏差。
- 使用两层 agent 架构：IDE 中的 coding agent 负责推理与改代码，后端 capability server 负责规范化、规划和编排；执行阶段用 Task IR + 依赖 DAG + 拓扑排序来按步骤落地代码修改。
- 为提升 PRD 分解能力，作者基于真实 PRD 自建数据集，对 Qwen2.5-72B / Qwen2.5-VL-72B 进行了 LoRA 微调；文本和多模态数据集各含 182 个样本，按 8:2 划分。

## Results
- **PRD 分解文本设置**：F1 从 **0.568** 提升到 **0.743**；Precision 从 **0.506** 提升到 **0.822**，Recall 从 **0.685** 到 **0.722**。这说明领域微调显著增强了从 PRD 中识别 UI 控件类别的能力。
- **PRD 分解多模态设置**：F1 从 **0.211** 提升到 **0.848**；Precision 从 **0.202** 提升到 **0.880**，Recall 从 **0.256** 提升到 **0.865**。相较未微调多模态基线，提升非常大。
- **视觉信息贡献**：对已微调多模态模型，去掉图像后 F1 从 **0.848** 降到 **0.751**，表明 PRD 中的截图/草图等视觉线索对 UI 控件类别识别有明显帮助。
- 数据与训练设置方面：文本与多模态数据集各 **182** 条，最佳模型使用 **LoRA rank=4**、训练 **30 epochs**，运行在 **4×H20 GPU** 环境。
- 论文还声称端到端评估显示其在真实案例中具有较高 **UI fidelity** 和较稳健的 **interaction logic** 实现，但当前摘录未给出 UI fidelity 研究的完整量化数字或与具体 baseline 的详细对比。

## Link
- [http://arxiv.org/abs/2603.01460v1](http://arxiv.org/abs/2603.01460v1)
