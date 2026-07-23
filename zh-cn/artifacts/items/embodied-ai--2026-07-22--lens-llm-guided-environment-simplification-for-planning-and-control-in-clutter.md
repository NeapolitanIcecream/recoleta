---
source: arxiv
url: https://arxiv.org/abs/2607.19633v1
published_at: '2026-07-22T00:05:00'
authors:
- Aileen Liao
- Rachel Holladay
- Dinesh Jayaraman
- Michael Posa
topics:
- robot-manipulation
- scene-abstraction
- llm-guided-planning
- vision-language-action
- cluttered-environments
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# LENS: LLM-guided Environment Simplification for Planning and Control in Clutter

## Summary
## 摘要
LENS 使用由大语言模型引导的闭环抽象层，在杂乱的操作场景中进行规划或控制之前，移除或合并与任务无关的物体。论文报告称，该方法提高了 TAMP、接触隐式模型控制和 π0.5 视觉-语言-动作模型的成功率与可扩展性，但所提供的摘录未包含部分硬件和 VLA 结果细节。

## 问题
- 杂乱环境会增加物体数量、接触、碰撞约束、决策分支和视觉干扰因素，使经典规划器和学习型机器人策略变得更慢、更不可靠。
- 现有场景抽象通常需要针对任务手工设计启发式规则，创建成本高，且难以适应不同任务和布局。
- 这会影响实际部署，因为即使大多数物体与任务无关，下游系统仍会继承非结构化真实场景的全部复杂性。

## 方法
- GPT-4o 根据任务描述和场景表示识别相关物体，并将可以视为同一实体的物体进行分组。
- LENS 剪除无关物体，并将具有功能耦合或动态耦合关系的物体合并为复合实体，同时保守地保留物理表示。
- 精简后的场景被原样传入 TAMP 系统、C3+ 接触隐式控制器或 π0.5 VLA 模型；对于 VLA，剪除操作会生成一张移除干扰物后的图像，并对相应区域进行修复填充。
- 如果执行超时或失败，LENS 会结合失败反馈再次向 VLM 发起查询并修改抽象；在报告的 TAMP 实验中，最多进行两轮反馈迭代。

## 结果
- VLM 查询平均耗时 1.76 秒，论文称相对于执行时间可以忽略不计，因此未将其计入运行时间比较。
- 在基于模型的控制实验中，LENS-C3+ 在 45 次试验中成功 39 次，而完整场景基线在 30 次试验中成功 17 次。
- 当物体数量为 6 个时，基线 C3+ 控制器的运行时间约为 1,000 秒，比 LENS 高出约一个数量级；当物体数量为 7 个时，基线运行时间超过 4,000 秒，而 LENS 仍保持在约 40–135 秒的范围内。
- TAMP 在轻度杂乱、重度杂乱以及带堆叠物体的杂乱环境中进行了 50 个回合的评估。LENS 在轻度杂乱环境中的收益有限，但在更严重的杂乱环境中优于基线；基线在这些环境中经常超时。由于提供的文本未重现图表数据，无法获得精确的成功率数值。
- 论文称，LENS 在仿真和硬件实验中都提升了 π0.5 VLA 的表现，但摘录未包含相应的表格数值或硬件成功率。
- 报告结果支持 LENS 在所测试的桌面任务中提升可扩展性和鲁棒性，但尚不足以证明其在更广泛的机器人本体、环境或实验范围之外的任务中的表现。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.19633v1](https://arxiv.org/abs/2607.19633v1)
