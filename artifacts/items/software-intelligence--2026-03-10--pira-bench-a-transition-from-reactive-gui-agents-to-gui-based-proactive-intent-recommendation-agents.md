---
source: hf_daily
url: https://huggingface.co/papers/2603.08013
published_at: null
authors: []
topics:
- gui-agents
- multimodal-llm
- proactive-assistance
- benchmark
- intent-recommendation
relevance_score: 0.86
run_id: fa4f5d9d-bee2-47ee-b80f-c690622f57d0
---

# PIRA-Bench: A Transition from Reactive GUI Agents to GUI-based Proactive Intent Recommendation Agents

## Summary
### TL;DR: 该论文提出 **PIRA-Bench**，用于评测多模态大模型是否能从连续GUI视觉轨迹中**主动预测用户意图并给出推荐**，并提供一个带记忆与状态跟踪的基线框架 **PIRF** 来处理长时程、噪声和多任务交织的屏幕操作。

### Problem:
- 现有GUI agents大多是**被动式**：必须等待用户明确下指令，无法像真正的智能助手那样主动预判需求。
- 真实屏幕使用过程是**连续且混乱的**：包含长轨迹、无意义浏览、噪声操作、以及多个任务线程来回切换，远比传统单步GUI任务复杂。
- 缺少专门评测“**基于连续视觉输入的主动意图推荐**”能力的基准，导致这类能力难以系统比较和推进。

### Approach:
- 提出 **PIRA-Bench**：一个面向主动GUI agent的benchmark，输入是**连续截图/视觉轨迹**，而非单次明确指令。
- 数据设计强调**弱监督、长时程、多意图交织、噪声片段和用户画像上下文**，要求模型在复杂环境中识别“何时该推荐、推荐什么”。
- 提出 **PIRF** 作为基线：一个**记忆感知、状态跟踪**框架，用于帮助通用MLLM管理多个任务线程并过滤误导性视觉输入。
- 核心机制可简单理解为：让模型一边“看连续屏幕历史”，一边“记住用户当前可能在做什么”，再在合适时机提出候选意图或动作建议。

### Results:
- 论文的摘要/节选中**未提供具体量化结果**，没有给出准确率、成功率、数据规模或相对基线提升数字。
- 最强的具体主张是：**PIRA-Bench** 专门覆盖传统reactive GUI数据集不具备的场景，包括**多意图交织**、**噪声段**和**用户偏好上下文**。
- 另一个核心主张是：**PIRF** 能帮助通用MLLM在复杂屏幕轨迹中进行**多线程任务管理**并处理**误导性视觉输入**。
- 作者将该工作定位为迈向**稳健的、主动式GUI个人助理**的初步基础设施，而非已在摘要中展示大幅SOTA数字提升的结果论文。

## Links
- Canonical: https://huggingface.co/papers/2603.08013
