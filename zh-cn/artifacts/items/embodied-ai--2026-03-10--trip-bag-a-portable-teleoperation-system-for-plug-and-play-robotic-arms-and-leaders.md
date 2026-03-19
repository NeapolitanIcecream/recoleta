---
source: arxiv
url: http://arxiv.org/abs/2603.09226v1
published_at: '2026-03-10T05:49:47'
authors:
- Noboru Myers
- Sankalp Yamsani
- Obin Kwon
- Joohyung Kim
topics:
- robot-data-collection
- teleoperation
- bimanual-manipulation
- portable-robotics
- imitation-learning
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# TRIP-Bag: A Portable Teleoperation System for Plug-and-Play Robotic Arms and Leaders

## Summary
TRIP-Bag提出了一种可装入商用行李箱的便携式双臂遥操作数据采集系统，试图同时兼顾实验室级高保真遥操作与野外场景部署能力。其核心价值是降低机器人操作数据采集门槛，以支持学习型操作策略的数据扩展。

## Problem
- 机器人操作学习缺少大规模、高质量、跨环境的示教数据，这直接限制了模仿学习和机器人基础模型的发展。
- 便携式手持/视觉采集方案虽然适合野外数据收集，但通常存在人与机器人之间的**embodiment gap**，导致动作难以直接用于目标机器人。
- 传统遥操作系统能提供高保真数据，但通常依赖实验室固定基础设施，运输、装配和校准成本高，难以扩展到多场景数据采集。

## Approach
- 提出**TRIP-Bag**：把两台可插拔机械臂、两个缩放式puppeteer leader、3个RGB-D相机和计算单元全部集成进一个商用行李箱中，实现“开箱即用”的遥操作平台。
- 采用**joint-to-joint直接映射**的puppeteering遥操作，而非手持设备/视觉手部估计，从机制上减少embodiment gap，并保留完整本体状态记录。
- 软件基于ROS2与PAPRLE框架：leader发布关节状态，teleoperation节点实时转换为follower命令，同时执行自碰撞检查与跟踪误差反馈。
- 数据采集时同步记录3路RGB-D图像、机器人关节位置/速度/力矩等观测，以及关节命令动作；相机30 Hz、关节更新125 Hz、最终同步记录50 Hz。
- 系统通过可插拔接口和折叠收纳设计提升部署速度与跨地点运输能力，目标是在真实厨房、办公室、工坊等环境中快速收集高保真双臂操作数据。

## Results
- 便携性：整套系统**总重29.8 kg**，装入标准商用行李箱；论文称其可作为托运行李跨国运输。专家从开箱到首次遥操作的平均准备时间为**200秒**，文中同时概述为**5分钟以内**。
- 数据规模：作者使用该系统在**22个不同环境**中收集了**1238条示教**，覆盖两项双臂任务；另从**10名非专家用户**处收集了**200条示教**用于可用性分析。
- 非专家可用性：每位非专家先观看**3分钟**教学视频，再对每个任务进行**10次试验**。文中报告**10/10参与者最终都完成了Task 1**，且成功完成时间随试验次数持续下降；Task 2起初更难，但成功率也随重复练习上升。未给出更细的逐轮数值表。
- 学习可行性：作者用收集数据训练了**ACT (Action Chunking Transformer)** 基线策略，每个任务单独训练；输入为**3路RGB-D + 当前关节状态**，输出未来关节轨迹。结果表明策略“能够完成任务”，并表现出失败后再抓取等行为。
- 定量性能：论文摘录**未提供**策略成功率、平均回报、与ALOHA/Gello/手持方案等基线的数值对比，因此其主要强证据是部署速度、采集规模、跨环境数量，以及非专家可快速上手的实验观察。
- 相比表格中的已有方案，作者声称TRIP-Bag同时具备：**in-the-wild部署、puppeteering、joint-space控制、direct embodiment mapping、calibration-free、operator gripper feedback、full proprioceptive logging**；并声称据其所知这是首个同时满足这些属性的系统。

## Link
- [http://arxiv.org/abs/2603.09226v1](http://arxiv.org/abs/2603.09226v1)
