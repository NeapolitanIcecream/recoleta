---
source: arxiv
url: http://arxiv.org/abs/2603.10268v1
published_at: '2026-03-10T22:56:03'
authors:
- Syed Yusuf Ahmed
- Shiwei Feng
- Chanwoo Bae
- Calix Barrus Xiangyu Zhang
topics:
- agent-testing
- gui-agents
- multi-agent-framework
- real-world-evaluation
- software-testing
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# SpecOps: A Fully Automated AI Agent Testing Framework in Real-World GUI Environments

## Summary
SpecOps 是一个面向真实 GUI 环境中 LLM 智能体的全自动测试框架，用多专家智能体把测试流程拆成生成、搭建、执行和验证四个阶段。它旨在替代手工构造任务或仿真环境评测，更稳定地发现真实产品级智能体中的缺陷。

## Problem
- 现有智能体评测通常依赖**人工设计任务与脚本**，扩展成本高，且难覆盖快速演化的产品级智能体。
- 很多方法运行在**模拟/文本环境**中，无法真实反映 GUI、多模态交互、CLI、网页和浏览器扩展中的复杂行为；这很重要，因为真实部署中的错误会影响邮件、文件、HR 问答等高风险业务。
- 通用 agent 或静态脚本在测试时容易**早期失败并级联崩溃**，还会混淆“测试者的任务”和“被测智能体的任务”，导致既测不准也报不出 bug。

## Approach
- 将端到端测试拆成四个专职阶段：**Test Case Generation、Environment Setup、Test Execution、Validation**，每个阶段由不同的 LLM specialist 负责，减少职责混淆。
- 使用**adaptive strategy**维护一份持续更新的测试规格，把环境设置、用户提示词、预期行为和验证规则绑定在一起，保证跨阶段一致性。
- 在生成阶段采用**双专家自反思机制**：Test Architect 先生成测试，Test Analyst 再检查提示是否完整、环境是否可构造、oracle 是否通用，避免测试本身有漏洞。
- 在执行阶段把不同平台统一抽象成**键盘/鼠标/UI 屏幕交互**，并通过屏幕变化截图做运行监控，以支持 CLI、web app 和 browser extension 等多种界面。
- 在验证阶段汇总文本、截图和环境状态等证据，用专门的 Judge/Auditing 式分析来定位缺陷，而不是让执行代理自行“修 bug”。

## Results
- 在**5 个真实世界智能体**、覆盖**3 个领域（Email、File System、HR Q&A）**的评测中，SpecOps 声称优于 AutoGPT 和 LLM 生成自动化脚本等基线。
- 提示/规划相关指标上，SpecOps 报告**100% prompting success rate**，而基线仅为**11%–49.5%**。
- 执行方面，论文声称实现了**perfect execution of planned steps**，即计划步骤执行完全成功；摘录中未给出更细的分项数字。
- 缺陷发现方面，SpecOps 共发现**164 个真实 bug**，并达到**F1 = 0.89**。
- 实用性方面，每个测试的成本**低于 0.73 美元**，运行时间**低于 8 分钟**。
- 与相关工作对比，作者声称 SpecOps 是首个同时具备**automated test generation、real-world apps、product-level agents、automated validation**的端到端全自动框架。

## Link
- [http://arxiv.org/abs/2603.10268v1](http://arxiv.org/abs/2603.10268v1)
