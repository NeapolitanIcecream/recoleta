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
隔离验证把安全属性证明放在代理运行时里，而不是依赖模型按预期行为。论文用 Dafny 验证了 PocketFlow，这样每个带类型的 AI 动作都必须通过经过检查的边界策略。

## 问题
- 代理式 AI 系统会触发外部影响，比如文件系统读取、工具调用、网络访问、金融操作、数据库变更或基础设施篡改。
- 模型级安全方法依赖学习到的行为，论文认为这类行为无法形式化验证，而且在部署中会失效。
- 这个方法对边界失效很重要：如果每个影响都经过一个带类型的动作接口，即使模型发出恶意或意外的动作，运行时也能阻止超出策略的影响。

## 方法
- 将 AI 建模为一个 havoc oracle：这是 Dafny 里的一个外部方法，可以在带类型的 `Action` 空间里返回任意值。
- 安全策略写在动作参数、建模的边界事件和系统状态上。这个主张依赖效果排他性：每个相关的外部影响都必须经过建模接口。
- 证明使用抽象的边界安全状态机和具体的 PocketFlow 操作模型之间的前向模拟细化。
- Dafny 证明检查每个具体边界事件都对应一个抽象的安全事件，因此被拒绝的动作会变成无影响事件，而不是未建模行为。
- 一个代理式合成流水线生成规范、操作模型和细化证明，并通过信息屏障和验证闸门减少自指或空洞规范。

## 结果
- 定理 3.2 声称了普遍的边界安全：在任意具体 oracle 下的每条轨迹上，只要抽象的 havoc 安全、边界事件细化和效果排他性成立，具体策略在每一步都成立。
- PocketFlow 实例使用了一个带类型的动作接口，包含 4 种变体：`NoAction`、`ReadPathAction`、`ToolCallAction` 和 `StepAction`。
- 经过验证的边界策略导出了 3 条记录的不变式：每个读取路径都保持在工作区根目录下，每次工具调用都在允许列表中，步数计数器保持在上限内。
- 证明用 Dafny 机械化实现，并包含 `RefinementInit`、`RefinementNext` 和 `ContainmentVerificationSoundness` 等命名引理。
- 合成过程分 7 个阶段，在迭代修复 Dafny 证明之前加入了消解、空洞性和区分闸门。
- 这段摘要没有给出运行时基准、吞吐量结果、攻击成功率或对比表；它最强的实证主张是一个经过 Dafny 检查的 PocketFlow 验证工件。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09045v1](https://arxiv.org/abs/2605.09045v1)
