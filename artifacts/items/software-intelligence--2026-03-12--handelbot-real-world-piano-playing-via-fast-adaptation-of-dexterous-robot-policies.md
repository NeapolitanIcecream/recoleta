---
source: arxiv
url: http://arxiv.org/abs/2603.12243v1
published_at: '2026-03-12T17:56:29'
authors:
- Amber Xie
- Haozhi Qi
- Dorsa Sadigh
topics:
- dexterous-robotics
- sim-to-real
- residual-reinforcement-learning
- robot-piano-playing
- bimanual-manipulation
relevance_score: 0.18
run_id: materialize-outputs
---

# HandelBot: Real-World Piano Playing via Fast Adaptation of Dexterous Robot Policies

## Summary
HandelBot提出了一种把仿真学到的灵巧手钢琴策略快速适配到真实世界的两阶段方法，用极少真实交互数据实现双手机器人弹钢琴。它针对毫米级精度任务中的sim-to-real落差，结合规则化轨迹校正与残差强化学习，显著优于直接部署仿真策略。

## Problem
- 真实世界双手机器人弹钢琴需要**毫米级空间精度、精确时序和长时程双手协调**，而仿真到现实的微小误差就会导致按错键或漏按。
- 依赖遥操作或人类演示来收集高质量灵巧手数据**成本高、难扩展、甚至对快速独立手指动作不可行**。
- 纯仿真RL虽能学到粗粒度协调，但**直接迁移到真实钢琴时性能很差**，特别是在接触动力学和控制器失配下。

## Approach
- 先在仿真中用RL训练基础钢琴策略，获得一个能在模拟器中工作的**粗略开放环轨迹**与结构先验。
- 第一阶段做**策略精修**：在真实钢琴上执行轨迹，比较目标键与实际按下的键，按规则只调整手指的横向关节，让手指逐步对准正确琴键；更新按时间块进行，并带前瞻与步长退火以保持平滑。
- 第二阶段做**残差强化学习**：冻结精修后的基础轨迹，只学习小幅纠正量，加到下一步目标关节位置上，从而更安全、更高效地适配真实动力学。
- 真实世界奖励直接来自**MIDI按键输出**；训练使用TD3，并可加入与“正确横向移动方向”一致的引导噪声来帮助探索。
- 系统在双手硬件平台上运行：两只Tesollo DG-5F手、两台Franka机械臂、MIDI键盘，并加入IK与碰撞约束保证部署安全。

## Results
- 论文声称据其所知，这是**首个基于学习的真实世界双手机器人钢琴演奏系统**，并在**5首知名乐曲**上评测：Twinkle Twinkle、Ode to Joy、Hot Cross Buns、Fur Elise、Prelude in C。
- 相比直接sim-to-real部署，HandelBot整体**提升1.8×**，且只需要**30分钟真实交互数据**即可完成快速适配（摘要与引言明确给出）。
- 训练预算方面，RL方法训练**100条轨迹**；较长曲目约**30k环境交互/1小时**，较短曲目约**16k交互/30分钟**。
- 闭环直接部署的仿真策略表现很弱，例如F1×100：**Ode to Joy 5±2.46**、**Twinkle Twinkle 23±6.2**、**Hot Cross Buns 8±2.1**、**Prelude in C 29±2.2**、**Fur Elise 18±3.2**；并行仿真混合执行虽略好，但仍低，如**12±2.6、24±2.5、9±2.9、40±1.0、20±4.9**。
- 消融实验中，Twinkle Twinkle上HandelBot达到**81±4.1** F1×100；改折扣因子后降到**73±2.5**（γ=0.75）和**69±0.2**（γ=0.9）；去掉引导噪声仍有**81±0.7**，始终启用引导噪声为**77±0.9**。
- 虽然正文指出“HandelBot在所有歌曲上都取得最高F1”，但给定摘录**未包含完整主结果表的所有具体数值**；最强的可验证定量主张是**1.8×提升、30分钟真实数据、5首歌评测，以及上述表格中的F1分数**。

## Link
- [http://arxiv.org/abs/2603.12243v1](http://arxiv.org/abs/2603.12243v1)
