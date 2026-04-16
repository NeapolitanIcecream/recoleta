---
source: hn
url: https://github.com/tonone-ai/tonone
published_at: '2026-04-06T23:25:26'
authors:
- thisisfatih
topics:
- multi-agent-software-engineering
- code-intelligence
- automated-software-production
- developer-tooling
- agent-orchestration
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Inspired by gstack: I stopped prompting Claude and gave it job titles instead

## Summary
## 摘要
Tonone 是一个开源插件和 agent 包，能把一次编码会话变成一组按角色分工的 AI 专家，覆盖工程、产品、设计、研究、安全和运维。它的核心主张是：相比每个人各用一个通用助手、再手动传递输出，这种方式更适合完成端到端的工作流。

## 问题
- 团队常常为不同角色分别使用不同的 AI 助手，然后再由人工在不同人员和工具之间传递输出。该项目认为，这会在每次交接时丢失上下文。
- 单个通用助手无法在产品规划、编码、基础设施、安全、测试和部署之间维持稳定的领域分工。
- 这对软件生产有影响，因为规划、实现、评审和发布通常涉及多个专业领域，而上下文割裂会拖慢进度，或降低输出质量。

## 方法
- Tonone 定义了 23 个具名专家，每个都对应一个领域，例如后端、基础设施、安全、可观测性、产品、研究、UX、分析、测试或营销。
- 它使用 Apex（工程）和 Helm（产品）等 lead agents，把工作分配给合适的专家，并将他们的输出合并到同一个工作流中。
- 该系统既以 Claude Code 插件命令的形式提供，也以基于 markdown 的 agent 和 skill 文件形式提供给 Codex CLI。Skills 存放在 `skills/<name>/SKILL.md` 中，读取这些工作流文档后即可调用 agents。
- 这个包支持对现有代码库进行并行侦察。在 `/apex-takeover` 流程中，agents 会检查架构、基础设施、CI/CD、安全、可观测性、后端、数据库和前端，然后生成系统地图、风险评估、quick wins 和路线图。
- 工程任务按 S/M/L 三个执行级别划分，并附带 token 和成本估算。一个例子给出：小型认证任务约 30K tokens、约 $0.05；中等版本约 120K tokens、约 $0.20；更大范围的构建约 250K tokens、约 $0.45。

## 结果
- 摘录中没有提供基准研究、受控评估，也没有给出与其他 agent 系统或 prompt 基线相比的质量指标。
- 明确的规模说法是：23 个专家和 125 项技能，覆盖工程、产品、设计、研究、分析、营销、移动端、固件、ML、基础设施和安全。
- 项目声称在 Claude Code 中只需 2 条安装命令即可完成设置：`claude plugin marketplace add tonone-ai/tonone` 和 `claude plugin install tonone@tonone-ai`。
- 主要的定量示例是“Build user authentication for our SaaS”这一任务的分级：S 使用 Spine + Warden，约 30K tokens、约 $0.05；M 使用 Spine + Warden + Flux + Relay，约 120K tokens、约 $0.20；L 再加入 Vigil + Atlas，约 250K tokens、约 $0.45。
- 它声称可以由多个专家并行完成 takeover 分析，并输出包含系统地图、风险评估、quick wins 和路线图的最终报告，但摘录没有提供准确率、速度或用户研究数据。
- 该包采用 MIT 许可证，并被描述为可通过 Claude Code v1.0+ 和 Codex CLI 使用，工具会直接读取 agent 和 skill 的 markdown 文件。

## Problem

## Approach

## Results

## Link
- [https://github.com/tonone-ai/tonone](https://github.com/tonone-ai/tonone)
