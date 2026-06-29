---
source: hn
url: https://stephen.bochinski.dev/blog/2026/05/24/whats-left-for-ai-assisted-coding/
published_at: '2026-05-24T22:28:29'
authors:
- sbochins
topics:
- ai-assisted-coding
- code-intelligence
- software-agents
- developer-tools
- human-ai-interaction
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# What's Left for AI-Assisted Coding

## Summary
## 总结
文章认为，AI 辅助编码受制于缺少共享记忆和安全的自主测试权限，这个问题在大型团队里尤其明显。原因在于，代理可以完成清晰任务的代码编写，但更大的项目还需要稳定的决策和对变更有效性的证明。

## 问题
- 代理会在会话之间丢失需求、既有决策和团队上下文，所以开发者要花时间反复说明信息。
- 上下文缺失会让代理做出错误假设，这些问题往往要到项目后期才暴露。
- 代理无法安全地独立验证许多变更，因为类似生产环境的测试需要跨部署、测试和权限系统的访问。

## 方法
- 为单个开发者添加持久记忆，让代理在不同会话之间保留需求和偏好。
- 添加团队共享记忆，让项目决策、约束和已知需求都能被代理获取。
- 在验证需要时，给代理受控权限去部署、测试，并进入类似生产环境。
- 通过最小权限控制和升级路径来处理访问问题，因为大型公司有很多访问系统和部署流程。

## 结果
- 文中没有提供定量结果、数据集、指标或基线对比。
- 文章指出，大规模 AI 辅助编码还缺少 2 项能力：共享记忆和自主端到端测试。
- 文章称，代理在拿到足够上下文时，已经能较好地完成清晰任务，但没有给出衡量过的成功率。
- 文章称，如果同时解决这两个缺口，工程师就会更接近只写规格说明，而让代理处理后续编码和验证。

## Problem

## Approach

## Results

## Link
- [https://stephen.bochinski.dev/blog/2026/05/24/whats-left-for-ai-assisted-coding/](https://stephen.bochinski.dev/blog/2026/05/24/whats-left-for-ai-assisted-coding/)
