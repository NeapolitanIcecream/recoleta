---
source: hn
url: https://github.com/ruvnet/RuView
published_at: '2026-03-08T23:42:57'
authors:
- CGMthrowaway
topics:
- wifi-sensing
- csi-pose-estimation
- through-wall-sensing
- edge-ai
- self-supervised-learning
relevance_score: 0.42
run_id: materialize-outputs
---

# WiFi-DensePose – open-source software that sees you through walls using wifi

## Summary
这是一个开源的基于 WiFi CSI 的无摄像头人体感知系统，目标是在本地边缘设备上实现姿态、存在检测和生命体征推断，甚至宣称可穿墙工作。它把学术上的 WiFi DensePose 概念扩展为可部署的软件/固件栈，并强调自学习、低成本和离线运行。

## Problem
- 传统视觉传感依赖摄像头、可穿戴设备或云端模型，在隐私、遮挡、烟雾/粉尘、视线受限和穿墙场景下受限。
- 现有 WiFi 姿态研究常依赖同步摄像头标注训练，难以在真实房间中低成本、长期、自适应部署。
- 需要一种能利用现有无线信号、在边缘端实时运行、且尽量无需标注与联网的人体/环境感知方案；这对安防、医疗监测、智能空间和机器人在非视距环境中的感知都重要。

## Approach
- 核心机制很简单：人移动、呼吸或心跳会扰动室内 WiFi 无线电波；系统读取这些扰动的 CSI（子载波幅度/相位），再把它们变成“人体姿态 + 生命体征 + 房间指纹”。
- 感知流水线为：ESP32/CSI 设备采集 CSI → 多信道/多节点融合（如 3 个信道 × 56 子载波 = 168 虚拟子载波）→ 相干性门控过滤噪声 → 信号处理（Hampel、SpotFi、Fresnel、BVP、频谱图）→ Transformer/GNN/注意力骨干 → 输出 17 个关键点、呼吸/心率、存在状态等。
- 系统强调“自学习”与边缘部署：从原始 WiFi 数据学习 128 维环境嵌入/房间指纹，宣称不依赖摄像头、标签或云；模型可在 ESP32 级别硬件上运行，文中称模型约 55 KB。
- 通过多静态 mesh 方案提升覆盖与抗遮挡能力：N 个节点形成 N×(N-1) 条收发链路，结合跨视角注意力融合、卡尔曼跟踪和环境场模型，减少盲区并支持多人跟踪。
- 还加入跨环境泛化/域不变设计（MERIDIAN），用硬件归一化、对抗域分类器和几何条件化，试图做到“train once, deploy in any room”。

## Results
- 论文摘录**没有提供标准学术基准上的姿态精度数字**（如 MPJPE/PCK、具体数据集对比、误差条或 SOTA 排名），因此无法验证其人体姿态/穿墙感知准确率。
- 工程性能方面，项目声称 Rust v2 相比 Python v1 **端到端提速 810x**，其中运动检测 **提升 5,400x**；生命体征检测单线程吞吐 **11,665 frames/s**。
- 设备与系统规模方面，声称单个 AP 可区分约 **3–5 人**，多 AP 可近线性扩展；举例称 **4 个 AP** 的零售 mesh 可覆盖约 **15–20 名** 占用者。
- 多静态配置方面，声称 **4 个 ESP32-S3 节点（总价约 $48）** 可产生 **12 条 TX-RX 测量链路**，并通过信道跳频把带宽从 **20→60 MHz**；还声称实现 **20 Hz 双人跟踪**，在 **10 分钟** 内 **零 identity swaps**。
- 边缘/硬件指标方面，ESP32-S3 管线声称可进行 **28 Hz CSI 流式采集**，边缘模块大小约 **5–30 KB**，本地决策延迟 **<10 ms**，整模型可压到 **55 KB** 并运行在约 **$8** 的 ESP32 上。
- 验证与工程完备性方面，文本声称 **542+**、**609**、**1,031** 等多组测试全部通过，以及 **7/7** 审计检查通过；但这些更多证明代码/实现完整性，不等同于感知任务上的科学效果验证。

## Link
- [https://github.com/ruvnet/RuView](https://github.com/ruvnet/RuView)
