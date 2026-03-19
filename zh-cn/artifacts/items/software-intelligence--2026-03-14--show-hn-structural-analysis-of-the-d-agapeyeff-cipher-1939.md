---
source: hn
url: https://msgtrail.com/posts/unmasking-the-dagapeyeff-cipher-a-multi-faceted-architecture
published_at: '2026-03-14T23:34:30'
authors:
- evaneykelen
topics:
- cryptanalysis
- unsolved-cipher
- structural-analysis
- esperanto
- simulated-annealing
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Structural analysis of the D'Agapeyeff cipher (1939)

## Summary
这篇文章提出对1939年未解的 D’Agapeyeff 密码进行一种“结构+计算”联合分析：用版面几何解释异常数字聚集，再用现代密码分析测试潜在明文语言。核心主张是，14x14 方阵中的异常列来自底层的 2×7 位置脉冲，而计算上最有希望的解释是一个 2x98 列换位配合 Polybius 方阵、且明文更像 Esperanto 而非英语。

## Problem
- 要解决的问题是：D’Agapeyeff 密码在 **80 多年**内始终未被可靠破译，传统人工与计算方法都未能提取可读明文。
- 这很重要，因为它是经典未解密码之一；若能解释其结构，可缩小搜索空间、纠正错误语言假设，并为历史密码研究提供方法论。
- 文章还试图回答一个更具体的问题：14x14 排列中异常符号集中到第 14 列，究竟是排版巧合，还是加密结构留下的痕迹？

## Approach
- 先做**结构分析**：把 **196** 个数字对尝试排成多个矩形，重点观察 **14x14**。作者发现 **5 类异常符号**（04、71、94、92、93）共 **8 次出现**都落在第 **14 列**。
- 将该现象解释为底层的 **2×7 pulse**：这些异常都出现在同时满足“2 的节拍”和“7 块末尾”的位置，因此在 14x14 中会系统性落到最后一列；其中 **04** 位于第 **98** 对，正好是全长 **196** 的中点。
- 再做**计算分析**：不再默认明文是英语，而是假设为 **Esperanto**，并用 **Simulated Annealing** 搜索一个 **2x98 columnar transposition + Polybius square substitution** 的组合模型。
- 通过多次独立运行，检查是否稳定恢复相似词汇与接近自然语言的评分；作者将这种跨随机种子的一致性视为不是“过拟合乱码”的证据。

## Results
- 结构上，作者声称 **196** 个符号排成 **14x14** 时，异常符号的 **8 次出现**全部集中在第 **14 列**；其中 **92** 的 **3 次**和 **93** 的 **2 次**也全部在该列，被视为“统计显著”的非随机聚集。
- 关键定位结果是：著名异常 **04** 出现在第 **98** 个数字对，即全文 **196** 的正中，把文本分成两个 **7x14** 半区。
- 计算上，作者报告使用 Esperanto 四元语料时，**30 次独立求解运行**都收敛出相似的 Esperanto 词汇，如 **ESTIS, KAJ, KIEL, TRADUK, KODO, KONTRAU, LANDO**。
- 文章声称该 **2x98 + Polybius + Esperanto** 模型的适应度分数“**far exceed any English baseline**”，但摘录中**没有提供具体分数、数据表、显著性检验或可复现实验配置**。
- 最强的实质性结论不是“已破译”，而是：**密码仍未被解开**，但作者认为已经把视觉结构证据（14x14 / 2×7）与计算语言学证据（2x98 / Esperanto）对齐，显著缩小了合理假设空间。

## Link
- [https://msgtrail.com/posts/unmasking-the-dagapeyeff-cipher-a-multi-faceted-architecture](https://msgtrail.com/posts/unmasking-the-dagapeyeff-cipher-a-multi-faceted-architecture)
