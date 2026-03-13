---
source: arxiv
url: http://arxiv.org/abs/2603.08520v1
published_at: '2026-03-09T15:54:18'
authors:
- Yi Chen
- Yun Bian
- Haiquan Wang
- Shihao Li
- Zhe Cui
topics:
- llm-code-security
- iterative-refinement
- multi-agent
- cegis
- semantic-constraints
relevance_score: 0.92
run_id: materialize-outputs
---

# SCAFFOLD-CEGIS: Preventing Latent Security Degradation in LLM-Driven Iterative Code Refinement

## Summary
本文研究了LLM驱动的迭代式代码优化中，一个常被忽视的问题：代码功能可能持续改进，但安全性会在多轮迭代中悄悄下降。作者提出SCAFFOLD-CEGIS，用显式语义约束和多代理门控验证来阻止这种“潜在安全退化”。

## Problem
- 论文要解决的是**LLM多轮代码 refinement 过程中的潜在安全退化**：即使每轮看起来在改进功能、性能或可维护性，安全防护逻辑也可能被逐步删除、削弱或绕开。
- 这很重要，因为现实中的AI编程工具已从一次性生成转向多轮交互；如果安全约束只是提示词中的“软要求”，模型会因规格漂移而偏离原始安全目标。
- 现有SAST门控并不够用。作者指出它对“结构性退化”有盲区，甚至会制造伪安全感：受保护基线下的潜在安全退化率从 **12.5%** 上升到 **20.8%**。

## Approach
- 核心方法是 **SCAFFOLD-CEGIS**：借鉴CEGIS思想，把原本隐含在prompt里的安全要求，转成**可验证的硬约束**，在每次代码修改时强制检查。
- 框架采用四个代理协作：SecurityArchitectAgent 挖掘安全关键元素并生成“语义锚点”；ImplementerAgent 在这些约束下生成候选代码；GatekeeperAgent 做四层门控；AssimilatorAgent 从失败案例中提炼经验反馈给后续迭代。
- 最关键的机制是**语义锚定（semantic anchoring）**：把验证函数、清洗逻辑、鉴权检查、API签名和安全不变量等固定下来，防止模型在重构时不小心删掉。
- 四层门控验证包括：测试正确性检查、安全单调性检查（不允许新SAST风险上升）、diff预算控制（限制单次改动规模）、锚点完整性检查（确保关键防御逻辑仍在）。
- 失败同化机制会把被拒绝候选中的错误模式总结成自然语言规则，帮助后续生成避免重复犯错。

## Results
- 在 GPT-4o 的观察实验中，**43.7%** 的迭代链在 **10轮** 后的漏洞数高于初始基线，说明“迭代优化反而伤安全”的现象真实存在。
- 即使使用显式安全加固提示，退化仍存在：文中报告在该设置下退化率仍为 **28.6%**。
- 作者构建了包含 **24** 个编程任务样本、覆盖 **6** 类安全场景、**2** 种语言（Python/Java）、**3** 个模型、**4** 种迭代策略的数据设置，总计 **288** 条迭代链和 **2,880** 个迭代步骤。
- 对SAST门控的分析表明，它不能有效抑制潜在安全退化，反而把潜在安全退化率从 **12.5%** 提高到 **20.8%**，表明纯规则型静态分析无法覆盖“删除防御逻辑/弱化异常处理”这类结构性问题。
- 与 **6** 种现有防御方法相比，完整的 SCAFFOLD-CEGIS 将潜在安全退化率降到 **2.1%**。
- 该框架在作者实验设置下实现了 **100% safety monotonicity rate**，即每一步迭代都不比前一步更不安全。

## Link
- [http://arxiv.org/abs/2603.08520v1](http://arxiv.org/abs/2603.08520v1)
