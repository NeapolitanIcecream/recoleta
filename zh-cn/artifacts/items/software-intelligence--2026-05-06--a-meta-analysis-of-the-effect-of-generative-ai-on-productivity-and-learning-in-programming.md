---
source: arxiv
url: https://arxiv.org/abs/2605.04779v1
published_at: '2026-05-06T11:32:25'
authors:
- Sebastian Maier
- "Moritz Gunzenh\xE4user"
- Jonas Schweisthal
- Manuel Schneider
- Stefan Feuerriegel
topics:
- code-intelligence
- ai-coding-assistants
- developer-productivity
- programming-education
- meta-analysis
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# A meta-analysis of the effect of generative AI on productivity and learning in programming

## Summary
## 摘要
这项元分析发现，GenAI 编码助手能在编程中带来中等幅度的生产力提升，但在企业和开源场景中的提升要小得多。研究还发现，除非学生可以在测评中使用 AI，否则编程学习没有可靠提升。

## 问题
- 关于 GenAI 编码助手的证据在实验室研究、开源项目、企业工作和教育场景中并不一致。
- 这个问题很重要，因为团队可能会高估短时受控任务中的生产力收益，而教育者可能会把 AI 辅助下的考试表现误认为是保留下来的编程技能。
- 论文衡量两个结果：通过任务用时、提交次数和代码行数衡量编程生产力；通过考试表现衡量学习。

## 方法
- 作者检索了 ACM、arXiv、Scopus 和 Web of Science 中 2019 年至 2025 年的研究。
- 他们筛选了 10,115 条记录，纳入了 23 项研究，共 27 个效应量。
- 他们在随机效应元分析下使用 Hedges' g，将 GenAI 辅助编程与无辅助编程进行比较。
- 他们使用 RoB2 和 ROBINS-I 评估偏倚。
- 他们针对研究场景、工具界面、编程语言、参与者类型、随机化、研究设计、测评访问权限和研究时长进行了调节变量分析。

## 结果
- 生产力：14 项研究产生了 16 个效应量，覆盖 3,535 名参与者和 6,355 个代码仓库。合并效应为正且显著：Hedges' g = 0.33，95% CI [0.09, 0.58]，SE = 0.13，p = 0.008。
- 生产力效应在研究之间差异很大：I² = 99%，τ² = 0.22，Q(15) = 206.06，p < 0.001。
- 研究场景解释了约 36% 的生产力异质性：实验室研究显示 g = 0.73，p < 0.001；企业研究显示 g = 0.19，p = 0.448；开源研究显示 g = 0.01，p = 0.975。
- 学习：10 项研究产生了 11 个效应量，包含 1,069 名参与者。合并学习效应较小且不显著：Hedges' g = 0.14，95% CI [-0.18, 0.47]，SE = 0.17，p = 0.389。
- 学习效应也存在差异：I² = 86%，τ² = 0.25，Q(10) = 54.96，p < 0.001。
- 测评访问权限影响了学习差异：测评期间允许使用 AI 时，g = 0.76，95% CI [0.24, 1.28]，p = 0.004；测评期间禁止使用 AI 时，g = -0.06，95% CI [-0.36, 0.24]，p = 0.674。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04779v1](https://arxiv.org/abs/2605.04779v1)
