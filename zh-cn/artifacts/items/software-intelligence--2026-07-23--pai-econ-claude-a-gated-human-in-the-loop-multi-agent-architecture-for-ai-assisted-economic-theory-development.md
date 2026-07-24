---
source: arxiv
url: https://arxiv.org/abs/2607.21268v1
published_at: '2026-07-23T12:40:47'
authors:
- Chen Zhu
- Xiaolu Wang
- Weilong Zhang
topics:
- multi-agent-systems
- human-ai-interaction
- agent-reliability
- quality-gates
- ai-for-social-science
relevance_score: 0.68
run_id: materialize-outputs
language_code: zh-CN
---

# pAI-Econ-claude: A Gated Human-in-the-Loop Multi-Agent Architecture for AI-Assisted Economic Theory Development

## Summary
## 摘要
pAI-Econ-claude 是一种带门控、人在回路中的多智能体工作流，用于在没有自动化系统能够认证正确性的情况下发展经济理论。在五项匹配任务的比较中，盲评评估者在其中四项任务中更偏好带门控的工作流；作者报告的是可审计性的提升，而非形式化验证。

## 问题
- 大语言模型生成的经济理论可能包含与经典模型不匹配、命题过于琐碎、证明存在缺口、福利解释缺乏依据以及引文不可靠等问题。
- 这些错误之所以重要，是因为经济理论需要对制度、假设、均衡概念、机制和福利作出判断，而这些内容无法由一种廉价且机器可读的正确性信号共同检验。

## 方法
- 该工作流使用专门化智能体，通过持久化共享工作区进行协调；每个阶段都会写入可检查的记录，而不是只传递临时消息。
- 九个质量门针对特定失败模式进行诊断并建议回环，但不认证正确性。
- 人类检查点保留对高成本决策的控制权，尤其是均衡概念、命题集合、反例，以及对门控否定结论的回应。
- 经典模型库和理论谱系协议会在模型确定之前，将拟议模型与有名称的经济学传统进行比较。

## 结果
- 在 5 项匹配的经济理论任务中，2 名盲评评估者对全部 5 项成对排名达成一致，并在其中 4 项任务中偏好完整工作流；在 1 项任务中则偏好基线。
- 平均失败严重度从无门控基线的 1.58 降至带门控工作流的 1.16；平均总体有用性则从 2.60 提高到 3.10。
- 最大的收益出现在以下情形：现实检验否定了一个错误的市场结构前提，证明审查促使系统修改了一个错误的福利主张。
- 负面案例表明，该工作流可能过度简化一个具有经济重要性的人力资本机制；尽管存在尚未解决的形式化错误，评估者仍偏好内容更丰富的基线。
- 完整工作流使用的、相对于计划且按滚动五小时计算的用量额度，是配对基线的 4.6 至 18 倍，因此该评估无法证明其具备成本效益。
- 证据支持可审计性的提升和针对性的错误拦截，但不支持形式化正确性认证或可靠的自主理论发展。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.21268v1](https://arxiv.org/abs/2607.21268v1)
