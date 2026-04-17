---
source: arxiv
url: http://arxiv.org/abs/2604.04812v1
published_at: '2026-04-06T16:16:24'
authors:
- Yuchen Cao
- Hanlin Zhang
- Jacky Wai Keung
- Yang Chen
- Linqi Song
topics:
- benchmarking
- code-generation
- trading-systems
- iterative-repair
- auditability
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# SysTradeBench: An Iterative Build-Test-Patch Benchmark for Strategy-to-Code Trading Systems with Drift-Aware Diagnostics

## Summary
## 摘要
SysTradeBench 是一个基准，用于将自然语言交易策略转成受治理、可执行的代码，并支持在多轮过程中进行构建、测试和修补。它衡量 LLM 是否能生成有效的交易系统，包括审计日志、确定性行为、泄漏检查，以及修复过程中受限的语义漂移。

## 问题
- 现有金融和代码基准并不测试完整的策略到代码工作流，也不把它当作具备执行、修复循环和漂移控制的可审计软件来评估。
- 单一回测指标可能掩盖严重问题，例如前视偏差泄漏、非确定性、风险规则失效或缺少审计记录。
- 这在交易中很重要，因为上线的策略代码必须遵循预期规则，通过治理检查，并且在审查时保持可复现。

## 方法
- 该基准为每个模型提供标准化的策略文档，以及 12 个交易策略对应的冻结、可由机器检查的语义定义。
- 每次提交都必须生成三类产物：策略卡、可运行的 Python 策略代码，以及结构化审计日志，用于追踪信号、风险检查、订单、持仓和盈亏。
- 一个沙箱执行器会运行严格的有效性门槛检查，涵盖解析、schema 合规、执行、确定性、反泄漏和审计完整性，然后对四个维度打分：规格忠实度、风险纪律、可靠性/可审计性，以及样本外稳健性指标。
- 系统最多支持 3 轮 build-test-patch 迭代。每轮运行后，模型会收到包含失败项和分数的证据包，但补丁被限制为最多修改 50 行，并通过校验和、不变量和回归轨迹检查语义漂移。
- 评测覆盖 17 个模型，使用冻结的 2024-2025 年市场数据，涵盖美国股票、加密货币和中国 A 股，并在质量分数之外报告成本效益。

## 结果
- 论文报告了 17 个模型在 12 个策略上的结果。
- 表现最好的模型有效率至少达到 91.7%，综合得分在 7.29-7.85 区间。
- 由证据驱动的迭代会提高质量，但也会推动收敛：生成代码在 Iter2 时相似度达到 95.4%，到 Iter3 时变成字节级完全一致。
- 该基准使用 5 个强制有效性门槛，并要求审计完整性至少达到 95%；未通过任一门槛的提交不会进入 D1-D4 评分。
- 当前论文中的样本外评估仍有限：D4 使用抽样的 10-bar 测试窗口和零交易成本；完整的 2025 测试集评估以及 0.1-20 个基点的成本扫描被推迟，因为 1020 次回测大约需要 450 CPU 小时。
- 主要经验结论是，LLM 适合快速原型开发和浅层缺陷修复，而对于需要解法多样性和更强稳健性的关键策略，人类量化研究员仍然必不可少。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04812v1](http://arxiv.org/abs/2604.04812v1)
