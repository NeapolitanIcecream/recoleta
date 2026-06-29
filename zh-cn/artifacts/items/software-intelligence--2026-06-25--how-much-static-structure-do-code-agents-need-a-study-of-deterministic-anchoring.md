---
source: arxiv
url: https://arxiv.org/abs/2606.26979v1
published_at: '2026-06-25T12:50:01'
authors:
- Zhihao Lin
- Mingyi Zhou
- Yizhuo Yang
- Li Li
topics:
- code-agents
- static-analysis
- fault-localization
- repository-navigation
- swe-bench
- code-intelligence
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# How Much Static Structure Do Code Agents Need? A Study of Deterministic Anchoring

## Summary
## 摘要
CodeAnchor 以纯文本注释的形式，为以 grep 优先的代码代理添加静态程序链接。论文称，这些注释在不改变代理循环的情况下，让仓库导航更准确、更短，也更可重复。

## 问题
- 以 grep 优先的代码代理会漏掉调用图、继承、导入、配置使用和数据流链接，因此常停在附近的文本匹配处，而没有找到需要修改的函数。
- 这一点很关键，因为同一问题的两次运行可能访问不同文件并产生不同结果，使失败难以检查和复现。
- 论文研究在基线已经很强时，静态结构能带来多少帮助：在报告的匹配设置下，Codex 在 SWE-bench Lite 上达到 83.2% Func@5，而基于图的 LocAgent 为 59.5%。

## 方法
- CodeAnchor 离线运行轻量静态分析，然后把发现的事实作为普通注释插入到函数、类、文件和配置项旁边。
- 代理仍使用普通文本搜索和文件读取。打开代码时，附近的注释会显示 CALLS、CALLED_BY、IMPORTS、BASE、DERIVED、CONFIG_USAGE、DATA_DEP、IO_DEP 和 TEST_REF 等链接。
- 论文比较了原始 grep 与 Anchor-Topo、Anchor-Dense 和 Anchor-Inv。Anchor-Topo 添加调用、继承、导入和包含关系链接；Anchor-Dense 添加配置和数据流提示；Anchor-Inv 保留 CALLED_BY 等反向链接，同时删除正向链接。
- Python 原型使用 PyCG 构建调用图，并用 AST 遍历处理导入、包含关系、继承、配置使用、常量、I/O 和测试链接。

## 结果
- 在 SWE-bench Lite 上，轻量拓扑将函数定位的 Func@5 提高 2.2 个百分点，并将导航缩短 1.6 个交互轮次。
- 标签把结构链接跟随率从 0.15-0.18 提高到 0.21-0.24，并在报告的稳定性研究中将运行间方差约减半。
- 在中等规模仓库上，论文报告单次运行可靠性的 Pass@1 提高了 3.4 个百分点。
- 在 SWE-bench Lite 上，新增注释带来约 9.9% 的输入 token 成本，摘要中描述为约 10%。
- 静态图构建时间分别为：pytest-7432（73k LOC）6.8 秒，sklearn-15512（247k LOC）21.1 秒，astropy-12907（341k LOC）58.4 秒，django-13658（367k LOC）133.4 秒。
- 论文报告称，纯反向链接有助于枢纽较多的仓库；密集标签的收益会递减，除非任务依赖隐式配置或数据流链接。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.26979v1](https://arxiv.org/abs/2606.26979v1)
