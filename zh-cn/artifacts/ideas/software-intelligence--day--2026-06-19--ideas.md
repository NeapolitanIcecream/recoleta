---
kind: ideas
granularity: day
period_start: '2026-06-19T00:00:00'
period_end: '2026-06-20T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- agent security
- agent observability
- model routing
- small language models
- software engineering AI
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-security
- topic/agent-observability
- topic/model-routing
- topic/small-language-models
- topic/software-engineering-ai
language_code: zh-CN
---

# 受控智能体运营

## 摘要
智能体团队现在有了可测试的具体控制模式：用于过期状态故障的确定性重放、用于多文件安全缺陷的发布前源码审计，以及用于常规知识工作的会话锁定模型路由。公开证据大多来自产品或文章主张，因此更有用的做法是开展范围较窄的本地试验，并衡量误报、成本、延迟和回滚行为。

## 用于生产环境智能体过期状态事件的时间事实账本
生产环境智能体团队可以在事件响应中加入确定性重放步骤，用来处理由事实变化导致的故障。StaleTrace 描述了一个范围较窄的设计：接收智能体的工具调用和已记录的事实事件，把这些事实重放到带有效期窗口的时间事实账本中，并比较智能体使用的事实与当时有效的事实。输出包括根因、影响范围和事件报告。

第一个有用的构建可以是一个面向单个生产环境智能体的适配器，把工具调用、客户或账户状态变化以及时间戳导出为可重放日志。团队应在一小组历史事件上测试它，这些事件中，当前数据库状态掩盖了智能体在决策时看到的内容。值得复用的公开主张是确定性审计路径：不调用 LLM，不使用嵌入，并且相同输入产生相同判定。缺失的衡量项是，重放是否比团队当前的 trace 和日志审查更快发现真实的过期状态故障。

### 资料来源
- [Show HN: StaleTrace – A temporal ledger that catches stale-state agent bugs](../Inbox/2026-06-19--show-hn-staletrace-a-temporal-ledger-that-catches-stale-state-agent-bugs.md): 概述 StaleTrace 的时间账本设计、输入类型、确定性审计主张，以及缺少基准测试结果这一点。
- [Show HN: StaleTrace – A temporal ledger that catches stale-state agent bugs](../Inbox/2026-06-19--show-hn-staletrace-a-temporal-ledger-that-catches-stale-state-agent-bugs.md): 展示产品流程：输入工具调用和已记录事实，重放有效期窗口，暴露过期或冲突状态，并生成事件报告。

## 面向多文件安全缺陷的发布前源码审计
安全团队可以把智能体式静态审计作为发布门禁试用，用于普通 SAST 和在线测试经常漏掉的代码路径：授权链、功能开关控制的流程、管理路由、移动应用逻辑，以及多仓库变更。Aikido Code Audit 声称可以跨文件和模块跟踪引用，返回根因和代码证据，并生成 AutoFix 拉取请求。

一个可操作的测试是在重要版本合并前进行为期两周的审计。只把带代码证据的发现转入开发者分诊，然后衡量确认问题率、重复率、修复时间，以及与最近一次渗透测试或人工审查的重叠情况。Aikido 报告称，早期用户每个代码库发现的问题中位数约为 25 个，并声称覆盖完整渗透测试所发现问题的 70–80%，成本约为其十分之一，但摘录没有给出公开数据集或可复现协议。可把供应商数据作为开展受控发布门禁试验的理由，并在本地衡量误报和修复接受情况。

### 资料来源
- [Aikido Code Audit](../Inbox/2026-06-19--aikido-code-audit.md): 概述产品主张、目标漏洞类别、报告的早期用户数据，以及缺少公开评估协议这一点。
- [Aikido Code Audit](../Inbox/2026-06-19--aikido-code-audit.md): 描述重要版本发布前的预期工作流、跨文件引用跟踪、代码证据和 AutoFix 拉取请求。
- [Aikido Code Audit](../Inbox/2026-06-19--aikido-code-audit.md): 列出仅基于源码即可覆盖的示例，例如 ReDoS、仅管理员可访问的路由、多个仓库、功能开关控制的路径、未部署变更和移动应用。

## 面向办公文档和电子表格任务的会话锁定模型路由测试
如果文档、邮件和电子表格助手的推理费用较高，团队可以测试一个路由器：把常规工作发送给较小模型，把困难工作发送给前沿模型，并在会话期间固定该模型。报告中的 GDPVal-AA 设置在 GPT-5.5 和 GPT-5.4 Mini 之间路由，达到 1759 ELO，而单独使用 GPT-5.5 为 1769 ELO，并把路由开销控制在每次请求 0.01 美元以下。

构建范围应较小：分类任务类型和难度，在会话开始时选择一次模型，记录成本、延迟、缓存命中率和用户修正率，并对一组最终输出样本进行盲审。会话锁定很重要，因为会话中途切换模型可能破坏提示缓存并改变输出行为。证据还显示，经领域调优的小模型可作为专门工作负载的候选，包括约 5B 活跃参数的 MAI-Code-1-Flash，它在 SWE-Bench Pro 上得分 51.2%，高于 Claude Haiku 4.5 的 35.2%，同时最多少用 60% token。

### 资料来源
- [Knowledge workers don't need frontier models](../Inbox/2026-06-19--knowledge-workers-don-t-need-frontier-models.md): 概述路由方法、GDPVal-AA 分数、路由器开销、会话锁定，以及声称的成本和延迟收益。
- [Knowledge workers don't need frontier models](../Inbox/2026-06-19--knowledge-workers-don-t-need-frontier-models.md): 给出 GDPVal-AA 设置、模型选择、排行榜背景和 ELO 对比。
- [Knowledge workers don't need frontier models](../Inbox/2026-06-19--knowledge-workers-don-t-need-frontier-models.md): 报告 MAI-Code-1-Flash 的规模、SWE-Bench Pro 结果、token 减少主张，以及它在 GitHub Copilot 自动选择器中的使用。
