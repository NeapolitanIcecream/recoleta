---
source: hn
url: https://github.com/unloopedmido/contextlevy
published_at: '2026-05-24T23:31:25'
authors:
- nonlooped
topics:
- code-intelligence
- ai-agent-tooling
- pull-request-analysis
- repository-context
- developer-workflow
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Built a small PR guardrail for token bloat, worth maintaining?

## Summary
## 摘要
ContextLevy 是一个 PR 保护措施，用来估算一项改动会把未来 AI 编码代理的上下文膨胀多少。它针对生成文件、日志、快照、锁文件变动和类似的仓库噪声，在这些内容变成长期代理开销之前就把它们拦住。

## 问题
- 当仓库里出现大量高噪声或低信号文件时，AI 编码代理会变慢、成本更高，也更难用。
- Pull request 可能会加入生成的客户端、覆盖率输出、构建产物、vendor 文件、日志、快照或代理指令转储，同时又不会破坏应用测试。
- 现有的 bundle-size 检查并不衡量 AI 辅助开发里的仓库上下文成本。

## 方法
- ContextLevy 扫描 GitHub pull request 的 diff，并根据改动文件估算上下文权重。
- 它会对高风险文件分类，包括生成输出、快照、日志、锁文件变动、vendor 文件和代理指令转储。
- 当配置的阈值被超过时，它会发出一条聚焦的 PR 评论。
- 它可以作为 GitHub Action 或 npm CLI 运行，并使用 workflow 里可用的 pull request 元数据和 diff patch。
- 它不依赖外部模型分析：没有 LLM 调用、没有代码上传、没有外部分析服务，也不需要遥测。

## 结果
- 摘要没有提供基准指标、准确率、延迟数据或前后成本下降数据。
- 它声称有 2 种交付方式：GitHub Action 和 npm CLI。
- 它声称有 4 项隐私和运行约束：没有 LLM 调用、没有代码上传、没有外部分析服务、也不需要遥测。
- GitHub Action 的设置使用 3 个列出的权限：contents: read、pull-requests: write 和 issues: write。
- 报告的输出包括 PR 评论、JSON CLI 输出、可配置的失败模式、阈值调节、忽略路径和 pre-push hook 用法。

## Problem

## Approach

## Results

## Link
- [https://github.com/unloopedmido/contextlevy](https://github.com/unloopedmido/contextlevy)
