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
- robot-programming-by-demonstration
- vision-based-branching
- interactive-robot-learning
- anomaly-detection
- task-graph-execution
relevance_score: 0.31
run_id: materialize-outputs
---

# See and Switch: Vision-Based Branching for Interactive Robot-Skill Programming

## Summary
本文提出 **See & Switch**，一个用于机器人示教编程的交互式框架：机器人在执行到“决策状态”时，通过手眼相机图像自动选择后续技能分支，或检测新情境并请求人类补充示教。它把条件任务图、视觉分支选择和多种示教方式统一起来，以提升真实环境变化下的鲁棒性。

## Problem
- 传统 Programming by Demonstration / Learning from Demonstration 往往只是重放单条示教轨迹，遇到门是否关闭、物体位置变化、障碍出现等环境变化时容易失败。
- 条件任务图能表达“如果场景不同就走不同技能分支”，但关键难点是：机器人必须在执行过程中基于感知 **可靠地选对分支**，并在遇到未见过的新情境时 **发现异常并请求新示教**。
- 这很重要，因为如果不能在线感知并切换，示教式机器人系统就难以从实验室走向真实、多变、由非专家使用的场景。

## Approach
- 将任务表示为**可增量扩展的技能部件图**：节点是 skill parts，边通过 decision states 连接；执行时可在这些决策点切换到不同后继技能。
- 提出基于视觉的 **Switcher**：在每个决策状态读取手眼相机图像，用 DINO 视觉特征判断当前应切换到哪个后继技能分支。
- 同一个视觉表征空间同时用于**异常/OOD 检测**：若当前图像不像任何已知分支上下文，则触发 anomaly，让用户决定是新增分支（recovery demonstration）还是仅用这次数据细化已有技能。
- 采用 **decision-state-local** 的局部分类思路：只在当前决策点的允许后继集合中做分类，而不是做全局场景理解，从而降低歧义并简化学习问题。
- 设计了**示教方式无关**的输入抽象层，统一支持 kinesthetic teaching、joystick/keyboard、hand gestures，使用户能在执行中原地补充恢复示教。

## Results
- 在 **3 个灵巧操作任务**（Peg pick、Probe measure、Cable wrap）上验证系统，并进行了 **8 名参与者** 的用户研究。
- 数据规模为 **192 次示教**（8 users × 3 tasks × 3 modalities × 2–3 variants）和 **576 次真实机器人 rollouts**（每次示教约 3 次执行回放）。
- 论文声称对新手用户，系统可**可靠完成分支选择和异常检测**：跨 **576** 次真实机器人执行，**branch selection accuracy = 90.7%**，**anomaly detection accuracy = 87.9%**。
- 约 **4%** 的示教因安全问题被过滤，约 **3%** 的情况下允许用户第二次尝试；作者据此说明该系统在真实交互设置下具备可用性。
- 文段中未给出更细的分任务/分模态/分基线数值比较，但明确指出其方法相较依赖手工分支或低维本体感觉信号的方法，提供了**视觉驱动、可在线扩图、且与示教模态无关**的条件技能编程能力。

## Link
- [http://arxiv.org/abs/2603.08057v1](http://arxiv.org/abs/2603.08057v1)
