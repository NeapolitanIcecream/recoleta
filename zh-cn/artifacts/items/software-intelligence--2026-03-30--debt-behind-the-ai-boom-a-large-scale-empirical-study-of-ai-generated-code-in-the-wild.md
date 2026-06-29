---
source: arxiv
url: http://arxiv.org/abs/2603.28592v1
published_at: '2026-03-30T15:38:05'
authors:
- Yue Liu
- Ratnadira Widyasari
- Yanjie Zhao
- Ivana Clairine Irsan
- David Lo
topics:
- ai-generated-code
- technical-debt
- code-quality
- static-analysis
- software-maintenance
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild

## Summary
## 总结
本文衡量了 AI 编程助手在真实 GitHub 仓库中引入的技术债务有多少，以及这些问题在代码进入生产后会保留多久。主要发现是，AI 作者提交经常引入静态分析问题，而且相当一部分问题后来仍留在仓库中。

## 问题
- 以往研究在受控实验中显示，AI 生成代码会有质量和安全问题，但没有说明这些代码合并到真实仓库后会发生什么。
- 团队需要知道，AI 引入的 bug、安全问题和可维护性问题会不会很快修复，还是会一直留在代码库里，变成技术债务。
- 这件事很重要，因为 AI 代码已经在生产开发中很常见，长期存在的低质量代码会增加未来的维护和审查成本。

## 方法
- 作者建立了一个大型数据集，包含 **304,362 个已验证的 AI 作者提交**，来自 **6,275 个 GitHub 仓库**，覆盖五个主流助手：GitHub Copilot、Claude、Cursor、Gemini 和 Devin。
- 他们用明确的 Git 元数据识别 AI 作者提交，例如 bot 账户、作者邮箱、作者名和 co-author trailer，而不是用分类器或间接代理。
- 对每个 AI 作者提交，他们在提交前后分别做静态分析，精确判断是哪一次变更引入或修复了问题。
- 分析使用了 Python 的 Pylint 和 Bandit，以及 JavaScript 和 TypeScript 的 ESLint 和 njsscan，并跟踪代码异味、运行时 bug 和安全问题。
- 然后，他们把每个新引入的问题一直追踪到仓库的最新版本，查看它是否仍然存在。

## 结果
- 研究在 **3,841 个仓库**和 **26,564 个提交**中找到了 **484,606 个不同的 AI 引入问题**。这意味着，**61.2%** 的研究仓库和 **8.7%** 的 AI 作者提交至少引入了一个问题。
- **代码异味**占比最高：**431,850 个问题（89.1%）**。其余是 **28,149 个运行时 bug（5.8%）** 和 **24,607 个安全问题（5.1%）**。
- 文中指出，**每个 AI 编程助手的提交中都有超过 15%** 会引入至少一个问题，不过摘录里没有给出各工具的具体百分比。
- 最常见的代码异味规则包括 **宽泛的异常处理（41,723；8.6%）**、**未使用的变量或参数（28,718；5.9%）** 和 **未使用的参数（24,444；5.0%）**。
- 最常见的运行时 bug 是 **未定义变量或引用：23,091 个问题（4.8%）**。常见的安全问题包括 **子进程未做 shell 检查：4,334 个（0.9%）** 和 **try-except-pass：4,040 个（0.8%）**。
- 在长期留存方面，**24.2%** 被追踪的 AI 引入问题一直存活到仓库的最新版本，这支持了论文的判断：AI 生成代码会在真实项目中带来长期维护成本。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28592v1](http://arxiv.org/abs/2603.28592v1)
