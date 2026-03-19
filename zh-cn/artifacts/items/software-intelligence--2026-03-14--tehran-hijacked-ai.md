---
source: hn
url: https://www.dailymail.co.uk/debate/article-15640991/ChatGPT-Islamic-terrorist-propaganda.html
published_at: '2026-03-14T23:24:41'
authors:
- nailer
topics:
- llm-safety
- disinformation
- wikipedia-manipulation
- knowledge-sources
- propaganda
relevance_score: 0.48
run_id: materialize-outputs
language_code: zh-CN
---

# Tehran Hijacked AI

## Summary
这篇文章声称，恐怖组织与伊朗等政权正在通过操纵 Wikipedia，把宣传内容“洗白”后输入到主流 AI 系统中，从而影响公众认知。其核心论点是：当大模型依赖受污染的开放知识源时，AI 可能复述带偏见甚至危险的叙事。

## Problem
- 文章要解决的问题是：**Wikipedia 被宣传机器渗透后，AI 可能继承并放大这些失真信息**，把恐怖组织描述成普通政治或“抵抗”力量。
- 这很重要，因为 Wikipedia 被学生、记者、政策制定者和 AI 平台广泛使用；一旦上游知识源被污染，错误叙事会在下游被反复传播。
- 文中强调，这种“信息洗白”让原始宣传来源在传播链中被隐藏，使失真内容看起来像可信中立知识。

## Approach
- 这不是一篇正式学术论文，而是一篇**调查性评论**；方法主要是作者对 ChatGPT 回答、Wikipedia 条目及其引用来源进行案例核查。
- 核心机制很简单：宣传组织先影响 Wikipedia 条目内容与引文，再由 AI 因训练或检索依赖 Wikipedia 而复述这些说法。
- 作者通过多个人物/组织案例对比，指出 Wikipedia 条目措辞与伊斯兰圣战组织、哈马斯、伊朗官媒等原始材料高度重合，且关键暴力背景被省略。
- 作者还给出大规模计数，试图说明 Wikipedia 对伊朗国家媒体、代理人媒体及圣战媒体的引用并非孤例，而是系统性现象。

## Results
- 文中案例称，询问 ChatGPT“**Hezbollah 是什么**”时，系统给出“**a Lebanese political party**”而非“美国认定的恐怖组织”，并且**只给出 1 个引用：Wikipedia**。
- 对巴勒斯坦伊斯兰圣战指挥官 **Abu al-Walid al-Dahdouh**，作者称 ChatGPT将其描述为“**prominent commander**”，而未突出其恐怖活动背景；同时其 Wikipedia 条目中 **4 个来源里有 3 个直接来自 Palestinian Islamic Jihad 网站**。
- 作者声称其研究发现 **29,000+** 个 Wikipedia 引用指向**伊朗国家媒体**；其中 **Tasnim News** 被描述为最常见来源之一。
- 文章还称，Wikipedia 中有 **8,400+** 次引用来自与**伊朗代理组织（包括 Hamas、Hezbollah）相关媒体**，**1,000+** 次来自**穆斯林兄弟会相关媒体**，以及 **100+** 次来自**基地组织相关媒体**。
- 关于 **2025 Shabelle offensive** 条目，文中称其**近 50 次**引用 **Radio Furqaan**（青年党官方媒体），并有**十余次**引用 **Shahada News Agency**。
- 文章没有提供可复现实验、对照基线或标准学术评测指标；最强的具体主张是：**AI 对 Wikipedia 的依赖可能把被操纵的叙事规模化传播。**

## Link
- [https://www.dailymail.co.uk/debate/article-15640991/ChatGPT-Islamic-terrorist-propaganda.html](https://www.dailymail.co.uk/debate/article-15640991/ChatGPT-Islamic-terrorist-propaganda.html)
