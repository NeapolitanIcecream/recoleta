---
kind: ideas
granularity: day
period_start: '2026-04-03T00:00:00'
period_end: '2026-04-04T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- evaluation
- software-engineering
- security
- benchmarks
- competitive-programming
tags:
- recoleta/ideas
- topic/coding-agents
- topic/evaluation
- topic/software-engineering
- topic/security
- topic/benchmarks
- topic/competitive-programming
language_code: zh-CN
---

# 代码仓库智能体安全门禁

## Summary
代码智能体评测正在转向真实仓库状态、真实用户故障轨迹和真实扩展安全检查。近期最明确的变化包括：基于支持故障构建的内部回放测试套件、带仓库健康度评分的有状态 pull-request 序列基准，以及第三方技能在进入开发者机器或 CI 之前的隔离步骤。

## 基于代码智能体支持故障构建的真实仓库回放测试套件
采用代码智能体处理代码仓库工作的团队，需要一个基于自身故障历史构建的回归测试工具，而不只是依赖基准测试提示。ABTest 给出了一条可操作的方法：把已确认的用户报告故障抽象成可复用的工作流模式和动作类型，再在真实代码仓库中把它们回放为可执行测试，并检查预期文件状态和执行轨迹。论文中的数字足以说明这应当被视为产品要求。基于 400 个已确认故障，论文生成了 647 个锚定真实仓库的测试用例，并在 Claude Code、Codex CLI 和 Gemini CLI 中发现了 642 个新的真实异常。

一个具体做法是建立内部回放测试套件，起点可以是某个代码智能体部署的 issue 跟踪工单、Slack 事故报告和支持升级记录。第一版不需要基于模型的模糊测试。它可以先覆盖一小组反复出现的工作流故障，例如编辑了错误文件、回滚后留下部分变更、在工作区状态过期时声称执行成功，或者运行了错误的命令序列。在每次智能体升级、每次工具权限变更、每次脚手架变更时都运行这套测试。对于已经让智能体接触生产代码仓库的团队来说，这种门禁成本低于等用户报告在真实使用中不断累积。

### Evidence
- [ABTest: Behavior-Driven Testing for AI Coding Agents](../Inbox/2026-04-03--abtest-behavior-driven-testing-for-ai-coding-agents.md): ABTest 将 400 个已确认的故障报告转换为 647 个锚定真实仓库的可执行测试用例，并在主流代码智能体中确认了 642 个新异常。
- [ABTest: Behavior-Driven Testing for AI Coding Agents](../Inbox/2026-04-03--abtest-behavior-driven-testing-for-ai-coding-agents.md): 论文描述了真实仓库交互中的实际工作流故障，例如编辑错误文件和产生非预期副作用。

## 带仓库健康度评分的有状态 pull-request 序列评测
代码智能体的评测体系现在需要带持久状态的多 PR 序列，以及代码仓库健康度检查。SWE-STEPS 给出了明确理由。当评测从彼此隔离的 pull request 转向相互依赖的序列时，报告的成功率会明显下降：在一个 split 上，Claude Sonnet 4.5 从 66.25% 降到 43.75%，Gemini 3 Flash 从 56.52% 降到 36.59%。论文还报告，智能体编写的代码会让仓库健康度变差，包括比人工基线更高的认知复杂度和技术债务。

一个具体的流程调整，是在现有单任务基准旁边增加一条有状态评测轨道。可以先从一个活跃仓库中的一小段历史 pull request 链开始，在多个步骤之间保留工作区状态，并同时评估功能正确性和变更后的可维护性信号，例如静态分析告警或复杂度增长。对于要判断智能体能否连续几天处理积压工作的平台团队，这类测试很有用；对于要比较不同智能体的采购方，这也有用，因为许多排行榜分数来自每次都清空状态的评测，而这种做法会抹去先前错误的后果。

### Evidence
- [Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution](../Inbox/2026-04-03--beyond-isolated-tasks-a-framework-for-evaluating-coding-agents-on-sequential-software-evolution.md): SWE-STEPS 报告称，孤立的 PR 评测会把成功率高估最多 20 个百分点，并给出了连续评测下的具体下降幅度。
- [Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution](../Inbox/2026-04-03--beyond-isolated-tasks-a-framework-for-evaluating-coding-agents-on-sequential-software-evolution.md): 论文指出，先前低效或有缺陷的代码会产生溢出效应，并通过更高的复杂度和技术债务损害仓库健康度。

## 面向代码智能体文档和模板的技能接入隔离
将第三方技能加载到代码智能体中的组织，需要在安装前设置一道技能接入门禁，检查文档示例和配置模板。新的供应链论文说明了为什么这一步应该放在安装路径上。它的攻击方法把恶意逻辑藏在看似普通的技能文档中，让智能体在正常的安装或编码过程中复制并执行这些内容。在 1,070 个对抗技能样本中，四个框架和五个模型上的绕过率达到 11.6% 到 33.5%。静态分析能拦住大多数攻击，但仍有 2.5% 同时绕过静态检查和模型对齐，作者还报告了四个已确认漏洞。

一个具体做法是为技能和 MCP 风格扩展增加隔离步骤：解析 SKILL.md 和相关文档，提取可执行代码片段和配置片段，标记网络目标和 shell 命令，并要求先通过一次干净的隔离运行，之后技能才能接触开发者工作站或 CI 密钥作用域。团队可以先从市场导入的技能和高权限内部技能开始。直接价值在于减少一类通过示例和模板进入系统的攻击，而开发者往往会把这些内容当成无害的参考文本。

### Evidence
- [Supply-Chain Poisoning Attacks Against LLM Coding Agent Skill Ecosystems](../Inbox/2026-04-03--supply-chain-poisoning-attacks-against-llm-coding-agent-skill-ecosystems.md): 论文记录了通过文档驱动的代码智能体技能投毒，并测量了其在不同框架和模型上的绕过率。
- [Supply-Chain Poisoning Attacks Against LLM Coding Agent Skill Ecosystems](../Inbox/2026-04-03--supply-chain-poisoning-attacks-against-llm-coding-agent-skill-ecosystems.md): 摘要指出，技能文档会作为操作指令发挥作用，并因系统级权限而带来主机被攻陷的风险。
