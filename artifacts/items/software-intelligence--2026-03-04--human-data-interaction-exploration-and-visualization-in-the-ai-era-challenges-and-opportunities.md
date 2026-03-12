---
source: arxiv
url: http://arxiv.org/abs/2603.05542v1
published_at: '2026-03-04T14:18:17'
authors:
- Jean-Daniel Fekete
- Yifan Hu
- Dominik Moritz
- Arnab Nandi
- Senjuti Basu Roy
- Eugene Wu
- Nikos Bikakis
- George Papastefanatos
- Panos K. Chrysanthis
- Guoliang Li
- Lingyun Yu
topics:
- human-ai-interaction
- visual-analytics
- multimodal-data
- foundation-models
- interactive-data-systems
relevance_score: 0.42
run_id: materialize-outputs
---

# Human-Data Interaction, Exploration, and Visualization in the AI Era: Challenges and Opportunities

## Summary
这是一篇立场型/综述型论文，讨论 AI 时代下人—数据交互、探索与可视化系统面临的新挑战，并提出面向未来的人本研究方向。核心观点是：传统以吞吐和平均延迟为中心的设计已不够，需要把系统、接口、AI 模型与可视化作为一个协同整体来重构。

## Problem
- 论文要解决的是：在 **大规模、异构、多模态、非结构化数据** 与 **LLM/VLM 等基础模型** 普及后，现有交互式数据分析系统为何难以继续支持高质量的人类分析与决策。
- 这很重要，因为分析过程要求 **接近人类思维速度的响应**；哪怕几秒级延迟，也会打断推理、减少观察次数、引入探索偏差，并削弱人机协作效果。
- 另一关键问题是 AI 带来的 **不确定性、错误传播、偏差、不可解释性与验证成本**，使得用户更难信任和校准 AI 生成的分析结果。

## Approach
- 这不是提出单一算法的实验论文，而是提出一个 **端到端的人本框架**：把数据管理、AI 组件、交互界面与可视化视为紧耦合系统，联合设计而不是分开优化。
- 论文强调从传统“把界面当作 SQL 工作负载”升级为 **界面/感知约束驱动的系统设计**：不仅优化查询快慢，还要考虑哪些视图先更新、哪些结果必须同步、用户感知到的延迟是否流畅。
- 对多模态与 AI 分析，作者主张采用 **渐进式计算、近似查询、预取、索引、接口感知优化、混合主动式交互** 等机制，让系统先快速给出可用反馈，再持续细化结果。
- 在交互层面，论文主张发展 **自然语言、手势、AR/VR、叙事型与生成式可视化** 等新界面，并把可视化从“被动输出”变成支持探索、验证、注意力引导与信任校准的主动组件。
- 在人机分工上，核心机制可简单理解为：**AI 负责生成候选理解与操作建议，人类负责监督、验证、纠错与最终判断**，系统则负责让这一循环足够快、透明和可信。

## Results
- 该文从给定摘录看是 **综述/前瞻论文**，**没有报告新的实验数据、基准数据集或量化 SOTA 指标**。
- 文中给出的最明确量化信号之一是：在 IEEE VIS 会议论文中，**只有 2%** 的文章使用与“scalability（可扩展性）”相关的关键词，用以说明可视化领域对可扩展性的系统性关注仍不足。
- 论文明确声称交互分析需要 **毫秒级（order-of-millisecond）** 响应，而许多现有数据系统仍面向 **秒级甚至分钟级** 响应；这种时间尺度错配会降低探索效率并带来偏差。
- 论文还提出强主张：未来系统应支持 **大规模、多模态、非结构化数据** 与 **基础模型不确定性** 下的交互分析，但摘录中未提供对应的定量验证结果。
- 因而本文的主要“突破”不在于数值提升，而在于提出一套跨数据库、可视化、HCI、AI 的 **统一问题框架与研究议程**。

## Link
- [http://arxiv.org/abs/2603.05542v1](http://arxiv.org/abs/2603.05542v1)
