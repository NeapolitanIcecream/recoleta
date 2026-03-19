---
source: arxiv
url: http://arxiv.org/abs/2603.04245v1
published_at: '2026-03-04T16:33:35'
authors:
- Jialiang Wei
- Ali Ebrahimi Pourasad
- Walid Maalej
topics:
- ui-feedback
- genai-for-software-engineering
- image-editing
- mobile-ui
- human-ai-collaboration
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# LikeThis! Empowering App Users to Submit UI Improvement Suggestions Instead of Complaints

## Summary
本文提出 **LikeThis!**，把用户对移动应用 UI 的模糊抱怨转成带有可视化改进方案的可执行反馈。核心思想是让 AI 基于“用户评论+截图”生成多个 UI 改进备选，供用户直接选择后提交给开发者。

## Problem
- 现有应用商店反馈常常**含糊、情绪化或缺乏可操作性**，开发者难以理解并据此改进 UI。
- 纯文本很难准确表达 UI 问题；而专业设计工具又**不适合普通用户**快速制作界面改进草图。
- 这很重要，因为低质量反馈会降低用户与开发者之间的沟通效率，拖慢产品迭代和 UI 改进。

## Approach
- 提出一个两阶段 GenAI 流程：先做 **Suggestion Generation**，再做 **UI Editing**。
- 第一步用多模态大模型读取**用户文本反馈+应用截图**，生成多个文字化“解决方案规格”（如增大字体、提升对比度）。
- 第二步把这些规格连同原始截图输入图像编辑模型，生成多个**修改后的 UI 备选图**；用户从中选择最符合自己意图的一项提交。
- 系统还支持可选**mask 标注问题区域**，以便将修改约束在局部区域。
- 论文还实现了一个 **iOS 原型**，支持截图、问题描述、区域标记、查看候选方案、迭代修改与最终提交。

## Results
- 在基于 **UICrit** 数据集的模型基准测试中，作者从 **300** 个 critique/screen 构建评测，其中 **120** 张用于模型对比、**60** 张用于 masking、**120** 张用于消融；两位标注者在 **120** 个任务上的一致率为 **80.42%**。
- 在 **120** 个任务、共 **240** 次标注中，**GPT-Image-1** 明显优于 Flux、Gemini、Bagel：用户偏好第一名次数 **214**，而其他模型仅 **14 / 8 / 4**。
- 问题解决度（Issue Resolution）上，**GPT-Image-1 平均 2.74/3**，高于 **Flux 1.60**、**Gemini 1.83**、**Bagel 1.38**；其“完全修复”频次为 **200**，而其他模型分别为 **58 / 73 / 32**。文中称这些差异在统计上显著（**Wilcoxon-Mann-Whitney, p ≤ 0.05**）。
- 保真度（Fidelity）上，各模型都较高，但 **GPT-Image-1 2.83** 仍具竞争力；鲁棒性（不引入新问题）上 **GPT-Image-1 2.88**，高于 **Flux 2.62**、**Gemini 2.23**、**Bagel 2.02**。
- 论文总结称，除 GPT-Image-1 外，其余模型只能在约 **25%–53%** 的界面上至少部分解决问题。
- 用户研究覆盖 **10** 个生产应用、**15** 名用户；参与者认为 **85.5%** 的生成建议“多数准确或非常准确”。开发者评估表明，带生成改进图的反馈比纯反馈**更易理解、也更可执行**。

## Link
- [http://arxiv.org/abs/2603.04245v1](http://arxiv.org/abs/2603.04245v1)
