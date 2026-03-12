---
source: arxiv
url: http://arxiv.org/abs/2603.03823v1
published_at: '2026-03-04T08:20:25'
authors:
- Jialong Chen
- Xander Xu
- Hu Wei
- Chuan Chen
- Bing Zhao
topics:
- software-engineering-benchmark
- code-maintenance
- continuous-integration
- llm-agents
- repository-level-eval
relevance_score: 0.03
run_id: materialize-outputs
---

# SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via Continuous Integration

## Summary
SWE-CI 提出一个面向**长期代码维护**的新基准，用持续集成（CI）式多轮演化来评估智能体，而不是只看一次性修补是否通过测试。它强调：真正重要的不只是“修好当前问题”，而是让代码在未来几十轮修改中仍然容易扩展且少回归。

## Problem
- 现有代码基准大多是**静态、一次性**评测，只衡量当前功能正确性，难以区分“勉强能过测试的脆弱补丁”和“便于后续演化的高可维护实现”。
- 现实软件开发主要是**长期维护与需求迭代**；论文指出软件维护约占生命周期成本的 **60%–80%**，因此只测单次修复会偏离真实价值。
- 缺少能在**连续多轮修改**中观察技术债、回归控制和长期可维护性的仓库级 benchmark。

## Approach
- 构建 **SWE-CI**：首个基于**Continuous Integration loop** 的仓库级基准，任务来自真实 GitHub Python 仓库的长期演化片段。
- 每个任务由一个 **base commit** 和一个 **target/oracle commit** 组成；智能体需要从基础版本出发，经过多轮分析、编码、测试，逐步逼近目标版本对应的测试行为。
- 提出 **evolution-based evaluation**：每一轮需求不是预先固定，而是根据“当前代码 vs 目标代码”的测试差距动态生成，使早期设计决策会影响后续轮次难度。
- 设计 **Architect–Programmer 双智能体协议**：Architect 先总结失败、定位原因、生成不超过 5 条高层需求；Programmer 再理解需求、规划并实现修改，模拟真实 CI 团队流程。
- 提出两项核心指标：**normalized change** 把测试通过数变化标准化到 [-1,1]；**EvoScore** 对多轮 normalized change 做未来加权平均（后期轮次权重更高），用来近似衡量长期可维护性。

## Results
- 数据集规模：最终 **100 个任务**，来自 **68 个仓库**；每个 base/target 对平均跨越 **233 天**、**71 个连续提交**，且至少包含 **500 行**非测试源码修改。
- 数据构建流程：从 **4,923** 个候选仓库出发，得到 **8,311** 个候选 commit 对；环境构建后保留 **1,458** 个；自动过滤后剩 **137** 个，最终选取前 **100** 个。
- 实验设置：评测了 **8 家提供商的 18 个模型**，总消耗超过 **100 亿 tokens**，每个任务最多 **20 轮**，单次测试超时 **3600 秒**。
- 主要结论 1：同一提供商家族内，**新模型总是优于旧模型**；作者称 **2026 年后发布的模型**相较前代提升更明显。定性上，**Claude Opus 系列**整体领先，**GLM-5**也表现突出。
- 主要结论 2：不同提供商对短期收益 vs 长期可维护性的偏好不同；当提高 EvoScore 的未来权重时，**MiniMax、DeepSeek、GPT**更偏长期收益，**Kimi、GLM**更偏短期收益，**Qwen、Doubao、Claude**相对稳定。该部分**未给出具体分数表**。
- 主要结论 3：当前模型在长期维护中的**回归控制仍然较弱**。大多数模型的 **zero-regression rate < 0.25**；只有 **两个 Claude-opus 系列模型 > 0.5**。这说明即使静态修复能力提升，自动化长期维护仍远未解决。

## Link
- [http://arxiv.org/abs/2603.03823v1](http://arxiv.org/abs/2603.03823v1)
