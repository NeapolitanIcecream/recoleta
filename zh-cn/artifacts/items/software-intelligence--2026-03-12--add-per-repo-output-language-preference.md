---
source: hn
url: https://news.ycombinator.com/item?id=47358750
published_at: '2026-03-12T23:32:35'
authors:
- nishiohiroshi
topics:
- code-review
- developer-tools
- localization
- human-ai-interaction
- repo-configuration
relevance_score: 0.67
run_id: materialize-outputs
language_code: zh-CN
---

# Add per-repo output language preference

## Summary
该内容介绍了 GitAuto 新增的按代码仓库设置输出语言偏好的功能，使非英语开发团队可以用母语阅读 AI 生成的代码评审评论与 GitHub 评论。它主要提升跨语言团队的人机协作体验，而不是提出新的模型或算法。

## Problem
- 非英语开发团队在审阅 AI 生成的 PR 时，若评论默认是英语，会增加理解成本并影响协作效率。
- 多仓库团队可能需要不同的语言配置，缺少按仓库粒度的语言偏好会降低可用性。
- 在全球化软件开发中，AI 工具若不能适配本地语言，会限制其在代码评审流程中的落地价值。

## Approach
- 在 GitAuto 中加入 **per-repo output language preference**，即按仓库配置输出语言。
- 代码评论和 GitHub 评论可根据仓库设置，自动以团队母语输出。
- 支持 **70+ languages**，说明其机制核心是把 AI 评审输出层做本地化适配，而不是改变 PR 主内容格式。
- PR 标题和正文仍保持英文，意味着系统采用“评论本地化、主协作对象标准化”的折中方案。

## Results
- 支持范围：可为仓库配置 **70+ 种语言** 的输出偏好。
- 直接能力声明：非英语团队现在可以用其母语阅读 **GitAuto code comments** 和 **GitHub comments**。
- 保持兼容性：**PR titles and bodies stay in English**，有助于维持跨团队或开源协作中的统一格式。
- 未提供定量实验结果：摘录中没有准确率、审阅效率、用户满意度、A/B 测试或与基线系统的数字对比。最强具体主张是其已上线按仓库语言配置功能，并覆盖 70+ 语言。

## Link
- [https://news.ycombinator.com/item?id=47358750](https://news.ycombinator.com/item?id=47358750)
