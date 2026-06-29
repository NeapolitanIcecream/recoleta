---
source: arxiv
url: https://arxiv.org/abs/2605.20530v1
published_at: '2026-05-19T22:05:12'
authors:
- Parsa Mazaheri
- Kasra Mazaheri
topics:
- llm-agents
- agent-evaluation
- tool-use
- trajectory-diagnosis
- benchmark-audit
- code-intelligence
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# AgentAtlas: Beyond Outcome Leaderboards for LLM Agents

## Summary
## 摘要
AgentAtlas 认为，用最终任务成功来评估使用工具、编辑代码、浏览网页并在用户环境中执行操作的 LLM agent，范围太窄。它提出了用于控制决策和轨迹失败的共享标签，然后展示了提示格式和评估轴如何改变同一批样本上的模型排名。

## 问题
- agent 排行榜常只报告一个结果分数，这会掩盖危险操作、遗漏确认、过度拒绝、循环、错误恢复和错误工具使用。
- 这对可部署的 agent 很重要，因为最终答案正确，也可能来自有害或无效的动作路径。
- 现有 agent 基准衡量的单位不同，比如任务成功率、pass^k 一致性、提示注入攻击成功率，或失败步骤定位，所以在代码、网页、操作系统、工具使用和安全任务之间很难比较结果。

## 方法
- 论文为 agent 定义了六种控制决策：Act、Ask、Refuse、Stop、Confirm 和 Recover。
- 论文使用九类轨迹失败分类法，并增加两个独立标签：`primary_error_source` 和 `impact`。
- 论文对 15 个 agent 基准做了审计，覆盖六个行为轴，用来说明哪些 agent 行为被直接计分、部分覆盖或完全缺失。
- 论文在 Control、Trajectory 和 Security 三个切分上，对 1,342 个样本做固定的合成评估，模型包括 8 个：4 个闭源模型和 4 个开源权重模型。
- 论文比较了 taxonomy-aware 提示和 taxonomy-blind 提示。前者显示标签菜单，后者要求自由形式诊断，再映射回同一组标签。

## 结果
- 在论文的合成运行中，去掉显式的轨迹标签菜单后，所有模型的分数都下降了 14–40 个百分点，blind 模式下的轨迹准确率收缩到 0.54–0.62，8 个模型都一样。
- taxonomy-aware 的控制准确率很集中：8 个模型里有 7 个得分在 0.870–0.946 之间，gpt-oss-20B 为 0.743。
- 没有模型同时拿下报告中的三个轴。Claude Haiku 4.5 在控制和轨迹上都得 0.95，但工具上下文效用保留只有 0.28；gpt-5.4-mini 的工具上下文效用为 0.98，但轨迹只有 0.82。
- 基准审计发现工具执行覆盖面很广，15 个基准里有 9 个属于强覆盖。记忆和状态只有 1 个基准达到强覆盖，即 ToolSandbox；效率这一项没有任何强覆盖基准。
- 论文引用外部证据说明不同轴的敏感性：在含糊的 SWE-bench Verified 任务上，使用不确定性感知策略把解决率从 61.2% 提高到 69.4%；tau-bench 在 pass^1 上把 Claude Opus 4.5 排第一，得分 0.70，而在 pass^4 上把 Qwen3.5 排第一，得分 0.56。
- 作者把这次 1,342 个样本的运行定位为测量协议演示，不是公开基准发布，并说明生成的金标准标签来自一个 Claude Opus 4.7 检查点，没有人工校准子集。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.20530v1](https://arxiv.org/abs/2605.20530v1)
