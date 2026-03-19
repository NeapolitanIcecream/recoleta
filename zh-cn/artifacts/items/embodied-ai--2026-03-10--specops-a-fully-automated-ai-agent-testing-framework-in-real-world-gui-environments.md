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
- llm-agents
- gui-testing
- automated-testing
- real-world-evaluation
- multi-agent-framework
relevance_score: 0.09
run_id: materialize-outputs
language_code: zh-CN
---

# SpecOps: A Fully Automated AI Agent Testing Framework in Real-World GUI Environments

## Summary
SpecOps 是一个面向真实 GUI 环境中 LLM 智能体的全自动测试框架，目标是在尽量少人工参与下完成从用例生成到缺陷判定的端到端测试。它通过分阶段的专用智能体与屏幕级监控，提升了真实产品级智能体测试的可靠性、覆盖性与实用性。

## Problem
- 现有智能体评测/测试方法往往依赖人工设计任务与脚本，扩展到真实产品级 GUI 智能体时成本高、效率低。
- 许多框架只在模拟环境或文本环境中运行，无法覆盖真实世界中的多模态交互、UI 导航和非确定性行为，因此测试结果不够真实可靠。
- 通用 agentic 系统或静态自动化脚本在测试场景中容易因早期错误而偏离目标、级联失败，既难发现真实 bug，也难进行稳健验证。

## Approach
- 将测试流程拆成四个明确阶段：测试用例生成、环境搭建、测试执行、结果验证；每个阶段由一个专门的 LLM specialist agent 负责，减少任务混淆。
- 采用“自适应测试规格”机制：先由 Test Architect 生成测试设想，再由 Test Analyst 反思和修正，使提示词、环境需求和验证 oracle 在全流程中保持一致。
- 用 UI 作为跨平台统一抽象，通过键盘/鼠标原语和屏幕截图来操作并监控被测智能体，因此可覆盖 CLI、Web app、浏览器扩展等不同载体。
- 在执行与验证中加入反馈回路和人类式视觉监控，遇到输入失败、界面变化或环境限制时可重试、调整，并保留屏幕证据用于后续判错与审计。

## Results
- 在 **5 个**多样化真实世界产品级智能体上评测，覆盖 **3 个领域**：Email、File System、HR Q&A。
- 声称是首个同时实现 **Automated test generation + Real-world apps + Product-level agents + Automated validation** 的端到端全自动测试框架；对比表中优于 OSWorld、AgentDojo、AgentCompany、ToolEmu 等相关工作在自动化完整性上的覆盖。
- **Prompting success rate 达到 100%**，而基线（如通用 agentic 系统/LLM automation scripts）仅为 **11%–49.5%**。
- 论文声称实现了 **planned steps 的完美执行**，但摘录中未提供更细的逐项执行率分解数字。
- 共识别出 **164 个真实 bug**，缺陷检测 **F1 = 0.89**，并称在 planning accuracy、execution success、bug detection effectiveness 上优于 AutoGPT 与 LLM-crafted automation scripts。
- 实用性方面，每个测试 **成本低于 0.73 美元**，**运行时间低于 8 分钟**。

## Link
- [http://arxiv.org/abs/2603.10268v1](http://arxiv.org/abs/2603.10268v1)
