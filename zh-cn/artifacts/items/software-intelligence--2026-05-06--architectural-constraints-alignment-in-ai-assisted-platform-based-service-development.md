---
source: arxiv
url: https://arxiv.org/abs/2605.04973v1
published_at: '2026-05-06T14:28:28'
authors:
- Julius Irion
- Moritz Leugers
- Paul Hartwig
- Simon Kling
- Tachmyrat Annayev
- Alexander Schwind
- Maria C. Borges
- Sebastian Werner
topics:
- ai-assisted-development
- service-scaffolding
- rag
- platform-engineering
- backstage
- software-architecture
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Architectural Constraints Alignment in AI-assisted, Platform-based Service Development

## Summary
## 摘要
AI 辅助的服务脚手架在生成代码必须满足公司特定的部署、CI/CD、安全和平台约束时，常常无法通过。论文声称，在已批准的 Backstage 模板上使用 RAG，再加上一段简短的澄清式对话，比开放式的 Copilot 风格生成更能产出可部署的服务起点。

## 问题
- 通用 LLM 编码工具可以生成原型，但无法访问组织特定的架构规则、基础设施依赖和部署标准。
- 这会带来问题，因为生产服务必须符合现有 CI/CD、安全策略、Kubernetes 设置和平台模板，否则开发者需要花时间调试生成的基础设施代码。
- 论文将这个问题与“vibe coding”作比较。在这种方式中，用户反复提示 AI 编码工具，直到服务看起来可以工作。

## 方法
- 系统摄取已批准的 Backstage 服务模板，其中包括样板代码、配置、CI/CD 流水线和安全策略。
- 它使用 `all-MiniLM-L6-v2` 对这些模板进行嵌入，并将其存储在 Chroma 中用于语义搜索。
- GPT-4o-mini 澄清循环会向用户询问缺失需求，例如服务目的、技术栈、数据库、API 风格和 CI/CD 需求。
- 如果用户无法回答技术问题，系统可以根据其余上下文进行推断，而不是阻塞检索。
- 最终用户需求会被嵌入，并与模板目录匹配；系统推荐最接近的预批准脚手架。

## 结果
- 在 RAG 模板选择测试中，系统在 10/10 次运行中选择了正确的标准答案模板，成功率为 100%。
- 在 vibe-coding 用户研究中，7 名参与者使用由 GPT-5-mini 驱动的 GitHub Copilot 和 Visual Studio Code；只有 2/7 通过了所有部署质量门禁。
- vibe coding 的平均质量门禁成功率为 43%，RAG 系统为 100%。
- vibe coding 平均需要 22 条提示、941k 输入 token、12.1k 输出 token，每次运行约 $0.26；RAG 系统使用的中位数为 3 条提示、3.2k 输入 token、0.26k 输出 token，每次运行约 $0.001。
- 所有 vibe-coding 参与者都接近 45 分钟上限，而 RAG 交互用时不到 5 分钟。
- 这项研究规模较小：7 名学术参与者、1 个 vibe-coding 任务，并且除部署检查和 pod 日志外，没有完整的功能测试。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04973v1](https://arxiv.org/abs/2605.04973v1)
