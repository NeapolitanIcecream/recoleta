---
source: hn
url: https://news.ycombinator.com/item?id=47371155
published_at: '2026-03-13T23:01:31'
authors:
- Aamir21
topics:
- test-generation
- pull-request-analysis
- e2e-testing
- traceability
- graph-based-reasoning
relevance_score: 0.01
run_id: materialize-outputs
---

# Generate tests from GitHub pull requests

## Summary
这篇内容提出一个面向 GitHub Pull Request 的自动测试生成系统，目标是在 AI 辅助编码时代补上经常缺失的高质量端到端测试。它通过读取代码变更、依赖关系和需求上下文，自动生成与 PR 绑定的测试场景与覆盖报告。

## Problem
- AI 编码工具虽然能快速生成代码，但通常缺少完整的端到端测试覆盖，尤其是真实用户场景测试。
- 在作者观察的多个代码仓库中，团队开始使用 Copilot 类工具后，新代码增长与高质量 e2e 测试数量之间的比例明显恶化。
- 测试常被拆成开发后的独立工作，导致 PR 阶段遗漏边界条件、逻辑路径和需求可追踪性，这会影响软件质量与交付可靠性。

## Approach
- 系统直接读取 Pull Request，分析变更文件与代码 diff，定位需要补测的区域。
- 利用单仓或多仓依赖图识别未覆盖的逻辑路径，从而找出开发者可能漏掉的测试点。
- 结合 PR 评论中的 user story、requirements，以及可选接入的 Jira/CMS/TMS 信息，理解需求上下文与验收标准。
- 基于上述信息自动生成测试场景、产出 e2e 自动化测试，并给出与 PR 关联的覆盖报告与需求追踪表。
- 作者提到内部使用 graphRAG 辅助上下文获取，但未展开方法细节。

## Results
- 文中没有提供正式基准测试、数据集或可复现实验数字，因此无法给出定量性能提升。
- 作者声称在早期实验中，系统**持续**发现开发者遗漏的边界情况，但未说明命中率、覆盖率提升或缺陷发现率。
- 给出的示例展示了从代码位置到 Requirement ID、验收标准、测试类型、测试 ID、测试描述和状态的完整追踪链路，例如 `src/api/auth.js:45-78` 对应 `GITHUB-234 / JIRA-API-102`，生成了一个无效 token 返回 `400` 的集成测试用例。
- 核心具体产出是：PR 触发后，系统读取 diff + Jira ticket，生成缺失测试与 coverage report，并把测试和需求做显式绑定。

## Link
- [https://news.ycombinator.com/item?id=47371155](https://news.ycombinator.com/item?id=47371155)
