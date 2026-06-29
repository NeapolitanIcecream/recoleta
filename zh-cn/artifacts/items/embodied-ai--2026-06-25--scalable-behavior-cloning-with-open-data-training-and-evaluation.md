---
source: arxiv
url: https://arxiv.org/abs/2606.27375v1
published_at: '2026-06-25T17:59:57'
authors:
- Arthur Allshire
- Himanshu Gaurav Singh
- Ritvik Singh
- Adam Rashid
- Hongsuk Choi
- David McAllister
- Justin Yu
- Yiyuan Chen
- Huang Huang
- Pieter Abbeel
- Xi Chen
- Rocky Duan
- Phillip Isola
- Jitendra Malik
- Fred Shentu
- Guanya Shi
- Philipp Wu
- Angjoo Kanazawa
topics:
- behavior-cloning
- vision-language-action
- robot-data-scaling
- sim2real
- dexterous-manipulation
- bimanual-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Scalable Behavior Cloning with Open Data, Training, and Evaluation

## Summary
## 摘要
ABC 发布了一个用于双臂操作的开放行为克隆栈，核心是 ABC-130K。ABC-130K 是一个 3,553 小时的真实世界遥操作数据集，包含 195 个任务中的 134,806 个 episode。论文还报告了模型消融、仿真数据、仿真到真实的相关性，以及 DiT 和 VLA 策略在真实世界中的 rollout。

## 问题
- 机器人操作的行为克隆很难复现，因为大型数据集、硬件设置、训练代码和评估 rollout 往往不公开或不完整。
- DiT 和 VLA 机器人策略的设计选择在真实机器人上测试成本很高，因此研究人员需要成本更低、且能跟踪真实世界性能的信号。
- 复杂的双臂和灵巧操作任务需要比标准抓取放置数据集更丰富的数据。

## 方法
- ABC-130K 包含 3,553 小时、134,806 个 episode、195 个任务，以及 1,552 小时带子目标标注的数据；任务包括抓取放置、折叠、插入、工具使用、交接和装配。
- 该发布内容包括硬件设置、数据加载、训练和部署代码、模型权重、ABC-Eval 真实 rollout 分数，以及 ABC-Sim。
- ABC-DiT 使用一个 2B 参数的扩散 transformer，采用 DINOv3 视觉特征，并通过 cross-attention 连接 action token。
- ABC-VLA 使用一个 4B Gemma 3 VLM，并配有扩散动作头；论文比较了 cross-attention、FAST 联合训练和 AdaLN 连接器。
- ABC-Sim 增加了 MuJoCo 任务、VR 遥操作、超过 400 小时的仿真数据，以及用于生成更高质量图像的 Blender 重新渲染。

## 结果
- 论文称 ABC-130K 是最大的开源遥操作数据集：3,553 小时真实世界数据、134,806 个 episode 和 195 个任务；ABC-Eval 包含超过 100 小时的真实策略 rollout。
- 在内部 7,000 小时语料上训练 200k 步后的架构消融显示：最佳 DiT，即 DINOv3 cross-attention，达到 32.9% 的平均严格成功率和 67.5% 的平均进度；CLIP-AdaLN DiT 达到 13.4% 和 47.3%。
- VLA 连接器消融显示：AdaLN 达到 32.8% 的平均严格成功率和 61.4% 的平均进度；FAST 加 cross-attention 达到 3.6% 和 32.6%；普通 cross-attention 达到 0.0% 和 11.7%。
- 表 1 中的具体任务结果包括：bottles 任务中，DINOv3-DiT 的进度为 93.1%，CLIP-AdaLN 为 53.6%，CLIP-cross-attention 为 74.1%；dishrack 任务的严格成功率由 CLIP-cross-attention DiT 取得最高值，为 34.7%。
- 离线诊断在 16 个 checkpoint 上跟踪了真实性能：训练损失与严格成功率的 Pearson r=-0.89，Spearman rho=-0.93；验证动作误差与严格成功率的 r=-0.84，rho=-0.83；验证损失与严格成功率没有显著关系，r=-0.04。
- 仿真在三个任务的 12 个 checkpoint 上跟踪了真实性能：严格成功率的 Pearson r=0.85，p=4.2e-4；任务进度的 Pearson r=0.91，p=5.0e-5。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.27375v1](https://arxiv.org/abs/2606.27375v1)
