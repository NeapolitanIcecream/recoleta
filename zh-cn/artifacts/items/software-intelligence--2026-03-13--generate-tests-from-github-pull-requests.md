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
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# Generate tests from GitHub pull requests

## Summary
这项工作提出一种从 GitHub Pull Request 自动生成端到端测试的方法，目标是补上 AI 编码工具常遗漏的真实用户场景测试。它强调把代码变更、依赖关系和需求描述关联起来，为每个 PR 产出可追踪的测试与覆盖报告。

## Problem
- AI 编码工具虽然能快速生成代码，但通常只补充单元测试或集成测试，缺少高质量的端到端用户场景测试。
- 在作者观察的仓库中，启用 Copilot 类工具后，新增代码与高质量 e2e 测试的比例“显著下降”，导致关键逻辑路径和边界条件更容易漏测。
- 这很重要，因为 PR 阶段如果缺乏与需求绑定的自动化测试，缺陷会更晚暴露，且测试责任会被割裂给开发或测试团队单独承担。

## Approach
- 系统直接读取 Pull Request，分析变更文件和 diff，定位本次提交影响到的代码区域。
- 它利用单仓或多仓依赖图识别“未覆盖的逻辑路径”，也就是本次改动中哪些分支和流程还没有被测试到。
- 系统结合 PR 中的用户故事、需求说明或关联 Jira/TMS/CMS 信息，理解验收标准，再生成测试场景。
- 最终产出与 PR 绑定的自动化 e2e 测试及覆盖报告，并提供从代码引用到 requirement/test ID 的追踪关系。
- 作者提到内部使用 graphRAG 辅助上下文检索，但未展开技术细节。

## Results
- 文中**没有提供正式基准数据、数据集名称或可复现实验指标**，因此无法确认相对 baseline 的量化提升。
- 作者声称在“早期实验”中，系统**持续发现开发者遗漏的边界情况**，这是最强的实证性结论，但未给出发现率、准确率或覆盖率数字。
- 工作流上，系统可在“Push PR → 读取 diff + Jira ticket → 生成缺失测试和覆盖报告”这一流程中自动运行，说明其定位是 PR 级测试生成而非离线测试建议。
- 给出的示例展示了需求追踪粒度：如 `src/api/auth.js:45-78` 对应 `GITHUB-234 / JIRA-API-102`，并生成一个集成测试 `IT-01` 来验证“无效 token 返回 400”，状态为 Pass。

## Link
- [https://news.ycombinator.com/item?id=47371155](https://news.ycombinator.com/item?id=47371155)
