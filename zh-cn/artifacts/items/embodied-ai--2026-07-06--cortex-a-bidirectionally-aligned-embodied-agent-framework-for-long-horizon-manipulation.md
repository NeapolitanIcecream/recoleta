---
source: arxiv
url: https://arxiv.org/abs/2607.05377v1
published_at: '2026-07-06T17:55:05'
authors:
- Jiaqi Peng
- Xiqian Yu
- Delin Feng
- Yuqiang Yang
- Wenzhe Cai
- Jing Xiong
- Ganlin Yang
- Jinliang Zheng
- Jiafei Cao
- Xueyuan Wei
- Jiangmiao Pang
- Yuan Shen
- Tai Wang
topics:
- vision-language-action
- long-horizon-manipulation
- generalist-robot-policy
- hierarchical-planning
- robot-data-scaling
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Cortex: A Bidirectionally Aligned Embodied Agent Framework for Long-horizon Manipulation

## Summary
## 摘要
Cortex 是一个面向长时程操作的分层机器人系统，可将高层目标转换为 VLA 策略可执行的子任务。论文报告了它在仿真中的提升，以及在端到端 VLA 基线失败的真实零样本化学和清洗任务中的成功结果。

## 问题
- 单体式 VLA 策略根据当前观测作出反应，在长任务中会丢失进度信息，导致重复动作和误差累积。
- 现有规划器-执行器系统经常生成低层机器人策略无法执行的计划，尤其是在子任务缺少物体属性、空间线索或可达性约束时。
- 这个问题很重要，因为清洗实验器皿或执行多步骤化学流程等真实操作任务需要进度记忆、子任务切换和物理可执行性。

## 方法
- Cortex 使用高层 VLM 规划子任务并维护文本记忆，同时由低层 VLA 将当前子任务执行为机器人动作。
- 该接口将计划限制在 32 个标准操作技能原语内，例如 pick、place、stack 和 unscrew，并使用严格的语言模板。
- 作者为超过 4,000 小时的开源视频和真实机器人视频标注子任务元数据，然后加入 30 小时仿真数据，其中包含物体属性、空间标识符、交互次数和考虑可达性的路径安排。
- 训练采用事件均衡采样，让 VLM 看到更多接近子任务边界的帧，因为此时它必须决定是保持当前子任务、更新记忆，还是输出下一个子任务。
- 推理时，Cortex 异步运行 VLM 和 VLA，并通过提示词和后处理规则将 VLM 输出约束在 VLA 技能库内。

## 结果
- 开环 VLM 评估：使用完整约束配置的 Cortex 在步骤级达到 8.318 的平均总分，相比之下 Gemini 为 6.925，Qwen3-VL-8B-Instruct 为 6.739，GPT-5 为 6.268。
- 开环 episode 级评估：使用完整约束配置的 Cortex 平均总分为 7.810，相比之下 GPT-5 为 7.231，Gemini 为 6.860，Qwen3-VL-8B-Instruct 为 6.292。
- LIBERO-Long 零样本仿真：Cortex 成功率达到 95.5%，高于 pi_0.5 的 92.4%、MemoryVLA 的 93.4%、OpenVLA-OFT 的 94.5% 和 Gemini-3.1-Pro 的 91.0%。
- RoboTwin：摘要报告成功率为 86.8%，比单体式 pi_0.5 基线高 4.1 个百分点；长时程划分报告成功率为 88.00%。
- 真实世界 14 步化学任务，20 次试验：Cortex 达到 11.0/14 的平均进度和 65% 的成功率，而 pi_0.5 和 pi_mem 的成功率均为 0%。
- 真实世界 14 步清洗任务，20 次试验：Cortex 达到 10.5/14 的平均进度和 55% 的成功率，而 pi_0.5 和 pi_mem 的成功率均为 0%；使用同类 VLA 策略并由人类控制子任务时，成功率达到 70%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.05377v1](https://arxiv.org/abs/2607.05377v1)
