---
source: hn
url: https://github.com/arryllopez/meerkat
published_at: '2026-03-05T23:28:54'
authors:
- arryleo10
topics:
- blender-plugin
- real-time-collaboration
- 3d-scene-editing
- websocket-sync
- collaborative-software
relevance_score: 0.54
run_id: materialize-outputs
---

# Show HN: Real-time collaborative editing plugin for Blender

## Summary
Meerkat 是一个面向 Blender 的实时协作编辑插件，目标是在同一场景内支持多人同时编辑并同步变换。它用轻量级网络同步替代手工传递 `.blend` 文件，试图降低团队协作中的版本冲突与覆盖风险。

## Problem
- Blender **缺少内置实时协作**，团队通常依赖聊天或云盘传递 `.blend` 文件，容易出现版本分叉和互相覆盖。
- 多人共同编辑 3D 场景时，**对象位置/旋转/缩放的变化无法即时共享**，协作效率低。
- 远程协作还面临网络接入问题，因此需要同时支持**局域网直连和云中继**。

## Approach
- 系统分为两部分：**Rust 后端** 和 **Python Blender 插件**；前者负责 WebSocket 会话、对象 ID/变换 diff 与中继逻辑，后者负责在 Blender 内捕获本地改动并应用远端更新。
- 核心机制是**只同步对象 ID 与 transform 增量**，而不是完整 mesh 数据，从而尽量降低带宽占用。
- 插件通过 Blender 的 **depsgraph update handlers** 监听场景变化，把本地对象的位移、旋转、缩放广播到会话中的其他用户。
- 支持**共享会话、多人场景编辑、存在感提示、彩色选择高亮**，并提供**冲突处理**以减少同时编辑时的覆盖问题。
- 网络层同时提供**点对点连接**（同一网络下无需中继）和**可选云 relay**（远程团队无需端口转发）。

## Results
- 文本**没有提供正式量化实验结果**，也没有给出基准数据集、延迟、吞吐、带宽或用户研究指标。
- 已声明的功能结果包括：**多人同时编辑同一 Blender 场景**、**对象 position/rotation/scale 实时同步**、**会话 host/join**、**冲突处理**、**用户在线与选择状态显示**。
- 工程实现上给出了明确技术栈与环境：**Rust 1.75+、Python 3.10+、Blender 4.0+**；后端使用 **tokio + axum + WebSocket**。
- 论文/项目声称的最强具体收益是：通过**仅传输对象 ID 和变换**而非完整 mesh，达到**更低带宽开销**；但文中**未给出具体数值对比**。
- 当前状态为**Alpha 即将发布**，因此成果更接近早期系统原型展示，而非经过全面评测的研究突破。

## Link
- [https://github.com/arryllopez/meerkat](https://github.com/arryllopez/meerkat)
