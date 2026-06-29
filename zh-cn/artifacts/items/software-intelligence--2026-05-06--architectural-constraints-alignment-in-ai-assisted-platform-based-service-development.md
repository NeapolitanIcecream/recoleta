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
当生成的代码必须满足公司特定的部署、CI/CD、安全和平台约束时，AI 辅助的服务脚手架经常失效。论文认为，在经批准的 Backstage 模板上做 RAG，再加一个简短的澄清对话，比开放式的 Copilot 式生成更容易产出可部署的服务起点。

## 问题
- 常见的 LLM 编码工具可以生成原型，但拿不到组织特有的架构规则、基础设施依赖和部署标准。
- 这很重要，因为生产服务必须适配现有的 CI/CD、安全策略、Kubernetes 配置和平台模板，否则开发者会把时间花在调试生成的基础设施代码上。
- 论文把这个问题和“vibe coding”做对比，也就是用户反复向 AI 编码工具提问，直到服务看起来能运行。

## 方法
- 系统接入经批准的 Backstage 服务模板，其中包含样板代码、配置、CI/CD 流水线和安全策略。
- 它用 `all-MiniLM-L6-v2` 对这些模板做向量化，并存入 Chroma 进行语义检索。
- 一个 GPT-4o-mini 的澄清循环会询问用户缺失的需求，比如服务用途、技术栈、数据库、API 风格和 CI/CD 需求。
- 如果用户无法回答某个技术问题，系统可以根据剩余上下文推断，而不是阻断检索。
- 系统会对最终用户需求做向量化，并与模板目录匹配；然后推荐最接近的预批准脚手架。

## 结果
- 在 RAG 模板选择测试中，系统 10 次都选中了正确的真实模板，成功率为 100%。
- 在 vibe coding 用户研究中，7 名参与者使用了由 GPT-5-mini 驱动的 Visual Studio Code 和 GitHub Copilot；只有 2/7 通过了全部部署质量门禁。
- vibe coding 的平均质量门禁通过率是 43%，RAG 系统是 100%。
- vibe coding 平均需要 22 次提示、941k 输入 token、12.1k 输出 token，每次运行约 0.26 美元；RAG 系统中位数只需 3 次提示、3.2k 输入 token、0.26k 输出 token，每次运行约 0.001 美元。
- 所有 vibe coding 参与者都接近 45 分钟的上限，而 RAG 交互不到 5 分钟。
- 这项研究规模很小：只有 7 名学术参与者、1 个 vibe coding 任务，而且除了部署检查和 pod 日志外，没有做完整的功能测试。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04973v1](https://arxiv.org/abs/2605.04973v1)
