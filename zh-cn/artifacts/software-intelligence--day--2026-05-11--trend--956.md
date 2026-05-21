---
kind: trend
trend_doc_id: 956
granularity: day
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-12T00:00:00'
topics:
- coding agents
- agent runtimes
- tool-use evaluation
- workflow security
- context compression
- CAD automation
run_id: materialize-outputs
aliases:
- recoleta-trend-956
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-runtimes
- topic/tool-use-evaluation
- topic/workflow-security
- topic/context-compression
- topic/cad-automation
language_code: zh-CN
---

# 智能体系统承担更多责任前需要可检查的执行过程

## Overview
最强信号是，智能体需要可检查的执行过程和更严格的任务证据。DuST 把带执行标签的候选代码用作训练数据，Shepherd 记录实时智能体状态以支持分叉，ComplexMCP 显示工具智能体在有状态软件工作上仍落后于人类。

## Clusters

### 执行反馈用作训练信号
DuST 把生成的代码样本当作成对监督的来源。基础模型为每个问题采样 64 个候选程序，沙箱把每个候选标记为通过或失败，混合分组用 Group Relative Policy Optimization (GRPO) 训练同一个模型，使其把正确程序排在错误程序之前。奖励只评分排序质量，但生成能力也提高了。

在 LiveCodeBench v6 上，Qwen3-30B-Thinking 的 pass@1 从 65.4% 升至 68.5%。它的判断分数从 70.1 升至 76.3 NDCG，Best-of-4 准确率从 68.7% 升至 72.6%。这个结果给出了推理后复用测试时扩展数据的具体做法。

#### Evidence
- [Primal Generation, Dual Judgment: Self-Training from Test-Time Scaling](../Inbox/2026-05-11--primal-generation-dual-judgment-self-training-from-test-time-scaling.md): 摘要给出了 DuST 的数据构造、GRPO 排序目标和 LiveCodeBench 收益。

### 元智能体的可追踪运行时状态
Shepherd 把一次智能体执行变成另一个智能体可以检查、分叉、重放和修改的类型化对象。每次模型调用、工具调用、文件写入和环境动作都会成为 Git 式轨迹中的事件。分叉对进程和文件系统使用写时复制隔离，因此不同的后续路径可以从同一个历史状态开始。

论文报告的系统指标足够支撑智能体搜索。对于最高 5.8 GB 的 Terminal-Bench 2.0 镜像，Shepherd 的分叉耗时为 134–143 ms。在最大镜像上，完整文件系统复制耗时达到 53,462 ms。重放在八个任务中对 Claude Haiku 4.5 也达到约 95% 的提示缓存命中率。

#### Evidence
- [Shepherd: A Runtime Substrate Empowering Meta-Agents with a Formalized Execution Trace](../Inbox/2026-05-11--shepherd-a-runtime-substrate-empowering-meta-agents-with-a-formalized-execution-trace.md): 摘要描述了 Shepherd 的类型化轨迹、分叉/重放操作和性能结果。

### 有状态工具和 CAD 基准暴露能力狭窄
ComplexMCP 通过 Model Context Protocol (MCP) 测试智能体，包含 300 多个工具和七个有状态沙箱。报告中表现最好的模型 Gemini-3-Flash 在 47 个任务上的成功率为 55.31%。人类用户通过同一接口达到 93.61%。失败包括工具检索饱和、跳过环境检查，以及出错后恢复能力差。

BenchCAD 对多模态设计工作施加了类似压力。它包含 17,900 个经过执行验证的 CadQuery 程序，覆盖 106 个工业零件族。该基准把图像到代码生成、视觉问答、代码问答和编辑任务分开评测。模型读取 CAD 代码的能力强于从渲染图中推断相同细节的能力：最高 Code QA 约为 0.838，而 Vision QA 峰值为 0.587。

#### Evidence
- [ComplexMCP: Evaluation of LLM Agents in Dynamic, Interdependent, and Large-Scale Tool Sandbox](../Inbox/2026-05-11--complexmcp-evaluation-of-llm-agents-in-dynamic-interdependent-and-large-scale-tool-sandbox.md): 摘要报告了 MCP 工具规模、有状态沙箱、人类和模型成功率，以及失败模式。
- [BenchCAD: A Comprehensive, Industry-Standard Benchmark for Programmatic CAD](../Inbox/2026-05-11--benchcad-a-comprehensive-industry-standard-benchmark-for-programmatic-cad.md): 摘要报告了 BenchCAD 数据集规模、任务和问答结果。

### 工作流上下文和压缩记忆需要更强检查
JAW 表明，当攻击者控制的内容进入连接令牌、工具或密钥的提示时，智能体工作流可能被劫持。它结合了工作流路径分析、提示来源追踪、能力检查和载荷演化。论文报告了 4,174 个可劫持的 GitHub 工作流和八个可劫持的 n8n 模板，影响包括凭据泄露和命令执行。

上下文问题也出现在编码智能体内部。In-Context Autoencoder (ICAE) 把观察压缩成连续记忆 token，让智能体运行更长轨迹，但细节损失会损害真实问题解决。在 SWE-bench Verified 上，压缩系统解决了 500 个问题中的 7 个，低于未压缩的 Qwen3-8B 基线 19 个，也远低于监督微调模型的 86 个。

#### Evidence
- [Comment and Control: Hijacking Agentic Workflows via Context-Grounded Evolution](../Inbox/2026-05-11--comment-and-control-hijacking-agentic-workflows-via-context-grounded-evolution.md): 摘要给出了 JAW 方法、受影响的工作流类型、数量和报告的影响。
- [On Problems of Implicit Context Compression for Software Engineering Agents](../Inbox/2026-05-11--on-problems-of-implicit-context-compression-for-software-engineering-agents.md): 摘要报告了 ICAE 设置和 SWE-bench Verified 解决率下降。
