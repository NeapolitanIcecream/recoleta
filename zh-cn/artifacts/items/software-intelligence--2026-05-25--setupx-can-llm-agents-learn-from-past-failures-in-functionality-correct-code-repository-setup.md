---
source: arxiv
url: https://arxiv.org/abs/2605.26186v2
published_at: '2026-05-25T08:33:15'
authors:
- Zihang Zhou
- Ziqian Ren
- Yukai Wu
- Yingjie Xiong
- Wei Zhou
- Chao Peng
- Dong Zhang
- Bingheng Yan
- Xuanhe Zhou
- Fan Wu
topics:
- llm-agents
- repository-setup
- code-intelligence
- automated-software-engineering
- verification
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# SetupX: Can LLM Agents Learn from Past Failures in Functionality-Correct Code Repository Setup?

## Summary
## 摘要
SETUPX 是一个用于配置代码仓库的 LLM 智能体系统，目标是让仓库中记录的命令和测试在可复现的容器里运行。它从过往运行中学习可复用的配置修复方案，用 Docker 回滚来测试这些方案，并通过独立的 prosecutor-judge 审计检查结果。

## 问题
- 仓库配置经常失败，因为不同项目的依赖、构建工具、包安装和验证步骤都不一样。
- 现有智能体通常把每个仓库都当成新问题处理，因此会重复遇到同样的失败，而不是复用相似仓库里的修复方法。
- 配置出错时，构建或安装命令可能会正常退出，看起来像是成功了，但后续的软件任务依赖一个可用的执行环境。

## 方法
- SETUPX 把过去的配置修复方案存成 eXPerience Units（XPUs）。每个 XPU 包含错误信号、自然语言建议、可执行的修复命令，以及成功/失败遥测信息。
- 检索器会根据当前错误状态、向量相似度、历史成功率和一个 LLM 重排序器来搜索 XPUs，重排序器从 10 个候选中选出前 3 个。
- 智能体会在 Docker 容器里尝试检索到的修复方案，并使用 LIFO 快照栈，这样在失败或后续会造成损害的安装尝试后可以回滚。
- 循环内验证器在配置过程中运行只读检查，并区分由配置引起的失败和项目本身的问题。
- 事后 Prosecutor-Judge 流程中，一个智能体收集具体的失败指控，另一个智能体在最终通过/失败裁决前独立核验每一项指控。

## 结果
- 在 EnvBench 的一个整理后的 100 个仓库 Python 基准上，SETUPX+XPU 的通过率为 92%。
- 在相同的 prosecutor-judge 裁决下，它比 Claude Code 高 19 个百分点，比 ExecutionAgent 高 33 个百分点，比其他专用工具高 47–54 个百分点。
- 不使用 XPU 的 SETUPX 达到 82%，说明 XPU 记忆比基础智能体循环高 10 个百分点。
- 在高难度仓库上，SETUPX+XPU 达到 79%，而 Claude Code 为 63%，不使用 XPU 的 SETUPX 为 72%。
- 在领域失败次数上，SETUPX+XPU 相比最强的 CLI 基线把失败数从 27 降到 8；在 Toolchain 仓库中，它是 0/20 失败，基线是 5/20。
- 在 22 个多仓库场景上，SETUPX 和 Qwen Code 都在 17/22 个场景拿到 Full 或 Mostly，但 SETUPX 拿到 6 个 Full 判定，而 Qwen Code 只有 1 个。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.26186v2](https://arxiv.org/abs/2605.26186v2)
