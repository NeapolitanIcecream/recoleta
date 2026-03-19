---
source: arxiv
url: http://arxiv.org/abs/2603.05578v1
published_at: '2026-03-05T17:44:29'
authors:
- Bowei Xia
- Mengkang Hu
- Shijian Wang
- Jiarui Jin
- Wenxiang Jiao
- Yuan Lu
- Kexin Li
- Ping Luo
topics:
- language-agents
- tool-creation
- benchmarking
- mcp
- self-evolving-agents
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Tool-Genesis: A Task-Driven Tool Creation Benchmark for Self-Evolving Language Agent

## Summary
这篇论文提出 **Tool-Genesis**，一个面向“语言智能体能否从抽象任务需求中自行创建可复用工具”的诊断型基准，而不再假设工具接口已知。其核心发现是：即使最强模型，单次生成时也常在接口或实现上出小错，而这些小错会沿流水线被放大，显著拖垮最终任务成功率。

## Problem
- 现有工具使用/工具生成评测大多是 **spec-first**：默认给定接口、schema 或高质量参考规范，因此无法真正测试模型是否能从抽象需求中**推断工具接口并实现工具**。
- 许多评测只看最终任务成败，属于“**黑盒评估**”；一旦失败，很难区分是接口设计错、代码逻辑错，还是后续工具使用策略错。
- 这很重要，因为真实部署里工具规格经常缺失、API 会变化、长尾需求会出现；如果智能体不能自己创建、修复、维护工具，就难以实现真正的**自演化语言智能体**。

## Approach
- 作者构建了一个 **requirement-driven** 基准：只给自然语言需求，不给预设工具规格，要求模型完成两步：**接口预测**（生成 MCP schema）和**工具物化**（生成可执行 server 实现）。
- 评测被拆成两种设置：**Oracle Materialization** 用真值 schema 测实现能力，**Cascaded Materialization** 用模型自己预测的 schema 测端到端能力，从而把“接口错误”与“实现错误”尽量分开。
- 他们设计了四层诊断指标：L1 表面合规与服务可执行性，L2 **Schema-F1** 看接口语义匹配，L3 用 **UT_soft / UT_hard** 测功能正确性与边界/负例鲁棒性，L4 用固定代理配合生成工具去解任务，并报告 **Oracle-Normalized Success Rate**。
- 数据集来自真实 MCP server 生态，经抓取、过滤、任务与轨迹生成、单元测试生成和人工复核得到；最终保留 **86 个 servers、508 个 tools、2150 个 tasks、9441 个 unit tests**，覆盖 **24 个 domain classes**。

## Results
- 数据集规模上，Tool-Genesis 包含 **86** 个可执行 MCP servers、**508** 个工具、**24** 个领域、**2150** 个任务、**9441** 个单测；平均每个任务 **6** 个执行步骤、使用 **3** 个工具，表明它不是简单单步调用基准。
- 在 **Direct** 单次生成下，最佳模型 **gpt-5.1** 只有 **Schema-F1=0.688、UT_soft=0.281、UT_hard=0.161、SR=0.372**；说明即使强模型，真正可用的工具创建能力仍然有限。
- 在 **Code-Agent** 闭环修复下，表现显著提高：**gpt-5.1** 达到 **Compliance=0.895、Exec=0.941、Schema-F1=0.867、UT_soft=0.421、UT_hard=0.246、SR=0.604**，是表中最高 SR 结果之一。
- 其他模型也显示闭环修复收益明显：例如 **gemini-3-flash-preview** 从 Direct 的 **Exec 0.140 / Schema-F1 0.116 / SR 0.103** 提升到 Code-Agent 的 **Exec 0.977 / Schema-F1 0.912 / SR 0.581**。
- 开源/开放权重模型中，**Kimi-K2** 在 Code-Agent 下达到 **Schema-F1=0.898、UT_soft=0.389、UT_hard=0.235、SR=0.585**；**Qwen3-32B** 达到 **SR=0.495**，**DeepSeek-v3.2** 达到 **SR=0.449**。
- 论文最强的具体主张不是“工具创建已被解决”，而恰恰相反：**小的接口或实现缺陷会级联放大，导致下游效用骤降**；闭环执行反馈能明显缓解，但即便最优配置，严格单测和最终成功率仍远未饱和。

## Link
- [http://arxiv.org/abs/2603.05578v1](http://arxiv.org/abs/2603.05578v1)
