---
source: arxiv
url: http://arxiv.org/abs/2603.08938v2
published_at: '2026-03-09T21:13:52'
authors:
- Rui Liu
- Tao Zhe
- Dongjie Wang
- Zijun Yao
- Kunpeng Liu
- Yanjie Fu
- Huan Liu
- Jian Pei
topics:
- agent-operating-system
- natural-language-interface
- multi-agent-orchestration
- personal-knowledge-graph
- skill-recommendation
- semantic-security
relevance_score: 0.9
run_id: materialize-outputs
---

# AgentOS: From Application Silos to a Natural Language-Driven Data Ecosystem

## Summary
本文提出 **AgentOS**，主张把操作系统从以 GUI/应用为中心，重构为以自然语言入口和多智能体协调为中心的个人代理操作系统。核心观点是：未来 OS 的关键问题不再只是系统工程，而是持续进行意图挖掘与知识发现的数据挖掘问题。

## Problem
- 现有本地智能体仍作为传统 OS 上的普通应用运行，与为 GUI/CLI 设计的旧架构不匹配，导致上下文割裂、交互碎片化和自动化脆弱。
- “Screen-as-Interface” 让代理依赖视觉抓取、点击和按键模拟，容易因界面变化失效，并丢失底层语义信息。
- 传统基于应用级权限的安全模型难以约束自主代理，带来“Shadow AI”、提示注入、数据泄露和误操作风险；这很重要，因为智能体正快速成为新的主流人机交互层。

## Approach
- 提出 **Single Port**：用统一的文本/语音自然语言入口替代桌面、窗口、图标等 GUI 主范式，必要时才动态生成可视界面。
- 设计 **Agent Kernel**：向上做意图解析、上下文维护和多模态理解；向下把用户目标拆成子任务，协调多个 agent 通过 MCP 与文件系统、网络和设备交互。
- 把传统应用重构为 **Skills-as-Modules**，用户可直接用自然语言定义可组合技能，系统按需编排形成工作流。
- 将 AgentOS 落地表述为 KDD 管线：用 **个人知识图谱（PKG）** 做上下文推理，用 **双塔推荐** 做技能检索，用 **序列模式挖掘（SPM）** 优化工作流，用新评测衡量 **Intent Alignment**。
- 为安全与容错补充 **Semantic Firewall**、污点感知记忆、数据防泄漏和系统级快照回滚，以控制提示注入、幻觉和高权限误执行。

## Results
- 这是一篇 **愿景/架构论文**，节选中 **没有给出实验结果、基准分数或定量性能提升**，未报告在具体数据集上相对基线的数值收益。
- 文中唯一明确数字化采用信号是：OpenClaw 在数周内获得 **100,000+ GitHub stars**，被作为本地自主代理爆发的背景证据，而非 AgentOS 本身的实验结果。
- 论文的主要突破性主张是：把 OS 的核心目标从 **CPU/内存/磁盘 I/O** 转向 **Intent Alignment、任务完成率、工具调用准确率** 等以用户意图达成为中心的指标体系。
- 论文还声称 AgentOS 可把系统演化机制从静态补丁升级，转为依赖 **SPM、推荐系统、PKG、MIRA** 等方法的持续学习式优化，但未提供量化验证。

## Link
- [http://arxiv.org/abs/2603.08938v2](http://arxiv.org/abs/2603.08938v2)
