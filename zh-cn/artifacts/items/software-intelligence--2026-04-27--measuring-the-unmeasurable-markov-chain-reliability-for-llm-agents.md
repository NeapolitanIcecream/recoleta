---
source: arxiv
url: https://arxiv.org/abs/2604.24579v1
published_at: '2026-04-27T15:05:45'
authors:
- Phat T. Tran-Truong
- Xuan-Bach Le
topics:
- llm-agents
- agent-reliability
- markov-chain
- evaluation-metrics
- trace-analysis
- multi-agent-systems
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Measuring the Unmeasurable: Markov Chain Reliability for LLM Agents

## Summary
## 摘要
TraceToChain 将 LLM 代理的执行轨迹转换为一个吸收马尔可夫链，用来估计一次运行何时到达成功或失败。它把 pass@k、pass^k 和 reliability decay curve 放进同一个成功时间分布里，并给出拟合检验和不确定性区间。

## 问题
- LLM 代理按多步运行，但基准报告常把可靠性压缩成一个标量，例如 pass@1 或 pass@k。
- 单个通过率无法回答步数预算、备用工具或平均失效时间这类问题，除非再跑一次基准。
- 部署团队需要证据，说明基于轨迹得到的可靠性模型能拟合留出轨迹，而且有有限样本不确定性。

## 方法
- 对每条轨迹的每一步做特征化，例如推理、工具调用、观察、重试和错误，然后用 Ward 聚类和基于轮廓系数选择的簇数，把步骤聚成瞬态状态标签。
- 拟合一个吸收离散时间马尔可夫链 M=(Q,R_success,R_failure)，用带 Laplace 平滑的 MLE，其中 Q 描述瞬态状态之间的转移，退出向量描述成功或失败。
- 把可靠性看作到达成功吸收态的首次到达：R(d)=Pr(在第 d 步前成功)，其中基本矩阵 N=(I-Q)^-1 给出闭式可靠性量。
- 用一阶与二阶 AIC 检验，以及对首次到达 CDF 的 KS 检验，判断轨迹是否支持一阶链。
- 对转移项和派生的可靠性指标，报告 Dirichlet 后验可信区间和轨迹级 bootstrap 区间。

## 结果
- 在 7 个受控的 MAST 风格设置上，按严格的 50/50 拟合/测试划分，留出集上的经验 RDC 与解析 RDC 一致，最大 L_inf^RDC=0.053，中位数 0.048。
- 双样本 KS 检验在 7/7 个设置上接受了拟合链，p>0.05，最小 p=0.78。
- 每个条目的 95% 后验区间和 bootstrap 区间在中位数上相差约 0.01。
- 该方法称 pass@k、pass^k 和 RDC 是同一个成功首次到达分布的投影，因此把分母和时间范围的选择明确化。
- 论文说明，原始 SWE-bench 和 tau-bench 的轨迹验证仍是后续工作，因为这些轨迹需要步级特征数据。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24579v1](https://arxiv.org/abs/2604.24579v1)
