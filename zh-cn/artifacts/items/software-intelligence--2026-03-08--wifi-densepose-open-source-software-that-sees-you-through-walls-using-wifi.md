---
source: hn
url: https://github.com/ruvnet/RuView
published_at: '2026-03-08T23:42:57'
authors:
- CGMthrowaway
topics:
- wifi-sensing
- through-wall-sensing
- edge-ai
- pose-estimation
- vital-sign-monitoring
- rust
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# WiFi-DensePose – open-source software that sees you through walls using wifi

## Summary
这是一个开源的边缘WiFi感知系统，试图仅用无线信号而非摄像头/可穿戴设备来重建人体姿态、检测存在并估计呼吸和心率。其核心卖点是低成本ESP32/CSI硬件、本地运行、自监督学习，以及面向多节点部署的工程化实现。

## Problem
- 传统人体感知通常依赖摄像头、云端推理或可穿戴设备，带来隐私、部署成本、视线遮挡和联网依赖问题。
- 仅凭普通环境中的无线信号进行姿态/生命体征/隔墙感知很难，因为CSI信号噪声大、强依赖房间环境、多人时易混叠。
- 该问题重要在于可为医疗、安防、机器人、建筑与灾害救援提供**无接触、非视觉、可离线**的空间感知能力。

## Approach
- 用CSI（Channel State Information）替代图像：人体移动或呼吸会改变WiFi多径散射，系统从这些扰动中恢复17个身体关键点、呼吸率、心率和存在状态。
- 信号链路是“物理+学习”混合：先做相位清洗、Hampel滤波、SpotFi/Fresnel/BVP/频谱等处理，再送入基于Transformer/图网络/交叉注意力的模型。
- 多节点多频融合：4-6个ESP32节点以TDM协作，跨1/6/11信道融合为168个虚拟子载波，并对N×(N-1)链路做注意力加权融合与coherence gate稳定化。
- 强调边缘自学习：声称不需要训练摄像头、云端或人工标注，可在设备侧形成128维房间/活动指纹，并持续适应新环境；同时提出MERIDIAN跨房间泛化与SONA持续适应机制。
- 工程实现上，系统提供Rust主实现、REST/WebSocket API、WASM边缘模块、RVF单文件模型封装，以及ESP32独立运行能力。

## Results
- **速度/吞吐**：声称Rust v2相对Python v1实现**810x端到端加速**，运动检测达**5,400x提升**；生命体征检测单线程可达**11,665 frames/s**。
- **硬件/部署**：边缘节点可低至**约$1/节点**（文中也多处写**$8-$9 ESP32-S3**），多静态方案中**4个ESP32-S3总计$48**，形成**12条TX-RX链路**并实现**360°覆盖**。
- **实时性与采样**：ESP32-S3节点可进行**28 Hz CSI流式采集**；多节点追踪声称支持**20 Hz双人跟踪**。
- **多人跟踪**：文中宣称在多静态融合下，**两人跟踪20 Hz、10分钟内0次identity swap**；单AP可区分约**3-5人**，**4 AP**零售网格可覆盖约**15-20名占用者**。
- **模型/资源**：自学习模型声称可在**$8 ESP32**上运行，模型占用**55 KB内存**，输出**128维指纹 + 17关节姿态**。
- **验证/测试**：仓库层面声称**60个边缘模块**已实现、**609 tests passing**；另处称**542+** Rust测试；独立审计部分报告**1,031 tests passed, 0 failed**。但**未提供标准学术数据集上的姿态误差、心率MAE、跨房间泛化精度等关键对比指标**，因此其最强证据主要是工程基准与仓库自述测试结果，而非经论文式量化评测的SOTA对比。

## Link
- [https://github.com/ruvnet/RuView](https://github.com/ruvnet/RuView)
