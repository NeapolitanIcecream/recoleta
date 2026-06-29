---
source: arxiv
url: https://arxiv.org/abs/2606.04708v1
published_at: '2026-06-03T10:38:45'
authors:
- Siyuan Yang
- Linzheng Guo
- Ouyang Lu
- Zhaxizhuoma
- Daoran Zhang
- Xinmiao Wang
- Ting Xiao
- Fangzheng Yan
- Zhijun Chen
- Yan Ding
- Chao Yu
- Chenjia Bai
- Xuelong Li
topics:
- vision-language-action
- robot-data-scaling
- umi-data
- fisheye-perception
- trajectory-validation
- robot-foundation-model
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training

## Summary
## 总结
VISTA 通过解决两个失效来源来适配 UMI 手持示教数据用于 VLA 训练：鱼眼腕部相机感知和机器人不可执行的动作轨迹。它把一个 800 万样本的鱼眼 VQA 数据集与轨迹验证和两阶段 VLA 训练结合起来。

## 问题
- UMI 和 FastUMI 让真实机器人数据采集更便宜，也不那么依赖单一机器人，但它们的腕部鱼眼视角与预训练 VLM 主干使用的标准图像不同。
- 人工采集的 UMI 轨迹可能违反目标机器人的关节限位、与机器人本体发生碰撞，或需要机器人无法跟踪的控制器运动。
- 这些问题很重要，因为用原始 UMI 数据训练的 VLA 可能学到无法解析自身腕部相机输入的视觉特征，以及在部署时会失败的动作。

## 方法
- VISTA 构建了 UMI-VQA，这是一个面向腕部鱼眼观测的 800 万样本 VQA 数据集：其中 300 万是真实 UMI VQA 对，500 万是从 RefSpatial 改造得到的鱼眼风格空间多样性样本。
- 真实的 UMI-VQA 划分覆盖物体定位、场景理解、描述生成、交互定位和空间推理，并处理以夹爪为中心的畸变和遮挡。
- 物理验证流程先检查轨迹完整性，然后在训练前对有效轨迹的连续性、自碰撞风险和执行保真度打分。
- 训练分两阶段：先在 UMI-VQA 和已验证动作标记上做联合自回归学习，再用流匹配动作专家进行连续动作细化。
- 预训练集包括 10 万条通过验证的真实 UMI 轨迹，以及 800 万个 UMI-VQA 样本。

## 结果
- 摘要称 VISTA 在 UMI 风格的仿真基准和 20 个真实世界操作任务上超过了 pi-0.5、LingBot-VLA 和 Wall-X，但没有给出成功率或表格数值。
- 评测覆盖两个仿真基准，RoboTwin-UMI 和 LIBERO-UMI，以及 20 个真实世界任务。
- UMI-VQA 包含 800 万个样本：300 万个真实腕部鱼眼 VQA 对和 500 万个空间多样性补充样本。
- 300 万个真实 UMI-VQA 部分的报告分布为：物体定位 84.2 万，27.5%；场景理解 40.6 万，13.2%；描述生成 10.3 万，3.3%；交互定位 89.4 万，29.1%；空间推理 82.4 万，26.9%。
- 硬件使用约 180 度的鱼眼视场，重量约 600 克，并报告约 3 毫米的融合位姿精度。
- 论文报告 UMI-VQA 提升了下游策略性能，且更高的物理验证分数能预测更好的部署结果，但摘要没有给出数值相关性或消融分数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.04708v1](https://arxiv.org/abs/2606.04708v1)
