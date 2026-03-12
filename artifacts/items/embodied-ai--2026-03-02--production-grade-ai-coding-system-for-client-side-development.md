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
- design-to-code
- client-side-development
- prd-understanding
- multimodal-code-generation
relevance_score: 0.05
run_id: materialize-outputs
---

# Production-Grade AI Coding System for Client-Side Development

## Summary
本文提出一个面向真实工业客户端开发的 AI 编码系统，把 Figma 设计稿、PRD 文档和企业工程规范转成可审计的中间产物，再分阶段生成代码。核心贡献是用结构化流水线替代一次性生成，并通过面向 UI 组件的 PRD 拆解显著提升需求理解与实现对齐。

## Problem
- 现有 design-to-code 或代码生成方法常偏向视觉翻译或单次生成，难以同时满足**设计一致性、交互逻辑、企业规范**等生产环境要求。
- 客户端开发输入异构：Figma 提供布局与样式，但缺少行为语义；PRD 有行为描述，但常常**非结构化、含糊、不完整**。
- 真实移动端工程还面临复杂代码库、平台差异、调试成本高、运行时可观测性弱等问题，因此“生成能上线的代码”比普通原型生成更难，也更重要。

## Approach
- 采用**多阶段、产物驱动**流水线：先做上下文规范化，再做任务规划，最后按依赖增量执行代码生成；每一步都保存持久化 artifact，支持审核、恢复和复现。
- 将 **PRD 理解建模为类似 NER 的 UI 组件实体抽取任务**：从 PRD 中识别按钮、输入框、列表等组件，并把逻辑绑定到具体 UI 组件，减少需求与实现错位。
- 对 Figma 做规范化，生成分层设计 IR、样式 token 和组件集合；可选用 YOLO 检测 UI 元素，修正冗余层级并补充显式节点。
- 通过检索增强注入企业知识，如组件使用规则、间距系统、资源规范等，把项目约束显式提供给模型。
- 用 Task IR + sibling DAG + Kahn 拓扑排序组织执行，使任务按依赖可恢复、可追踪地推进，而不是开放式自由生成。

## Results
- 在 PRD 拆解任务上，**文本基线**的 F1 为 **0.568**，经领域微调后提升到 **0.743**；Precision 从 **0.506** 提升到 **0.822**，Recall 从 **0.685** 到 **0.722**。
- **多模态基线**表现很差，F1 仅 **0.211**；经微调后，多模态模型达到 **0.848 F1**，Precision **0.880**、Recall **0.865**，说明任务特化训练是关键。
- 对微调后的多模态模型去掉图像后，F1 从 **0.848** 降到 **0.751**，表明视觉信息对 PRD 到 UI 控件类别识别有明显补充作用。
- 训练数据方面，作者构建了两个专用数据集：**文本集 182 条样本**、**多模态集 182 条样本**，均按 **8:2** 划分训练/测试；最优模型基于 **Qwen2.5-72B-Instruct** 与 **Qwen2.5-VL-72B-Instruct**，采用 **LoRA rank=4**、**30 epochs**。
- 论文还声称端到端评估显示具有**较高 UI fidelity**与**较稳健的交互逻辑实现**，但在给定摘录中除 PRD 拆解外，未提供更多完整的端到端量化表格或与外部方法的详细数值对比。

## Link
- [http://arxiv.org/abs/2603.01460v1](http://arxiv.org/abs/2603.01460v1)
