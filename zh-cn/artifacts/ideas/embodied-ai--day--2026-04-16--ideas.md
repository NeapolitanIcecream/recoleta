---
kind: ideas
granularity: day
period_start: '2026-04-16T00:00:00'
period_end: '2026-04-17T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- data generation
- dexterous manipulation
- sim2real
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/data-generation
- topic/dexterous-manipulation
- topic/sim2real
language_code: zh-CN
---

# 机器人操作的物理数据增强

## 摘要
这个时间窗口里的机器人工作给出三项具体的流程变化。移动操作团队可以在现有示范周围加入停靠姿态增强，以恢复导航误差下的性能。类别级操作团队可以通过在类别内变换物体几何来生成新的真实示范，这对把手和接触敏感任务很有用。灵巧手团队可以用贴附式便携遥操作装置降低采集成本，同时提升真实硬件上的操作者成功率和速度。

## Docking-pose augmentation for mobile manipulation policies
移动操作需要一条对停靠姿态更稳健的数据管线，而不只是更好的控制器。DockAnywhere给出了一套具体做法：在一个停靠姿态下录制少量示范，把每条轨迹拆成接近运动段和接触丰富的技能段，保留操作段不变，只为新的可行基座姿态重生成接近段。论文还为这套流程改了相机设置，使用固定的第三人称 RGB-D 视角，再在三维点云空间里编辑观测，让新视角和复用的动作序列保持对齐。

这对已经在用“导航后接固定基座操作”两阶段栈的团队很实用。论文里的失败模式很直接：普通 DP3 在一个停靠点上成功率为 88.6%，而在五个停靠点上评测时降到 17.8%。用了 DockAnywhere 增强后，总体成功率达到 78.9%，而且大部分提升在四个增强后的停靠点时就已经出现。一个成本低的验证方法是：拿现有的一个移动操作任务，从一个停靠点收集示范，合成三个或四个附近停靠点，再看在未见过的停止位置上成功率是否能恢复，同时不用重新采集任务的接触阶段。

### 资料来源
- [DockAnywhere: Data-Efficient Visuomotor Policy Learning for Mobile Manipulation via Novel Demonstration Generation](../Inbox/2026-04-16--dockanywhere-data-efficient-visuomotor-policy-learning-for-mobile-manipulation-via-novel-demonstration-generation.md): Provides the core method, failure mode under docking shifts, and the main success-rate comparisons including 78.9% overall success and the drop to 17.8% for plain DP3 across five docking points.
- [DockAnywhere: Data-Efficient Visuomotor Policy Learning for Mobile Manipulation via Novel Demonstration Generation](../Inbox/2026-04-16--dockanywhere-data-efficient-visuomotor-policy-learning-for-mobile-manipulation-via-novel-demonstration-generation.md): Confirms the paper frames the method as lifting one demonstration to diverse feasible docking configurations for mobile manipulation.

## Real-to-real shape augmentation for category-level manipulation
类别级操作团队现在可以围绕物体几何来做真实到真实的数据生成，而不用为每个新的杯子、壶或把手形状重新采集示范。ShapeGen为每个物体类别建立形状库，在同一类别的物体之间学习稠密形变，再让人工为每个源示范做轻量标注，用来标出任务相关点并调整抓取。论文报告的标注成本大约是每个源示范 1 分钟，这让流程接近普通的遥操作采集。

这些提升足以支持只针对几何导致失败的任务做定向部署。在未见过的物体上，hang_mug 从 5% 提升到 45%，hang_mug_hard 从 5% 提升到 50%，serve_kettle 从 35% 提升到 75%。这里最弱的结果是 pour_water，只从 55% 升到 60%，所以它更适合把手、挂钩和倾倒姿态这类功能接触点很明确的任务。一个成本低的检查方法是：扫描训练中已经用到的一小组物体，基于五个手工采集的源示范生成形变后的示范，然后在留出的形状上比较成功率，再决定要不要扩大这条管线。

### 资料来源
- [ShapeGen: Robotic Data Generation for Category-Level Manipulation](../Inbox/2026-04-16--shapegen-robotic-data-generation-for-category-level-manipulation.md): Contains the simulator-free real-to-real method, the minimal human annotation requirement, and the task-level gains on unseen object instances.
- [ShapeGen: Robotic Data Generation for Category-Level Manipulation](../Inbox/2026-04-16--shapegen-robotic-data-generation-for-category-level-manipulation.md): Confirms the paper targets category-level geometric variation in real-world manipulation.

## Attached dexterous teleoperation rigs for lower-cost real-hand data collection
灵巧手实验室有机会通过标准化一套便携式、贴附式的遥操作装置来降低数据采集成本。DEX-Mouse 用现成部件搭建，成本低于 150 美元，不需要按用户校准，还加入了基于电流的动觉力反馈。贴附式设置之所以重要，是因为它减少了人手动作和机器人手动作之间的失配：机器人手装在操作者前臂上，系统用简单的比例重定向，而不是更重的、依赖形态的映射堆栈。

论文里的用户研究给出了一个有用的初始基准。在贴附配置下，DEX-Mouse 的总体成功率达到 86.67%，平均完成时间为 10.05 秒，优于研究中的两个手套基线。和远程遥操作相比，差距也很大：DEX-Mouse 自身的总体成功率是 86.67%，而远程模式只有 52.5%。如果实验室在定制手套和更简单的采集装置之间做选择，马上就能做一个小而便宜的测试：在贴附模式和远程模式下跑同样的三个接触丰富任务，记录每个操作者的完成率和耗时，再看更高质量的数据能否抵消更受限的物理布置。

### 资料来源
- [DEX-Mouse: A Low-cost Portable and Universal Interface with Force Feedback for Data Collection of Dexterous Robotic Hands](../Inbox/2026-04-16--dex-mouse-a-low-cost-portable-and-universal-interface-with-force-feedback-for-data-collection-of-dexterous-robotic-hands.md): Provides the hardware cost, attached-versus-remote setup, and the user-study results including success rates and completion times.
- [DEX-Mouse: A Low-cost Portable and Universal Interface with Force Feedback for Data Collection of Dexterous Robotic Hands](../Inbox/2026-04-16--dex-mouse-a-low-cost-portable-and-universal-interface-with-force-feedback-for-data-collection-of-dexterous-robotic-hands.md): Confirms the system is open-sourced for replication and adoption and states the headline attached-configuration result.
