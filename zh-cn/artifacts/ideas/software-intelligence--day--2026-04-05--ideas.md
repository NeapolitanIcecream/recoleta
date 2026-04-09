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

# 软件代理控制关卡

## Summary
软件代理的控制面正在变得更具体，尤其是在工单、编译器和评审关卡为系统提供明确边界的地方。近期最清晰的产品形态包括：一个用于有边界维护工作的 Jira 关联执行闭环，一个用编译器反馈提高编译成功率的 GnuCOBOL 修复服务，以及一个在提示词驱动的系统变化被当作常规代码修改通过之前就将其拦下的架构评审关卡。

## 带验证器关卡和隔离 worktree 的 Jira 工单执行闭环
Jira 关联的代理闭环已经具体到可以在那些已经通过工单管理合规、安全修复和积压清理的团队中试点。可行的产品形态应当收窄：让代理摄取结构化输入，把工作映射到规范化积压列表，通过固定的 Jira 状态认领工单，在隔离的 worktree 中做修改，并且只在产品和安全验证通过后更新 Jira。论文中的案例使用了明确的自主执行、人工审核和重新摄取阈值，以及锁处理、重试和 Jira 故障期间的降级运行。这对那些真正卡在审计性和大量小型维护任务状态控制上的团队有意义，而不只是卡在代码生成上。

首个部署目标可以是验证规则清晰的重复性工单族，比如依赖更新、低风险修复或积压去重。最低成本的测试是运营性的：在一个有边界的队列上运行两周，衡量重复建单、终态完成率、验证器通过率，以及被推送到人工审核的项目占比。这里的证据更能支持控制和可追溯性，而不是广泛的软件交付覆盖，所以产品起步时应贴近现有工单流程，避免接入开放式任务入口。

### Evidence
- [Closed-Loop Autonomous Software Development via Jira-Integrated Backlog Orchestration: A Case Study in Deterministic Control and Safety-Constrained Automation](../Inbox/2026-04-05--closed-loop-autonomous-software-development-via-jira-integrated-backlog-orchestration-a-case-study-in-deterministic-control-and-safety-constrained-automation.md): Jira 支撑的确定性控制闭环、置信度阈值、验证器关卡和已观察到的终态结果，支持一个具体的工单自动化工作流。
- [Closed-Loop Autonomous Software Development via Jira-Integrated Backlog Orchestration: A Case Study in Deterministic Control and Safety-Constrained Automation](../Inbox/2026-04-05--closed-loop-autonomous-software-development-via-jira-integrated-backlog-orchestration-a-case-study-in-deterministic-control-and-safety-constrained-automation.md): 摘要内容确认了有边界的 AI 动作、运行次数、对抗式审查发现，以及持续运行产生的工件。

## 用于 LLM 生成维护补丁的 GnuCOBOL 修复闭环
针对 COBOL 生成的编译器引导修复，现在已经足够适合内部维护工具。具体做法是在 GnuCOBOL 外围搭一个生成与修复服务：先为一个有边界的维护任务生成代码，再编译，把编译器错误回传给模型，直到程序编译通过或耗尽重试预算才停止。这很适合那些需要帮助处理遗留系统小改动、但又不能接受连基本编译都过不了的原始模型输出的团队。

最强的近期用途不是完整应用生成，而是目标明确的工作，比如把变更请求转成候选补丁、补齐重复样板代码，或起草已经有测试夹具的独立批处理作业更新。论文报告的编译成功率提升幅度很大，其中 GPT-4o 从 41.8% 提升到 95.89%，pass@1 也有改善。一个有用的评估方案很直接：抽取一组固定的维护工单，对比一次生成和编译器引导修订，记录编译成功率、测试通过率，以及仍然需要人工修复的错误类别。错误分类本身也能作为产品输入，因为程序结构使用错误和内置函数误用是反复出现的失败模式。

### Evidence
- [COBOLAssist: Analyzing and Fixing Compilation Errors for LLM-Powered COBOL Code Generation](../Inbox/2026-04-05--cobolassist-analyzing-and-fixing-compilation-errors-for-llm-powered-cobol-code-generation.md): 摘要报告了 COBOL 修复闭环、错误分类，以及在加入编译器反馈后的大幅编译成功率提升。
- [COBOLAssist: Analyzing and Fixing Compilation Errors for LLM-Powered COBOL Code Generation](../Inbox/2026-04-05--cobolassist-analyzing-and-fixing-compilation-errors-for-llm-powered-cobol-code-generation.md): 摘要内容确认了 GPT-4o-mini 和 GPT-4o 在迭代式编译器引导修复下的改进。

## 面向代理生成 pull request 的架构差异关卡
在团队把代理用于高度依赖图表的工作之前，架构评审需要单独增加一个检查步骤。这里有两部分证据可以放在一起看。一部分显示，仅仅改变提示词措辞，就会改变生成系统的形态，新增 schema 校验器、重试处理器、工具注册表、代理循环和 SQLite 状态存储等组件。另一部分显示，当前视觉语言模型读取软件架构图的能力仍然偏弱，最佳报告准确率只有 70.18%，在更难的图类型和关系密集的问题上还会明显下降。团队如果让代理根据图表、提示词和不完整规格来实现系统，就应当默认会发生架构漂移，除非它明确记录决策并把这些决策和源工件逐项核对。

可行的产品形态是在 CI 或代码评审工具里加入架构差异关卡。记录提示词、生成出的文件图、依赖新增项、基础设施组件，以及引用到的图表或 ADR。然后在构建引入状态存储、编排循环、外部工具或新的接口契约时，要求进行结构化评审。对于图表输入，让模型只做提取和高亮这类评审者能快速核验的任务，不要让它对行为图或关系密集图直接下最终判断。最低成本的验证方式，是把这个关卡应用到一周内代理生成的 pull request 上，统计它拦下了多少原本会被当作普通代码修改放过的、未经过评审的架构变更。

### Evidence
- [Architecture Without Architects: How AI Coding Agents Shape Software Architecture](../Inbox/2026-04-05--architecture-without-architects-how-ai-coding-agents-shape-software-architecture.md): 摘要报告了由提示词驱动的架构分化，以及不同变体中新增的具体组件。
- [Benchmarking and Evaluating VLMs for Software Architecture Diagram Understanding](../Inbox/2026-04-05--benchmarking-and-evaluating-vlms-for-software-architecture-diagram-understanding.md): 摘要报告了 SADU 基准上软件架构图的准确率上限和失败模式。
- [Benchmarking and Evaluating VLMs for Software Architecture Diagram Understanding](../Inbox/2026-04-05--benchmarking-and-evaluating-vlms-for-software-architecture-diagram-understanding.md): 摘要内容确认了当前 VLM 表现与设计阶段软件工程需求之间的差距。
