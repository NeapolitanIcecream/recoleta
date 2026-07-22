---
kind: trend
trend_doc_id: 935
granularity: day
period_start: '2026-07-21T00:00:00'
period_end: '2026-07-22T00:00:00'
topics:
- "\u5177\u8EAB\u4E16\u754C\u6A21\u578B"
- "\u673A\u5668\u4EBA\u5B66"
- "\u52A8\u4F5C\u8868\u793A"
- "\u771F\u5B9E\u5230\u4EFF\u771F"
- "\u4EA4\u4E92\u5F0F\u4EFF\u771F"
run_id: materialize-outputs
aliases:
- recoleta-trend-935
tags:
- recoleta/trend
- "topic/\u5177\u8EAB\u4E16\u754C\u6A21\u578B"
- "topic/\u673A\u5668\u4EBA\u5B66"
- "topic/\u52A8\u4F5C\u8868\u793A"
- "topic/\u771F\u5B9E\u5230\u4EFF\u771F"
- "topic/\u4EA4\u4E92\u5F0F\u4EFF\u771F"
language_code: zh-CN
---

# 结构化动作接口支撑具身世界模型

## 概览
围绕动作相关状态的前一日信号仍在延续，但今天的五篇论文更直接地将结构引入世界建模。视觉轨迹、物理分解和可模拟的回放记录，将动作与预测后果连接起来。证据来自异质的预印本，且评估大多彼此独立，因此它表明了一种共同的设计方向，而不是已经确定的最优架构。

## 研究发现

### 视觉动作表示
RoboInter1.5 和 Masked Visual Actions 都将具有明确空间含义的信号置于意图与预测结果之间。RoboInter1.5 在超过 230,000 个回合中提供物体对齐、可供性、接触点和运动轨迹。Masked Visual Actions 则将实体的像素空间轨迹提供给预训练视频模型；同一个检查点既能预测场景响应，也能根据目标物体运动推断机器人运动。在 DROID 上，它报告的 LPIPS 为 0.0945，而 Ctrl-World 为 0.362。综合来看，这些论文支持将视觉结构作为一种能够适配不同具身形态的控制接口，但所查阅的 RoboInter1.5 摘录没有提供下游对比指标。

#### 资料来源
- [RoboInter1.5: A Holistic Intermediate Representation Suite for Embodied World Modeling and Robotic Manipulation](../Inbox/2026-07-21--robointer1-5-a-holistic-intermediate-representation-suite-for-embodied-world-modeling-and-robotic-manipulation.md): 报告了超过 230,000 个回合和十多种中间表示类型，包括对齐、可供性、接触点和运动轨迹。
- [Masked Visual Actions for Unified World Modeling](../Inbox/2026-07-21--masked-visual-actions-for-unified-world-modeling.md): 使用掩码像素空间轨迹进行正向和逆向建模，并报告 DROID 上的 LPIPS 为 0.0945，而 Ctrl-World 为 0.362。

### 物理原因与可回放状态
两篇论文都明确区分物理原因，而不是让一个潜在状态转移吸收所有变化。DWM 将动作驱动的影响与重力、漂移等持续存在的环境影响分开；在三个经过修改的模拟基准上，它使规划成功率平均提高 13.1 个百分点。Agentic Real2Sim 将记录的交互重建为基于物理的回合孪生体，其中包含几何、物体状态、对齐和回放指标。其测试中表现最好的后端成功回放了 100 个 DROID 回合中的 48 个，既显示出自动转换的实用性，也表明其当前仍较为脆弱。

#### 资料来源
- [DWM: Separating World Effects from Actions in Latent World Models](../Inbox/2026-07-21--dwm-separating-world-effects-from-actions-in-latent-world-models.md): 在训练期间分离与动作无关的世界影响，并报告在三个 W 变体基准上的规划平均绝对增益为 13.1 个百分点。
- [Agentic Real2Sim: Physics-based World Modeling with Vision-Language Agents](../Inbox/2026-07-21--agentic-real2sim-physics-based-world-modeling-with-vision-language-agents.md): 构建基于物理的回合孪生体；测试中表现最好的后端在 100 个 DROID 回合中成功回放了 48 个。

### 作为可用系统的世界模型
这些论文还将延迟、硬件成本和下游用途视为世界模型质量的一部分。ABot-World-0 报告称，在一块 RTX 5090 上可持续生成最高 16 FPS 的 720P 视频，首个动作条件帧的延迟为 1.2 秒，峰值内存约为 19 GiB。Masked Visual Actions 使用想象回放进行策略评估和候选排序，Agentic Real2Sim 则同时比较模型成本与回放成功率。这些结果将评估范围扩展到视觉保真度之外，但基准覆盖仍不均衡，所查阅的 ABot-World-0 文本也缺少数值基线对比。

#### 资料来源
- [ABot-World-0: Infinite Interactive World Rollout on a Single Desktop GPU](../Inbox/2026-07-21--abot-world-0-infinite-interactive-world-rollout-on-a-single-desktop-gpu.md): 报告在 RTX 5090 上以最高 16 FPS 进行 720P 流式生成，动作到首帧延迟为 1.2 秒，峰值显存约为 19 GiB。
- [Masked Visual Actions for Unified World Modeling](../Inbox/2026-07-21--masked-visual-actions-for-unified-world-modeling.md): 将想象回放用于策略评估、基于模型的规划和逆向运动合成。
- [Agentic Real2Sim: Physics-based World Modeling with Vision-Language Agents](../Inbox/2026-07-21--agentic-real2sim-physics-based-world-modeling-with-vision-language-agents.md): 报告了四个视觉语言模型后端的回放成功率和模型费用，所有后端的绝对成功率都低于 50%。
