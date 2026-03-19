---
source: arxiv
url: http://arxiv.org/abs/2603.07557v1
published_at: '2026-03-08T09:40:54'
authors:
- Yixi Lin
- Jiangrong Wu
- Yuhong Nan
- Xueqiang Wang
- Xinyuan Zhang
- Zibin Zheng
topics:
- llm-agent-security
- privacy-auditing
- data-flow-analysis
- taint-tracking
- tool-using-agents
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# AgentRaft: Automated Detection of Data Over-Exposure in LLM Agents

## Summary
AgentRaft研究LLM智能体在跨工具调用中把不该传出的敏感数据一并传出的隐私风险，并提出首个自动化检测框架。核心价值在于把这种“数据过度暴露”从模糊风险变成可系统发现、可量化审计的问题。

## Problem
- 论文定义了LLM Agent中的**Data Over-Exposure (DOE)**：智能体在执行多步工具链时，把超出用户意图且非任务必需的数据传给下游/第三方工具。
- 这很重要，因为现代Agent常用“读文件/邮件 → 处理 → 发送”的链式工作流，工具返回的数据往往过宽，而LLM又缺乏稳定的上下文隐私边界感，容易造成敏感信息泄露。
- 传统静态程序分析难以处理LLM驱动的动态、概率性工具编排；而手工设计测试提示词又成本高、覆盖差，因此需要自动化DOE发现方法。

## Approach
- 构建**Cross-Tool Function Call Graph (FCG)**：先用静态类型兼容性筛出可能连接的函数对，再用LLM基于函数描述做语义验证，得到有效跨工具数据流路径。
- 沿FCG遍历源到汇的调用链，并把每条链转成可执行的**高保真用户提示词**，尽量确定性地触发目标多步工具调用。
- 在运行时做**细粒度数据流/污点跟踪**，记录哪些源数据最终传到了下游sink工具。
- 用基于GDPR、CCPA、PIPL的数据最小化原则的**多LLM投票委员会**，判断传输数据中哪些是用户明确想传的、哪些是任务真正必需的、哪些属于过度暴露。

## Results
- 评测环境来自**6,675个真实世界工具**，覆盖**4个主流场景**：Data Management、Software Development、Enterprise Collaboration、Social Communication。
- 论文声称DOE是系统性风险：**57.07%** 的潜在工具调用链存在未授权敏感数据暴露；从字段粒度看，**65.42%** 的已传输数据字段被判定为过度暴露。
- 与非引导随机搜索基线相比，随机方法在**300次尝试后仍难超过20%漏洞覆盖率**；AgentRaft在**50个prompts**内达到**69.15%**发现率，并在**150个prompts**时接近**99%** DOE覆盖。
- 多LLM投票审计相对基线将DOE识别效果提升**87.24%**（文中表述为outperforming baselines by 87.24% / improving DOE identification by 87.24%）。
- 审计成本方面，AgentRaft把**每条调用链验证成本降低88.6%**，支持更大规模、低成本的隐私合规检测。

## Link
- [http://arxiv.org/abs/2603.07557v1](http://arxiv.org/abs/2603.07557v1)
