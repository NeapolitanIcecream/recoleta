---
source: hn
url: https://www.eventual.ai/blog/egodex-scenario-search
published_at: '2026-07-01T22:45:06'
authors:
- sammysidhu
topics:
- robot-data-scaling
- dexterous-manipulation
- multimodal-search
- egocentric-video
- hand-pose-geometry
relevance_score: 0.7
run_id: materialize-outputs
language_code: zh-CN
---

# Finding a Needle in the Haystack: Querying Physical AI Data with Daft

## Summary
## 摘要
Daft 用一个按帧组织的表，结合手部几何和文本语义来搜索 Apple EgoDex 视频。主要价值是更快找回未标注的机器人操作片段，用于审计、故障挖掘和微调。

## 问题
- 机器人团队会收集很长的第一视角视频和手部姿态流，但任务级标签会掩盖细粒度事件，例如扭转、紧握和特定物体的抓取。
- 故障挖掘和重新训练需要精确时刻，而不是整段 episode，尤其是在数据持续到达时。
- 仅靠文本搜索会漏掉手部姿态和动作细节，这些细节存储在传感器几何数据中。

## 方法
- 该系统为 Daft 增加原生 HDF5 支持，并将每个 EgoDex HDF5/MP4 对读入按帧组织的 DataFrame，其中包含 episode、frame、task、video 和 pose 字段。
- 它使用有状态的 GPU UDF，以 1 fps 用 Google SigLIP-2 将视频帧编码为 768D 向量。文本查询用同一模型编码，并按余弦相似度排序。
- 它从 EgoDex 手部数据计算几何列：48 个手腕/指尖姿态值，以及跨 68 个关节的 204 个骨架值。
- 它派生按帧和时间特征，例如指尖距离、弯曲度、捏合、手掌朝向、张开度、手腕位置、手腕速度、弯曲速度和前臂滚转。
- 查询会用姿态/动作谓词过滤帧，按可选文本相似度对匹配结果排序，按 episode 分组，并返回可导航的 [start, end] 匹配片段。

## 结果
- 文章没有报告精确率、召回率、延迟、吞吐量或完整数据集规模的基准测试。
- 已实现的流水线存储 1 fps 的 SigLIP 嵌入，每个嵌入有 768 个维度，并与从 48 个姿态值和 204 个骨架值计算出的几何特征一起保存。
- 张开手掌查询会筛选张开度在 0.9 到 1.0 区间内的帧，并返回前 5 个匹配的 episode。
- 在 k=2 示例中，hammer grip + "stapler" 将实际手持订书机的 episode 排在第 1 位；第 2 个匹配是误报，内容涉及一个小黑盒。
- 针对 "Assemble soft legos into a tower" episode 的抬起查询找到了 12 个独立的 [start, end] 片段，UI 将前 5 个显示为不同的积木抬起动作。
- 文章称，仅用几何的查询可以区分张开和闭合的手掌以及写字握姿，而 grasping + "shirt" 这类组合查询会找回两个折叠 T 恤的 episode。

## Problem

## Approach

## Results

## Link
- [https://www.eventual.ai/blog/egodex-scenario-search](https://www.eventual.ai/blog/egodex-scenario-search)
