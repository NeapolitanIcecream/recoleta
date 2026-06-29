---
source: arxiv
url: https://arxiv.org/abs/2606.10728v1
published_at: '2026-06-09T11:37:15'
authors:
- Jiale Zhao
- Guoxin Chen
- Fanzhe Meng
- Wayne Xin Zhao
- Ruihua Song
- Ji-Rong Wen
- Kai Jia
topics:
- software-agents
- code-generation
- repository-generation
- software-benchmarks
- multi-agent-systems
- training-data
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# DeNovoSWE: Scaling Long-Horizon Environments for Generating Entire Repositories from Scratch

## Summary
## 摘要
DeNovoSWE 是一个包含 4,818 个样本的训练集，面向从文档生成完整软件仓库的智能体。用它对 Qwen3-30B-A3B 进行微调后，BeyondSWE-Doc2Repo 的得分从 5.8% 提升到 47.2%。

## 问题
- 代码智能体的训练数据大多是修复问题的数据，因此几乎不给规划和构建整个仓库提供监督。
- 生成完整仓库需要与可执行行为一致的文档、能验证结果的测试，以及阻止访问原始代码的沙箱。
- 这对自动化软件生产很重要，因为任务会跨越文件、API、依赖项和组件交互。

## 方法
- 该流程会筛选真实仓库，要求 Docker 环境稳定，原始测试通过率至少 90%，测试覆盖率高于 50%。
- 它把每个仓库拆分为功能能力，将测试和追踪到的函数/类映射到这些能力，并记录直接组件和对行为关键的间接组件。
- 草稿、评审和修复智能体在沙箱内编写和修改能力级文档，然后把它合并成一个文档到仓库任务。
- 清理步骤会删除源代码、测试、包缓存、构建产物和 Git 历史；运行时命令规则和 LLM 轨迹审计会阻止恢复参考实现的尝试。
- 面向难度的过滤会根据每个样本的可执行行数、两个 LLM 难度分数和观测到的 rollout 通过率，保留训练轨迹。

## 结果
- DeNovoSWE 包含 4,818 个文档到仓库样本，规模大约是 NL2RepoBench 的 104 个任务的 46 倍，也远大于 BeyondSWE-Doc2Repo 的 50 个任务。
- 用 DeNovoSWE 微调 Qwen3-30B-A3B 后，BeyondSWE-Doc2Repo 的表现从 5.8% 提升到 47.2%，提高了 41.4 个百分点。
- 数据集中的仓库平均有 205.0 个单元测试，中位数 79.0，P75 为 197.0，P90 为 464.0，最大值 8,903。
- 平均测试覆盖率为 85.5%，中位数 89.6%，P75 为 96.5%，P90 为 99.9%，最大值 100%。
- 评估覆盖仓库结构：测得的源文件平均为 19.3 个，中位数 9.0，P75 为 21.0，P90 为 42.0，最大值 1,995。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10728v1](https://arxiv.org/abs/2606.10728v1)
