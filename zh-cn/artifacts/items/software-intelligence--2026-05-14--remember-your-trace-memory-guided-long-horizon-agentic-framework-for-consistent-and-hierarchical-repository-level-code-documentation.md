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
## 总结
MemDocAgent 把仓库文档生成做成一次有状态的代理运行，后续文档会受早先检索结果和已写文档的影响。论文声称，在完整性、真实性、有用性和信息充分性上，它都优于开源和闭源文档基线。

## 问题
- 仓库级文档需要在函数、模块和整个项目之间保持一致，因为开发者和编码代理会用它来理解大型代码库。
- 现有系统会把各个组件分别文档化，这会导致对同一源文件的重复检索，平均重叠率为 50%，也会产生冲突描述，跨文档不一致平均为 13%。
- 以往输出往往只覆盖一个层级，所以要么缺少实现细节，要么缺少仓库级架构。

## 方法
- MemDocAgent 在生成前先构建依赖图并固定遍历顺序。依赖项先于依赖它们的内容被文档化，模块在子组件和子模块之后被文档化，仓库级内容在模块之后被文档化。
- 单个代理在一次长运行中处理所有文档单元，而不是针对每个组件重置。
- RepoMemory 存储生成的文档、抽取的主张、依赖链接、源代码、验证分数、子单元和缓存的搜索结果。
- 代理使用四个动作：Read 从 RepoMemory 或代码库检索上下文，Write 起草文档，Verify 检查事实质量和跨文档冲突，Finish 把接受的文档提交到记忆中。
- 验证使用关于事实一致性、完整性和有用性的自评分，再加上一个基于本地 NLI 的矛盾检查，用来对照已经验证过的相关文档。文中报告的验证阈值是 0.9。

## 结果
- 在 DevEval 的 20 个 Python 仓库上，使用 Qwen3-Coder 的 MemDocAgent 生成了 3,323 份文档，完整性得分为 0.979，真实性得分为 0.916，有用性得分为 0.690。同一 Qwen3-Coder 组里最强的开源基线得分分别是 0.845、0.835 和 0.628。
- 使用 GPT-5-mini 时，MemDocAgent 在 3,323 份文档上取得 0.958 的完整性、0.952 的真实性和 0.800 的有用性。该组里最强的开源基线得分分别是 0.860、0.850 和 0.708。
- 与闭源基线相比，DeepWiki 在 404 份文档上的完整性、真实性和有用性分别为 0.920、0.762 和 0.755；Claude-Code /init 在 20 份文档上的对应得分分别为 0.744、0.734 和 0.696。GPT-5-mini MemDocAgent 在这三项汇总指标上都超过了两者。
- 论文报告，MemDocAgent 消除了重复的源文件检索，并且比现有系统将跨文档不一致降低了 75.5%。
- 在不同层级上，GPT-5-mini MemDocAgent 的组件完整性/真实性/有用性得分为 0.952/0.974/0.750，模块为 0.974/0.924/0.858，仓库级文档为 0.949/0.959/0.791。
- 对于信息充分性，论文评估了 564 个 DevEval 组件测试用例，方法是根据文档和签名重建缺失的函数体。摘要说明 MemDocAgent 在这第四项标准上表现最好，但没有给出 Pass@k 或 CodeBLEU 数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14563v1](https://arxiv.org/abs/2605.14563v1)
