---
source: hn
url: https://github.com/dogtorjonah/context-warp-drive
published_at: '2026-07-13T23:32:39'
authors:
- Dr_Jonah
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
- human-ai-interaction
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Context Warp Drive – deterministic, zero-LLM context compaction

## Summary
## 摘要
Context Warp Drive 是一个确定性的零 LLM 上下文压缩引擎，面向长期运行且使用工具的智能体。它在将可见上下文控制在令牌预算内的同时，保留精确标识符、原始历史记录和可复用的提供商提示前缀。

## 问题
- 长时间运行的智能体会超出上下文限制，因此只能截断内容或调用 LLM 进行摘要。
- 截断可能删除较早的证据和标识符；摘要会增加模型调用、延迟和非确定性，还会重写缓存前缀。
- 长期运行的软件智能体需要在折叠、进程重启和硬上下文重置后保持连续性。

## 方法
- 将较早的轮次折叠为确定性的结构骨架，同时完整保留最近轮次。
- 把 UUID、哈希、路径、端口和问题引用提取到有预算限制的 Coordinate Closet 中，使关键标识符保持原样。
- 冻结已封存的提示前缀，使相同输入产生逐字节一致的输出，并让提供商提示缓存可以跨轮次和阶段复用这些前缀。
- 构建召回索引：当后续活动触及相关路径、论点或标识符时，将已折叠的证据重新分页载入准备好的上下文。
- 增加感知模型的压力预算、硬 Rebirth 种子、提供商适配器、情节存储，以及一个在提示之外保存执行状态且无依赖的 Task Rail。

## 结果
- 一次生产环境中的 Claude 部署在 1 小时 49 分钟内处理 954 次工具调用，记录到 92.6% 的缓存读取命中率；论文还报告称，在高轮次工作负载中，约 90% 的输入令牌由缓存提供。
- 在一个使用精确 o200k_base BPE 计数和 Claude Sonnet 定价的确定性 16 轮故障调试基准测试中，该方法相比截断降低了 63% 的成本，相比摘要降低了 72%。
- 折叠和召回核心没有产生额外的 LLM 调用，也没有执行 I/O；代码库包含 900 多个确定性测试，覆盖折叠、召回、冻结、提供商适配器、任务轨道和集成。
- 随附的 Rebirth 连续性研究报告称：首次操作相对于完整上下文摘要具有非劣性表现；连续执行到第 684 次 Rebirth 时行为保持稳定；首个边界行的缓存读取命中率为 92.8%，普通热行则为 94.5%。
- 生产缓存遥测数据来自单次部署，缺少真实工作负载下的 A/B 对照组；离线比较的规模也较小。更大规模、受控的长期评估仍待开展。

## Problem

## Approach

## Results

## Link
- [https://github.com/dogtorjonah/context-warp-drive](https://github.com/dogtorjonah/context-warp-drive)
