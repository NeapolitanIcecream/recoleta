---
source: arxiv
url: https://arxiv.org/abs/2606.32009v1
published_at: '2026-06-30T17:44:16'
authors:
- Xiaopeng Lin
- Ruoqi Yang
- Shijie Lian
- Zhaolong Shen
- Bin Yu
- Changti Wu
- Haibao Liu
- Yuxiang Zhang
- Hong Li
- Qiyuan Su
- Haochen Liu
- Xuguo He
- Yukun Shi
- Cong Huang
- Zhirui Zhang
- Bojun Cheng
- Kai Chen
topics:
- vision-language-action
- humanoid-manipulation
- human-video-learning
- robot-data-scaling
- dexterous-manipulation
- zero-shot-transfer
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Human-as-Humanoid: Enabling Zero-Shot Humanoid Learning from Ego-Exo Human Videos with Human-Aligned Embodiments

## Summary
## 摘要
Human-as-Humanoid 将同步的人类 ego-exo 视频转换为可执行的 60-DoF 人形机器人动作标签，用于 VLA 训练。论文声称的收益包括更快的人形机器人动作数据采集，以及在若干灵巧任务上无需目标任务机器人示范即可部署到真实机器人。

## 问题
- 高 DoF 人形机器人 VLA 需要目标机器人控制器空间中的观察-动作对，但直接进行人形机器人遥操作速度慢、人工成本高，也难以获得多样数据。
- 人类第一视角视频包含有用的双手操作信息，但缺少机器人关节动作，并且在人形机器人的尺度、关节、手部、视角和可达工作空间上存在差异。
- 这个问题重要，因为机器人数据规模和动作标签质量会限制通用人形机器人操作策略。

## 方法
- 作者基于 PrimeU 构建系统。PrimeU 是一种与人体对齐的上半身人形机器人，具有 60 个可控 DoF：两条 7-DoF 手臂、两只 20-DoF 灵巧手、3-DoF 颈部和 3-DoF 腰部。
- 人类示范使用同步的第一视角和外部视角视频。第一视角与部署时的观察匹配，外部视角用于恢复上半身和手部运动。
- 流水线跟踪人体，恢复上半身和手部关键点，对其进行平滑处理，然后通过分阶段 IK 将其重定向为 PrimeU 关节空间动作片段。
- 训练时，策略输出保持在可执行的关节空间中，同时使用可微 FK 损失监督手腕姿态和指尖位置，使关节预测保留操作几何关系。
- 动作模型使用 VLM 编码器和流匹配 DiT 来预测未来的 60-DoF 动作片段；摘录称每个片段包含 40 个未来状态。

## 结果
- 转换流水线运行速度约为 20 FPS，接近论文所述的 15 Hz 采集设置。
- 论文在数据采集分析中称，相比基于动作捕捉的人形机器人遥操作，该方法的原始示范吞吐量提高了 4.8–7.2 倍。
- 使用人类衍生机器人动作训练的动作 tokenizer 在重建未见过的机器人轨迹时，归一化 MAE 平均为 0.008，第 95 百分位为 0.0097。
- PrimeU 的人体测量学对齐结果报告为：肩宽 40.4 cm，对比人类参考值 41.5 cm；臂展 80.3 cm，对比 78.6 cm；手长 19.3 cm，对比 19.3 cm。
- 论文报告称，仅使用转换后的人类标签进行后训练的策略可以部署到真实人形机器人任务上，包括套环放置、装袋、拧瓶盖和倒水，并且没有使用目标任务机器人示范。
- 摘录没有提供这些真实机器人 rollout 的任务成功率、消融数据，也没有给出与使用机器人示范训练的策略之间的对比。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.32009v1](https://arxiv.org/abs/2606.32009v1)
