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
Hi-WM 把一个学习到的世界模型用作机器人策略的测试、人工纠正和后续改进的场所。论文声称，这样可以降低通用机器人策略后训练的成本，同时提高真实世界操作任务的成功率。

## 问题
- 预训练的通用机器人策略在面向特定任务的场景、接触密集型操作和长时程执行中仍会失败，因此在部署前需要后训练。
- 传统的人类纠错式后训练成本高，因为每次纠错都需要真实机器人时间、场景搭建、复位和真实环境中的操作员监督。
- 现有世界模型工作主要把模型用于 rollout 生成或评估，而不是用作在失败状态附近收集人类纠错数据的交互场所。

## 方法
- Hi-WM 不直接在真实机器人上执行当前策略，而是在动作条件世界模型中展开策略，然后只在 rollout 出现错误或可能失败时让人介入。
- 世界模型在 14D 连续双臂动作空间上训练，并加入失败案例和边界工作区数据，使其更贴近动作并与真实执行保持一致。
- 系统会缓存中间状态，因此操作员可以回退到失败点，并从同一状态分支出多个不同的纠正续写。
- 这些纠正片段会与原始真实世界数据集合并，用于对策略进行后训练；论文用两个骨干模型 Diffusion Policy（DP）和 Pi0 做了测试。
- 交互接口与硬件无关：键盘、机器人手臂遥操作和 VR 控制器都会映射到同一策略动作空间。

## 结果
- 在 3 个真实世界操作任务和 2 个策略骨干上，Hi-WM 的平均真实世界成功率比基础策略提高 **37.9 个百分点**，比世界模型闭环基线提高 **19.0 个百分点**。
- **DP** 的真实世界成功率（%）为：基础 **42.1 / 52.9 / 47.0**，WM-CL **76.3 / 64.7 / 70.6**，Hi-WM **92.1 / 85.3 / 94.1**，对应 **Fold Towel / Push-T / Route Rope**。
- **Pi0** 的真实世界成功率（%）为：基础 **55.3 / 76.5 / 64.7**，WM-CL **78.9 / 79.4 / 82.4**，Hi-WM **97.4 / 97.1 / 100.0**，对应同样的三个任务。
- 世界模型评估与真实世界表现高度一致，**Pearson r = 0.953**，这支持在介入时用模型来评估策略。
- 加入边界案例数据后，世界模型的视觉保真度提高：从基础增强到完整增强，**PSNR 18.50 -> 22.53**，**SSIM 0.815 -> 0.942**，**LPIPS 0.152 -> 0.055**。
- 论文还声称，在加入边界案例增强后，工作区边界附近的世界到真实位置精度更好，但摘要片段没有给出该测试的完整数值表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21741v1](http://arxiv.org/abs/2604.21741v1)
