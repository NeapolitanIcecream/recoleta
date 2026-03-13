---
source: hn
url: https://gimletlabs.ai/blog/sram-centric-chips
published_at: '2026-03-09T23:10:19'
authors:
- gmays
topics:
- ai-inference
- sram-centric-accelerators
- memory-hierarchy
- llm-serving
- heterogeneous-computing
relevance_score: 0.56
run_id: materialize-outputs
---

# The emerging role of SRAM-centric chips in AI inference

## Summary
这篇文章分析了为何以SRAM为中心的AI加速器在推理，尤其是LLM decode阶段，开始相对传统GPU展现优势。核心观点是：真正的架构分界不是“SRAM vs HBM”，而是“近计算内存 vs 远计算内存”，不同推理阶段应映射到不同硬件。

## Problem
- 文章要解决的问题是：**为什么某些AI推理负载更适合SRAM-centric芯片而不是GPU，以及如何判断二者的适用边界**。
- 这很重要，因为LLM推理正遭遇**memory wall**：计算能力增长快于内存带宽，而agentic workloads据文中称会产生约**15倍**于传统聊天模型的token需求，端到端时延和吞吐成为关键瓶颈。
- 传统“单一硬件跑完整个推理流程”的方式越来越低效，尤其是自回归的decode阶段，其算术强度低、内存压力高，难以充分利用GPU的高算力。

## Approach
- 文章采用**架构分析 + 工作负载分解**的方法，对比GPU与SRAM-centric芯片在内存物理特性和系统设计上的根本差异。
- 核心机制可用最简单的话概括为：**如果数据能放在离计算很近的片上内存里，就能减少搬运、降低延迟、提高带宽；如果数据太大，就需要依赖容量更大的远端内存，但会更慢。**
- 作者指出决定胜负的关键不是芯片品牌，而是**working set size → arithmetic intensity → memory placement choice**：工作集越大且复用越少，越偏向近计算高带宽内存；复用高、算术强度高的任务则更适合GPU。
- 在推理流程上，文章强调**prefill与decode分离**：prefill更偏计算密集，适合高算力GPU；decode更偏内存带宽密集，适合SRAM-centric硬件。
- 进一步提出更细粒度的**异构拆分/多硅调度**思路，例如把speculative decoding中的小draft model放到SRAM-centric硬件，把批量验证放到GPU上。

## Results
- 文中不是实验论文，**没有给出系统化基准测试结果或统一实验表格**，因此缺少可复现的定量性能评测。
- 文中给出的关键硬件数字包括：**SRAM读取延迟约1 ns**，而**DRAM/HBM读取约10–15 ns**，用于说明片上SRAM的低延迟优势。
- 文中列举GPU片上SRAM容量：**H100约50 MB SRAM**，**B200约126 MB SRAM**；而更激进的SRAM-centric设计投入更多片上存储。作为上限示例，**Cerebras整片晶圆级芯片约44 GB SRAM**，但即便如此大模型权重仍需跨芯片分布。
- 文中引用产业趋势数字：NVIDIA在2024年12月据称以**200亿美元**授权Groq IP；Cerebras宣布了一个为OpenAI推理工作负载服务的**750 MW**交易，作为SRAM-centric路线获得市场验证的信号。
- 文中引用d-Matrix CTO的行业观察：计算性能大约每两年增长**3倍**，而内存带宽仅增长约**1.6倍**，支撑“内存墙”论点。
- 在未来方案上，文中提到d-Matrix即将推出的Raptor据称可通过计算上方堆叠定制DRAM提供**比HBM4高10倍带宽**；但这属于厂商声明，不是本文实测结果。

## Link
- [https://gimletlabs.ai/blog/sram-centric-chips](https://gimletlabs.ai/blog/sram-centric-chips)
