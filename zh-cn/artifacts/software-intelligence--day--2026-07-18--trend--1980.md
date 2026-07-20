---
kind: trend
trend_doc_id: 1980
granularity: day
period_start: '2026-07-18T00:00:00'
period_end: '2026-07-19T00:00:00'
topics:
- "AI \u4EE3\u7406"
- "\u6846\u67B6\u5DE5\u7A0B"
- "\u4EE3\u7406\u5B89\u5168"
- "\u53EF\u9760\u6027"
- "\u53EF\u89C2\u6D4B\u6027"
run_id: materialize-outputs
aliases:
- recoleta-trend-1980
tags:
- recoleta/trend
- "topic/ai-\u4EE3\u7406"
- "topic/\u6846\u67B6\u5DE5\u7A0B"
- "topic/\u4EE3\u7406\u5B89\u5168"
- "topic/\u53EF\u9760\u6027"
- "topic/\u53EF\u89C2\u6D4B\u6027"
language_code: zh-CN
---

# 代理可靠性正围绕模型进行工程化构建

## 概览
近期对代理框架和可执行检查的关注，正以面向实现的形式延续。今天的材料将组织上下文、静态风险检测、可观测性和容量管理置于模型周围。证据具有实践性，但仍然有限：材料包括项目文档、监控仪表板和招聘信息，而不是受控的比较研究。

## 研究发现

### 代码库与部署前控制
两个项目都将模型视为可靠代理系统中的一个组件。Harness Engineering 提议将本地要求、权限、过往故障和证明检查编码到代码库中，使后续运行能够继承组织判断。SafeAI 在运行时测试前离线扫描代理代码，检查提示注入、暴露的工具、Model Context Protocol（MCP）配置错误以及缺失的治理措施。两者共同将前几天关于证据门控的主题延伸到代码库设计和持续集成，但两个项目都没有报告独立的比较基准。

#### 资料来源
- [Harness Engineering](../Inbox/2026-07-18--harness-engineering.md): 将框架工程定义为在保持模型和代理不变的同时调整上下文与工具。
- [We built an open-source static AI risk analyzer in 5 days using AI coding agents](../Inbox/2026-07-18--we-built-an-open-source-static-ai-risk-analyzer-in-5-days-using-ai-coding-agents.md): 识别代理特有的风险面，并将离线扫描置于部署之前。

### 运行时可靠性与容量
运行可靠性也正成为核心产品工作。Cofounder 的代理平台职位将端到端工作流中的执行可靠性、追踪、指标、测试、成本和集成质量明确列为工程职责。另一方面，Codex Resets 记录了 26 周内 35 次使用限额重置，平均间隔为 8.9 天；保留的公告将重置与流量快速增长、服务中断和配额消耗异常迅速联系起来。该仪表板不是受控的服务质量研究，但它说明了容量和计量为何属于代理可靠性技术栈。

#### 资料来源
- [Hiring Private equity firm doing 9M in revenue](../Inbox/2026-07-18--hiring-private-equity-firm-doing-9m-in-revenue.md): 将执行可靠性、可观测性、检测、成本和集成工作列为职责范围。
- [Codex Resets](../Inbox/2026-07-18--codex-resets.md): 报告了 26 周内 35 次重置、8.9 天的平均间隔以及 67.7 天的最长间隔。
