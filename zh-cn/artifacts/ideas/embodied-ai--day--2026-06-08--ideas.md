---
kind: ideas
granularity: day
period_start: '2026-06-08T00:00:00'
period_end: '2026-06-09T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- vision-language-action models
- world models
- failure recovery
- humanoid control
- robot data collection
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/world-models
- topic/failure-recovery
- topic/humanoid-control
- topic/robot-data-collection
language_code: zh-CN
---

# 实用的 VLA 部署控制

## Summary
机器人团队可以围绕冻结的 VLA 策略做出具体改动：加失败专用恢复层、在执行时提供低延迟 steering 和安全滤波、并用更轻的手持夹爪采集双臂数据。共同的落地压力来自实际部署摩擦：策略可以知道任务，但仍可能抓空、撞到附近物体，或者缺少足够多的接触丰富任务示范。

## 针对冻结 VLA 操作策略的失败专用恢复包装层
一个有用的下一步是给现有的 VLA 策略外面加一层恢复模块，用来处理常见的偏离轨迹状态，比如空抓、物体掉落、放错位置和未完成的接触步骤。基础策略可以保持不变，恢复系统负责识别失败类型、选择修正目标或残差动作，并在任务回到正轨后把控制权交回去。

ReCoVLA 展示了这种模式的一个更重版本：Qwen3-VL-8B-Instruct 先分类失败和恢复阶段，编译器再生成分阶段奖励，残差策略在仿真中训练。它把 Fetch 任务的仿真成功率从 36.7% 提高到 66.7%，在零样本实物测试中的平均成功率是 61.7%。B2FF 给出了面向前瞻式 VLA 的更轻方案：先生成 12 个未来图像里程碑，在受到扰动后选出其中一个；在注入失败的 LIBERO 上，UD-VLA 的平均成功率从 56.3% 提高到 74.0%。ProbeAct 提供了只在运行时生效的方案，用隐藏状态探针、运动学失败检测和多次失败后的 Control Barrier Function 区域，把 LIBERO-plus 的成功率从 69.6% 提高到 74.1%。

机器人团队可以先把自己的失败操作日志回放到一个小的失败分类里，按抓取、搬运、放置和关节动作失败来分。第一轮测试应当把冻结策略和包装层在注入失败样本、以及一小组真实复测样本上做对比，测任务成功率、恢复成功率和每次恢复多走了多少步。

### Evidence
- [ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies](../Inbox/2026-06-08--recovla-vlm-guided-reward-compilation-for-failure-recovery-in-vision-language-action-policies.md): ReCoVLA keeps the base VLA frozen, classifies failure state, compiles stage-gated rewards, and reports simulation and physical recovery gains.
- [Back to the Familiar Future: Failure Recovery for VLA Policies via Pre-Imagined Milestone Selection](../Inbox/2026-06-08--back-to-the-familiar-future-failure-recovery-for-vla-policies-via-pre-imagined-milestone-selection.md): B2FF selects pre-generated future-image milestones for recovery and reports a 56.3% to 74.0% gain on failure-injected LIBERO.
- [ProbeAct: Probe-Guided Training-Free Failure Recovery in Vision-Language-Action Models](../Inbox/2026-06-08--probeact-probe-guided-training-free-failure-recovery-in-vision-language-action-models.md): ProbeAct uses hidden-state probes, kinematic failure detection, and CBF zones to improve LIBERO-plus success for a frozen VLA.

## VLA 控制环中的逐步 steering 和碰撞过滤
VLA 部署需要给人和安全逻辑留出控制环入口，因为高层语言指令在执行时常常会留下歧义。现在有两个实用补充值得一起测试：一个是给人类监督者的简单方向输入，另一个是每一步都读取模型自己的目标信号、再把不安全动作从障碍物旁边推开的安全滤波器。

Flow Control 把人类输入这部分用在 flow-matching VLA 上。键盘命令给出六个笛卡尔方向之一，系统把它转成关节速度初始化，flow head 再把这个粗信号映射成一个动作块。在 Two-Block 任务中，pi_0.5-DROID 在含糊指令下 85% 的时间选对了方块，而朝左方块定向后，在更长的 steering horizon 下，左方块抓取几乎达到满分；在那个设置里，抓放成功率报告接近 100%。注意力引导的安全滤波器论文处理的是安全这部分：它读取冻结 VLA 里的选定注意力头，在线确定当前目标，并用 CBF-QP 滤波器让末端执行器远离其他物体。在动态 SafeLIBERO Level III 上，碰撞率从只在初始化时工作的滤波器的 70.75% 降到 26.88%，安全成功率从 25.5% 升到 55.75%。

采用测试很直接：用同一个冻结策略跑含糊的双物体任务和带移动障碍物的任务，然后对比不加包装、只做 steering、只做安全滤波、以及两者一起用。关键指标是纠正延迟、碰撞率、安全成功率，以及包装层把原本已经成功的基线动作改掉了多少。

### Evidence
- [Flow Control: Steering Vision-Language-Action Models with Simple Real-Time Inputs](../Inbox/2026-06-08--flow-control-steering-vision-language-action-models-with-simple-real-time-inputs.md): Flow Control describes keyboard-direction steering by modifying the initial condition of a flow-matching VLA action sampler and reports Two-Block steering results.
- [Your Model Already Knows: Attention-Guided Safety Filter for Vision-Language-Action Models](../Inbox/2026-06-08--your-model-already-knows-attention-guided-safety-filter-for-vision-language-action-models.md): The attention-guided safety filter reads VLA attention online, applies a CBF-QP filter, and reports large collision-rate and safe-success gains on dynamic SafeLIBERO.

## 手指对齐的手持夹爪，用于更高吞吐量的双臂数据采集
依赖 UMI 风格采集的开放机器人学习实验室，可以在继续买更多机器人之前先试一个硬件改动：把数据采集换成更轻、手指对齐的手持夹爪，配合固定架 VR 追踪和像 LeRobot 这样的标准导出路径。操作目标是更长的采集时长、更好的精细操作，以及更少的操作者疲劳。

YUBI 用捏合对齐的设计替代了手枪式握把：拇指驱动一个夹爪指，食指和中指驱动另一个。这个夹爪连同 VR 控制器重 319 g，而原始 UMI 是 780 g，带 VR 的手枪握把系统至少 905 g；论文还说，除了 Quest 3S 追踪设备外，每个单元都能用不到 200 美元做出来。报告中的采集规模是 8,434 小时、120 万个 episode、680 万个 video-language-action 三元组、119 个任务、179 名操作者和 22 张桌子，时间跨度两个月。用 YUBI 手腕数据训练出的单个 pi_0.5-based 策略，在使用同样的 YUBI 末端执行器时，可以迁移到 UR、Franka 和 Toyota ELEY 三种机械臂上。

一个低成本验证方式是在正式采集前做并排操作者研究：10 名新手、重复的小物体抓取试验、1 小时疲劳检查，以及按每个操作者小时的可用 episode 数来算吞吐量。如果更轻的夹爪能改善小物体控制和单次会话时长，下一步就可以搭一个固定桌面采集架，配同步手腕相机、俯视 RGB-D、6 自由度夹爪位姿、夹爪角度、任务文本和子动作标签。

### Evidence
- [YUBI: Yielding Universal Bidigital Interface for Bimanual Dexterous Manipulation at Scale](../Inbox/2026-06-08--yubi-yielding-universal-bidigital-interface-for-bimanual-dexterous-manipulation-at-scale.md): YUBI reports the finger-aligned gripper design, weight and cost comparisons, dataset scale, LeRobot conversion, and cross-arm policy transfer results.
