---
kind: ideas
granularity: day
period_start: '2026-06-13T00:00:00'
period_end: '2026-06-14T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software factories
- local AI
- data privacy
- Rails
- database correctness
- LLM inference
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-factories
- topic/local-ai
- topic/data-privacy
- topic/rails
- topic/database-correctness
- topic/llm-inference
language_code: zh-CN
---

# 受控的代理式工程工作流

## Summary
工程团队可以通过在上下文、支出、验证和数据不变量上加明确控制，把代理式开发推进到更窄的生产工作流里。最直接的近期开关是有支出上限的 Claude Code 子代理链、带代理可读契约和代理自跑测试门禁的项目规范，以及在加锁前要求写明数据库不变量的 Rails 变更审查。

## 为调试工作流设置支出上限的 Claude Code 子代理链
使用 Claude Code 做事故分诊或代码质量扫描的团队，应把嵌套子代理当作一个已配置的工作流来管理，并配上预算、允许列表和深度规则。Claude Code v2.1.172 允许子代理再生成子代理，最多五层，每一层都有自己的提示词、模型选择和 20 万 token 上下文。这适合日志检索这类噪声很大的任务，因为父会话只需要一个简短结论。

一个可行的配置，是在项目级 `.claude/agents/<name>.md` 链里放一条调试路径：一个 Opus 分诊代理、若干 Sonnet 复现代理，以及用于 grep、生成测试或汇总日志的 Haiku 叶子代理。每个代理定义都应使用 `Agent()` 指明它可以生成的唯一子代理。在把这条链用于生产事故前，要先加上按会话计算的支出上限。文中报告的失败规模足以说明为什么要这么做：每个分支每层大约有 7 倍 token 开销，有用户跑到每分钟 887,000 token，还有一个案例在 23 个子代理运行三天后出现了 47,000 美元账单。

最低成本的测试是一条真实事故回放。记录 token、耗时、生成的代理数量，以及父会话是否拿到了足够证据来做决定，而不需要原始日志倾倒。

### Evidence
- [Claude Code v2.1.172: Sub-Agents Can Now Spawn Sub-Agents](../Inbox/2026-06-13--claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents.md): 概括了 Claude Code 的嵌套子代理、五层深度、独立上下文、模型路由、token 开销和已报告的成本事故。
- [Claude Code v2.1.172: Sub-Agents Can Now Spawn Sub-Agents](../Inbox/2026-06-13--claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents.md): 说明了在子代理定义里需要支出上限和 `Agent()` 允许列表。
- [Claude Code v2.1.172: Sub-Agents Can Now Spawn Sub-Agents](../Inbox/2026-06-13--claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents.md): 描述了分层路由和循环生成的风险。

## 面向编码代理 pull request 的可读项目契约和隔离测试门禁
要求编码代理处理的不只是小改动时，就需要一份代理在写代码前能读懂的项目契约。这个契约可以是一份 `AGENTS.md`，也可以是一组 markdown 文件，写清架构边界、验证命令、编码规则和发布预期。再配上一套代理自己能执行的分层门禁：lint、类型检查、单元测试、安全扫描、集成测试、UI 测试，以及系统支持时的发布检查。

这里的运营压力来自共享验证容量。软件工厂的文章说，当多个请求共用一个 staging 环境、一个分支或一个部署名额时，并行代理工作就会停住。一个有用的起点，是让代理运行验证脚本，自己创建或重置测试环境，执行所需检查，并把轨迹附在 pull request 上。人工评审随后只看失败项、风险较高的 diff 和产品判断。评审意见、事故和指标也应该回流到契约里，让重复错误变成明确指令。

先从一个服务和一种常见请求开始。只要代理能接单、产出 pull request、在没有开发者盯着环境的情况下跑完约定检查，并留下足够证据让评审快速通过或拒绝，这个试点就算成功。

### Evidence
- [Designing Software for Software Factories](../Inbox/2026-06-13--designing-software-for-software-factories.md): 列出了项目契约、分层验证、代理运行测试循环、隔离环境和反馈记录，作为代理式开发循环的要求。
- [Designing Software for Software Factories](../Inbox/2026-06-13--designing-software-for-software-factories.md): 描述了并发请求处理，以及共享 staging、分支或部署名额造成的瓶颈。
- [Designing Software for Software Factories](../Inbox/2026-06-13--designing-software-for-software-factories.md): 指出软件工厂工作流需要模式、契约和脚手架。

## 在 AI 生成改动中加锁前先审查 Rails 不变量
接受 AI 生成后端改动的 Rails 团队，应在涉及资金、预订、配额、角色或库存的 pull request 里加入不变量审查。评审者应先用一句话写出要保护的数据规则，再检查数据库是否用最小合适的机制来强制它：唯一索引、`CHECK`、`SERIALIZABLE`、加锁的父行、advisory lock，或顺序加锁。

这可以抓住生成式 Rails 代码里的常见失败模式。`lock`、`lock!` 和 `with_lock` 看起来很简单，但它们的行为取决于事务范围、隔离级别、适配器行为和查询形状。行锁可以修复单行丢失更新，不能保护跨多行、缺失行，或像“每个活动最多 100 个预订”这样的谓词。文章还指出，`Seat.lock.find(id)` 如果外面没有事务，锁会立刻释放。

一个轻量的落地方式，是给 pull request 加检查清单，并且对每条高风险路径做两个并发测试：一个测试同一行的同时写入，另一个测试更宽的不变量。如果第二个测试失败，修复应放在数据库规则或事务设计里，而不是再加一个应用层守卫。

### Evidence
- [Rails: The Sharp Parts. Lock Is Not a Mutex](../Inbox/2026-06-13--rails-the-sharp-parts-lock-is-not-a-mutex.md): 概括了为什么 Rails 锁容易误用，并建议从不变量出发，选择最小的数据库机制。
- [Rails: The Sharp Parts. Lock Is Not a Mutex](../Inbox/2026-06-13--rails-the-sharp-parts-lock-is-not-a-mutex.md): 说明 Rails 的悲观锁取决于事务边界、隔离级别、数据库行为和查询形状，而且行锁不能覆盖多行不变量。
- [Rails: The Sharp Parts. Lock Is Not a Mutex](../Inbox/2026-06-13--rails-the-sharp-parts-lock-is-not-a-mutex.md): 列出了评审者在动用锁之前应先问的不变量问题。
