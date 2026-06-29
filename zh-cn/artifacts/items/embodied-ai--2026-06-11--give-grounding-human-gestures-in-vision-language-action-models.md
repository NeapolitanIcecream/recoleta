---
source: arxiv
url: https://arxiv.org/abs/2606.13435v1
published_at: '2026-06-11T14:59:38'
authors:
- Pengfei Liu
- Gen Li
- Junqiao Fan
- Boyu Ma
- Jindou Jia
- Yang Xiao
- Jianfei Yang
topics:
- vision-language-action
- human-robot-interaction
- gesture-grounding
- robot-manipulation
- foundation-model-adaptation
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# GIVE: Grounding Human Gestures in Vision-Language-Action Models

## Summary
## 摘要
GIVE 为预训练的视觉-语言-动作策略加入了对人类手势的理解，用于机器人递交任务。它之所以重要，是因为只靠文本的指令跟随会漏掉指向和张开手掌这类线索，进而导致目标选错和交互失败。

## 问题
- 现有 VLA 策略通常把操作当作纯文本驱动任务。
- 在人机交互中，手势往往包含目标物体和任务状态信息。
- 语言指令含糊或信息不足时，意图落地会出错，执行也会失败。

## 方法
- GIVE 在不改基础策略架构的前提下加入手势信息。
- 它使用一条视觉路径，把手部骨架和指向时的指尖射线叠加到机器人相机图像上。
- 它使用一条语义路径，调用预训练 VLM，把稳定手势转成一个简短文本元组，包含手势类型和执行指令。
- 语义输出按阶段缓存，物体名称保持泛化，让视觉路径负责目标落地。
- 增强后的图像和文本输入到一个预训练的 \u0003c0_0.5 VLA 策略中，该策略用流匹配动作目标训练。

## 结果
- 在搭载 Galaxea R1-Lite 双臂机器人的真实抓取后递交试验中，GIVE 达到 86.7% 的 Identify SR、80.0% 的 Grasp SR、80.0% 的 React SR 和 80.0% 的 Handover SR。
- 基线 \u0003c0_0.5 的 Identify SR 为 46.7%，Grasp SR 为 6.7%，React SR 为 3.3%，Handover SR 为 0.0%。
- 论文报告，相比基线，目标物体识别准确率提高了 40%，整体任务成功率提高了 80%。
- 在视觉-语义消融中，只用关键点时 Identify SR 为 56.7%，关键点加射线时为 70.0%，完整的视觉加语义系统则达到 86.7% 的 Identify SR。
- 在语义解析中，视觉叠加让目标落地准确率在 20 次试验中从 40.0% 提升到 90.0%。
- 在未见过的参与者上，GIVE 对已见参与者、未见参与者 A 和未见参与者 B 的 Identify SR 分别为 8/10、8/10 和 6/10，而基线分别为 4/10、1/10 和 0/10。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.13435v1](https://arxiv.org/abs/2606.13435v1)
