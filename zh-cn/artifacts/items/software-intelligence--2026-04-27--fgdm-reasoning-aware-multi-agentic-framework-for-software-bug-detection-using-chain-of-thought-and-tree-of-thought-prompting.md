---
source: arxiv
url: https://arxiv.org/abs/2604.24831v1
published_at: '2026-04-27T17:22:15'
authors:
- Srita Padmanabhuni
- Bhargavi Karuturi
- Jerusha Karen Indupalli
- Santhan Reddy Chilla
- Vivek Yelleti
topics:
- software-bug-detection
- program-repair
- multi-agent-systems
- code-intelligence
- chain-of-thought
- flow-graphs
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# FGDM: Reasoning Aware Multi-Agentic Framework for Software Bug Detection using Chain of Thought and Tree of Thought Prompting

## Summary
## 摘要
FGDM 是一个多智能体漏洞检测与修复系统，它把源代码转成流图，定位有问题的节点，修复这些节点，再重建代码。它面向 Python 和 C 程序，这些程序里的缺陷依赖控制流、数据流和跨块上下文。

## 问题
- 它处理大型或互联程序中的自动化漏洞检测与修复问题，因为逐行的机器学习和深度学习方法会漏掉代码块之间的依赖。
- 这很重要，因为缺陷发现得太晚会造成错误输出、运行损失和缓慢的人工调试。
- 这篇论文也针对 LLM 在代码修复中的失效模式，包括修复方案幻觉、推理不稳定和提示敏感性。

## 方法
- FGDM 使用四个顺序执行的智能体：Flow Graph Builder、Semantic Fault Localizer、Graph Repair 和 Source Code Reconstruction。
- 系统把代码转换为流图，其中节点是代码块，边表示包含关系、数据流、控制流和函数调用。
- 故障定位在图上运行，标记有缺陷的节点，并检查依赖是否断裂、流是否不匹配。
- 修复智能体尽可能只修改出错区域，然后用规则验证图结构，检查缺陷覆盖和最小边变更。
- Chain-of-Thought 和 Tree-of-Thought 提示引导这些智能体，FAISS 检索提供相似的历史缺陷和修复。

## 结果
- 评估使用了 BugsInPy 项目中的 100 个程序：Ansible、Black、FastAPI、Keras、Luigi、Matplotlib、Pandas、Scrapy、SpaCy 和 Tornado。
- 作者把 Python 程序转换成 C 版本，并用 Gemini 2.5 Flash API 智能体测试了两种语言。
- 与论文中的基线方法相比，FGDM 声称 Python 的平均 Levenshtein 距离降低了 24.33，C 降低了 8.37。
- FGDM 报告修复结果与参考表示之间的平均余弦相似度为：Python 0.951，C 0.974。
- Python 表格中的示例条目包括 Pandas-102：Levenshtein 距离从 FGDM-Standard 的 9 降到 FGDM-CoT 的 1 和 FGDM-ToT 的 1，余弦相似度从 0.9892 升到 0.9994。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24831v1](https://arxiv.org/abs/2604.24831v1)
