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

# 面向智能体编写代码的仓库防护措施

## Summary
编码智能体的采用需要仓库级检查，在生成代码到达评审者之前捕捉漏掉的测试、后端结构违规和不安全的维护编辑。具体工作可以围绕现有智能体小步加入：为生产代码提交搜索受影响测试，为后端结构和迁移行为加入 CI 验证器，并建立限制大范围重构的代码异味分诊循环。

## 在智能体编写测试补丁前搜索受影响测试
使用智能体在生产代码变更后更新测试的团队，应先加入一个独立的受影响测试发现步骤，再允许智能体编辑测试套件。这个步骤应要求给出三份清单：预计会失败的测试、仍会通过但需要语义更新的测试，以及需要新增测试覆盖的行为。评审者可以先把清单与依赖跟踪、近期覆盖率、已变更的公共 API 和仓库搜索结果对比，再接受生成的补丁。

TEBench 说明了为什么这个步骤应放在补丁生成之前。在使用 Claude Code、Codex CLI 和 OpenCode 的七种配置中，受影响测试识别的 F1 保持在 45.7% 到 49.4% 之间。过时测试最难，平均 F1 约为 36%，因为智能体主要跟随执行失败，漏掉了那些仍然通过但已不再检查变更行为的测试。ProCodeBench 给出一个相关信号：仓库上下文能改善基于真实 VS Code 轨迹的意图预测，而模拟轨迹会高估性能。一个成本较低的内部检查是抽样近期生产代码提交，让智能体列出受影响测试清单，并让维护者在衡量生成补丁质量之前，对漏掉的过时测试和缺失测试案例打分。

### Evidence
- [Breaking, Stale, or Missing? Benchmarking Coding Agents on Project-Level Test Evolution](../Inbox/2026-05-07--breaking-stale-or-missing-benchmarking-coding-agents-on-project-level-test-evolution.md): TEBench 报告了较低的受影响测试识别 F1，并指出过时测试是最难的类别。
- [An Empirical Study of Proactive Coding Assistants in Real-World Software Development](../Inbox/2026-05-07--an-empirical-study-of-proactive-coding-assistants-in-real-world-software-development.md): ProCodeBench 报告称，仓库上下文有助于意图预测，真实开发者轨迹比模拟轨迹更难处理。

## 面向架构、数据库和 ORM 要求的后端生成 CI 门禁
后端团队在接受智能体生成的服务或功能补丁时，应把结构性要求编码为可执行检查，并与 API 测试一起运行。一个实用的门禁会先运行常规 HTTP 行为测试套件，再验证允许的分层、数据库选择、迁移或 schema 设置，以及 ORM 使用情况。数据库检查应为 PostgreSQL 或 SQLite 准备明确的 fixture，因为数据层缺陷是反复出现的失败来源。

Constraint Decay 在 80 个后端生成任务中固定同一个 OpenAPI 契约，并发现加入 Clean Architecture、数据库和 ORM 约束后，能力较强的智能体配置在断言通过率上损失约 30 个百分点。数据库要求造成的边际损失最大：PostgreSQL 造成 19.3 ± 2.5 个断言通过率百分点损失，SQLite 造成 14.3 ± 2.5 个百分点损失。ScarfBench 指向企业 Java 迁移中的同一个采用障碍：智能体经常能到达编译或部署阶段，却不能保留行为；204 个定向迁移任务中只有 1 个达到完整的行为等价。一个有用的初始测试是，把这个门禁用于已经通过 API 测试的智能体创建的后端 pull request，并统计结构或数据层检查会阻止评审的频率。

### Evidence
- [Constraint Decay: The Fragility of LLM Agents in Backend Code Generation](../Inbox/2026-05-07--constraint-decay-the-fragility-of-llm-agents-in-backend-code-generation.md): Constraint Decay 量化了架构、数据库和 ORM 约束下的断言通过率损失，其中数据库要求造成的损失最大。
- [ScarfBench: A Benchmark for Cross-Framework Application Migration in Enterprise Java](../Inbox/2026-05-07--scarfbench-a-benchmark-for-cross-framework-application-migration-in-enterprise-java.md): ScarfBench 显示，即使编译或部署成功率提高，跨框架企业 Java 迁移中保留行为的成功率仍然很低。

## 带假阳性标签和净新增异味检查的代码异味分诊
架构异味修复应先作为分诊流程启动，在异味被标记为真阳性、假阳性或部分有效之前，先暂停智能体编辑。智能体仍可帮助收集受影响模块、解释依赖路径、提出小补丁，并报告补丁后的异味变化。评审者在批准任何跨模块重构之前，应同时看到已移除的异味和新引入的异味。

SmellBench 给出了设置这个控制点的原因。专家评审在 scikit-learn 的 65 个严重静态检测结果中发现了 41 个假阳性，假阳性率为 63.1%。最佳智能体解决了 47.7% 的案例，但最激进的修复设置引入了 140 个新异味。第一版实现可以是在现有异味检测器外加一个 pull request 机器人：要求分诊标签，在拟议变更前后运行检测器，并在净异味数量增加或受影响模块清单超出评审预算时阻止大范围智能体编辑。

### Evidence
- [SmellBench: Evaluating LLM Agents on Architectural Code Smell Repair](../Inbox/2026-05-07--smellbench-evaluating-llm-agents-on-architectural-code-smell-repair.md): SmellBench 报告称，严重架构异味的假阳性率很高，解决率有限，并且最激进的智能体设置引入了 140 个新异味。
