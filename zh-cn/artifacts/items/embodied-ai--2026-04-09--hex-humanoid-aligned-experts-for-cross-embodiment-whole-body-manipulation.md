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
## 概要
HEX 是一个面向全尺寸人形机器人的视觉-语言-动作系统，目标是完成全身操作任务。在这类任务中，手臂、手、腿、腰部和身体平衡需要协同工作。它的核心主张是：用共享的身体部位格式来建模人形机器人状态，并预测短期未来的本体感觉状态，可以提升协调性、泛化能力和真实机器人上的任务成功率。

## 问题
- 现有机器人 VLA 策略通常直接预测高维动作，但不建模身体各部位如何通过姿态与平衡相互影响，这会削弱人形机器人全身控制的效果。
- 全身操作需要同时处理移动、操作和动态稳定，尤其是在快速反应和长时程任务中。
- 跨形态训练很难，因为不同人形机器人有不同的关节、传感器和状态维度。

## 方法
- HEX 使用一种**与人形机器人对齐的通用状态表示**：它将每台机器人的本体感觉映射到固定的标准身体部位槽位中，如手臂、手、腿、头部和腰部；缺失部位则使用学习得到的 token 表示。
- 它加入了一个 **Unified Proprioceptive Predictor (UPP)**，接收这些部位 token，并预测短时域的未来身体状态。UPP 使用共享 transformer，并配合具备形态感知能力的 mixture-of-experts 层，使不同身体部位和不同机器人形态可以路由到不同专家。
- 在视觉上下文方面，HEX 保存过去帧的紧凑**历史查询特征**，而不是反复编码长图像序列。论文在实验中将视觉历史窗口设为 **2** 帧。
- 它的 **Action Expert** 采用双重条件生成动作：一个分支关注视觉-语言特征，另一个分支关注预测得到的未来本体感觉特征；系统再通过一个学习得到的门控机制决定状态预测对动作的影响程度。
- 训练时结合了**流匹配动作目标**和辅助的**未来状态预测损失**。完整系统采用分层结构：高层是 VLA 策略，低层是用于保持平衡执行的 RL 全身控制器。

## 结果
- 论文声称，在人形机器人全身操作任务上，HEX 的真实世界表现达到**最先进水平**，衡量指标包括**任务成功率**和**泛化能力**，对比对象包括 **ACT, SwitchVLA, GR00T N1.5, and $\Pi_{0.5}$**。
- 它报告称，在**快速反应**和**长时程**任务上的提升最明显，因为这些任务最依赖时间一致性和全身协同。
- 实验在两个真实人形机器人平台上进行：**Tienkung 2.0** 和 **Tienkung 3.0**。
- 给出的摘录**不包含数值表格或精确成功率数值**，因此无法仅根据这段文本核实它相对基线的具体优势幅度。
- 论文还声称，共享的身体部位状态编码和基于 MoE 的本体感觉预测提升了**跨形态泛化**，但这段摘录没有给出定量迁移指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07993v1](http://arxiv.org/abs/2604.07993v1)
