---
source: hn
url: https://github.com/arryllopez/meerkat
published_at: '2026-03-05T23:28:54'
authors:
- arryleo10
topics:
- blender-plugin
- real-time-collaboration
- 3d-editing
- websocket-sync
- collaborative-tools
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Real-time collaborative editing plugin for Blender

## Summary
Meerkat 是一个面向 Blender 的实时协同编辑插件，目标是在同一场景中支持多人同时编辑并同步变换。它通过轻量级网络同步与冲突处理，试图替代团队间手动传递 `.blend` 文件的低效流程。

## Problem
- Blender 缺少内置的实时协作能力，团队通常只能通过聊天或云盘来回传递 `.blend` 文件，容易发生版本混乱和相互覆盖。
- 多人同时编辑 3D 场景时，若没有低延迟同步、冲突处理和在线状态可视化，协作效率会很低。
- 这个问题重要，因为 3D 内容制作常常是多人协作流程，缺少实时协同会直接拖慢创作与审阅速度。

## Approach
- 系统分为两个部分：Rust 后端负责 WebSocket 会话、对象 ID/变换差分同步和中继逻辑；Python Blender 插件负责监听 Blender 场景更新并发送/应用远端改动。
- 核心机制很简单：**不传完整网格数据，只传对象 ID 以及位置/旋转/缩放等变换增量**，从而降低带宽占用并实现实时同步。
- 插件接入 Blender 的 depsgraph update handlers，捕获本地修改；远端修改以 delta 形式回放到本地场景。
- 支持 host/join 会话、同局域网点对点连接，以及可选云中继，减少远程协作部署门槛。
- 通过冲突解决、在线用户显示和选中高亮，尽量让同时编辑时不会互相覆盖工作内容。

## Results
- 文本**没有提供定量实验结果**，没有给出延迟、带宽、吞吐量、用户研究或与其他系统的基线对比数字。
- 公开声称已支持的能力包括：多人场景编辑、对象变换实时同步、共享会话、冲突解决、在线成员可见性、点对点模式、可选云中继。
- 文本明确指出后端仅传输“object IDs and transforms rather than full mesh data”，其最强具体主张是**以更小带宽实现实时同步**，但未给出具体节省比例。
- 代码与工程层面给出了一些成熟度信号：Rust backend（tokio + axum）、Blender 4.0+ 插件测试、`cargo test`/`clippy` 支持，但项目仍处于 **Alpha dropping soon / not yet released** 阶段。

## Link
- [https://github.com/arryllopez/meerkat](https://github.com/arryllopez/meerkat)
