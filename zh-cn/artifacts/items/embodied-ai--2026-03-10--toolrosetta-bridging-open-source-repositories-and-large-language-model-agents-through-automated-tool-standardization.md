---
source: arxiv
url: http://arxiv.org/abs/2603.09290v1
published_at: '2026-03-10T07:19:43'
authors:
- Shimin Di
- Xujie Yuan
- Hanghui Guo
- Chaoqian Ouyang
- Zhangze Chen
- Ling Yue
- Libin Zheng
- Jia Zhu
- Shaowu Pan
- Jian Yin
- Min-Ling Zhang
- Yong Rui
topics:
- llm-agents
- tool-standardization
- model-context-protocol
- repo-to-tool
- scientific-agents
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# ToolRosetta: Bridging Open-Source Repositories and Large Language Model Agents through Automated Tool Standardization

## Summary
ToolRosetta 旨在把分散在开源代码仓库和 API 中、难以直接调用的工具，自动转换成 LLM 代理可调用的 MCP 标准工具。它试图用自动化标准化替代人工封装，从而提升工具复用、任务完成率和跨领域扩展能力。

## Problem
- 论文解决的是：开源仓库里的实用工具很多，但接口异构、依赖复杂、缺少统一可执行标准，导致 LLM 代理很难可靠调用。
- 这很重要，因为当前工具型代理高度依赖人工整理和手工封装工具，扩展到大规模、长尾、跨学科工具时成本高且不可扩展。
- 如果不能自动把代码变成可调用服务，LLM 即使“看懂”仓库，也很难真正完成科学计算或复杂工作流任务。

## Approach
- 核心方法是一个多代理自动转换框架：先理解用户任务，再搜索相关 GitHub 仓库/API，然后把候选代码自动包装成 MCP 兼容服务。
- 其机制可以简单理解为“把杂乱代码仓库翻译成统一工具接口”：包括仓库克隆、语义分析、环境配置、接口抽取、服务生成与验证。
- 系统包含 Planning agent、Tool-search agent、MCP-construction agent、Security agent 和 Review agent，分别负责规划、检索、构建、安全检查和失败修复。
- 为提高成功率，ToolRosetta 使用 Review-Revise-Fix (RRF) 迭代修复流程，对转换失败案例做根因分析并多轮修补。
- 它还加入安全检查层，用于发现潜在恶意代码、隐私泄露或木马风险，降低开放生态下直接执行第三方代码的风险。

## Results
- ToolRosetta 自动将 **122** 个 GitHub 仓库中的 **1580** 个工具转换为标准化可执行接口，覆盖 **6** 个大领域与 **35** 个子学科。
- 在 122 仓库转换基准上，首轮转换成功率为 **53.0%**，高于 GPT-4o service-only baseline 的 **49.6%**；人工工程师为 **82.9%**。若让 GPT-4o 一次性生成完整仓库到 MCP 的全栈，成功率仅 **3.3% (4/122)**。
- 效率方面，ToolRosetta 平均每仓库耗时 **210.1 s**，人工为 **1589.4 s**（约 **26.5 min**），相当于 **86.8%** 时间下降、**7.6×** 加速。
- 经过 **3** 轮 RRF 修复后，领域宏平均转换成功率从 **54.2%** 提升到 **69.3%**，基准加权成功率从 **53.0%** 提升到 **68.4%**；其中 Scientific Community & Society 提升最大，达 **+24.4** 个百分点。
- 下游任务上，ToolRosetta 在 6 个科学类别上的宏平均任务完成准确率达到 **55.6%**，在 **35** 个子学科平均为 **52.1%**；并在 **6** 类中的 **5** 类排名第一。文中称其相对最强基线的六领域宏平均准确率提升 **超过 31%**。
- 在 **21** 个 OOD 子领域上，ToolRosetta 平均准确率 **57.4%**，明显高于 SciToolAgent **11.7%**、ChemCrow **3.3%**、RepoMaster **24.0%**、OpenAgents **21.5%**。把 ToolRosetta 转换出的工具注入其他系统后，RepoMaster 从 **24.2%** 提升到 **34.8%**（**+10.6**），OpenAgents 从 **22.0%** 提升到 **35.4%**（**+13.4**）。
- 案例研究中，针对钙钛矿材料发现，系统提出一种 **铅含量降低 50%** 的 Sn–Pb 配方，湿实验验证光电转换效率 **17%**，与其预测的 **16%–19%** 区间接近。

## Link
- [http://arxiv.org/abs/2603.09290v1](http://arxiv.org/abs/2603.09290v1)
