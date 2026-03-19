---
source: arxiv
url: http://arxiv.org/abs/2603.08190v1
published_at: '2026-03-09T10:19:13'
authors:
- Moustapha El Outmani
- Manthan Venkataramana Shenoy
- Ahmad Hatahet
- Andreas Rausch
- Tim Niklas Kniep
- Thomas Raddatz
- Benjamin King
topics:
- agentic-ai
- regression-testing
- multi-agent-systems
- retrieval-augmented-generation
- human-ai-collaboration
- software-testing
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Human-AI Collaboration for Scaling Agile Regression Testing: An Agentic-AI Teammate from Manual to Automated Testing

## Summary
本文研究一个面向敏捷工业场景的“Agentic AI 队友”，把已验证的手工测试规格自动生成为系统级回归测试脚本，并保留人工审核与治理。核心价值是在不打破现有 CI/敏捷流程的前提下，提升测试自动化吞吐、缓解手工到自动化的积压。

## Problem
- 论文要解决的是：在敏捷回归测试中，**手工测试规格产生速度快于可执行自动化脚本的编写速度**，导致自动化缺口持续扩大，拖慢反馈与发布节奏。
- 这很重要，因为在 Hacon 的工业环境中，**手工测试仍占 82–87%**，且其绝对数量**每个发布增长 10–20%**；而自动化覆盖率每次发布仅**增加 1–2%**，说明团队难以靠纯人工追上需求变化。
- 现有 LLM/测试生成研究通常缺少对**可维护性、断言质量、项目约定、人工协作与治理**的工业级关注，难直接落地到真实敏捷团队。

## Approach
- 核心方法是一个**检索增强生成（RAG）+ 有界多智能体工作流**：从历史“测试规格-脚本”样例中检索相关案例，让 AI 先写出测试脚本草稿。
- 系统包含多个角色：**Generator** 负责生成候选脚本，**Evaluator** 根据 Jenkins 执行日志和评估矩阵检查语法/可执行性/步骤覆盖/语义正确性，**Reporter** 生成给测试经理和测试工程师的 Markdown 报告。
- 工作机制很简单：把 Jira/Xray 导出的已验证测试规格放入输入目录，Copilot 异步批处理生成脚本并在 Jenkins 环境执行；若结果不够好，就在预设迭代上限内继续“生成-执行-评估”循环。
- 人机协作设计强调**AI 有限自治、人工最终把关**：AI 不能直接把产物并入回归套件，测试工程师必须审阅脚本、日志、报告和 MLflow 追踪信息后，决定接受、重构或重写。
- 该方案被设计成“**silent teammate**”，即在冲刺开始前异步准备首稿，不打断工程师日常工作，同时保持流程可追溯、可配置、可扩展。

## Results
- 评估基于**61 个测试规格**，覆盖**6 个功能域**；每个用例平均约**6 步**（范围 **2–18**），故事点为 **3–8**；其中**46 个 AI 生成脚本**被分配给**5 名测试工程师**审阅与重构，另有**10 个代表性脚本**做了人工语义审查。
- 生产力方面，人工语义审查显示：**每个脚本有 30–50% 的 AI 生成代码在人工修改后保持不变**。论文据此声称 AI 明显减少了初始编写工作量，并帮助缩小手工到自动化测试的缺口。
- 论文没有给出更标准化的时间节省百分比、缺陷率、通过率或与具体基线方法的严格对照实验数值；最强的量化证据主要是**30–50% unchanged code** 以及前述工业背景中的**82–87% 手工占比、1–2% 自动化增长、10–20% 手工测试增长**。
- 质量与协作方面，即使输入规格被预先评为**A–B（较高质量）**，AI 仍会因缺乏隐式领域知识而出现**过于字面化实现、误解业务语义、幻觉 API/方法名、不符合团队 clean code 规范**等问题。
- 作者将 AI 产出定位为接近**“初级测试工程师的首稿”**：功能上常有可用部分，但**远未达到免审直接上线**的程度；人工审查仍是保证可维护性、团队规范一致性和长期质量的必要条件。

## Link
- [http://arxiv.org/abs/2603.08190v1](http://arxiv.org/abs/2603.08190v1)
