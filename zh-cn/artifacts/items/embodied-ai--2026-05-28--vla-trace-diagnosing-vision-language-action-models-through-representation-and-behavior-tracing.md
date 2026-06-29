---
source: arxiv
url: https://arxiv.org/abs/2605.30117v1
published_at: '2026-05-28T15:50:56'
authors:
- Haoyuan Shi
- Xiancong Ren
- Yingji Zhang
- Qinfan Zhang
- Jiayu Hu
- Haozhe Shan
- Han Dong
- Jinpeng Lu
- Yinda Chen
- Yi Zhang
- Yong Dai
- Xiaozhu Ju
topics:
- vision-language-action
- robot-policy-diagnostics
- mechanistic-interpretability
- attention-knockout
- representation-analysis
- semantic-grounding
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# VLA-Trace: Diagnosing Vision-Language-Action Models through Representation and Behavior Tracing

## Summary
## 摘要
VLA-Trace 是一个用于视觉-语言-动作策略的诊断套件，连接表示漂移、基于注意力的因果测试和 rollout 行为。结果显示，π0.5 和 OpenVLA 在动作解码时走的是不同路径，而且两者都难以处理细粒度的语言变化。

## 问题
- VLA 模型可以执行机器人任务，但它们在生成动作时如何使用视觉和语言，难以检查。
- 这很重要，因为表示受损、语言使用薄弱或视觉捷径都会导致策略失败，而常规成功率无法解释这些失败。

## 方法
- 该方法比较三个 checkpoint：预训练的 VLM、预训练的 VLA，以及任务微调后的 VLA。
- 它使用跨模态 CKA 和 checkpoint-drift CKA 来衡量视觉、文本和联合表示在机器人适应过程中的变化。
- 它在推理时阻断选定的注意力路径，测试动作 token 是否依赖图像 token、文本 token 或跨模态 prefill 交互。
- 它运行带有注意力定位、视觉 patch 遮罩和输入编辑的行为探针，测试空间落地、捷径使用和指令遵循。

## 结果
- 在 LIBERO-10 上，π0.5 在全路径基线下达到 93.5% 成功率。去掉生成时的图像访问后降到 0.0%，去掉生成时的文本访问后仍有 39.0% 成功率。
- 在 LIBERO Goal、Spatial 和 Object 上，π0.5 在去掉生成时文本访问后仍保持较高成功率：96.5%、99.0% 和 98.0%。去掉生成时图像访问后分别为 4.0%、0.0% 和 0.0%。
- OpenVLA 在 LIBERO-10 基线上的成功率为 58.0%。去掉生成时文本访问后，在 LIBERO-10、Goal、Spatial 和 Object 上都降到 0.0%；去掉生成时图像访问后分别为 1.0%、16.0%、44.0% 和 32.5%。
- LIBERO-10 上的注意力定位显示，动作注意力与 Robot+Object 区域的重叠比仅与 object 区域的重叠更高。对于 π0.5，full-rollout Robot+Object mass 为 0.6328，IoU90 为 0.2233，hit rate 为 0.6349；对于 OpenVLA，同样的指标分别为 0.5882、0.1965 和 0.9597。
- 视觉遮罩结果显示，π0.5 对可见任务对象依赖很强。在一个设置中，它在 LIBERO-10 上的基线成功率为 75.00%，在 LIBERO-Object 上为 95.60%，在 LIBERO-Spatial 上为 95.80%，在 LIBERO-Goal 上为 80.00%；把目标对象替换成背景后，这些数值平均下降 76.45 个百分点。
- 主要定性结论是，两种模型都能生成有视觉落地的轨迹，但当提示或输入被编辑时，两者在细粒度语义遵循上都有限。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.30117v1](https://arxiv.org/abs/2605.30117v1)
