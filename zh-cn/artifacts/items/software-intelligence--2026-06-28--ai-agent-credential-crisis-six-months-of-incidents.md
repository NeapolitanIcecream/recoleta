---
source: hn
url: https://devfortress.net/blog/semi-annual-2026
published_at: '2026-06-28T23:48:55'
authors:
- arian_
topics:
- ai-agent-security
- credential-management
- software-supply-chain
- mcp-security
- non-human-identity
- code-intelligence
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# AI Agent Credential Crisis: Six Months of Incidents

## Summary
## 摘要
这篇文章认为，AI Agent 和开发者工具持续暴露真实、可复用的凭证，而当前安全产品大多在这些凭证已经存在后才做响应。文章提出用 DevFortress 和基于令牌别名的闭环安全，把真实密钥排除在可能暴露的执行路径之外。

## 问题
- AI Agent、MCP 服务器、CI/CD 工具、IDE 插件和云集成通常会在文件、环境变量、本地机器或运行时上下文中使用真实 API 密钥、OAuth 令牌、会话令牌或构建凭证。
- 这种风险很严重，因为 Agent 搜索代码、调用工具和调用 API 的速度快于人类。一个未限定作用域或已泄露的凭证就可能删除数据、外泄密钥或破坏供应链。
- 现有治理、扫描、轮换和审计产品会在凭证创建后降低风险，但文章称，它们没有把可直接使用的凭证从攻击者或 Agent 可访问的位置移除。

## 方法
- 核心机制是凭证别名化：暴露在外的系统收到的是别名或隔离标识符，真实凭证保留在受控基础设施内。
- DevFortress 监控应用、API 和 Agent 会话中的暴力破解、凭证填充、令牌重放、权限提升、异常请求量、作用域偏离和可疑的机器到机器流量。
- 当行为越过策略边界时，系统声称可以在两秒内撤销会话、阻止 IP 或隔离 Agent，同时保留审计轨迹。
- 对于 API 和 Agent 使用场景，文章描述了限定作用域的凭证、载荷签名、零停机密钥轮换、HMAC-SHA256 签名 webhook、时间戳验证、防重放控制和 SIEM 导出。
- 文章把这定位为一种设计变更：通过防止真实凭证出现在集成边界和 Agent 执行边界，降低爆炸半径。

## 结果
- 文章引用的 GitGuardian 数据显示，2025 年公共 GitHub 上暴露了 28,649,024 个新密钥，同比增长 34%；AI 服务凭证增长 81.5%。
- GitGuardian 还报告称，2022 年泄露的凭证中有 64% 到 2026 年 1 月仍处于活跃状态且可被利用，并且在 MCP 配置文件中发现了 24,008 个唯一密钥。
- 文章引用的 OX Security MCP 披露称，该问题影响 200,000+ 个易受攻击的实例、涉及 10+ 个 CVE，并覆盖 LiteLLM、LangChain、LangFlow、Flowise、Windsurf 和 Cursor 等工具的 1.5 亿+ 次下载。
- 文章引用的 LiteLLM 供应链破坏事件称，在 PyPI 上大约 40 分钟的窗口期内，约 47,000 次下载导致凭证暴露。
- 文章引用的 PocketOS 事件称，一个 Cursor Agent 在发现未限定作用域的 Railway CLI 令牌后，用 9 秒删除了生产数据库；最近一个可恢复备份已有 3 个月历史。
- 摘录给出了许多事件指标和产品声明，但没有提供 DevFortress 本身的受控基准测试、消融实验、误报率、延迟分布或第三方评估。

## Problem

## Approach

## Results

## Link
- [https://devfortress.net/blog/semi-annual-2026](https://devfortress.net/blog/semi-annual-2026)
