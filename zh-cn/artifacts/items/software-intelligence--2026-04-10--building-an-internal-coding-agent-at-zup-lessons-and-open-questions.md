---
source: arxiv
url: http://arxiv.org/abs/2604.09805v1
published_at: '2026-04-10T18:28:59'
authors:
- Gustavo Pinto
- Pedro Eduardo de Paula Naves
- Ana Paula Camargo
- Marselle Silva
topics:
- coding-agents
- enterprise-ai
- tool-design
- agent-safety
- human-oversight
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Building an Internal Coding Agent at Zup: Lessons and Open Questions

## Summary
## 摘要
本文介绍了 Zup 的内部编码代理 CodeGen，并指出，生产环境成功更多取决于工具设计、安全控制、状态处理和信任校准，而不只是提示词调优或模型选择。
这是一篇基于真实部署的经验总结论文，包含具体的架构和产品决策，以及开放的研究问题。

## 问题
- 企业团队可以搭建编码代理原型，但很多原型在生产中失败，因为真实代码库、shell 访问、CI/CD 集成和开发者信任带来的风险，超出了基准测试的覆盖范围。
- 常见失败模式包括文件重写被截断或损坏、危险的 shell 操作、上下文过时导致的编辑、会话不可靠，以及开发者信任不足。
- 这很重要，因为不可靠的代理会增加评审负担、带来安全事件，并浪费工程时间，原型也就无法变成日常工具。

## 方法
- Zup 将 CodeGen 做成三部分系统：开发者机器上的 CLI 执行器、FastAPI 后端，以及名为 Maestro 的中央编排引擎，后者运行 ReAct 风格的工具循环。
- 代理把推理交给 LLM，而编排器负责上下文组装、工具分发、停止条件、日志记录、重连和安全边界。
- 工具设计是方法中的核心部分：`read` 强制使用当前上下文，`edit` 采用有针对性的字符串替换，而不是整文件重写，`shell` 则在分层限制和审计日志下运行命令。
- 安全控制覆盖整个工具集，而不是把每个工具单独隔离，因为一个工具可以绕过另一个工具的限制，只要它们的能力有重叠。
- 人工监督是渐进式的：用户可以先在编辑和 shell 命令的审批模式下使用，再用计划模式查看拟执行动作，随着信任增加切换到自主模式。

## 结果
- 论文没有报告受控基准提升，也没有给出 A/B 测试指标，比如 pass@k、SWE-bench 或生产效率变化。
- 论文称，改进工具描述、参数模式和错误契约，比单纯做提示词工程更能带来可靠行为，但没有给出数值对比。
- 论文报告了一个具体设计变化：用有针对性的字符串替换编辑取代整文件重写，减少了长文件中因截断和遗漏导致的失败，但没有提供失败率。
- 已部署系统包含具体运行参数：Redis 会话内存的 TTL 为 24 小时，WebSocket 会话在 20 分钟无活动后断开，任务重连可恢复长时间运行的作业。
- 论文指出，开发者通常先进入审批模式，之后切换到自主模式，这种渐进式监督模型帮助了采用，但没有提供采用数据。
- 它最强的贡献是来自生产级内部代理的实践证据，以及 13 项设计决策和 6 个开放问题的清单，而不是一个带有量化基准提升的新算法。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09805v1](http://arxiv.org/abs/2604.09805v1)
