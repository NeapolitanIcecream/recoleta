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
## 摘要
这篇论文衡量了 AI 编码助手在其代码进入生产环境后，会给真实的 GitHub 仓库增加多少技术债。主要发现是，AI 编写的提交经常引入静态分析问题，而且其中相当一部分问题在之后的仓库版本中仍然存在。

## 问题
- 先前研究已经在受控实验中发现 AI 生成代码存在质量和安全问题，但没有说明这些代码合并进真实仓库后会发生什么。
- 团队需要知道，AI 引入的 bug、安全问题和可维护性问题，究竟会很快被修复，还是会作为技术债留在代码库中。
- 这很重要，因为 AI 代码已经广泛用于生产开发，而持续存在的低质量代码会提高未来的维护和评审成本。

## 方法
- 作者构建了一个大规模数据集，包含 **304,362 个经过验证的 AI 编写提交**，来自 **6,275 个 GitHub 仓库**，覆盖五个主要助手：GitHub Copilot、Claude、Cursor、Gemini 和 Devin。
- 他们使用明确的 Git 元数据来识别 AI 编写的提交，例如 bot 账户、作者邮箱、作者姓名和 co-author trailer，而不是使用分类器或间接代理指标。
- 对于每个 AI 编写的提交，他们都会在提交 **前后** 对代码运行静态分析，以归因该次变更具体引入或修复了哪些问题。
- 分析工具包括 Python 的 Pylint 和 Bandit，以及 JavaScript 和 TypeScript 的 ESLint 和 njsscan，并跟踪代码异味、运行时 bug 和安全问题。
- 然后他们把每个新引入的问题一直追踪到仓库的最新版本，以查看这些问题是否仍然存在。

## 结果
- 研究在 **3,841 个仓库** 和 **26,564 个提交** 中发现了 **484,606 个不同的 AI 引入问题**。这意味着，纳入研究的仓库中有 **61.2%** 至少出现过一个被引入的问题，而 AI 编写提交中有 **8.7%** 至少引入了一个问题。
- **代码异味占绝大多数**：**431,850 个问题（89.1%）**。其余包括 **28,149 个运行时 bug（5.8%）** 和 **24,607 个安全问题（5.1%）**。
- 论文指出，**每个 AI 编码助手都有超过 15% 的提交** 会引入至少一个问题，不过这段摘录没有给出各工具的具体比例。
- 最常见的代码异味规则包括 **过宽的异常处理（41,723；8.6%）**、**未使用的变量或参数（28,718；5.9%）**，以及 **unused argument（24,444；5.0%）**。
- 最常见的运行时 bug 是 **未定义变量或引用：23,091 个问题（4.8%）**。常见的安全问题包括 **subprocess without shell check：4,334（0.9%）** 和 **try-except-pass：4,040（0.8%）**。
- 在长期留存方面，**被追踪的 AI 引入问题中有 24.2% 一直保留到仓库最新版本**，这支持了论文的结论：AI 生成代码会在真实项目中带来持续的维护成本。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28592v1](http://arxiv.org/abs/2603.28592v1)
