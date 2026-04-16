---
source: arxiv
url: http://arxiv.org/abs/2604.04871v1
published_at: '2026-04-06T17:18:53'
authors:
- Tianzhu Qin
- Yiqing Xu
topics:
- multi-agent-workflow
- statistical-software
- code-verification
- ai-assisted-development
- software-testing
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# StatsClaw: An AI-Collaborative Workflow for Statistical Software Development

## Summary
## 概要
StatsClaw 是一个用于构建统计软件的 AI 辅助工作流，使用彼此分离的代理分别负责规划、编码、模拟、测试、审查和发布。它的核心主张是，严格的信息隔离和必需的理解检查可以降低 AI 同时写出错误代码和与之相匹配的错误测试的风险。

## 问题
- 统计方法通常只有通过软件包才能真正被用户使用，但把数学公式转成可靠的代码、测试和文档需要大量工程工作。
- 标准的 AI 编码工作流可能会出现关联性失败：如果模型误解了某个公式，它可能会围绕同一个错误同时写出实现和测试，这样错误代码仍然会通过测试。
- 这对统计软件尤其重要，因为无声的数值错误看起来可能很合理，却会产生错误估计，拖慢采用速度，并损害研究工具的可信度。

## 方法
- StatsClaw 在单个 Claude Code 会话中运行多代理工作流。规划代理读取完整源材料，并分别为实现、测试和模拟编写独立文档。
- builder、tester 和 simulator 各自只收到属于自己的规范。builder 看不到测试规范或真实模拟参数；tester 看不到代码；simulator 看不到算法实现。
- 在写任何代码之前，规划代理必须先生成一个 `comprehension.md` 工件，列出方程、符号、假设和实现细节。用户可以在这个阶段中止流程或提出澄清。
- 该工作流使用带门控的状态机和重试信号：`Hold` 用于用户澄清，`Block` 用于测试失败，`Stop` 用于审查失败；每种情况在升级前最多重试 3 次。
- 在 probit 演示中，系统从一份 4 页 PDF 构建出一个包含 3 种估计器的 R 包：Newton-Raphson MLE、Albert-Chib Gibbs sampling 和 random-walk Metropolis-Hastings，然后用独立测试和 Monte Carlo 模拟进行验证。

## 结果
- 论文报告了一次端到端的 probit 软件包构建，包含 3 种估计方法，以及一项模拟研究，覆盖 4 个样本量（`N = 200, 500, 1000, 5000`），每种设定 500 次重复，总计 6,000 次拟合（`4 x 500 x 3`）。
- 在 tester 流水线中，MLE 实现与 R `glm(family = binomial(link = "probit"))` 进行比对，文中给出的容差是 `10^-6`；后面的审查片段又写成匹配达到 `10^-8`。
- reviewer 报告称，Monte Carlo 验收标准 `7/7` 项全部满足，流水线隔离已验证，且未发现容差被放宽。
- 论文称，这 3 种 probit 估计器表现出符合预期的统计行为：偏差趋近 0，RMSE 遵循 `1/sqrt(N)`，95% 置信区间覆盖率接近名义水平 0.95。
- 摘要在完整定量表格之前被截断，因此没有提供关于偏差、RMSE、覆盖率、运行时间，以及摘要中提到的三软件包评估的完整数值结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04871v1](http://arxiv.org/abs/2604.04871v1)
