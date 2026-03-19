---
source: arxiv
url: http://arxiv.org/abs/2603.11383v1
published_at: '2026-03-11T23:53:28'
authors:
- Hendrik Chiche
- Antoine Jamme
- Trevor Rigoberto Martinez
topics:
- robot-teleoperation
- inverse-kinematics
- hand-tracking
- rgb-d-vision
- vision-language-action
relevance_score: 0.17
run_id: materialize-outputs
language_code: zh-CN
---

# Vision-Based Hand Shadowing for Robotic Manipulation via Inverse Kinematics

## Summary
本文提出一种基于单目第一人称RGB-D相机和解析逆运动学的手部影子跟随系统，把人手动作离线映射到低成本SO-ARM101机械臂。它试图用零训练、低硬件成本的方法替代昂贵遥操作设备，并与多种VLA策略进行对比。

## Problem
- 要把人手的自然关节运动稳定映射到低成本机械臂的关节命令并不容易，传统遥操作常依赖外骨骼、VR头显或主从机械臂，成本高且复杂。
- 纯模仿学习虽然可行，但需要示教数据、GPU训练和任务特定调参，部署门槛较高。
- 在真实场景中，手部或目标物遮挡会破坏视觉跟踪，直接影响抓取控制与泛化能力，因此这个问题对低成本机器人操作很重要。

## Approach
- 用安装在3D打印眼镜上的Intel RealSense D400采集第一人称RGB-D视频，MediaPipe Hands检测每只手21个2D关键点，再用深度图反投影到3D。
- 将手部3D点通过相机到机器人坐标变换映射到SO-ARM101基座坐标系，并根据拇指、食指和手腕几何关系构造末端位姿目标。
- 在PyBullet中用阻尼最小二乘逆运动学求解5-DOF机械臂关节角，再对关节解做EMA平滑以减少抖动。
- 用拇指与食指的几何夹角控制夹爪开合，并设计四级回退机制：指尖、近端关节、上一次有效值、默认半开值，以缓解深度缺失和遮挡。
- 先在PyBullet中预览轨迹，再通过LeRobot在真实机械臂上回放；同一流程也可导出演示数据供后续模仿学习训练。

## Results
- 在结构化抓取放置基准上（5个tile、每个10次，共50次），IK重定向管线达到 **90% (45/50)** 成功率，且 **无需训练数据**。
- 分tile结果中，离机器人更远、手势更自然的 **tile #1/#2 为 10/10、10/10**；靠近底座、易自遮挡的 **tile #5 降至 7/10**。
- 与4种VLA策略对比：**ACT 92%**（50k steps，约10 Hz）略高于本文IK；**SmolVLA 50%**（20k steps）；**pi_0.5 40%**（3k steps）；**GR00T N1.5 35%**（3k steps）。
- 延迟方面，MediaPipe约 **23 ms**、可视化叠加 **110 ms**、PyBullet IK约 **80 ms**，总计 **213 ms/帧**，有效吞吐约 **~5 FPS**，因此系统 **不是实时30 FPS**，而是先录制后离线处理。
- 作者声称其主要优势是 **零训练、任务无关、低成本硬件**；主要失败原因是 **手部自遮挡/环境遮挡** 导致关键点或夹爪角度无法可靠估计。
- 在非结构化真实环境（杂货店、药房）中，受周围物体遮挡影响，IK方法成功率降至 **9.3% (N=75)**，显示方法在受遮挡场景下仍有明显局限。

## Link
- [http://arxiv.org/abs/2603.11383v1](http://arxiv.org/abs/2603.11383v1)
