---
kind: ideas
granularity: day
period_start: '2026-04-05T00:00:00'
period_end: '2026-04-06T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- software-engineering
- compiler-feedback
- software-architecture
- agent-control
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/compiler-feedback
- topic/software-architecture
- topic/agent-control
language_code: zh-CN
---

# 软件代理控制门

## 摘要
软件代理工作里的控制面现在变得更具体了，尤其是在工单、编译器和评审门给系统划出硬边界的地方。最清楚的近期落地方案是：用于有边界维护工作的 Jira 关联执行循环、利用编译器反馈提升编译成功率的 GnuCOBOL 修复服务，以及在提示词驱动的系统变更被当成普通代码修改通过之前将其拦下的架构评审门。

## 带验证门和隔离工作树的 Jira 工单执行循环
一个与 Jira 关联的代理循环现在已经具体到可以在那些已经通过工单管理合规、修复安全问题和清理待办事项的团队里试点。这个方案的价值很窄：让代理接收结构化输入，把工作映射到一个规范化待办列表，通过固定的 Jira 状态认领工单，在隔离的工作树中修改代码，并且只在产品和安全验证之后更新 Jira。报告中的方案使用了明确的自治执行、人工复核和重新摄取阈值，还包括锁处理、重试，以及 Jira 故障期间的降级运行。这对那些被审计性和状态控制卡住、而不是被代码生成卡住的团队更有用，尤其是面对大量小型维护任务时。

首批落地目标可以是带有明确验证的重复工单家族，例如依赖更新、低风险修复或待办去重。一个成本较低的测试方法是运营层面的：在一个有边界的队列上运行两周，统计重复工单创建数、终态完成率、验证器通过率，以及被推给人工复核的条目占比。这里的证据在控制和可追踪性上更强，在更广泛的软件交付覆盖面上更弱，所以产品一开始应尽量贴近现有工单流程，避免开放式任务接入。

### 资料来源
- [Closed-Loop Autonomous Software Development via Jira-Integrated Backlog Orchestration: A Case Study in Deterministic Control and Safety-Constrained Automation](../Inbox/2026-04-05--closed-loop-autonomous-software-development-via-jira-integrated-backlog-orchestration-a-case-study-in-deterministic-control-and-safety-constrained-automation.md): 基于 Jira 的确定性控制循环、置信度阈值、验证门和观测到的终态结果，支持一个具体的工单自动化流程。
- [Closed-Loop Autonomous Software Development via Jira-Integrated Backlog Orchestration: A Case Study in Deterministic Control and Safety-Constrained Automation](../Inbox/2026-04-05--closed-loop-autonomous-software-development-via-jira-integrated-backlog-orchestration-a-case-study-in-deterministic-control-and-safety-constrained-automation.md): 摘要内容确认了受约束的 AI 动作、运行次数、对抗性审查发现，以及持续运行产物。

## 面向 LLM 生成维护补丁的 GnuCOBOL 修复循环
用于 COBOL 生成的编译器引导修复，现在看起来已经足够实用，可以用于内部维护工具。这个具体方案是围绕 GnuCOBOL 构建的生成和修复服务：为一个有边界的维护任务生成代码，编译它，把编译器错误回传给模型，然后只在程序编译通过或重试预算耗尽时停止。它适合那些需要帮助处理旧系统小改动，但不能接受原始模型输出连基本编译都过不去的团队。

最有前景的短期用途不是完整应用生成，而是有针对性的工作，例如把变更请求翻译成候选补丁、补齐重复样板代码，或者起草已经有测试夹具的独立批处理作业更新。报告中的提升在编译成功率上很大，GPT-4o 从 41.8% 提升到 95.89%，pass@1 也有提升。一个有用的评估计划很简单：抽取一组固定的维护工单，对比一次性生成和编译器引导修订，记录编译成功率、测试通过率，以及仍需要人工修复的错误类别。这个错误分类也能直接作为产品输入，因为程序结构使用错误和内置函数误用是反复出现的失败模式。

### 资料来源
- [COBOLAssist: Analyzing and Fixing Compilation Errors for LLM-Powered COBOL Code Generation](../Inbox/2026-04-05--cobolassist-analyzing-and-fixing-compilation-errors-for-llm-powered-cobol-code-generation.md): 摘要报告了 COBOL 修复循环、错误分类，以及在编译器反馈后的大幅编译成功率提升。
- [COBOLAssist: Analyzing and Fixing Compilation Errors for LLM-Powered COBOL Code Generation](../Inbox/2026-04-05--cobolassist-analyzing-and-fixing-compilation-errors-for-llm-powered-cobol-code-generation.md): 摘要确认了在迭代编译引导修复下，GPT-4o-mini 和 GPT-4o 的改进。

## 代理生成拉取请求的架构差异门
在团队信任代理处理图表密集型工作之前，架构评审需要单独的检查步骤。这里有两组证据汇合。第一组显示，仅靠提示词措辞就能改变生成出来的系统形态，加入模式验证器、重试处理器、工具注册表、代理循环和 SQLite 状态等组件。第二组显示，当前视觉语言模型在读取软件架构图方面仍然薄弱，最佳报告准确率只有 70.18%，在更难的图表类型和关系密集型问题上下降很明显。让代理根据图表、提示词和部分规格实现功能的团队，应当假定会出现架构漂移，除非把决策明确记录下来并和源工件逐一核对。

可落地的方案是在 CI 或评审工具里加一个架构差异门。记录提示词、生成的文件图、依赖新增、基础设施组件，以及引用到的图表或 ADR。然后在构建引入状态存储、编排循环、外部工具或新的接口契约时，要求进行结构化评审。对于图表输入，把模型限制在抽取和标注任务上，让评审者可以快速核对，不要让它对行为型或关系密集型图表做最终判断。最便宜的验证方式，是把这个门跑在一周的代理生成拉取请求上，统计它有多少次拦住了原本会被当成普通代码修改通过的、未经评审的架构变更。

### 资料来源
- [Architecture Without Architects: How AI Coding Agents Shape Software Architecture](../Inbox/2026-04-05--architecture-without-architects-how-ai-coding-agents-shape-software-architecture.md): 摘要报告了由提示词驱动的架构分化，以及各变体中的具体组件增加。
- [Benchmarking and Evaluating VLMs for Software Architecture Diagram Understanding](../Inbox/2026-04-05--benchmarking-and-evaluating-vlms-for-software-architecture-diagram-understanding.md): 摘要报告了 SADU 基准在架构图上的准确率上限和失败模式。
- [Benchmarking and Evaluating VLMs for Software Architecture Diagram Understanding](../Inbox/2026-04-05--benchmarking-and-evaluating-vlms-for-software-architecture-diagram-understanding.md): 摘要确认了当前 VLM 性能与设计阶段软件工程需求之间的差距。
