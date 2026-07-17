---
source: arxiv
url: https://arxiv.org/abs/2607.14896v1
published_at: '2026-07-16T12:13:41'
authors:
- Sizhong Qin
- Yi Gu
- Yao Jiang
- Ao Cai
- Changjian Zhou
- Shaoxuan Shuai
- Jiachang Wang
- Tianhao Shen
- Yueqiang Li
- Xinhao Li
- Li Zeng
- Yueshi Chen
- Dachen Gao
- Genrong Xu
- Wenjie Liao
- Xinzheng Lu
topics:
- engineering-agents
- executable-benchmark
- artifact-traceability
- workflow-validation
- multimodal-reconstruction
relevance_score: 0.61
run_id: materialize-outputs
language_code: zh-CN
---

# StructureClaw: Traceable LLM Agents and an Executable Benchmark for Structural Engineering Workflows

## Summary
## 摘要
StructureClaw 通过完整、可执行的证据链评估结构工程智能体，而不只是评估最终答案。其基准测试表明，受控技能与基于工件的工作流执行能够显著提升端到端成功率；但无效输入处理和多模态模型重建仍然较为困难。

## 问题
- 结构工程请求需要一致的需求、模型、验证记录、求解器输出、规范校核和报告；流畅的文本或看似可执行的代码可能掩盖缺失或不一致的工件。
- 现有智能体评估通常测试孤立能力，不要求完整、可执行且可追溯的工作流。
- 这一点很重要，因为只有当计算证据和执行历史能够支持所报告的结论时，工程结果才具备可审查性。

## 方法
- StructureClaw 使用受控的领域技能、类型化工具、后端提供程序和共享的类型化工件状态，以保留可检查的工作流输出。
- 一个 ReAct 风格的智能体循环负责选择工具、更新工件、验证模型、请求澄清、修复错误、执行受支持的后端，或在执行不受支持或不安全时安全终止。
- 结构模型协议记录几何、拓扑、材料、截面、支座、荷载、组合、单位和分析元数据；OpenSeesPy 提供主要的开源分析后端。
- StructureClaw-Bench 包含 150 个受控场景，平均分为标准工作流、交互鲁棒性和多模态结构模型重建三类。只有当一个场景中的所有必需路由、工件、执行、交互和报告断言均在一次运行中通过时，该场景才算成功。

## 结果
- 在 10 种智能体—模型配置中，每种配置均测试 50 个标准案例，平均成功率从仅使用通用技能模式下的 56.8% 提升至使用自动工作流时的 88.6%，增加了 31.8 个百分点。10 种配置均有所提升。
- Kimi-K2.6 在 50 个标准案例上达到 100.0%；DeepSeek-V4-Flash 和 GLM-5.2 均达到 96.0%。这是系统层面的结果，因为该比较同时改变了技能路由、结构先验、工件要求和验证指导。
- 自动模式下，结构类型匹配率为 98.0%，技能选择率为 100.0%，模型匹配率为 90.8%。
- 交互鲁棒性测试的平均成功率为 91.0%，各配置结果介于 88.0% 和 94.0% 之间；合并后的断言通过率分别为：澄清 89.6%、避免生成无效模型 90.7%，以及在适当情况下不执行分析 91.0%。
- 报告指出，剩余的薄弱环节包括安全处理无效数值输入，以及根据图像或 DXF 文件进行与测试固件一致的重建。摘要未提供多模态测试的总体成功率，因此无法在此量化多模态性能。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.14896v1](https://arxiv.org/abs/2607.14896v1)
