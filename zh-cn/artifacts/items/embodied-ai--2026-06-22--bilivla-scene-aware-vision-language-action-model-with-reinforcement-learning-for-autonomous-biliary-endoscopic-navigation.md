---
source: arxiv
url: https://arxiv.org/abs/2606.23531v1
published_at: '2026-06-22T16:11:15'
authors:
- Jinsong Lin
- Chi kit Ng
- Zhiyong Xiong
- Zikang Pan
- Yihan Hu
- Tabassum Tamima
- Ziyi Hao
- Eddie Cheung
- Jiewen Lai
- Huxin Gao
- Hongliang Ren
topics:
- vision-language-action
- surgical-robotics
- endoscopic-navigation
- reinforcement-learning
- robot-policy
- medical-robotics
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# BiliVLA: Scene-Aware Vision-Language-Action Model with Reinforcement Learning for Autonomous Biliary Endoscopic Navigation

## Summary
## 摘要
BiliVLA 是一种用于在体模中自主完成 ERCP 内镜导航的视觉-语言-动作策略。它把目标识别、边界框定位和 3-DoF 电机指令结合在一起，并通过监督微调和 GRPO 改进策略。

## 问题
- ERCP 插管需要在狭窄的单目视野中保持稳定导航，而该视野常有眩光、遮挡、组织接触和解剖差异。
- 现有机器人系统或视觉系统常把感知、规划和控制分开；当目标外观变化或视野变差时，这种方式可能失效。
- 更安全的自主导航很重要，因为反复插管会增加临床风险，包括 ERCP 后胰腺炎。

## 方法
- 模型接收一张内镜图像和一条特定阶段的指令，输出三项内容：目标类别、归一化边界框和离散动作。
- 机器人动作空间包含 11 个运动基元：8 个弯曲方向、前进、后退和停止，并映射到用于尖端弯曲以及插入或回撤的 3 DoF 驱动。
- 作者用来自 ERCP 体模装置的 1 万个图像-运动配对构建 BiliVLA-Motion：3000 个入口导航样本、2600 个管腔穿行样本和 4400 个结石定位样本。
- 场景感知监督把每条指令与目标类别和输出模式绑定，让策略学习在每个 ERCP 阶段应寻找哪种结构。
- 安全感知标签把接触壁面的帧设为全图边界框和后退指令，训练策略在视野显示危险近距离时回撤。
- 训练分为两个阶段：先用定位和动作标签对 Qwen3-VL-8B 进行 LoRA 监督微调，再用 GRPO，并以边界框 IoU、动作正确性和输出格式有效性作为奖励。

## 结果
- 在覆盖三个 ERCP 子任务的真实体模实验中，BiliVLA 报告的总体 mIoU 为 0.9625，动作精度为 91.96%，成功率为 84.85%。
- 与 EndoVLA 相比，总体动作精度从 84.44% 提高到 91.96%，成功率从 58.86% 提高到 84.85%。
- 与 Qwen3-VL 相比，总体成功率从 51.82% 提高到 84.85%，总体 mIoU 从 0.8117 提高到 0.9625。
- GRPO 使完整模型优于未使用 GRPO 的 BiliVLA：成功率为 84.85% 对 63.64%，动作精度为 91.96% 对 89.00%，mIoU 为 0.9625 对 0.9488。
- 按任务划分，完整模型的入口导航 mIoU 为 0.9162，PR 为 90.82%，SR 为 72.73%；管腔穿行 mIoU 为 0.9630，PR 为 91.46%，SR 为 100.00%；结石定位 mIoU 为 0.9816，PR 为 92.55%，SR 为 81.82%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23531v1](https://arxiv.org/abs/2606.23531v1)
