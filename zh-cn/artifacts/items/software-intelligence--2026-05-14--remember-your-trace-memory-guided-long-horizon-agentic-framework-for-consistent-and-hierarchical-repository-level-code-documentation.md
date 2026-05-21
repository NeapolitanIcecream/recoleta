---
source: arxiv
url: https://arxiv.org/abs/2605.14563v1
published_at: '2026-05-14T08:35:20'
authors:
- Suyoung Bae
- Jaehoon Lee
- Changkyu Choi
- YunSeok Choi
- Jee-Hyong Lee
topics:
- code-documentation
- repository-level-code-intelligence
- long-horizon-agents
- agent-memory
- software-engineering-automation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Remember Your Trace: Memory-Guided Long-Horizon Agentic Framework for Consistent and Hierarchical Repository-Level Code Documentation

## Summary
## 摘要
MemDocAgent 以一次有状态的代理运行生成仓库文档，因此较早的检索结果和已写文档会指导后续文档。论文称，相比开源和闭源文档基线，它在完整性、真实性、有用性和信息充分性上得分更高。

## 问题
- 仓库级文档需要在函数、模块和整个项目之间保持描述一致，因为开发者和编码代理会用它理解大型代码库。
- 现有系统会独立为各组件编写文档，导致重复检索源文件，论文报告平均重叠率为 50%，并造成描述冲突，论文报告平均跨文档不一致率为 13%。
- 以往输出通常只覆盖一个细节层级，因此会遗漏实现细节或仓库级架构。

## 方法
- MemDocAgent 构建依赖图，并在生成前固定遍历顺序。依赖项先于依赖它的单元生成文档，模块在子组件和子模块之后生成文档，仓库在模块之后生成文档。
- 单个代理在一次长运行中处理所有文档单元，而不是为每个组件重置。
- RepoMemory 存储已生成文档、抽取出的声明、依赖链接、源代码、验证分数、子单元和缓存的搜索结果。
- 代理使用四个动作：Read 从 RepoMemory 或代码库检索上下文，Write 起草文档，Verify 检查事实质量和跨文档冲突，Finish 将通过的文档提交到记忆中。
- 验证使用事实一致性、完整性和有用性的自评分，并用本地基于 NLI 的矛盾检测，与已验证的相关文档进行比较。论文报告的验证阈值为 0.9。

## 结果
- 在 DevEval 的 20 个 Python 仓库上，使用 Qwen3-Coder 的 MemDocAgent 生成了 3,323 份文档，完整性得分 0.979，真实性得分 0.916，有用性得分 0.690。同一 Qwen3-Coder 组中最强开源基线的得分为：完整性 0.845，真实性 0.835，有用性 0.628。
- 使用 GPT-5-mini 时，MemDocAgent 在 3,323 份文档上的完整性得分为 0.958，真实性得分为 0.952，有用性得分为 0.800。该组最强开源基线的得分为：完整性 0.860，真实性 0.850，有用性 0.708。
- 与闭源基线相比，DeepWiki 在 404 份文档上的完整性得分为 0.920，真实性得分为 0.762，有用性得分为 0.755；Claude-Code /init 在 20 份文档上的完整性得分为 0.744，真实性得分为 0.734，有用性得分为 0.696。GPT-5-mini MemDocAgent 在列出的三个汇总指标上均超过二者。
- 论文报告称，与现有系统相比，MemDocAgent 消除了重复源文件检索，并将跨文档不一致减少了 75.5%。
- 在不同层级上，GPT-5-mini MemDocAgent 的组件完整性/真实性/有用性得分为 0.952/0.974/0.750，模块得分为 0.974/0.924/0.858，仓库级文档得分为 0.949/0.959/0.791。
- 对于信息充分性，论文通过依据文档和签名重新生成缺失函数体，评估了 564 个 DevEval 组件测试用例。摘录称 MemDocAgent 在这第四项标准上表现最好，但未提供 Pass@k 或 CodeBLEU 数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14563v1](https://arxiv.org/abs/2605.14563v1)
