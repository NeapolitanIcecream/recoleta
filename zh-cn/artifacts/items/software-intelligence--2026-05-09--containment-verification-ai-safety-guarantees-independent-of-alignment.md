---
source: arxiv
url: https://arxiv.org/abs/2605.09045v1
published_at: '2026-05-09T16:36:45'
authors:
- Royce Moon
- Lav R. Varshney
topics:
- ai-safety
- formal-verification
- agentic-systems
- dafny
- runtime-containment
- software-engineering
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Containment Verification: AI Safety Guarantees Independent of Alignment

## Summary
## 摘要
Containment verification 在代理运行时中证明安全属性，而不依赖模型自行保持安全行为。论文用 Dafny 验证 PocketFlow，使每个类型化的 AI 动作都必须通过已检查的边界策略。

## 问题
- 代理式 AI 系统可能触发外部效果，例如文件系统读取、工具调用、网络访问、金融操作、数据库变更或基础设施篡改。
- 模型层面的安全方法依赖学习到的行为；论文称这些行为无法形式化验证，并且可能在部署中失效。
- 该方法适用于边界失效场景：如果每个效果都经过类型化动作接口，运行时就能阻止违反策略的效果，即使模型输出敌意动作或意外动作。

## 方法
- AI 被建模为 havoc oracle：一个 Dafny 外部方法，可以返回类型化 `Action` 空间中的任意值。
- 安全策略写在动作参数、建模的边界事件和系统状态之上。该主张依赖效果排他性：每个相关外部效果都必须经过建模接口。
- 证明使用抽象边界安全状态机与具体 PocketFlow 操作模型之间的前向模拟精化。
- Dafny 证明检查每个具体边界事件都匹配一个抽象安全事件，因此被拒绝的动作会变成无效果事件，而不是未建模行为。
- 一个代理式合成流水线生成规约、操作模型和精化证明，并使用信息屏障和验证门来减少同义反复式或空洞的规约。

## 结果
- Theorem 3.2 声称普适边界安全：如果抽象 havoc 安全性、边界事件精化和效果排他性成立，那么在任意具体 oracle 下的每条轨迹中，具体策略在每一步都成立。
- PocketFlow 实例使用带有 4 个变体的类型化动作接口：`NoAction`、`ReadPathAction`、`ToolCallAction` 和 `StepAction`。
- 已验证的边界策略产生 3 条记录的不变量：每个读取路径都保持在工作区根目录下，每个工具调用都在允许列表中，步数计数器保持在其边界内。
- 证明在 Dafny 中机械化，并包含 `RefinementInit`、`RefinementNext` 和 `ContainmentVerificationSoundness` 等具名引理。
- 合成过程有 7 个阶段，并在迭代式 Dafny 证明修复之前加入解析、空洞性和区分性验证门。
- 摘录没有给出运行时基准、吞吐量结果、攻击成功率或对比表；其最强的经验性主张是一个通过 Dafny 检查的 PocketFlow 验证工件。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09045v1](https://arxiv.org/abs/2605.09045v1)
