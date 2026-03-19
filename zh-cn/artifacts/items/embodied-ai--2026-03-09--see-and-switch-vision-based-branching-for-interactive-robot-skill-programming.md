---
source: arxiv
url: http://arxiv.org/abs/2603.08057v1
published_at: '2026-03-09T07:47:47'
authors:
- Petr Vanc
- Jan Kristof Behrens
- "V\xE1clav Hlav\xE1\u010D"
- Karla Stepanova
topics:
- programming-by-demonstration
- vision-based-branching
- dexterous-manipulation
- task-graphs
- anomaly-detection
relevance_score: 0.73
run_id: materialize-outputs
language_code: zh-CN
---

# See and Switch: Vision-Based Branching for Interactive Robot-Skill Programming

## Summary
本文提出 See & Switch，一个基于视觉的交互式机器人示教框架，用任务图中的分支技能片段来处理环境变化。它用手眼相机图像在执行时自动选择后续技能，或在遇到新情况时触发用户补充示教。

## Problem
- 传统 PbD/LfD 往往只能复现单条示教轨迹，遇到门关闭、物体位置变化、遮挡等真实环境变化时容易失败。
- 条件任务图虽然能表达“如果环境不同就走不同分支”，但关键难点在于：机器人如何基于高维视觉输入在线选对分支，并识别从未见过的新情境。
- 这很重要，因为若没有可靠分支选择与异常检测，非专家用户就难以通过示教逐步扩展机器人技能，系统也难以适应开放环境中的变化。

## Approach
- 将任务表示为**可扩展任务图**：节点是技能片段，执行到决策状态（DS）时可以切换到不同后继分支。
- 提出视觉 **Switcher**：在 DS 附近使用手眼相机图像，既做**分支分类**（选哪个后继技能），也做**OOD/异常检测**（是否需要新示教）。
- 使用冻结的 **DINO** 视觉特征作为表示，再在每个 DS 上训练局部分类器/估计器，只在该 DS 允许的候选分支集合内做判断，降低全局场景理解难度。
- 当检测到异常时，用户可在线提供**恢复示教**，系统自动插入新的 DS/分支并重训对应局部 Switcher，从而增量扩展任务图。
- 通过输入抽象层统一**拖动示教、摇杆控制、手势遥操作**三种教学方式，使纠错和恢复示教与具体输入模态无关。

## Results
- 在 **3 个灵巧操作任务**上验证：**Peg pick、Probe measure、Cable wrap**。
- 开展了 **8 名参与者**的用户研究，累计 **192** 次示教（由 **8 users × 3 tasks × 3 modalities × 2–3 variants** 构成）。
- 共评估 **576 次真实机器人 rollouts**；论文声称该方法对**新手用户**也能可靠执行分支选择与异常检测。
- 关键定量结果：跨 576 次真实机器人运行，**分支选择准确率 90.7%**，**异常检测准确率 87.9%**。
- 数据中约 **4%** 的示教因安全问题被过滤，约 **3%** 的情况下允许第二次尝试。
- 文摘未给出相对于某个明确基线方法的完整数值对比表；最强的实证主张是：视觉 Switcher 能在真实任务中实现可靠分支决策，并支持模态无关的在线恢复示教。

## Link
- [http://arxiv.org/abs/2603.08057v1](http://arxiv.org/abs/2603.08057v1)
