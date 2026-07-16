---
kind: ideas
granularity: week
period_start: '2026-06-08T00:00:00'
period_end: '2026-06-15T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action models
- manipulation
- real-robot evaluation
- temporal modeling
- contact control
- spatial grounding
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/manipulation
- topic/real-robot-evaluation
- topic/temporal-modeling
- topic/contact-control
- topic/spatial-grounding
language_code: zh-CN
---

# 机器人 VLA 评估盲点

## 摘要
机器人 VLA 团队可以采取三项近期改动：在比较策略前标准化物理 rollout，为接触密集型控制分离传感器更新频率，并用交互证据给示教标签打分。每项改动都针对一个当前汇总成功率可能掩盖的失效模式。

## 带 reset JSON 和进度评分的 UMI 风格真实机器人评估协议
在把模型分数视为可比之前，比较腕部视角操作策略的团队应加入一套共享的物理评估包。UMI-Bench 1.0 给出了具体模板：固定工作站、腕部 RGB 观察设置、动作接口、场景重置、rollout 日志和人工评分。每个 episode 都带有一张重置图像，以及包含任务 ID、物体元数据、位置、姿态、目标区域、split 和任务特定因素的场景 JSON。

这对那些发现策略排名会随相机位置、重置流程或物体姿态变化而变化的实验室有用。UMI-Bench 在 seen 和 unseen 条件单元中报告 Full Success Rate 和 0–100 Progress Score。结果说明了为什么 split 重要：平均 Progress Score 从 Seen/Seen episode 中的 59.62 降至组合偏移下的 40.19，并且位置、布局、姿态或动力学偏移比物体或外观变化造成的损害更大。两个长时程任务中，三个被评估模型的 Full Success Rate 都是 0%，这为评估团队提供了明确的压力测试，用来检查那些在较短任务上看起来可接受的策略。

### 资料来源
- [UMI-Bench 1.0: An Open and Reproducible Real-World Benchmark for Tabletop Robotic Manipulation with UMI Data](../Inbox/2026-06-09--umi-bench-1-0-an-open-and-reproducible-real-world-benchmark-for-tabletop-robotic-manipulation-with-umi-data.md): 总结 UMI-Bench 协议、episode 元数据、评分字段、条件 split 和已报告的模型结果。
- [UMI-Bench 1.0: An Open and Reproducible Real-World Benchmark for Tabletop Robotic Manipulation with UMI Data](../Inbox/2026-06-09--umi-bench-1-0-an-open-and-reproducible-real-world-benchmark-for-tabletop-robotic-manipulation-with-umi-data.md): 解释硬件设置、相机位置、重置流程和动作接口为什么会混淆真实世界策略比较。
- [UMI-Bench 1.0: An Open and Reproducible Real-World Benchmark for Tabletop Robotic Manipulation with UMI Data](../Inbox/2026-06-09--umi-bench-1-0-an-open-and-reproducible-real-world-benchmark-for-tabletop-robotic-manipulation-with-umi-data.md): 描述评估流程：示教采集、episode 规格、场景重置、策略执行、日志记录、评分和任务因素分析。

## 用于接触密集型 VLA 控制的异步模态缓冲区
接触密集型操作系统应测试一种控制器路径，让语言、视觉、力和本体感知按各自的时钟更新。DAM-VLA 展示了构建方式：语言编码一次，视觉稀疏更新，在控制频率下保留密集的力和本体感知历史，并让动作头在每个控制步读取所有潜在缓冲区。

实际运行中的问题是时序。力-力矩信号可以在 100–500 Hz 携带接触瞬态，而对控制有用的 RGB 变化可能更接近 3–10 Hz。单时钟 VLA 可能在重复视觉帧上浪费计算，并漏掉快速接触变化。在 DAM-VLA 的 Franka 测试中，异步设计在七个任务上的平均成功率达到 95.2%，最强同步基线为 40.95%。一个朴素的 100 Hz 同步变体降至 21.9%，所以工程上应先在插接、按按钮、清洁或类似接触任务上，将带时间戳的力事件、重规划频率和任务成功率与当前同步控制器进行比较。

### 资料来源
- [DAM-VLA: Decoupled Asynchronous Multimodal Vision Language Action model](../Inbox/2026-06-10--dam-vla-decoupled-asynchronous-multimodal-vision-language-action-model.md): 给出 DAM-VLA 架构、模态缓冲区设计、100 Hz 控制设置和真实机器人成功率对比。
- [DAM-VLA: Decoupled Asynchronous Multimodal Vision Language Action model](../Inbox/2026-06-10--dam-vla-decoupled-asynchronous-multimodal-vision-language-action-model.md): 说明力-力矩信号与 RGB 观察之间的传感器频率不匹配。
- [DAM-VLA: Decoupled Asynchronous Multimodal Vision Language Action model](../Inbox/2026-06-10--dam-vla-decoupled-asynchronous-multimodal-vision-language-action-model.md): 描述解耦处理原则和各模态的时间上下文。

## 用于机器人示教标签的交互证据过滤
机器人数据团队在使用大型示教集进行空间 grounding 之前，应给自动标签加入基于交互的可靠性分数。SPARC 的流程足够具体，可以复制到较小的流水线中：按夹爪阶段和语言拆分示教，提出候选物体，跟踪并提升到 3D，然后用抓取期间的运动、到夹爪的 3D 距离以及与机器人本体的重叠来给候选物体打分。

采用时的阻碍是杂乱场景中的标签噪声。检测器置信度可能给错误物体打高分，因为它衡量的是识别置信度，而不是机器人是否操作了该物体。SPARC 在 IA-Bench 上报告 80.2% 的交互物体定位准确率，检测器置信度基线为 58.1%。在 90% precision 的工作点，它保留 77.6% coverage，而最强的轨迹过滤基线保留 33.1%。实际落地时，可以先在现有示教的留出切片上运行该过滤器，检查低可靠性和高可靠性分桶，并用接受的标签训练一个空间 grounding 模型。

### 资料来源
- [SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale](../Inbox/2026-06-11--sparc-reliable-spatial-annotations-from-robot-demonstrations-at-scale.md): 总结 SPARC 的基于交互的评分、IA-Bench、定位准确率、coverage 和下游空间 grounding 结果。
- [SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale](../Inbox/2026-06-11--sparc-reliable-spatial-annotations-from-robot-demonstrations-at-scale.md): 将 SPARC 描述为一个带有边界框、轨迹、阶段标签和可靠性分数的自动标注系统。
- [SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale](../Inbox/2026-06-11--sparc-reliable-spatial-annotations-from-robot-demonstrations-at-scale.md): 解释检测器置信度为什么无法在杂乱机器人示教中判断被交互物体的身份。
