---
source: arxiv
url: https://arxiv.org/abs/2606.27295v1
published_at: '2026-06-25T17:13:02'
authors:
- Tao Lin
- Yuxin Du
- Yiran Mao
- Zewei Ye
- Yilei Zhong
- Bing Cheng
- Yiming Wang
- Jiting Liu
- Yang Tian
- Junchi Yan
- Feiran Wu
- Zenan Meng
- Hu Wei
- Yuqian Fu
- Gen Li
- Bo Zhao
topics:
- vision-language-action
- robot-pretraining
- language-action
- robot-data-scaling
- manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# LA4VLA: Learning to Act without Seeing via Language-Action Pretraining

## Summary
## 概要
LA4VLA 在标准 VLA 训练前，先用语言、本体感知和动作训练机器人策略，让策略在没有图像捷径的情况下学习由指令条件化的运动模式。它从 DROID 构建了 33,116 个经人工验证的语言-动作 episode，并报告一个 1B 参数 VLA 模型在仿真和真实世界任务中的成功率更高。

## 问题
- 标准 VLA 预训练给每条长轨迹分配一条高层指令，但包含数百个图像-动作对，因此语言-动作监督相比视觉-动作监督更稀疏。
- 论文的诊断实验显示，标准 VLA 策略在图像配对正确时能遵循方向，但在图像被移除、不匹配或冲突时会失败；这一点会影响真实机器人场景，因为真实场景在视角、背景、光照、布局和物体外观上会变化。

## 方法
- LA4VLA 将已有专家示范拆分为短的原子动作片段，例如抓取、抬起、放低、搬运、按压、旋转和重新定向。
- 一个 Qwen-3-VL-Plus 分割流水线使用采样视频帧、机器人状态关键帧提示、原语定义和原始任务指令，提出片段边界和低层动作描述。
- 人工标注员对候选片段按 0 到 3 分打分，并保留得分至少为 2 的片段。
- 最终的 LA 预训练输入移除图像，保留低层指令、本体感知状态和动作轨迹；论文测试了仅 LA、先 LA 后 VLA 的顺序预训练，以及混合 LA-VLA 预训练。

## 结果
- 数据集从 9,560 个 DROID VLA episode 开始，生成 56,899 个由 VLM 产生的候选片段；验证后保留 33,116 个 LA episode，共 1,524,990 帧。
- 每个 episode 的平均帧数从原始 VLA episode 的 287.83 降至最终 LA episode 的 46.05，得到更短且绑定到局部动作指令的片段。
- 在 100 个方向跟随诊断案例中，配对视觉输入达到 DAR 0.98 和 DCS 0.95；移除视觉输入后降至 DAR 0.63 和 DCS 0.16；冲突视觉输入下降到 DAR 0.35 和 DCS 0.03。
- LA4VLA-1B 报告在 MetaWorld 上的平均成功率为 87.53%，在 LIBERO 上为 96.28%，在真实世界操作任务上为 83.3%。
- 混合 LA-VLA 预训练相较于无预训练基线，使 LA4VLA-1B 在 MetaWorld 上提高 17.80 个百分点，在 LIBERO 上提高 3.43 个百分点，在真实世界任务上提高 45.0 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.27295v1](https://arxiv.org/abs/2606.27295v1)
