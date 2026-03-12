---
source: arxiv
url: http://arxiv.org/abs/2603.07949v1
published_at: '2026-03-09T04:30:57'
authors:
- Zihao Zheng
- Sicheng Tian
- Hangyu Cao
- Chenyue Li
- Jiayu Chen
- Maoliang Li
- Xinhao Sun
- Hailong Zou
- Guojie Luo
- Xiang Chen
topics:
- edge-cloud-inference
- vision-language-action
- robotics-systems
- dynamic-offloading
- kinematics-based-triggering
relevance_score: 0.78
run_id: fa4f5d9d-bee2-47ee-b80f-c690622f57d0
---

# RAPID: Redundancy-Aware and Compatibility-Optimal Edge-Cloud Partitioned Inference for Diverse VLA models

## Summary
- TL;DR: RAPID 用“机器人自身的运动学/动力学信号”替代易受视觉噪声干扰的视觉置信度触发器，实现对多类 VLA 模型更稳健的边云动态分流，在提升成功率/准确性的同时显著降低端侧时延与动作中断。
- Problem:
  - VLA（Vision-Language-Action）模型参数大、推理慢，端侧难以满足机器人实时控制。
  - 现有边云协同（ECC）动态分流多依赖视觉不确定性（如动作分布熵）来触发上云，容易被视觉噪声/遮挡/干扰物误触发，导致频繁上云、通信开销上升与动作连续性受破坏。
  - 现有方法忽略具身任务“分步动作重要性不均”的冗余特性（大量步骤可在端侧稳定执行，关键交互步骤才需要更强推理），使分流不够高效。
- Approach:
  - 兼容性最优（Compatibility-Optimal）触发：用与环境无关的关节瞬时加速度（由关节速度差分得到）检测任务切换/避障/急停等非线性运动突变；在滑动窗口内做均值-方差归一化得到“异常分数”，降低速度变化带来的误判。
  - 冗余感知（Redundancy-Aware）触发：用关节力矩的高频变化（Δτ）作为“步骤冗余”的轻量替代指标——平滑接近阶段力矩变化小（高冗余，可端侧继续执行缓存 action chunk），接触/操作阶段力矩突变大（低冗余，应上云重规划）；同样用滑动统计归一化以适配不同任务力尺度。
  - 动态融合：根据当前关节速度大小自适应分配“加速度监测 vs 力矩监测”的权重，在高速自由空间运动时更看重加速度突变、低速操作时更看重力矩波动，并用双阈值触发上云。
  - 系统实现优化：异步多速率架构（高频 500Hz 传感轮询 + 低频 20Hz 控制执行）、动作抢占（关键阶段丢弃剩余 chunk 并立即请求云端新 chunk）、冷却时间（cooldown）防止连续上云洪泛；端侧触发计算为 O(1) 轻量开销。
- Results:
  - 论文声明：相对 Edge-Only VLA 与视觉分流基线（如 ISAR/SAFE），RAPID **最高推理加速 1.73×**，且仅需 **$5\sim7** 的额外开销（实现/部署成本）。
  - 论文声明：在多样任务/环境下 **准确率最高提升 15.8%**（相对基线；摘录未给出更细的度量定义）。
  - 仿真基准（LIBERO + OpenVLA，表 III）：总时延从 **Edge-Only 782.5±28.5ms** 降至 **RAPID 222.9±11.4ms**；相对视觉分流 SAFE **377.7±26.2ms**，RAPID 进一步降低到 **222.9±11.4ms**。
  - 抗噪性证据（表 I）：视觉熵触发在噪声/干扰下导致总时延上升（例如标准 395.4ms → 视觉噪声 520.6ms → 干扰 685.3ms），论文据此主张运动学触发更稳定、可减少无效上云与动作中断。
  - 冗余分析（表 II）：在 Pick&Place/Drawer/Peg 等任务中，动作序列中 **冗余步骤占比 81.2%~86.4%**，其平均注意力权重 **0.005~0.008**，关键步骤权重显著更高（约 **0.058~0.076**）；RAPID 用力矩变化作为可观测替代信号来利用这一冗余。

## Links
- Canonical: http://arxiv.org/abs/2603.07949v1
