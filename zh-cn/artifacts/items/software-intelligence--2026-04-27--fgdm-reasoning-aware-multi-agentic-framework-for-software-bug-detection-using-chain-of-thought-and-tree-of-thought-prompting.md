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
FGDM 是一个多智能体缺陷检测与修复系统，会把源代码转换为流图，定位故障节点，修复这些节点，并重构代码。它面向 Python 和 C 程序，适用于缺陷依赖控制流、数据流和跨代码块上下文的场景。

## 问题
- 它处理大型或相互连接程序中的自动缺陷检测与修复问题；在这类程序中，逐行处理的 ML 和 DL 方法会漏掉代码块之间的依赖关系。
- 这一点很重要，因为较晚发现缺陷可能导致输出错误、运营损失和缓慢的人工调试。
- 论文还针对 LLM 在代码修复中的失效模式，包括虚构修复、不稳定推理和对提示词敏感。

## 方法
- FGDM 使用四个顺序执行的智能体：流图构建器、语义故障定位器、图修复器和源代码重构器。
- 系统把代码转换为流图，其中节点是代码块，边表示包含关系、数据流、控制流和函数调用。
- 故障定位在图上运行，标记有缺陷的节点，并检查断开的依赖关系和流不匹配。
- 修复智能体在可行时只修改故障区域，然后用缺陷覆盖率和最小边变更规则验证图结构。
- Chain-of-Thought 和 Tree-of-Thought 提示词引导这些智能体，FAISS 检索提供相似的历史缺陷和修复。

## 结果
- 评估使用了来自 BugsInPy 项目的 100 个程序：Ansible、Black、FastAPI、Keras、Luigi、Matplotlib、Pandas、Scrapy、SpaCy 和 Tornado。
- 作者把 Python 程序转换为 C 版本，并使用 Gemini 2.5 Flash API 智能体测试了两种语言。
- 与论文中的基线方法相比，FGDM 声称 Python 的平均 Levenshtein 距离减少 24.33，C 的平均 Levenshtein 距离减少 8.37。
- FGDM 报告称，修复输出与参考表示之间的平均余弦相似度在 Python 上为 0.951，在 C 上为 0.974。
- Python 表中的示例包括 Pandas-102：Levenshtein 距离从 FGDM-Standard 的 9 降至 FGDM-CoT 的 1 和 FGDM-ToT 的 1，余弦相似度从 0.9892 升至 0.9994。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24831v1](https://arxiv.org/abs/2604.24831v1)
