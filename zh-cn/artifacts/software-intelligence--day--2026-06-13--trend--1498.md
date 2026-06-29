---
kind: trend
trend_doc_id: 1498
granularity: day
period_start: '2026-06-13T00:00:00'
period_end: '2026-06-14T00:00:00'
topics:
- coding agents
- software factories
- local AI
- data privacy
- Rails
- database correctness
- LLM inference
run_id: materialize-outputs
aliases:
- recoleta-trend-1498
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-factories
- topic/local-ai
- topic/data-privacy
- topic/rails
- topic/database-correctness
- topic/llm-inference
language_code: zh-CN
---

# 代理式开发正在接受运行控制的检验

## Overview
当天最强的信号是对 AI 工作的运行控制。软件工厂需要契约和测试。Claude Code 的嵌套代理需要上下文边界和支出上限。本地 AI 工具又加了一层约束：当云端训练条款不清楚时，把敏感工作留在用户机器上。

## Clusters

### Coding-agent production loops
代理式开发现在被当作带有可测门槛的生产系统来描述。软件工厂提案定义了一个循环：接收客户请求，设计并实现改动，运行测试，并在有人作为停止按钮和选择性审查的前提下部署。它的实用建议集中在项目契约、AGENTS.md 风格的说明、分层验证、由代理运行的测试环境，以及从评审和事故中收集反馈。

Claude Code v2.1.172 增加了一个更底层的控制点。嵌套子代理现在最多可以再生成五层子代理，每一层都有自己的提示词、模型选择和 200K token 上下文窗口。这有助于把日志搜索这类噪声工作隔离开。它也带来成本风险：文章提到每个分支每层有 7 倍 token 开销、某用户每分钟达到 887,000 token，以及 23 个子代理运行三天后出现的 47,000 美元账单。

#### Evidence
- [Designing Software for Software Factories](../Inbox/2026-06-13--designing-software-for-software-factories.md): Defines the software-factory loop, contracts, test tiers, feedback capture, and limits of autonomous feedback.
- [Claude Code v2.1.172: Sub-Agents Can Now Spawn Sub-Agents](../Inbox/2026-06-13--claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents.md): Summarizes nested sub-agent behavior, the five-level cap, context isolation, model routing, and cost examples.

### Local AI and data control
本地推理既是一种部署模式，也是一种隐私答案。Llama.cpp 把大语言模型推理封装进一个小型 C/C++ 运行时，可以加载 GGUF 模型文件，检测 CPU 和 GPU 能力，使用量化权重，并在桌面、移动端和加速器目标上运行。它强调的是实用的可移植性：小模型可以在 4 GB RAM 上运行，7B–13B 模型通常能放进 2–10 GB 的 GGUF 文件。

ScreenMind 把这种本地优先模式用在一个敏感界面上：连续屏幕记忆。它捕捉屏幕变化，用 Gemma 4 做视觉分析，把光学字符识别和语义、关键词搜索结合起来，并把结果保存在本地。代价是速度。它报告的模式每张截图大约需要 76、40 或 12 秒。Atlassian Rovo 的讨论展示了同一问题的另一面：Jira 和 Confluence 数据包含运营知识、近期计划和公司文档，所以默认训练贡献条款对小型组织来说会变成产品风险问题。

#### Evidence
- [Llama.cpp – Run LLM Inference in C/C++](../Inbox/2026-06-13--llama-cpp-run-llm-inference-in-c-c.md): Summarizes Llama.cpp’s local inference runtime, GGUF loading, quantization, hardware support, and memory claims.
- [Show HN: I run a vision model on every screenshot, locally, on a 4GB GPU](../Inbox/2026-06-13--show-hn-i-run-a-vision-model-on-every-screenshot-locally-on-a-4gb-gpu.md): Summarizes ScreenMind’s local screen-memory workflow, Gemma 4 analysis, search stack, and reported runtime modes.
- [Atlassian "Data Contribution"](../Inbox/2026-06-13--atlassian-data-contribution.md): Summarizes Atlassian data contribution concerns around Rovo, customer content, opt-out limits, and metadata scope.

### Rails performance and data invariants
Rails 相关内容重点是去掉隐藏的运行时工作，并把数据库规则写清楚。Roundhouse 把请求不变的 Rails 行为编译成更简单的生成 Ruby，然后在 JRuby 上运行。在报告的基准里，JRuby 上的原生 Rails 在 HTML index 端点上达到每秒 1,057 个请求，是 CRuby+YJIT 的 2.2 倍。生成后的应用在 HTML 上比 JRuby 版 Rails 快 25 倍，在 JSON 上快 43 倍，完整对比达到 54 倍。内存代价更高：报告里 JRuby 大约占用 1–1.5 GB RSS。

锁定文章给出了正确性方面的对应内容。Rails 的 `lock`、`lock!` 和 `with_lock` 取决于事务范围、隔离级别、适配器行为和查询形状。行锁可以解决单行丢失更新，不能强制执行跨多行或涉及不存在行的规则。建议从不变量出发，选择能约束它的最小数据库机制，例如唯一索引、`CHECK`、`SERIALIZABLE`、advisory lock 或有序加锁。

#### Evidence
- [The Ruby JRuby Was Built to Run](../Inbox/2026-06-13--the-ruby-jruby-was-built-to-run.md): Summarizes Roundhouse’s transpilation approach and benchmark results across CRuby+YJIT and JRuby.
- [Rails: The Sharp Parts. Lock Is Not a Mutex](../Inbox/2026-06-13--rails-the-sharp-parts-lock-is-not-a-mutex.md): Summarizes Rails locking pitfalls, invariant-first design, and database enforcement options.
