---
source: arxiv
url: http://arxiv.org/abs/2603.11073v1
published_at: '2026-03-10T20:20:33'
authors:
- Md Nasir Uddin Shuvo
- Md Aidul Islam
- Md Mahade Hasan
- Muhammad Waseem
- Pekka Abrahamsson
topics:
- vibe-coding
- ai-assisted-development
- software-architecture
- rag-systems
- multi-tenancy
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Context Before Code: An Experience Report on Vibe Coding in Practice

## Summary
这是一篇关于“vibe coding”在真实可部署系统中使用体验的经验报告。作者发现，AI 生成代码能明显加速脚手架和常规实现，但在多租户隔离、访问控制、异步处理等生产级约束上仍需要人类主导设计与审计。

## Problem
- 论文要解决的问题是：对话式代码生成在**生产约束**下到底能否可靠地构建可部署系统，而不仅是快速原型；这很重要，因为企业系统常要求租户隔离、权限控制、可追踪检索和异步任务稳定性。
- 现有研究更多关注生产力、提示技巧或开发者感受，较少分析 AI 生成代码在**架构级约束**下的实际表现。
- 如果这些约束没有被正确落实，系统可能出现跨项目数据泄漏、错误权限访问、引用不可信或同步阻塞等高风险问题。

## Approach
- 作者以一个小型全栈团队的**经验报告**形式，回顾性分析了两个使用 conversational/vibe coding 构建的可部署系统：一个多项目 agent 学习平台，一个学术 RAG 系统。
- 核心机制很简单：先把功能需求和架构约束写清楚，再让大模型生成 API、数据模型、工具函数和前端组件；随后由人类检查这些代码是否真的满足隔离、权限、检索范围和异步执行要求。
- 两个系统都采用“**上下文先于代码**”的方法：在提示中显式给出项目隔离、角色分离、后台任务、检索范围、引用追踪等约束，而不是只描述功能。
- 证据来自提交记录、issue 讨论、提示迭代、部署日志和实现笔记；验证手段包括人工测试、代码审查和运行日志分析。
- 作者进一步总结出若干“**non-delegation zones**”：如多租户边界、访问控制策略、内存更新策略、引用对齐校验、后台任务编排和基础设施设计，这些部分不能安全地完全交给 AI 自动生成。

## Results
- 论文**没有提供受控实验或系统化定量指标**，作者在“Threats to Validity”中明确说明：**未进行**生产力、代码质量或缺陷率的定量比较。
- 经验层面的最强结论是：在**2 个**可部署系统案例中，vibe coding 都显著加速了脚手架、CRUD、路由、工具函数和 UI 模板开发，但关键架构约束经常被遗漏。
- 在案例 1（多项目 agent 学习平台）中，早期 AI 生成路由**缺少 project-level filtering**，存在跨项目访问风险；初始 memory update 还错误地采用**同步执行**，最终需要人工加入项目 ID 检查并迁移到后台 worker。
- 在案例 2（学术 RAG）中，早期实现会生成**未校验答案-引用对齐**的 citation，且 embedding ingestion 最初也是**同步**执行，导致大文件上传时响应变慢；开发者后续加入 citation alignment checks，并改为异步任务。
- 论文给出一个具体的工程分工转移表：减少的工作包括 **4 类**（boilerplate writing、CRUD scaffolding、basic routing、UI template creation），增加的工作也包括 **4 类**（architecture design、isolation auditing、policy specification、validation and monitoring）。
- 总体主张是：AI 辅助开发更适合作为**在明确架构边界内加速实现**的工具，而不是替代系统级设计；真正的突破不在于完全自动化，而在于识别哪些生产级任务仍必须由人类负责。

## Link
- [http://arxiv.org/abs/2603.11073v1](http://arxiv.org/abs/2603.11073v1)
