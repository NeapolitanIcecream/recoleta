---
source: arxiv
url: https://arxiv.org/abs/2607.07480v1
published_at: '2026-07-08T14:43:08'
authors:
- Erfan Entezami
- Madeline Endres
topics:
- ai-code-generation
- personalization-bias
- software-fairness
- human-ai-interaction
- web-development
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Biased or Personalized? The Impact of Personal Information on AI-driven Development

## Summary
## 摘要
AI 编码助手可以根据推断出的开发者年龄和性别改变生成的网站，即使任务提示的其他内容相同。论文通过受控生成实验和一个关于 ChatGPT 个性化的小型用户研究，在 Web 开发场景中展示了这一点。

## 问题
- 研究关注的是，关于开发者的个人信息是否会让生成的软件超出明示需求发生变化。
- 这个问题很重要，因为 AI 编码工具可能以用户不易察觉的方式个性化输出，包括 UI 选择、占位内容和代码组织。
- 如果这些变化符合年龄或性别刻板印象，生成的软件可能把偏见带入非专业用户制作的应用中。

## 方法
- 作者使用 ChatGPT-4.1 和 DeepSeek-V3.2 生成了 800 个网站，任务包括个人网站和在线商店。
- 他们创建了 20 个 persona，覆盖年轻女性、年长女性、年轻男性和年长男性。每个提示只改变 persona 的姓名和年龄。
- 他们测量了三个制品领域：界面设计、模板内容和代码结构。
- 对于分类结果，他们使用 chi-square、Fisher-Freeman-Halton 或 z 检验；对于连续代码指标，他们使用 Mann-Whitney U 检验，并采用 Benjamini-Hochberg 校正。
- 他们还进行了一个 20 人观察研究，参与者使用自己的 ChatGPT 账户构建个人网站，随后讨论个性化和偏见。

## 结果
- 在 120 个经过人工审查的个人网站中，每个网站都有 Hobbies 和 Skills 部分，但 Photo Gallery 只出现在 10/120 个案例中，且全部面向年长 persona；对 DeepSeek 来说，这一年龄效应为 z=3.25，p=0.003。
- Contact 部分出现了 58/120 次。年长 persona 获得了 37/58 个 Contact 部分，年轻 persona 为 21/58：z=2.92，p=0.004。在年轻 persona 中，年轻男性获得了 15 个 Contact 部分，年轻女性获得了 6 个：z=2.78，p=0.005。
- 颜色选择因 persona 群体而异。在 GPT-4.1 中，31 个深蓝色个人网站中有 24 个面向男性；在 DeepSeek 中，35 个深蓝色个人网站中有 29 个面向男性。在审查样本中，粉色和紫色只出现在面向女性的网站中。
- 颜色与 persona 的关联达到 p<0.05，报告的 Cramer's V 值为 0.36-0.53；示例包括 GPT-4.1 的深蓝色，p<0.001，V=0.535，以及 DeepSeek 的绿色，p<0.001，V=0.434。
- 对于在线商店，摘录报告称，为女性生成的网站包含更少文件和更少 JavaScript，p=0.007。
- 在 20 名参与者的研究中，参与者主要把个性化视为内容选择，而受控研究还发现了 UI 和代码结构中的人口统计学效应。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.07480v1](https://arxiv.org/abs/2607.07480v1)
