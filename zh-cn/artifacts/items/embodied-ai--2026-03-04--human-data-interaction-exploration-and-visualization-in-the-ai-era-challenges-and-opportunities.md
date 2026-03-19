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
- human-data-interaction
- visual-analytics
- foundation-models
- multimodal-analytics
- trustworthy-ai
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Human-Data Interaction, Exploration, and Visualization in the AI Era: Challenges and Opportunities

## Summary
这是一篇面向AI时代人机数据交互与可视分析的综述/立场论文，讨论大模型、多模态与非结构化数据如何重塑交互式数据分析系统。论文核心贡献不在提出单一新算法，而在系统化梳理挑战，并主张以人类认知、延迟感知、可信性和端到端协同设计为中心重构系统。

## Problem
- 论文要解决的问题是：在AI时代，交互式数据分析面对**大规模、异构、多模态、非结构化数据**以及**LLM/VLM带来的不确定性**时，现有人机数据交互和可视分析系统为何难以保持高效、可靠、可解释。
- 这很重要，因为分析者需要在不确定条件下反复探索、改写查询并验证中间结果；如果系统延迟过高、可扩展性不足或AI输出不可信，就会破坏推理过程、增加认知负担并削弱人机协作质量。
- 传统只看吞吐量、P95延迟或离线精度的评估方式不足以衡量真实交互体验，尤其当一次交互会触发多个查询、渐进式更新和多模态反馈时。

## Approach
- 这篇论文的核心方法是**观点综述 + 研究议程提出**：从数据库、AI、信息可视化、HCI和计算机图形学多个视角，统一总结AI时代人机数据交互系统的关键瓶颈与开放方向。
- 它主张把数据管理、AI模型、界面和可视化看作一个**端到端共同设计**的整体，而不是彼此松耦合的模块；系统设计应直接考虑界面结构、用户感知和交互上下文。
- 论文强调“**查询速度要接近人类思维速度**”，需要围绕感知对齐延迟、近似计算、预取、索引、渐进式分析和结果细化来设计底层系统。
- 它提出未来界面应走向**多模态、行动导向、混合主动**的交互范式，结合自然语言、手势、AR/VR、叙事式与生成式可视化，并让人始终保留监督、溯源和信任校准能力。
- 对AI部分，论文的基本机制性主张是：大模型很强，但不能替代结构化工具与人类在环验证；因此需要更清晰的系统抽象、可信分析机制和面向不确定性的交互设计。

## Results
- 这不是一篇报告新模型或新基准SOTA的实验论文；**给定摘录中没有提供新的定量实验结果、数据集对比或性能数字**。
- 文中给出的较具体量化观察包括：在IEEE VIS发表论文中，仅**2%**文章使用与“scalability”相关的关键词，用以说明可视化领域对可扩展性的系统性关注不足。
- 论文明确声称交互分析需要满足**毫秒级（order-of-millisecond）**响应，而很多现有数据系统更多针对**秒级或分钟级**响应优化，这种错配会减少观察次数并引入探索偏差。
- 论文还提出，哪怕只是**几秒**的延迟，也可能打断分析推理、改变探索路径并降低人机协作效果。
- 相比给出数值型突破，论文更强的具体贡献是：系统化提出若干研究方向，包括界面-系统协同优化、冷启动与渐进式可视分析、面向多模态/非结构化数据的新交互范式、以及在LLM/VLM参与下的可信分析与可解释反馈机制。

## Link
- [http://arxiv.org/abs/2603.05542v1](http://arxiv.org/abs/2603.05542v1)
