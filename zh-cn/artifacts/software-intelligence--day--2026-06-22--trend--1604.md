---
kind: trend
trend_doc_id: 1604
granularity: day
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-23T00:00:00'
topics:
- "LLM \u667A\u80FD\u4F53"
- "\u7F16\u7801\u667A\u80FD\u4F53"
- "\u4F01\u4E1A\u57FA\u51C6"
- "\u8FC7\u7A0B\u8BB0\u5FC6"
- "\u8F6F\u4EF6\u5B89\u5168"
- "\u4E0A\u4E0B\u6587\u6062\u590D"
- SysML
- Text-to-SQL
run_id: materialize-outputs
aliases:
- recoleta-trend-1604
tags:
- recoleta/trend
- "topic/llm-\u667A\u80FD\u4F53"
- "topic/\u7F16\u7801\u667A\u80FD\u4F53"
- "topic/\u4F01\u4E1A\u57FA\u51C6"
- "topic/\u8FC7\u7A0B\u8BB0\u5FC6"
- "topic/\u8F6F\u4EF6\u5B89\u5168"
- "topic/\u4E0A\u4E0B\u6587\u6062\u590D"
- topic/sysml
- topic/text-to-sql
language_code: zh-CN
---

# 智能体研究正在把工作场所交付、上下文恢复和安全证据放到同一张记分卡上

## Overview
当天证据最强的研究将大型语言模型（LLM）智能体视为生产系统，这类系统需要任务上下文、可复用流程和安全检查。DeepDiscovery、EnterpriseClawBench 和 AFTER 给出了最清楚的证据，包含具体任务、制品和迁移测试。

## Clusters

### 编码智能体的代码库上下文
DeepDiscovery 针对编码智能体中的一种常见失败：找到最显眼的文件，却漏掉注册代码、配置链接、测试或依赖注入路径。它的 Location-Inference 方法先从高置信度任务锚点出发，再在预算限制内沿显式依赖、隐式配置链接和模块邻近关系扩展。

论文报告的收益有实际意义。在包含 267 万行代码、超过 25,000 个文件的工业代码库中，它在中等任务上将 Full Recall Rate 提高 2.5 到 7.4 个百分点，在大型子项目任务上提高 1.6 到 9.2 个百分点。在 SWE-bench Verified 上，接入该方法的系统达到 78.6% 的求解率，比基线高 8.2 个百分点。

#### Evidence
- [From Fragments to Paths: Task-Level Context Recovery for Large Industrial Codebases](../Inbox/2026-06-22--from-fragments-to-paths-task-level-context-recovery-for-large-industrial-codebases.md): DeepDiscovery 方法、工业代码库规模、文件恢复收益，以及 SWE-bench Verified 结果。

### 带制品和可复用技能的工作场所基准
EnterpriseClawBench 将企业内部会话转成可复现任务，任务包含文件、预期交付物、角色标签、规则，以及文本或视觉评分规程。32 个 harness-model 组合中的最佳 Lite 分数为 0.663，仍能看到许多制品交付和内容质量失败。该基准还报告成本、运行时间、工具调用和 harness-model 配对，因此基础模型分数不能掩盖执行问题。

AFTER 将过程记忆作为带版本的技能文件来研究。静态技能平均增加 2.8 个准确率百分点，一轮细化再增加 3.7 到 6.7 个百分点。用多样化多模型轨迹训练的技能达到 73.1% 的跨模型测试准确率，而范围较窄的技能更新在跨角色迁移时可能损失准确率。

#### Evidence
- [EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions](../Inbox/2026-06-22--enterpriseclawbench-benchmarking-agents-from-real-workplace-sessions.md): EnterpriseClawBench 构建流程、评分维度、Lite 分数，以及 harness-model 结果。
- [Managing Procedural Memory in LLM Agents: Control, Adaptation, and Evaluation](../Inbox/2026-06-22--managing-procedural-memory-in-llm-agents-control-adaptation-and-evaluation.md): AFTER 任务集、过程技能评估、细化收益、跨模型迁移，以及跨角色失败。

### AI 构建软件的安全证据
vibe-coding 安全研究给出了这一时期最大的警示信号。作者收集了 10,517 个主要由 AI 编写的应用，并审计了 200 个已部署的 Web 应用。经过去重和可利用性检查后，人工审查者验证了 1,471 个可利用漏洞。反复出现的缺陷类型包括访问控制破坏、加密失败、注入、密钥暴露、占位逻辑和未过滤输入。

EVerest 提供了另一类安全证据：一个公开数据集，将电动汽车充电栈的需求、架构、文档和代码连接起来。它包含 84 条安全需求和 1,445 个细粒度标签。在构建过程中，作者发现并披露了一个真实的 CWE-1295 明文令牌存储弱点。

#### Evidence
- [Understanding the (In)Security of Vibe-Coded Applications](../Inbox/2026-06-22--understanding-the-in-security-of-vibe-coded-applications.md): VibeApps 语料库规模、已部署应用审计流程、已验证漏洞数量，以及反复出现的漏洞类型。
- [The EVerest Dataset for Secure Software Engineering](../Inbox/2026-06-22--the-everest-dataset-for-secure-software-engineering.md): EVerest 数据集内容、可追踪性标签、架构覆盖，以及发现的 CWE-1295 弱点。

### 专门工程任务中的领域上下文和人工审查
SysML v2 故障定位论文显示，当领域规则作为训练数据和推理上下文提供时，小型代码模型可以获得提升。一个车辆领域知识图谱编码物理接口和单位兼容性规则，然后指导合成故障生成和修复提示。在报告的评估集上，Qwen2.5 Coder 1.5B 在微调后的完整代码输出中达到 95.7% 的语义修复准确率，在补丁输出中达到 91.9%；其基线语义修复准确率为 0.62%。

WisdomAI 的 Text-to-SQL 文章对企业分析提出了相关的生产环境主张。它的 Adaptive Context Engine 使用 schema、日志、dbt、LookML、知识库、反馈和管理员审查来构建并更新业务上下文。在五个经过筛选的 LiveSQLBench 仅查询数据集上，报告的聚合准确率为：基线 20%，加入知识文件后 50%，上下文学习后 85%。

#### Evidence
- [Automated Semantic Fault Localization in SysML v2: A Human-in-the-Loop Framework Using Knowledge-Graph Augmented LLMs](../Inbox/2026-06-22--automated-semantic-fault-localization-in-sysml-v2-a-human-in-the-loop-framework-using-knowledge-graph-augmented-llms.md): SysML v2 知识图谱方法、合成数据设置、微调设置、语义修复准确率，以及补丁 token 结果。
- [What it takes to get high Text-to-SQL accuracy in production](../Inbox/2026-06-22--what-it-takes-to-get-high-text-to-sql-accuracy-in-production.md): Adaptive Context Engine 输入、上下文学习循环，以及报告的 Text-to-SQL 准确率结果。
