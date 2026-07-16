---
kind: ideas
granularity: day
period_start: '2026-06-09T00:00:00'
period_end: '2026-06-10T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software engineering
- multi-agent systems
- code security
- benchmarks
- test oracles
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/multi-agent-systems
- topic/code-security
- topic/benchmarks
- topic/test-oracles
language_code: zh-CN
---

# Repository-scale code assistant safeguards

## 摘要
代码代理评估正在转向可执行的仓库级工作、基于源代码的测试生成，以及对送入模型的上下文做安全检查。实际工作是加入跨文件和依赖关系的验收测试，基于实现证据生成 API 断言，并在评论、文档、示例和附近代码进入代码生成提示前先筛查它们。

## Repository-scale acceptance suite for coding-agent pilots
购买或部署代码代理的团队，应把完整仓库构建作为测试对象，而不只是修复单个 issue 或处理单文件任务。可行的套件可以先选 10 到 20 个内部服务或库，它们已经有稳定的 Docker 构建、有效的单元测试和清晰文档。代理拿到的是能力级文档，必须从零创建仓库结构、API、依赖关系和组件间行为。评分时，代理开始前应清除源代码、测试、包缓存、构建产物和 Git 历史，然后只用可执行检查评分。

DeNovoSWE 给出了这类设置的模板。它挑选 Docker 环境稳定、原始测试通过率高、测试覆盖率达标的仓库，再把测试和跟踪到的函数映射到文档里的能力。这个数据集有 4,818 个文档到仓库实例，用它微调 Qwen3-30B-A3B 后，BeyondSWE-Doc2Repo 的表现从 5.8% 提升到 47.2%。EsoLang-Bench 还适合做内部 DSL 和专有工具的压力测试：给代理一个持久工作区、本地执行和隐藏提交，然后看它能否在一次会话里学会不熟悉的可执行接口。

### 资料来源
- [DeNovoSWE: Scaling Long-Horizon Environments for Generating Entire Repositories from Scratch](../Inbox/2026-06-09--denovoswe-scaling-long-horizon-environments-for-generating-entire-repositories-from-scratch.md): DeNovoSWE describes whole-repository generation tasks, sandbox cleanup, Docker environments, executable checks, and the 5.8% to 47.2% fine-tuning result.
- [Frontier Coding Agents Use Metaprogramming to Adapt to Unfamiliar Programming Languages](../Inbox/2026-06-09--frontier-coding-agents-use-metaprogramming-to-adapt-to-unfamiliar-programming-languages.md): EsoLang-Bench shows how persistent workspaces, local interpreters, and hidden tests expose adaptation ability in unfamiliar executable interfaces.

## Prompt-context security gate for code generation
代码助手部署需要先扫描送入生成环节的上下文：注释、文档字符串、README 摘要、附近示例、变量名和参考片段。门禁应在生成前运行，标记不安全指令、易受攻击的示例、像 prototype shortcut 这样的可疑语义提示，以及靠近目标函数的高风险上下文。生成后还应对产物运行静态分析、污点检查和差分检查。

最便宜、也最有效的验证，是用团队自己的文档和示例做一套红队集。可以在安全任务里植入针对 SQL 注入、XSS、硬编码凭据、路径遍历和不安全加密的对抗性注释或示例，再看助手是否生成脆弱代码，以及门禁是否拦住提示或输出。在这项对抗性上下文研究中，脆弱代码生成率在 2,800 次试验里从 3.5% 上升到 37.4%，而放在目标函数前 10 到 50 个 token 的上下文，攻击成功率达到 62.1%。论文里的组合检测器在留出集上报告 89.1% 检出率和 0.3% 误报率。

### 资料来源
- [Context-Based Adversarial Attacks on AI Code Generators: Vulnerability Analysis and Implications](../Inbox/2026-06-09--context-based-adversarial-attacks-on-ai-code-generators-vulnerability-analysis-and-implications.md): The study reports attacks through comments, documentation, variable names, and examples, with vulnerability rates, nearby-context effects, and detector results.
- [Context-Based Adversarial Attacks on AI Code Generators: Vulnerability Analysis and Implications](../Inbox/2026-06-09--context-based-adversarial-attacks-on-ai-code-generators-vulnerability-analysis-and-implications.md): The abstract states the 2,800-experiment setup and the rise in vulnerability generation under adversarial context.

## Source-grounded semantic oracles for REST API tests
API 团队如果覆盖了很多端点，可以加一个代理步骤，让它读取实现源代码，并为 OpenAPI 规范可能漏掉的行为起草可执行断言。这个流程很适合先做小规模试点：对每个端点，收集传递性的导入闭包，提取输入约束、响应字段、异常路径、副作用和端点关系，然后生成状态、字段和跨操作一致性 oracle。每条断言进入 CI 前，都应由审阅代理或人工测试者检查其背后的源代码证据。

MASTOR 说明了为什么这值得在 REST 服务上测试。它瞄准的是状态码检查、崩溃检查和 schema 检查漏掉的失败，包括业务逻辑错误和状态相关不一致。在 13 个开源 RESTful API 项目上，它覆盖 296 个操作和 251,303 行代码，生成了 10,022 个 oracle，平均 mutation score 达到 75.4%。在 50 个操作的对比中，使用状态和字段 oracle 时，它得分 69.9%，高于 Direct Prompting 的 39.8% 和 SATORI 的 20.5%。

### 资料来源
- [MASTOR: A Multi-Agent Approach to Semantic Test Oracle Generation for RESTful APIs](../Inbox/2026-06-09--mastor-a-multi-agent-approach-to-semantic-test-oracle-generation-for-restful-apis.md): MASTOR details source analysis, oracle generation, reviewer checks, benchmark size, mutation scores, and baseline comparisons.
- [MASTOR: A Multi-Agent Approach to Semantic Test Oracle Generation for RESTful APIs](../Inbox/2026-06-09--mastor-a-multi-agent-approach-to-semantic-test-oracle-generation-for-restful-apis.md): The abstract explains the problem with simple REST API checks and the source-based multi-agent oracle-generation workflow.
