---
source: arxiv
url: https://arxiv.org/abs/2607.05677v1
published_at: '2026-07-06T22:44:45'
authors:
- Zihan Fang
- Yueke Zhang
- Ningzhi Tang
- Collin McMillan
- Toby Jia-Jun Li
- Yu Huang
topics:
- ai-coding-agents
- open-source-software
- code-intelligence
- human-ai-interaction
- repository-mining
- software-engineering-agents
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# From Conversation to Contribution: Characterizing Coding Agent in Open-Source Software

## Summary
## 摘要
这篇论文研究 AI 编码代理的聊天日志如何关联后续开源开发活动。作者将 13,360 个聊天会话与 GitHub 历史记录和开发者调查相连接，并报告了采用模式、代码库变化和可维护性担忧。

## 问题
- AI 编码助手现在支持多轮代码编辑、终端使用和感知项目的修改，但多数 OSS 研究只衡量提交、拉取请求或静态信号。
- OSS 维护者需要了解基于聊天的 AI 使用如何影响贡献流程、评审负担、代码维护和信任。
- 缺失的环节是从开发者与 AI 的对话到后续代码库活动的路径。

## 方法
- 作者使用 SpecStory 聊天日志，收集了来自 1,356 个 GitHub 代码库的 13,360 个 AI 聊天会话，包含 79,172 条用户消息，涉及 Cursor、GitHub Copilot 和 Claude Code 等工具。
- 过滤掉不可访问和过于简单的代码库后，他们分析了 1,240 个代码库、12,108 个保留的 AI 聊天会话、657,971 次提交、9,510 个拉取请求、12,747 个 issue，以及 120,489 条 CI/检查记录。
- 他们将聊天目的分为七个标签，包括 Code Writing、Failure Reporting、Inquiry、Validation 和 Workflow Control；GPT-5 分类器在人类标注集上的 macro-F1 为 0.83。
- 他们以每个代码库首次观察到的 AI 聊天为中心对齐，使用前后对比、中断时间序列模型、Wilcoxon 检验、回归，以及 HHI 等集中度指标。
- 他们调查了与这些代码库相关的开发者：589 份送达的邀请获得 25 份回复，回复率为 4.2%。

## 结果
- 较小、不太成熟、协作程度较低的代码库中 AI 使用更重。最终数据集覆盖 1,240 个代码库，创建时间为 2013 年 4 月至 2026 年 3 月，常见主要语言为 TypeScript 25.8%、Python 22.8% 和 JavaScript 12.9%。
- Code Writing 是主要聊天目的：它占会话的 34.7%，并且在 53.9% 的代码库中是占主导的目的。
- 采用 AI 后，项目往往有更多活跃贡献者，贡献者集中度更低，报告的显著性为 p < .001；沟通仍集中在较少参与者之间。
- 论文基于 bug/fix 活动、触及测试的提交、CI 结果、issue 和拉取请求，报告采用后可观察的代码质量信号或拉取请求合并率没有出现普遍恶化。
- 开发者认为其他人的 AI 生成代码比自己的 AI 生成代码更难维护，p = .029，并认为 AI 让 OSS 贡献更容易。
- 多数受访开发者，即 68%，愿意分享聊天历史；他们的担忧包括显得能力不足、增加评审者负担，以及向竞争者暴露想法。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.05677v1](https://arxiv.org/abs/2607.05677v1)
