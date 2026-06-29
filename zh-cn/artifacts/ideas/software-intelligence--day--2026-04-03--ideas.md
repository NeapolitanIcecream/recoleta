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

# 仓库代理安全门

## Summary
代码代理评估正在转向真实仓库状态、真实用户失败轨迹和真实扩展安全检查。眼下最明确的近期开销变化，是基于支持失败构建内部回放套件、带仓库健康评分的有状态 pull request 序列基准，以及在第三方技能接触开发者机器或 CI 之前设置隔离步骤。

## 从代码代理支持失败中构建以仓库为基础的回放套件
采用代码代理进行仓库工作的团队，需要一个基于自身失败历史构建的回归测试套件，而不只是基准提示。ABTest 给出了一条可行路径：把已确认的用户报障失败抽象成可复用的工作流模式和动作类型，再把它们回放成在真实仓库中执行的测试，并检查预期文件状态和执行轨迹。数据足以把这件事当成产品需求。论文从 400 个已确认失败中生成了 647 个以仓库为基础的案例，并在 Claude Code、Codex CLI 和 Gemini CLI 上发现了 642 个新的真实异常。

一个具体做法是为某个代码代理部署建立内部回放套件，输入来源包括工单、Slack 故障报告和支持升级单。第一版不需要基于模型的 fuzzing。它可以覆盖少量常见的工作流错误，比如改错文件、回滚后留下部分修改、在工作区状态过期时声称成功，或者执行了错误的命令序列。把这套测试放在每次代理升级、每次工具权限变更、每次脚手架变更时运行。对已经把代理接到生产仓库的团队来说，这比等用户在真实使用中不断报错要便宜得多。

### Evidence
- [ABTest: Behavior-Driven Testing for AI Coding Agents](../Inbox/2026-04-03--abtest-behavior-driven-testing-for-ai-coding-agents.md): ABTest converts 400 confirmed failure reports into 647 executable repository-grounded cases and confirms 642 new anomalies across major coding agents.
- [ABTest: Behavior-Driven Testing for AI Coding Agents](../Inbox/2026-04-03--abtest-behavior-driven-testing-for-ai-coding-agents.md): The paper describes practical workflow failures such as wrong-file edits and unintended side effects during real repository interaction.

## 带仓库健康评分的有状态 pull request 序列评估
代码代理的评估体系现在需要多 PR 序列、持久状态和仓库健康检查。SWE-STEPS 给出了直接理由。评估从孤立的 pull request 转向依赖序列后，报告成功率会明显下降：Claude Sonnet 4.5 在一个划分上从 66.25% 降到 43.75%，Gemini 3 Flash 从 56.52% 降到 36.59%。论文还报告，代理写出的代码让仓库健康变差，包括比人工基线更高的认知复杂度和技术债务。

一个具体的流程改动，是在现有单任务基准旁边增加一条有状态评测轨道。先从某个活跃仓库里选一小串历史 pull request，步骤之间保留工作区状态，同时给功能正确性和修改后的可维护性信号打分，比如静态分析告警或复杂度增长。这类测试对平台团队有用，他们要判断代理能不能在几天内处理积压工作；对买家也有用，因为很多排行榜分数来自干净重置，而这种重置会抹掉早先错误的后果。

### Evidence
- [Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution](../Inbox/2026-04-03--beyond-isolated-tasks-a-framework-for-evaluating-coding-agents-on-sequential-software-evolution.md): SWE-STEPS reports that isolated PR evaluation can overstate success by up to 20 points and gives concrete drops under continuous evaluation.
- [Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution](../Inbox/2026-04-03--beyond-isolated-tasks-a-framework-for-evaluating-coding-agents-on-sequential-software-evolution.md): The paper states that previous inefficient or buggy code causes spillover effects and degrades repository health through higher complexity and technical debt.

## 代码代理文档与模板的技能摄取隔离
把第三方技能加载进代码代理的组织，需要在安装前设置一个技能摄取门，检查文档示例和配置模板。新的供应链论文说明了为什么这一步要放在初始化流程里。攻击把恶意逻辑藏在看起来普通的技能文档中，让代理在正常设置或编码工作中复制并执行它。在 1,070 个对抗性技能上，绕过率在四个框架和五个模型中达到 11.6% 到 33.5%。静态分析能拦住大多数攻击，但仍有 2.5% 同时绕过静态检查和模型对齐，作者还报告了四个已确认漏洞。

一个具体做法是给技能和 MCP 风格扩展加一道隔离步骤：解析 SKILL.md 和相关文档，提取可执行片段和配置片段，标出网络目标和 shell 命令，并要求先在隔离环境中干净运行一次，才能让这个技能接触开发者工作站或 CI 秘钥范围。团队可以先从市场导入和高权限内部技能开始。直接价值是减少一类从示例和模板进入的攻击，而开发者常把这些内容当成无害的参考文本。

### Evidence
- [Supply-Chain Poisoning Attacks Against LLM Coding Agent Skill Ecosystems](../Inbox/2026-04-03--supply-chain-poisoning-attacks-against-llm-coding-agent-skill-ecosystems.md): The paper documents documentation-driven poisoning of coding-agent skills with measured bypass rates across frameworks and models.
- [Supply-Chain Poisoning Attacks Against LLM Coding Agent Skill Ecosystems](../Inbox/2026-04-03--supply-chain-poisoning-attacks-against-llm-coding-agent-skill-ecosystems.md): The abstract states that skill documentation functions as operational directives with system-level privilege implications for host compromise.
