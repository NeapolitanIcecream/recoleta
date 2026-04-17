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
这篇论文介绍了 Zup 的内部编码代理 CodeGen，并提出：生产环境中的成功更多取决于工具设计、安全控制、状态处理和信任校准，而不只是提示词调优或模型选择。
这是一篇基于真实部署经验的总结论文，给出了具体的架构和产品决策，以及若干尚未解决的研究问题。

## 问题
- 企业团队可以做出编码代理原型，但许多系统在生产环境中会失败，因为真实代码库、shell 访问、CI/CD 集成以及开发者信任会带来基准测试无法覆盖的风险。
- 常见失败模式包括文件重写出错或被截断、不安全的 shell 操作、基于过期上下文的编辑、会话不稳定，以及开发者信任不足。
- 这很重要，因为不可靠的代理会增加代码审查负担、引发安全事故，并浪费工程时间，最终让原型无法变成日常工具。

## 方法
- Zup 将 CodeGen 构建为三部分系统：开发者机器上的 CLI 执行器、FastAPI 后端，以及一个名为 Maestro 的中央编排引擎，后者运行 ReAct 风格的工具循环。
- 代理将推理交给 LLM，而编排器负责组装上下文、分发工具、设置停止条件、记录日志、处理重连和划定安全边界。
- 工具设计是方法中的核心部分：`read` 强制使用当前上下文，`edit` 使用有针对性的字符串替换，而不是重写整个文件，`shell` 在分层限制和审计日志下执行命令。
- 安全控制覆盖整个工具集合，而不是把每个工具彼此独立地处理，因为当能力重叠时，一个工具可能绕过另一个工具上的限制。
- 人类监督是渐进式的：用户可以先在审批模式下审核编辑和 shell 命令，使用规划模式查看拟议操作，随着信任增加再切换到自主模式。

## 结果
- 论文没有报告受控基准提升，也没有提供 pass@k、SWE-bench 或生产力变化等 A/B 测试指标。
- 论文声称，改进工具说明、参数模式和错误契约，比单纯做提示词工程带来了更可靠的行为，但没有给出数值比较。
- 论文报告了一个具体设计变更：用有针对性的字符串替换编辑取代整文件重写，减少了长文件中与截断和遗漏相关的失败，但没有提供发生率。
- 已部署系统包含一些明确的运行参数：使用 Redis 会话内存，TTL 为 24 小时；WebSocket 会话在不活动 20 分钟后断开；支持任务重连以恢复长时间运行的作业。
- 论文指出，开发者通常先从审批模式开始，之后再切换到自主模式，这种渐进式监督有助于采用，但没有提供采用数据。
- 论文最强的贡献是来自生产内部代理的实践证据，以及一份包含 13 个设计决策和 6 个开放问题的清单，而不是带有量化基准提升的新算法。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09805v1](http://arxiv.org/abs/2604.09805v1)
