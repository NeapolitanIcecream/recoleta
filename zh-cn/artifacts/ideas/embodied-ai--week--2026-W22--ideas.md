---
kind: ideas
granularity: week
period_start: '2026-05-25T00:00:00'
period_end: '2026-06-01T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- vision-language-action models
- real-robot evaluation
- dexterous manipulation
- tactile control
- continual learning
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/real-robot-evaluation
- topic/dexterous-manipulation
- topic/tactile-control
- topic/continual-learning
language_code: zh-CN
---

# 机器人操作部署检查

## 摘要
机器人 VLA 研究现在为团队提供了面向部署的具体控制检查：带回归测试的短时在线微调、显式 SE(3) 动作几何，以及在任务成功可能掩盖不安全操作时使用的接触力指标。

## 带旧任务回归检查的在线 VLA 微调站
试用预训练 VLA 策略的机器人团队，可以围绕在线 rollout、人工纠正、稀疏奖励检测器、回放，以及固定的动作归一化设置，搭建一个小型后训练站。目标用户是操作员：他们看到一个策略在微调后学会了新任务，随后发现早期技能退化了。

EXPO-FT 给出了可执行的模板：把预训练策略保留为基础策略，训练一个轻量编辑策略来修正 action chunk，让 Q-function 在基础 chunk 和编辑后的 chunk 之间选择价值更高的一个，并把在线 rollout 中的人工纠正存入回放。论文报告的真实机器人结果是：平均使用 19.1 分钟在线数据后，在八个操作任务上达到 30/30 成功，最终成功由人工观察者判断。

回归检查很关键，因为顺序 VLA 微调可能抹掉先前任务。在一项真实世界持续学习研究中，普通微调使 Stack Bowl 从 100.0 降到 15.0，使 Hang Cup 从 97.5 降到 25.0；使用 0.2 缓冲区比例、0.2 回放频率和固定动作归一化的回放方法，在四个任务上达到 93.5 的最终平均分。一个实用的采用检查是：在每个微调阶段后运行新任务和所有此前已验收任务，并在整条部署线上使用相同的动作缩放。

### 资料来源
- [EXPO-FT: Sample-Efficient Reinforcement Learning Finetuning for Vision-Language-Action Models](../Inbox/2026-05-25--expo-ft-sample-efficient-reinforcement-learning-finetuning-for-vision-language-action-models.md): EXPO-FT 描述了针对 VLA action chunk 的在线离策略 RL 微调、人工纠正、稀疏奖励，以及平均使用 19.1 分钟在线数据后达到 30/30 真实任务成功。
- [Can VLA Models Learn from Real-World Data Continually without Forgetting?](../Inbox/2026-05-26--can-vla-models-learn-from-real-world-data-continually-without-forgetting.md): 这项持续学习研究显示，普通顺序微调会造成严重遗忘；使用固定动作归一化的回放能带来强保留效果。

## 面向 VLA 操作策略的 SE(3) 轨迹记录
操作评估应要求 VLA 策略暴露其用于生成 action chunk 的未来末端执行器位姿。对于在 Franka、Kinova、ALOHA 或移动操作设置之间比较策略的实验室，这只是一个低成本接口改动：记录预测的位姿轨迹、已执行的 action chunk、夹爪命令、机器人状态，以及推理时使用的机器人描述。

OASIS 说明了这类轨迹记录的用途。它先预测一个 8 步相机坐标系 SE(3) 末端执行器轨迹，再解码 6-DoF 相对动作和夹爪命令。它的消融实验把最大增益归因于 SE(3) 轨迹预测器：LIBERO-Long 从 89.5% 升至 95.2%，LIBERO-Spatial 从 91.6% 升至 99.0%。它还报告，在 Franka Research 3 和 Kinova Gen3 机器人的真实世界测试中，平均成功率为 89.2%。

Qwen-VLA 指向同一记录需求的跨 embodiment 版本。它使用 embodiment-aware prompts 指定机器人标签、机械臂设置、控制频率和预测时域，然后用带 padding 和 mask 的共享张量格式训练动作和轨迹。一个简单的评估工具可以在相机视角、背景、物体布局和机器人 prompt 变化时比较位姿轨迹稳定性，然后再考虑只来自基准测试的成功率。

### 资料来源
- [OASIS: Observation-Action Space Alignment via SE(3) Trajectory Prediction for Robotic Manipulation](../Inbox/2026-05-25--oasis-observation-action-space-alignment-via-se-3-trajectory-prediction-for-robotic-manipulation.md): OASIS 在动作解码前使用 SE(3) 轨迹预测器，并报告了在 LIBERO、真实机器人和分布外扰动上的增益。
- [Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments](../Inbox/2026-05-28--qwen-vla-unifying-vision-language-action-modeling-across-tasks-environments-and-robot-embodiments.md): Qwen-VLA 使用 embodiment-aware prompts，以及跨操作、导航和机器人 embodiment 的共享动作与轨迹张量格式。

## 面向轻柔和灵巧操作任务的接触力报告
当物体可能被挤压、撞击、卡住或损坏时，机器人操作测试应在任务完成情况之外记录接触质量。具体做法是构建一个评估工具，在同一次 rollout 中记录平均和峰值夹持力、平均和峰值施加力、触觉接触位置，以及任务成功情况。

Tabero 给出了这个工具的 VLA 风格版本。它在 Isaac Lab 中生成同步的视觉、触觉、力、本体感知、动作和语言数据，把触觉标记运动或触觉图像编码为 token，并把位姿和力目标发送给混合控制器。它的基准报告四种力指标，并声称在“轻柔”指令下，平均夹持力降低超过 70%，同时保持高任务成功率。

CoP 给出了灵巧手版本。它把触觉 taxel 读数压缩为每个触觉感知区域的 3D 接触力和 3D 接触位置，然后在带传感器延迟和域随机化的仿真中训练策略。在跨六种形状的真实 peg-in-hole 插入中，CoP 达到 0.78 成功率，高于二值接触的 0.53 和原始 taxel 的 0.48。使用触觉夹爪或灵巧手的团队可以从一个盲插入任务或易碎物体抓取任务开始，并同时发布成功率、力轨迹和接触位置轨迹。

### 资料来源
- [Tabero: Learning Gentle Manipulation with Closed-Loop Force Feedback from Vision, Touch, and Language](../Inbox/2026-05-27--tabero-learning-gentle-manipulation-with-closed-loop-force-feedback-from-vision-touch-and-language.md): Tabero 加入触觉 token 和闭环力控制，评估夹持力和施加力，并报告在“轻柔”指令下平均夹持力降低超过 70%。
- [Beyond Binary: Sim-to-Real Dexterous Manipulation with Physics-Grounded Contact Representation](../Inbox/2026-05-27--beyond-binary-sim-to-real-dexterous-manipulation-with-physics-grounded-contact-representation.md): CoP 将密集触觉读数映射为接触力和接触位置，并报告其真实 peg-in-hole 成功率高于二值接触和原始 taxel 基线。
