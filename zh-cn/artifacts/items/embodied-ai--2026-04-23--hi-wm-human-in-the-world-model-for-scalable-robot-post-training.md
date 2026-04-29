---
source: arxiv
url: http://arxiv.org/abs/2604.21741v1
published_at: '2026-04-23T14:42:54'
authors:
- Yaxuan Li
- Zhongyi Zhou
- Yefei Chen
- Yanjiang Guo
- Jiaming Liu
- Shanghang Zhang
- Jianyu Chen
- Yichen Zhu
topics:
- world-models
- robot-post-training
- human-in-the-loop
- vision-language-action
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training

## Summary
## 摘要
Hi-WM把学习得到的世界模型作为测试机器人策略、由人类纠正错误、再用这些纠正数据改进策略的环境。论文称，这种方法能降低通用机器人策略后训练的成本，同时提高操作任务中的真实世界成功率。

## 问题
- 预训练的通用机器人策略在特定任务场景、高接触操作和长时程执行中仍会失败，因此在部署前还需要后训练。
- 标准的人类纠正式后训练成本很高，因为每次纠正都需要占用真实机器人时间，并进行场景搭建、重置和人工监督。
- 以往关于世界模型的工作主要把模型用于轨迹生成或评估，而不是把它作为一个交互环境，在接近失败的状态附近收集人类纠正数据。

## 方法
- Hi-WM先在动作条件世界模型中而不是真实机器人上闭环运行当前策略，然后只在轨迹变得错误或可能失败时请求人类介入。
- 该世界模型在14维连续双臂动作空间上训练，并加入失败案例和工作空间边界情况数据，使其更紧密地跟随动作并与真实执行保持一致。
- 系统会缓存中间状态，因此操作员可以回退到失败点，并从同一状态分支出多个不同的纠正续接轨迹。
- 这些纠正片段会与原始真实世界数据集合并，用于策略后训练；论文用两个骨干策略进行了测试，即 Diffusion Policy (DP) 和 Pi0。
- 介入接口与硬件无关：键盘、机械臂遥操作和 VR 控制器都映射到同一个策略动作空间。

## 结果
- 在 3 个真实世界操作任务和 2 个策略骨干上，Hi-WM 相比基础策略将真实世界平均成功率提高了 **37.9 个百分点**，相比世界模型闭环基线提高了 **19.0 个百分点**。
- **DP** 的真实世界成功率（%）：在 **Fold Towel / Push-T / Route Rope** 上，Base 为 **42.1 / 52.9 / 47.0**，WM-CL 为 **76.3 / 64.7 / 70.6**，Hi-WM 为 **92.1 / 85.3 / 94.1**。
- **Pi0** 的真实世界成功率（%）：在同样三个任务上，Base 为 **55.3 / 76.5 / 64.7**，WM-CL 为 **78.9 / 79.4 / 82.4**，Hi-WM 为 **97.4 / 97.1 / 100.0**。
- 世界模型评估与真实世界表现高度一致，**Pearson r = 0.953**，这支持在介入时用该模型评估策略。
- 加入边界情况数据后，世界模型的视觉保真度有所提高：从基础版到完整增强版，**PSNR 18.50 -> 22.53**，**SSIM 0.815 -> 0.942**，**LPIPS 0.152 -> 0.055**。
- 论文还称，在加入边界情况增强后，靠近工作空间边界的位置精度在世界到真实迁移中更好，但给出的摘录没有包含该测试的完整数值表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21741v1](http://arxiv.org/abs/2604.21741v1)
