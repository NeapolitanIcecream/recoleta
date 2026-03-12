---
source: hn
url: https://coasty.ai:443/
published_at: '2026-03-05T23:16:26'
authors:
- nkov47as
topics:
- computer-use-agent
- autonomous-operations
- sandbox-security
- gui-automation
- enterprise-agent
relevance_score: 0.1
run_id: materialize-outputs
---

# The Sandboxed Open-Source Agent that is 70% cheaper than E2B

## Summary
Coasty 是一个面向真实业务流程的开源沙箱式自主代理平台，主打在浏览器和企业软件中像人一样执行运营工作。给定文本更像产品页面而非学术论文，核心卖点是低成本、可审计、安全隔离，以及在 OSWorld 基准上的高成功率。

## Problem
- 企业中的营销、销售、运营、QA、报销与报告等大量流程性工作，通常需要专门团队手动在多个软件中重复执行，成本高且扩展慢。
- 传统聊天机器人只能回答问题，难以在真实软件环境中端到端完成“打开网页—填写表单—提取数据—发送邮件”这类操作。
- 在让 AI 直接操作业务系统时，企业还关心可靠性、纠错能力、审计追踪和会话隔离安全，这些是落地的关键。

## Approach
- 核心机制是一个**自主计算机使用代理**：用户用自然语言分配任务，系统自动打开浏览器或应用、导航界面、点击输入、读取页面信息并完成整条工作流。
- 平台强调**self-correcting execution**，即遇到误点、死路或异常时，代理会自行纠错、换路径并继续执行，而不是立即失败。
- 每次任务都运行在**isolated sandbox** 中，宣称不同会话彼此隔离，以降低数据泄露与环境污染风险。
- 系统提供**full audit trail**，记录每次点击、按键和决策，便于人工复核输出、追踪过程并继续下一步操作。
- 产品定位不是单轮问答，而是“AI workforce / autonomous operations platform”，面向跨营销、销售、运维、QA 等部门的连续业务执行。

## Results
- 文本宣称在 **OSWorld benchmark** 上达到 **82% success rate**，并称其为 **#1 in the world**；但摘录中**未给出具体对比方法、数据切分、评测设置或误差范围**。
- 标题声称其“**70% cheaper than E2B**”，但正文摘录**没有提供计算口径、工作负载假设或直接对照表**，因此无法独立验证。
- 成本宣传给出一个业务侧示例：**3-person operations team costs $12,000+/mo**，而 Coasty 声称可 **24/7** 运行相同工作负载；不过这不是标准学术基准结果。
- 产品宣称可在 **60 seconds** 内部署，并支持诸如**跨 10 个市场做竞品研究、维护 500 条销售线索、每周生成投资人更新、自动 QA、自动发送邮件**等端到端任务。
- 总体上，最强的可量化主张是 **82% OSWorld 成功率**；除此之外，其余更多是产品能力与商业价值陈述，而非完整论文式实验结果。

## Link
- [https://coasty.ai:443/](https://coasty.ai:443/)
