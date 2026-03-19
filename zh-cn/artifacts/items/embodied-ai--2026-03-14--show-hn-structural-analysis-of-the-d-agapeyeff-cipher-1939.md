---
source: hn
url: https://msgtrail.com/posts/unmasking-the-dagapeyeff-cipher-a-multi-faceted-architecture
published_at: '2026-03-14T23:34:30'
authors:
- evaneykelen
topics:
- classical-cryptanalysis
- unsolved-cipher
- transposition-cipher
- esperanto
- structural-analysis
relevance_score: 0.0
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Structural analysis of the D'Agapeyeff cipher (1939)

## Summary
本文分析1939年的D’Agapeyeff未解密码，提出其应同时从页面几何结构与计算语言学两方面理解。作者认为，14x14排版中的异常聚集与2x98转置模型及世界语明文假设相互印证，虽未完全破译，但显著缩小了搜索空间。

## Problem
- 该密码长达196个数字，80多年间人工与计算方法都未能恢复可读明文，属于经典未解密码问题。
- 仅用单一视角（只看排版几何，或只做无约束计算搜索）可能忽略关键结构线索，因此长期难以突破。
- 解决它之所以重要，在于它既是历史密码学难题，也可检验如何把物理排版痕迹与现代算法结合起来进行分析。

## Approach
- 先将196个符号放入不同矩形网格中比较，重点考察14x14布局，发现稀有“异常”符号（04、71、94、92、93）都落在第14列。
- 作者将这种聚集解释为底层“2x7脉冲”：这些异常都出现在同时满足2与7节律的位置，因此在14x14中自然汇聚到末列，而04还位于第98对，恰是全文中点。
- 在计算层面，作者不再假设英语明文，而是假设世界语，并使用模拟退火搜索结合“2x98列转置 + Polybius方阵替换”模型。
- 作者以多次独立运行的一致性作为证据：若不同随机种子反复收敛到相似世界语词汇与高分结果，则说明并非纯粹过拟合噪声。

## Results
- 在14x14网格中，5类异常符号共8次出现，被报告为**全部**落入第14列；其中92出现**3次**、93出现**2次**，而04、71、94各出现**1次**。
- 关键结构点是04位于第**98**个数字对，正好把196个符号分成两个**7x14**半区，作者将其视为显著的中轴/铰链线索。
- 计算实验方面，作者称使用世界语四元语法统计后，**30次**独立模拟退火运行都恢复出相近词汇，如**ESTIS, KAJ, KIEL, TRADUK, KODO, KONTRAU, LANDO**。
- 论文声称这些世界语结果的适应度“明显高于任何英语基线”，并“接近自然语言基线”，但摘录中**未提供具体分数、误差范围或正式基线数值**。
- 最强结论不是“已破译”，而是：14x14中的视觉聚集与2x98世界语转置模型彼此一致，说明密码可能具有明确的几何-语言双层结构。
- 作者也明确承认该密码**仍未被完全破解**，当前贡献主要是提出更有约束力的结构解释与候选解读方向。

## Link
- [https://msgtrail.com/posts/unmasking-the-dagapeyeff-cipher-a-multi-faceted-architecture](https://msgtrail.com/posts/unmasking-the-dagapeyeff-cipher-a-multi-faceted-architecture)
