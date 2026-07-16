---
kind: ideas
granularity: day
period_start: '2026-05-07T00:00:00'
period_end: '2026-05-08T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software engineering benchmarks
- repository evaluation
- test evolution
- agent control
- maintainability
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/repository-evaluation
- topic/test-evolution
- topic/agent-control
- topic/maintainability
language_code: zh-CN
---

# 代理写代码的仓库级防护

## 摘要
代理写代码要先经过仓库级检查，先抓住漏测、后端结构违规和不安全的维护改动，再让生成代码进入审阅。可做的工作不大，足以挂在现有代理周围：为生产提交做受影响测试搜索、为后端结构和迁移行为做 CI 验证、再加一个限制大范围重构的代码味道分诊流程。

## 在代理写测试补丁前先做受影响测试搜索
使用代理更新生产变更后的测试时，应先加一个单独的受影响测试发现步骤，再让代理修改测试套件。这个步骤应要求给出三份列表：预计会失败的测试、仍然通过但需要语义更新的测试、以及需要新增测试的行为。审阅者可以把这份列表和依赖追踪、最近的覆盖率、已变更的公共 API、以及仓库搜索结果对照后，再接受生成的补丁。

TEBench 说明了为什么这一步要放在生成补丁之前。使用 Claude Code、Codex CLI 和 OpenCode 的七种配置里，受影响测试识别的 F1 只有 45.7% 到 49.4%。过时测试最难，平均 F1 约为 36%，因为代理会跟着执行失败走，却漏掉那些已经通过、但不再检查变更后行为的测试。ProCodeBench 提供了相关信号：仓库上下文能提升对真实 VS Code 轨迹的意图预测，而模拟轨迹会高估性能。一个成本不高的内部检查是抽样最近的生产提交，让代理给出受影响测试清单，再让维护者在衡量生成补丁质量之前，先给漏掉的过时测试和缺失测试案例打分。

### 资料来源
- [Breaking, Stale, or Missing? Benchmarking Coding Agents on Project-Level Test Evolution](../Inbox/2026-05-07--breaking-stale-or-missing-benchmarking-coding-agents-on-project-level-test-evolution.md): TEBench reports low affected-test identification F1 and identifies stale tests as the hardest category.
- [An Empirical Study of Proactive Coding Assistants in Real-World Software Development](../Inbox/2026-05-07--an-empirical-study-of-proactive-coding-assistants-in-real-world-software-development.md): ProCodeBench reports that repository context helps intent prediction and that real developer traces are harder than simulated traces.

## 后端生成的 CI 门禁：架构、数据库和 ORM 要求
后端团队在接受代理生成的服务或功能补丁时，应该把结构要求和 API 测试一起写成可执行检查。一个实用的门禁会先运行常规的 HTTP 行为测试套件，再检查允许的分层、数据库选择、迁移或模式设置，以及 ORM 使用情况。数据库检查应该为 PostgreSQL 或 SQLite 配好明确的 fixture，因为数据层缺陷反复出现。

Constraint Decay 固定了一个基于 OpenAPI 的契约，覆盖 80 个后端生成任务，结果发现当加入 Clean Architecture、数据库和 ORM 约束后，能力较强的代理配置在断言通过率上下降了约 30 个百分点。数据库要求带来的边际损失最大：PostgreSQL 让断言通过率下降 19.3 ± 2.5 个点，SQLite 下降 14.3 ± 2.5 个点。ScarfBench 在企业 Java 迁移中指向同一个阻碍：代理经常能走到编译或部署阶段，但没有保住行为一致性，204 个定向迁移里只有 1 个完全保持行为等价。一个有用的起步测试，是把这个门禁跑在已经通过 API 测试的代理后端 pull request 上，统计有多少次结构或数据层检查本来会拦住审查。

### 资料来源
- [Constraint Decay: The Fragility of LLM Agents in Backend Code Generation](../Inbox/2026-05-07--constraint-decay-the-fragility-of-llm-agents-in-backend-code-generation.md): Constraint Decay quantifies assertion-pass losses under architecture, database, and ORM constraints, with database requirements causing the largest losses.
- [ScarfBench: A Benchmark for Cross-Framework Application Migration in Enterprise Java](../Inbox/2026-05-07--scarfbench-a-benchmark-for-cross-framework-application-migration-in-enterprise-java.md): ScarfBench shows low behavior-preserving success for cross-framework enterprise Java migration even when compile or deploy success improves.

## 用假阳性标签和净新增味道检查做代码味道分诊
架构味道修复应该先走分诊流程，代理修改要等到味道被标成真阳性、假阳性或部分有效之后再放行。代理仍然可以帮忙收集受影响模块、解释依赖路径、提出小补丁，并在补丁后报告味道变化量。审阅者在批准任何跨模块重构前，应该同时看到被移除的味道和新引入的味道。

SmellBench 给出了这个控制点的理由。专家审查发现，scikit-learn 中 65 个高严重度静态检测里有 41 个是假阳性，假阳性率为 63.1%。表现最好的代理解决了 47.7% 的案例，但最激进的修复设置又引入了 140 个新味道。第一版实现可以做成围绕现有味道检测器的 pull request 机器人：先要求分诊标签，在提议的变更前后各跑一次检测器，并且在净味道增加或受影响模块列表超出审查预算时阻止大范围代理修改。

### 资料来源
- [SmellBench: Evaluating LLM Agents on Architectural Code Smell Repair](../Inbox/2026-05-07--smellbench-evaluating-llm-agents-on-architectural-code-smell-repair.md): SmellBench reports high false-positive rates for hard architectural smells, limited resolution rates, and 140 new smells from the most aggressive agent setting.
