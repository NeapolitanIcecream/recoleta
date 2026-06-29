---
source: arxiv
url: https://arxiv.org/abs/2606.09182v1
published_at: '2026-06-08T08:20:50'
authors:
- Kehui Chen
- Yicheng Sun
- Jacky Keung
- Zhenyu Mao
- Xiaoxue Ma
topics:
- model-context-protocol
- llm-software-engineering
- enterprise-adoption
- tool-integration
- human-ai-interaction
- agent-systems
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Understanding How Enterprises Adopt the Model Context Protocol for LLM-Driven Software Engineering

## Summary
## 摘要
本文通过对20名从业者的访谈，研究企业如何在大模型驱动的软件工程中采用模型上下文协议（MCP）。研究发现，MCP帮助大模型连接工具、文件、数据库和内部系统，但团队仍然面临标准不统一、兼容性、状态处理、安全性和故障诊断方面的问题。

## 问题
- 企业希望大模型能跨工具和内部系统执行多步骤的软件工程工作，但纯函数调用和临时搭建的智能体方案往往会丢失上下文、增加集成工作量，并带来维护成本。
- 先前关于MCP的研究主要集中在基准测试、集成和安全设计上，来自真实企业部署的证据很少。
- 这个问题之所以重要，是因为MCP能否落地取决于运行层面的匹配程度，包括兼容性、治理、可审计性、故障恢复，以及团队在日常开发中如何使用它。

## 方法
- 作者对来自互联网和金融行业8家公司的20名MCP从业者进行了半结构化访谈：其中9名来自金融科技，11名来自互联网。
- 参与者涵盖宿主方、客户端、服务器和用户角色，包括资深架构师、软件开发者、业务分析师和算法设计师。
- 研究先做了3次预访谈，用来完善31个问题的访谈提纲；随后进行了正式的视频访谈，每次90到120分钟，整理出约40万字的转录数据。
- 作者还进行了10次每次30分钟的补充访谈，并使用开放编码，不同编码者之间的Cohen’s kappa为0.89。
- MCP的核心机制是一个共享协议层，由Host、Client、Server和Resource等角色组成，这样大模型就能通过标准接口调用外部工具并交换任务上下文，而不用为每个工具单独建立定制连接。

## 结果
- 20名参与者中有20名，也就是100%，认为MCP对他们的工作很重要。
- 20名参与者中有16名，也就是80%，认为MCP通过简化大模型与外部工具的连接提高了效率。
- 20名参与者中有15名，也就是75%，认为MCP改善了工作方式，包括内部任务管理和标准化任务执行。
- 20名参与者中有14名，也就是70%，认为MCP降低了运维和开发的技术门槛。
- 20名参与者中有16名，也就是80%，认为LLM+MCP比大模型函数调用略复杂，但长期开发工作更少，维护性更好。
- 20名参与者中有20名，也就是100%，认为在排障时快速定位故障是主要障碍；他们报告的采用问题还包括标准分散、与LangGraph和ADK等工具兼容性差、组件间协同困难、分布式状态管理，以及围绕数据泄露、访问控制、可审计性和合规性的安全担忧。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09182v1](https://arxiv.org/abs/2606.09182v1)
