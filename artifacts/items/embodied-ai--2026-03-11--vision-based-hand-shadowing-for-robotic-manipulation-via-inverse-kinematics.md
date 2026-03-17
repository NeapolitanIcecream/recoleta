---
source: arxiv
url: http://arxiv.org/abs/2603.11383v1
published_at: '2026-03-11T23:53:28'
authors:
- Hendrik Chiche
- Antoine Jamme
- Trevor Rigoberto Martinez
topics:
- inverse-kinematics
- hand-tracking
- robot-teleoperation
- vision-based-manipulation
- sim-to-real
relevance_score: 0.69
run_id: materialize-outputs
---

# Vision-Based Hand Shadowing for Robotic Manipulation via Inverse Kinematics

## Summary
本文提出一种基于单个第一人称RGB-D相机的离线手部影随（hand shadowing）到机器人控制流水线，用解析逆运动学把人手动作转成低成本SO-ARM101机械臂的关节命令。它试图以零训练替代昂贵遥操作硬件或数据驱动策略训练，并与多种VLA策略进行了对比。

## Problem
- 目标问题：如何把人手的自然动作，低成本地映射到机器人关节控制，用于遥操作、轨迹回放和示教数据采集。
- 重要性：传统遥操作往往依赖VR、外骨骼或主从机械臂等昂贵设备；模仿学习/VLA又需要演示数据、GPU训练和任务适配成本。
- 难点在于：单目第一人称视角下的手部关键点检测、深度恢复、坐标变换、抓取开合映射，以及遮挡导致的手部几何失真。

## Approach
- 使用安装在3D打印眼镜上的Intel RealSense D400采集**640×480、30 FPS**的第一人称RGB-D视频，并用MediaPipe Hands在CPU上检测每只手**21个关键点**。
- 将2D关键点通过深度图反投影到3D，相机坐标再经刚体变换映射到机器人坐标系；相机安装角固定为**50°**，并使用CAD导出的平移/旋转参数完成标定。
- 用拇指和食指根部（MCP）的中点作为末端执行器目标位置；用拇指/食指的几何关系构造目标朝向；若指尖不可见，则退化到基于腕部和掌部的朝向估计。
- 在PyBullet中求解带阻尼最小二乘的逆运动学，并对关节角做EMA平滑；夹爪控制由拇指—食指夹角驱动，带有**四级回退机制**（指尖、近端关节、上一帧、默认半开）。
- 生成的轨迹先在PyBullet中预览，再通过LeRobot回放到真实SO-ARM101；同一流程还能导出示教数据供ACT、SmolVLA、π0.5、GR00T N1.5等策略训练。

## Results
- 在结构化抓取放置基准上（**5个网格位置 × 每格10次 = 50次**），IK重定向方法达到**90%（45/50）**成功率，且**无需任何训练**。
- 分位置结果显示：最远的**tile #1/#2 为 10/10、10/10**，靠近机器人底座且更易发生手部自遮挡的**tile #5 为 7/10**。
- 与4个VLA策略比较：**ACT 92%**、**IK 90%**、**SmolVLA 50%**、**π0.5 40%**、**GR00T N1.5 35%**；其中VLA方法基于**50条示教轨迹**训练，ACT训练**50k steps**，SmolVLA **20k steps**，π0.5/GR00T **3k steps**。
- 速度方面，该流水线总处理延迟约**213 ms/帧**，其中MediaPipe **23 ms**、可视化叠加 **110 ms**、PyBullet IK **80 ms**，整体仅约**5 FPS**，因此是**离线处理**而非实时30 FPS控制。
- 在非结构化真实环境（杂货店、药店）中，因周围物体造成手部遮挡，IK方法成功率下降到**9.3%（N=75）**，表明其主要瓶颈是无标记手部跟踪在遮挡条件下的鲁棒性。
- 论文的最强主张是：在受控场景下，该解析IK方案以**零训练**接近甚至逼近最佳学习方法（仅比ACT低**2个百分点**），但在野外场景泛化上仍明显受限于遮挡。

## Link
- [http://arxiv.org/abs/2603.11383v1](http://arxiv.org/abs/2603.11383v1)
