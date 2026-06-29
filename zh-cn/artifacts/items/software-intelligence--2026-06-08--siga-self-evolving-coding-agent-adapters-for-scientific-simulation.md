---
source: arxiv
url: https://arxiv.org/abs/2606.09774v1
published_at: '2026-06-08T17:35:17'
authors:
- Matthew Ho
- Brian Liu
- Jixuan Chen
- Audrey Wang
- Lianhui Qin
topics:
- coding-agents
- scientific-simulation
- code-intelligence
- agent-adapters
- self-evolving-agents
- validation-guided-generation
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# SIGA: Self-Evolving Coding-Agent Adapters for Scientific Simulation

## Summary
## 摘要
SIGA 给编码代理加了一个很小的、面向模拟器的适配层，让它可以编写科学模拟输入 deck。在 GEOS 上，它在大约 5 分钟内给出接近专家水平的 deck 质量，而人工专家大约需要 3 小时。

## 问题
- GEOS、OpenFOAM 和 LAMMPS 这类科学模拟器需要专门的输入文件，里面的词汇、schema 规则、跨文件引用和有效停止条件都很严格。
- 科学家在仿真能跑起来之前，常常要花上数小时或数天看文档、改写示例并调试无效配置。
- 通用编码代理可以改文件和运行命令，但往往缺少模拟器合约，无法选对有效标签、填齐必需部分，也不知道什么时候 deck 已经完整。

## 方法
- SIGA 不是替换规划循环，而是包在一个冻结的编码代理框架外面。基础代理仍然负责浏览文件、编辑代码、运行 shell 命令和修复输出。
- 它增加了四个 grounding 组件：对文档、schema、示例和技术片段做语义检索；一个 775-token 的过程记忆备忘单；一个代理可调用的 XML 校验器；以及一个验证停止钩子。
- 对 GEOS，校验器使用 `xmllint --schema`。停止钩子会阻止最终提交，直到 `/workspace/inputs/` 里的 XML 文件都能解析并通过 schema 检查，同时返回结构化的修复反馈。
- 自进化循环会根据之前的轨迹重写适配器文本、记忆和辅助技能，同时保持模型和框架不变。

## 结果
- 在一个代表性的 GEOS 任务上，SIGA 在大约 5 分钟内生成了完整 deck，TreeSim 高于 0.90，和一个扩展预算的人类专家相当，而后者大约需要 3 小时。文中给出的墙钟加速约为 36 倍。
- 在一个更难的 GEOS 留出集上，grounding 把 bare agent 的 TreeSim 从 0.720 提高到 0.789，约为 10% 的相对提升。
- 在留出 GEOS 集上，grounded 设置把跨随机种子标准差降低了约 16 倍，这说明不稳定或失败运行更少了。
- 自进化后的 SIGA 变体在留出 GEOS 上达到最高均值，并与摘要中报告的最强手工设计配置持平或更好。
- 在 OpenFOAM 和 LAMMPS 上的迁移测试发现了不同的瓶颈：当结构完整性出问题时，验证最有帮助；当领域选择出错时，记忆和检索最有帮助。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09774v1](https://arxiv.org/abs/2606.09774v1)
