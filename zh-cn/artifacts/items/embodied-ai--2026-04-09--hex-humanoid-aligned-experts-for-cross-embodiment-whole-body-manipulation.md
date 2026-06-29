---
source: arxiv
url: http://arxiv.org/abs/2604.07993v1
published_at: '2026-04-09T09:01:43'
authors:
- Shuanghao Bai
- Meng Li
- Xinyuan Lv
- Jiawei Wang
- Xinhua Wang
- Fei Liao
- Chengkai Hou
- Langzhe Gu
- Wanqi Zhou
- Kun Wu
- Ziluo Ding
- Zhiyuan Xu
- Lei Sun
- Shanghang Zhang
- Zhengping Che
- Jian Tang
- Badong Chen
topics:
- humanoid-robotics
- vision-language-action
- whole-body-manipulation
- cross-embodiment-learning
- mixture-of-experts
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# HEX: Humanoid-Aligned Experts for Cross-Embodiment Whole-Body Manipulation

## Summary
## 摘要
HEX 是一个面向全尺寸人形机器人的视觉-语言-动作系统，目标是全身操作，也就是让手臂、手、腿、腰部和保持平衡协同工作。它的核心主张是：把人形机器人的状态建模成共享的身体部位格式，并预测短期本体感觉未来状态，可以提升协调性、泛化能力和真实机器人上的任务成功率。

## 问题
- 现有面向机器人的 VLA 策略常常直接预测高维动作，却没有建模身体各部分如何通过姿态和平衡相互依赖，这会削弱人形机器人的全身控制。
- 全身操作需要同时处理移动、操作和动态稳定性，尤其是在快速反应和长时程任务中。
- 跨具身训练很难，因为不同的人形机器人有不同的关节、传感器和状态维度。

## 方法
- HEX 使用 **humanoid-aligned universal state representation**：它把每台机器人的本体感觉映射到固定的规范身体部位槽位中，比如手臂、手、腿、头部和腰部；对缺失部位则用学习得到的 token。
- 它加入了 **Unified Proprioceptive Predictor (UPP)**，输入这些部位 token，预测短时程未来身体状态。UPP 使用共享 Transformer 和具备形态感知的 mixture-of-experts 层，让不同身体部位和不同机器人具身可以路由到不同专家。
- 对于视觉上下文，HEX 存储紧凑的 **history query features**，来自过去帧，而不是重复编码长图像序列。论文在实验中把视觉历史窗口设为 **2** 帧。
- 它的 **Action Expert** 通过双重条件生成动作：一条分支关注视觉-语言特征，另一条分支关注预测的未来本体感觉特征，学习到的门控决定状态预测对动作的影响程度。
- 训练结合了 **flow-matching action objective** 和辅助的 **future-state prediction loss**；完整系统以分层方式运行，上层是 VLA 策略，下层是用于保持平衡执行的 RL 全身控制器。

## 结果
- 论文声称，在人形机器人全身操作任务上，HEX 在真实世界表现达到 **state-of-the-art**，评价指标是 **task success rate** 和 **generalization**，对比对象包括 **ACT, SwitchVLA, GR00T N1.5, and $\Pi_{0.5}$**。
- 它在 **fast-reaction** 和 **long-horizon** 任务上的提升最大，这些任务最依赖时间一致性和全身协同。
- 实验在两个真实人形平台上进行：**Tienkung 2.0** 和 **Tienkung 3.0**。
- 这段摘要 **没有给出数值表格或确切的成功率数值**，所以仅凭提供的文本无法核实它相对基线的具体提升幅度。
- 论文还声称，借助共享的身体部位状态编码和基于 MoE 的本体感觉预测，跨具身泛化能力有所提升，但这段摘要没有提供定量迁移指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07993v1](http://arxiv.org/abs/2604.07993v1)
