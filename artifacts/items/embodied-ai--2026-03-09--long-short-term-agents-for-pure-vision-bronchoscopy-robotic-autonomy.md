---
source: arxiv
url: http://arxiv.org/abs/2603.07909v1
published_at: '2026-03-09T03:09:51'
authors:
- Junyang Wu
- Mingyi Luo
- Fangfang Xie
- Minghui Zhang
- Hanxiao Zhang
- Chunxi Zhang
- Junhao Wang
- Jiayuan Sun
- Yun Gu
- Guang-Zhong Yang
topics:
- surgical-robotics
- vision-only-navigation
- imitation-learning
- hierarchical-agents
- world-model-critic
- vision-language-guidance
relevance_score: 0.56
run_id: fa4f5d9d-bee2-47ee-b80f-c690622f57d0
---

# Long-Short Term Agents for Pure-Vision Bronchoscopy Robotic Autonomy

## Summary
- TL;DR: 提出一种仅用内镜视频+术前CT（无电磁/形状传感等外部定位）的分层“长-短期智能体”系统，实现机器人支气管镜的长航程自主导航，并在体模/离体/活体猪模型中达到接近专家的终点一致性。
- Problem:
  - 机器人支气管镜在深部、分叉多、视野窄且存在运动模糊/液体遮挡等伪影的气道中，长距离自主导航困难。
  - 现有临床导航多依赖电磁跟踪或形状传感，增加硬件与流程复杂度，并受CT-体内解剖不匹配、金属干扰等影响。
  - 需要一种“纯视觉”闭环控制方案，既能连续操控又能在分叉等歧义点做出正确决策。
- Approach:
  - 将术前CT分割气道与目标，并沿规划中心线渲染“虚拟支气管镜视图序列”，把导航变为逐个子目标的视觉对齐与自动切换。
  - 短期Reactive Agent：轻量Transformer（EfficientNet-B0编码当前帧与目标虚拟图，decoder-only Transformer输出动作），动作空间含前/后、四向弯折与“切换子目标”；用模仿学习（交叉熵）从专家演示训练，负责低延迟连续控制。
  - 长期Strategic Agent：仅在分叉/异常等关键点触发，融合两类高层指导：①基于术前中心线的几何动作建议（近10帧多数投票）；②多模态大模型(LLM)根据带方向标注的虚拟目标图+结构化提示给出高层动作序列。
  - 冲突消解：若长期建议落在短期策略top-K logits内则直接执行；若冲突来自LLM指导，则调用世界模型作为critic，对候选动作预测短期未来视觉rollout，并用LPIPS与目标虚拟视图比对，选取感知距离最小的动作。
- Results:
  - 高保真体模全肺17段：在17条轨迹上均到达规划终点（覆盖与专家一致）；平均到达代数(Generation)为5.53±1.55，优于GNM(4.24±1.60)与ViNT(3.65±1.62)。
  - 体模效率：相比专家遥操作，耗时更长但动作更少——450.7±69.5 s vs 273.5±77.5 s；动作数275.8±31.9 vs 346.8±45.9（P<0.001）。文中指出主要增时来自每步强制3 s安全执行窗口，模型推理约6 ms。
  - 体模视觉对齐：终点SSIM 0.841±0.066，高于结构相近的ViNT基线0.776±0.044，强调“长-短期分层+协作”对长航程误差累积的抑制作用。
  - 视觉伪影鲁棒性（镜头涂甘油，清洁vs污染初始SSIM降至0.59）：5条轨迹完成4/5（RB2失败）；伪影下终点SSIM 0.874±0.051，与清洁条件0.878±0.033无显著差异，但动作数显著增加419.4±72.9（清洁自驾270.0±40.4）。
  - 离体猪肺（3个样本、59条轨迹）：对第8代内目标保持>80%成功率；平均用时323.82±123.92 s、平均动作198.12±79.34；主要失败来自镜头被黏液持续覆盖或气泡完全遮挡导致目标不可见。
  - 活体猪（呼吸导致变形/运动伪影，7个任务）：100%成功(7/7)；与资深专家终点在CBCT坐标系下平均偏差4.90±2.64 mm（与资深-初级医生差异3.92±2.42 mm同量级）；终点视图SSIM为0.7701±0.0564（接近资深-初级0.7847±0.0401）；4个结节任务到结节最小距离6.77–20.55 mm（例：Traj1 自动6.77 mm vs 资深10.08 mm）；用时417.1±74.9 s显著慢于资深176.7±52.5 s（P=0.016），但动作数240.6±28.2与资深/初级无显著差异，作者将增时归因于每步3 s安全限制而非推理延迟。

## Links
- Canonical: http://arxiv.org/abs/2603.07909v1
