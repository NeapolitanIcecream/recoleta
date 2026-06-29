---
kind: ideas
granularity: day
period_start: '2026-05-22T00:00:00'
period_end: '2026-05-23T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software evaluation
- AI code quality
- developer tools
- AI cost tracking
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-evaluation
- topic/ai-code-quality
- topic/developer-tools
- topic/ai-cost-tracking
language_code: zh-CN
---

# 编码代理责任控制

## Summary
长时间运行的编码代理工作已经可以加入更具体的操作控制：演示用公开证据包、生成代码的明确人类负责人，以及绑定到已合并工作的 token 预算。要测试的内容足够小，可以放进评估发布流程、pull request 模板或本地开发者仪表盘里。

## 长时间运行的编码代理演示需要证据包
AI 团队在做大规模编码代理演示时，应该为每个主张发布一份简洁的证据包：提示词版本、生成的源代码、完整代理日志、重试和 dry-run 次数、重启事件、人工批准、总 token 数、美元成本，以及与公开代码的相似度报告。Google 的操作系统演示就是一个清晰的测试案例。公开说明写到 API 费用为 916.92 美元、token 预算为 26 亿，而批评文章指出没有公布长提示词、源代码或运行日志，也没有对公开的玩具操作系统代码做相似度分析或日志分析。

这是一个可以落地的评估层。内部发布门槛可以要求在演示被用于发布稿或销售证明前先交齐这份材料。外部读者仍然需要自行判断，但他们可以检查结果是来自通用代理运行、任务专用脚手架、反复重启，还是未披露的提示词工作。

### Evidence
- [Did Google's AI agents build an operating system for $916?](../Inbox/2026-05-22--did-google-s-ai-agents-build-an-operating-system-for-916.md): 总结了 Google 的操作系统代理主张中缺失的材料：提示词、代码、日志、重试次数、抄袭检查和成本报告。
- [Did Google's AI agents build an operating system for $916?](../Inbox/2026-05-22--did-google-s-ai-agents-build-an-operating-system-for-916.md): 描述了专用脚手架、子代理、重启基础设施、反作弊措施，以及人工介入报告不清楚的问题。
- [Did Google's AI agents build an operating system for $916?](../Inbox/2026-05-22--did-google-s-ai-agents-build-an-operating-system-for-916.md): 指出 Google 没有公布长提示词、生成代码或日志，也没有对抄袭代码做相似度或日志分析。
- [Did Google's AI agents build an operating system for $916?](../Inbox/2026-05-22--did-google-s-ai-agents-build-an-operating-system-for-916.md): 报告了公开的美元成本和 token 预算，这些都是证据包里有用的部分。

## AI 生成 pull request 的负责人审查记录
允许 AI 编写代码的工程团队，应该在 pull request 里加一个明确的负责人字段。负责人应说明哪些文件用了 AI，跑了哪些测试或检查，改动是否沿用了现有仓库模式，以及合并后谁能解释、重构、删除和运维这段代码。这对应的是 AI 代码量带来的维护风险：产出看起来完整，还是可能复制逻辑、制造薄弱边界，或藏起以后工程师无法安全修改的行为。

同样的规则也适用于使用 Claude Code 或类似工具的实验室和课程。那篇机器人案例显示，工具在 LaTeX、Python、卡尔曼滤波和 ROS 迁移上都能产出有效结果，但作者仍然需要在 package.xml 问题上把工具拉回来，并且拒绝了质量较弱的研究想法。对很多团队来说，一个简单政策就够了：可以用 AI，但有经验的人要对许可、准确性、测试和后续维护负责。

### Evidence
- [When Code Is Cheap, Does Quality Still Matter?](../Inbox/2026-05-22--when-code-is-cheap-does-quality-still-matter.md): 定义了生成代码的质量标准，即人能否解释、审查、重构、删除和运维它。
- [When Code Is Cheap, Does Quality Still Matter?](../Inbox/2026-05-22--when-code-is-cheap-does-quality-still-matter.md): 解释了 LLM 会让产出更便宜，但理解、修改、审查、调试和运维仍然昂贵。
- [The First Hit Is Free](../Inbox/2026-05-22--the-first-hit-is-free.md): 总结了 AI 辅助研究、教学和机器人工作的人工负责政策。
- [The First Hit Is Free](../Inbox/2026-05-22--the-first-hit-is-free.md): 给出作者在 ROS 迁移中把 Claude Code 拉回正轨的具体例子，并说明可以自由使用 AI，但责任由人承担。

## 把 token 预算绑定到已合并 pull request 和代理会话
开发工具团队应该在代理工作已经发生的地方加入 token 记账：代理会话视图、pull request、issue 和本地工作仪表盘。真正有用的指标不只是总 token 消耗。仪表盘应该按已合并的 pull request、已交付功能、已关闭 issue 和代理会话展示 token 和模型支出，并对重试循环、涉及超过三份文件的任务，以及把昂贵模型用在简单搜索或重构工作上的情况发出警告。

tokenflex.ing 的文章显示了大家对可见性的需求，尽管它对使用量的主张没有给出可复现的测量方法。Planet Maiko 提供了一个放置这种控制的实际位置：本地工作台，带代理聊天、应用内 diff 审查、GitHub 和 Linear 集成、本地 RAG，以及成本感知的模型路由。小团队可以先把 Claude Code 或 Cursor 的日志导入两周，再比较模型支出、已合并工作和回退变更。

### Evidence
- [I used $30,983 of AI tokens last month in Claude Code on $200/mo plan](../Inbox/2026-05-22--i-used-30983-of-ai-tokens-last-month-in-claude-code-on-200-mo-plan.md): 指出 token 可见性是主要问题，并提到需要按已交付功能或已合并 pull request 统计 token 的结果指标。
- [I used $30,983 of AI tokens last month in Claude Code on $200/mo plan](../Inbox/2026-05-22--i-used-30983-of-ai-tokens-last-month-in-claude-code-on-200-mo-plan.md): 展示了开发者往往要看过之后才知道实际 token 用量，并列出降低 Claude Code 支出的工作流改动。
- [I used $30,983 of AI tokens last month in Claude Code on $200/mo plan](../Inbox/2026-05-22--i-used-30983-of-ai-tokens-last-month-in-claude-code-on-200-mo-plan.md): 建议拆分更大的任务、用 grep 做简单操作、调整模型路由，并按已交付功能跟踪 token。
- [I was bored so I turned my dev tools into an alien planet ruled by my dog](../Inbox/2026-05-22--i-was-bored-so-i-turned-my-dev-tools-into-an-alien-planet-ruled-by-my-dog.md): 列出了 Planet Maiko 的本地执行、GitHub 和 Linear 集成、代理聊天、应用内 diff 审查和成本感知模型路由。
