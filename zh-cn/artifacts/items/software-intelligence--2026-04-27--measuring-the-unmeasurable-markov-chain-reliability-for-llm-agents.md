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
TraceToChain 将 LLM 智能体的执行轨迹转换为吸收马尔可夫链，用来估计一次运行在什么时间到达成功或失败。它把 pass@k、pass^k 和可靠性衰减曲线归入同一个成功时间分布，并提供拟合检查和不确定性区间。

## 问题
- LLM 智能体会执行多个步骤，但基准报告常把可靠性压缩成 pass@1 或 pass@k 这类单个标量。
- 单一通过率无法在不再跑一次基准的情况下回答步数预算、备用工具或平均失效时间问题。
- 部署团队需要证据来说明由轨迹得到的可靠性模型能拟合留出轨迹，并且带有有限样本不确定性。

## 方法
- 为每个轨迹步骤提取特征，例如推理、工具调用、观察、重试和错误，然后使用 Ward 聚类，并用轮廓系数选择聚类数量，将步骤聚成瞬态状态标签。
- 使用拉普拉斯平滑的 MLE 拟合吸收离散时间马尔可夫链 M=(Q,R_success,R_failure)，其中 Q 建模瞬态状态之间的转移，出口向量建模成功或失败。
- 将可靠性视为首次到达成功吸收态：R(d)=Pr(success by step d)，并用基本矩阵 N=(I-Q)^-1 给出闭式可靠性量。
- 使用一阶与二阶 AIC 检验以及首次到达 CDF 上的 KS 检验，检查轨迹是否支持一阶链。
- 报告转移条目和派生可靠性指标的 Dirichlet 后验可信区间，以及轨迹级 bootstrap 区间。

## 结果
- 在 7 个受控的 MAST 风格设置中，采用严格的 50/50 拟合/测试划分，留出的经验 RDC 与解析 RDC 匹配，max L_inf^RDC=0.053，中位数为 0.048。
- 双样本 KS 检验在 p>0.05 时接受了 7/7 个设置上的拟合链，最小 p=0.78。
- 每个条目的 95% 后验区间与 bootstrap 区间在中位数上相差约 0.01。
- 该方法认为 pass@k、pass^k 和 RDC 是同一个成功首次到达分布的投影，这使分母和时间范围选择更明确。
- 论文说明，原始 SWE-bench 和 tau-bench 轨迹验证仍是未来工作，因为这些轨迹需要步骤级特征数据。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24579v1](https://arxiv.org/abs/2604.24579v1)
