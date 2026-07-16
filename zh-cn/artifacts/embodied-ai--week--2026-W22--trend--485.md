---
kind: trend
trend_doc_id: 485
granularity: week
period_start: '2026-05-25T00:00:00'
period_end: '2026-06-01T00:00:00'
topics:
- robot learning
- vision-language-action models
- real-robot evaluation
- dexterous manipulation
- tactile control
- continual learning
run_id: materialize-outputs
aliases:
- recoleta-trend-485
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/real-robot-evaluation
- topic/dexterous-manipulation
- topic/tactile-control
- topic/continual-learning
language_code: zh-CN
---

# 机器人 VLA 主张现在需要真实控制证据

## 概览
本周机器人研究用真实执行来评估视觉-语言-动作（VLA）策略：在线微调速度、任务保持、接触质量和跨具身覆盖。EXPO-FT、OASIS 和 Qwen-VLA 支撑了证据最足的主张，多数证据来自真实机器人或操作基准。

## 研究发现

### 真实机器人训练后适配
多篇论文把 VLA 部署视为训练后的问题，并用机器人时间和失败恢复来衡量。EXPO-FT 报告，在平均使用 19.1 分钟在线机器人数据后，八个真实操作任务达到 30/30 成功。BORA 为灵巧手控制加入离线 critic 和一个小型人工引导残差 actor，在五个 Franka 机械臂加 12-DoF 手任务上达到 86.0% 平均成功率。一项持续学习研究给出对照：普通顺序微调会抹掉早期技能，而采用固定动作归一化的经验回放把最终平均分提高到 93.5。

#### 资料来源
- [EXPO-FT: Sample-Efficient Reinforcement Learning Finetuning for Vision-Language-Action Models](../Inbox/2026-05-25--expo-ft-sample-efficient-reinforcement-learning-finetuning-for-vision-language-action-models.md): EXPO-FT 报告，在平均使用 19.1 分钟在线数据后，真实任务成功率达到 30/30。
- [BORA: Bridging Offline Reinforcement Learning and Online Residual Adaptation for Real-World Dexterous VLA Models](../Inbox/2026-05-28--bora-bridging-offline-reinforcement-learning-and-online-residual-adaptation-for-real-world-dexterous-vla-models.md): BORA 报告了离线到在线 RL 在真实灵巧操作任务上的收益。
- [Can VLA Models Learn from Real-World Data Continually without Forgetting?](../Inbox/2026-05-26--can-vla-models-learn-from-real-world-data-continually-without-forgetting.md): 持续 VLA 研究量化了真实操作任务中的遗忘和基于回放的保持效果。

### 动作几何和跨任务迁移
证据较强的控制论文都在动作预测周围加入结构。OASIS 在解码动作块之前预测 SE(3) 中的未来末端执行器位姿，并报告 LIBERO 平均成功率 97.6%，真实世界测试平均成功率 89.2%。Qwen-VLA 使用具身感知提示和共享的动作与轨迹格式，用一个策略覆盖操作、导航和轨迹预测。VLA-Pro 把任务特定 LoRA 适配器存为程序性记忆，并在推理时检索，使保留 UR7e 任务的真实世界成功率从 5.8% 提高到 65.0%。

#### 资料来源
- [OASIS: Observation-Action Space Alignment via SE(3) Trajectory Prediction for Robotic Manipulation](../Inbox/2026-05-25--oasis-observation-action-space-alignment-via-se-3-trajectory-prediction-for-robotic-manipulation.md): OASIS 摘要给出了 SE(3) 轨迹机制，以及仿真和真实世界成功率结果。
- [Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments](../Inbox/2026-05-28--qwen-vla-unifying-vision-language-action-modeling-across-tasks-environments-and-robot-embodiments.md): Qwen-VLA 摘要描述了共享动作格式、具身提示和基准结果。
- [VLA-Pro: Cross-Task Procedural Memory Transfer for Vision-Language-Action Models](../Inbox/2026-05-28--vla-pro-cross-task-procedural-memory-transfer-for-vision-language-action-models.md): VLA-Pro 摘要报告了程序性记忆检索和真实世界保留任务收益。

### 触觉和力控制
接触质量开始进入评估目标。Tabero 加入触觉 token 和闭环力命令，然后同时测量成功率、抓握力和施加力。它报告在轻柔指令下平均抓握力降低超过 70%。CoP 将触觉 taxel 读数压缩为接触力和接触位置，用于仿真到真实的灵巧操作，在六种形状上达到 0.78 的真实插孔成功率。Mag-VLA 把同类执行关注点扩展到显微尺度双手机磁操控，接近成功率为 90%，且路径曲率升高时运输成功率下降。

#### 资料来源
- [Tabero: Learning Gentle Manipulation with Closed-Loop Force Feedback from Vision, Touch, and Language](../Inbox/2026-05-27--tabero-learning-gentle-manipulation-with-closed-loop-force-feedback-from-vision-touch-and-language.md): Tabero 摘要详细说明了触觉-力数据、闭环控制和降力主张。
- [Beyond Binary: Sim-to-Real Dexterous Manipulation with Physics-Grounded Contact Representation](../Inbox/2026-05-27--beyond-binary-sim-to-real-dexterous-manipulation-with-physics-grounded-contact-representation.md): CoP 摘要报告了接触表示和真实插孔结果。
- [Mag-VLA: Vision-Language-Action Model for Bimanual Magnetically Actuated Microrobot Manipulation](../Inbox/2026-05-27--mag-vla-vision-language-action-model-for-bimanual-magnetically-actuated-microrobot-manipulation.md): Mag-VLA 摘要报告了相位感知双手机器人控制和真实机器人成功率。

### 更低成本的验证和更小策略
成本是本周证据中的明确约束。ProgVLA 使用一个 0.1B 参数策略，配有压缩多模态 token 和进度头，在 LIBERO 上达到 91.1% 平均成功率，在 LIBERO Long 上达到 88.6%。它的真实 PiPER-arm 测试较低，100 次试验成功率为 68%，这为只看基准的主张提供了有用校验。日级趋势还把 HyperSim 和 SDPG 归入降低真实数据或 GPU 成本的工作，将效率和执行质量放在一起评估。

#### 资料来源
- [ProgVLA: Progress-Aware Robot Manipulation Skill Learning](../Inbox/2026-05-27--progvla-progress-aware-robot-manipulation-skill-learning.md): ProgVLA 摘要提供了参数量、基准分数、消融和真实机器人测试结果。
