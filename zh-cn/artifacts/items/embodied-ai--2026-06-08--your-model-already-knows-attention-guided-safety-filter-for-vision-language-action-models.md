---
source: arxiv
url: https://arxiv.org/abs/2606.09749v1
published_at: '2026-06-08T17:11:16'
authors:
- Seongbin Park
- Fan Zhang
- Baharan Mirzasoleiman
- Shahriar Talebi
- Nader Sehatbakhsh
topics:
- vision-language-action
- robot-safety
- control-barrier-functions
- attention-analysis
- collision-avoidance
- safe-libero
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Your Model Already Knows: Attention-Guided Safety Filter for Vision-Language-Action Models

## Summary
## 摘要
论文的主张是，冻结的 VLA 策略里已经有足够的注意力信号，可以识别当前要接近的目标物体，因此安全过滤器在控制过程中不需要再调用单独的 VLM，就能避开其他物体。该方法在 VLA 策略外面加了一个无需训练的包装层，并在动态 SafeLIBERO 场景中报告了很大的碰撞率下降。

## 问题
- VLA 机器人策略可以完成操作任务，但由于动作没有安全规则约束，仍可能与任务无关的物体碰撞。
- 以往的 CBF 安全过滤器通常在 episode 开始时用一次 VLM 或场景解析器来判断哪个物体是目标、哪些物体是障碍物，因此当障碍物移动时就会失效。
- 这会影响共享或变化中的场景部署，因为过时的障碍物标记会把原本安全的初始计划变成碰撞。

## 方法
- 作者发现，冻结 VLA 中少量注意力头会关注策略正在移动到的物体。
- 在每个控制步，他们读取一个选定的注意力头，将跟踪到的物体椭球投影到图像中，并把注意力质量分配给每个物体。
- 在滑动窗口内注意力密度最高的物体被当作活动目标；其余所有物体都被当作障碍物。
- YOLOE 分割跟踪器在线更新物体位置，而椭球形状在 episode 开始时拟合一次。
- 离散时间 CBF-QP 过滤器把 VLA 动作投影为一个附近的安全动作，保持末端执行器椭球与障碍物椭球分离。

## 结果
- 在带移动障碍物的 SafeLIBERO Level III 上，Knows 将平均碰撞率从仅在初始化时识别目标的 Naive 过滤器的 70.75% 降到 26.88%，在 spatial、object、goal 和 long 四个套件上的平均下降为 43.88 个百分点。
- 在同样的动态 Level III 设置中，平均安全成功率从 Naive 的 25.5% 提高到 55.75%。
- 在动态 Level III 中，Knows 在四个套件里的安全成功率都高于 Naive：spatial 为 54.5% 对 34.0%，object 为 70.5% 对 40.0%，goal 为 63.5% 对 9.5%，long 为 34.5% 对 18.5%。
- 与 Level III 上不使用 CBF 的方法相比，Knows 将碰撞率在 spatial 中从 84.5% 降到 29.0%，在 object 中从 48.5% 降到 14.0%，在 goal 中从 90.0% 降到 30.5%，在 long 中从 82.0% 降到 34.0%。
- 运行时间能放进 20 Hz 控制循环：每步总包装开销为 49.3 ms，其中注意力提取 0.8 ms，YOLOE 分割 19.3 ms，深度加质心更新 9.1 ms，目标识别 9.4 ms，OSQP 安全求解 11.4 ms。
- 被选中的注意力头还能预测 80 个长任务回合中的任务结果：早期目标质量的 AUC 为 0.93，早期目标密度的 AUC 为 0.89，通往无关目标的密度接近随机水平，AUC 为 0.55。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09749v1](https://arxiv.org/abs/2606.09749v1)
