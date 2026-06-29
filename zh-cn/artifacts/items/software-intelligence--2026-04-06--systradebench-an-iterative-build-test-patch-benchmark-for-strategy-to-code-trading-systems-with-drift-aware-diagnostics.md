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
SysTradeBench 是一个基准，用来把自然语言交易策略转成受治理、可执行的代码，并在多轮迭代中进行构建、测试和修补。它衡量大语言模型是否能生成有效的交易系统，同时提供审计日志、确定性行为、泄漏检查，以及在修复过程中尽量减少语义漂移。

## 问题
- 现有的金融和代码基准没有把完整的策略到代码流程当作可审计的软件来测试，也没有覆盖执行、修复循环和漂移控制。
- 单一的回测指标会掩盖严重问题，例如前视泄漏、非确定性、风险规则失效或缺少审计轨迹。
- 这在交易里很关键，因为上线的策略代码必须遵循预期规则，通过治理检查，并且在复核时保持可复现。

## 方法
- 这个基准为每个模型提供一份标准化策略文档，以及针对 12 个交易策略冻结的、可机器检查的语义。
- 每个提交都必须产出三项内容：策略卡、可运行的 Python 策略代码，以及结构化审计日志，用来记录信号、风险检查、订单、持仓和盈亏。
- 沙箱执行器运行一组硬性有效性门槛，检查解析、模式合规、执行、确定性、反泄漏和审计完整性，然后从四个维度评分：规范一致性、风险纪律、可靠性/可审计性，以及样本外鲁棒性指标。
- 系统最多支持 3 轮 build-test-patch 迭代。每轮运行后，模型会拿到包含失败项和得分的证据包，但修补最多只能改 50 行，并且要用校验和、不变量和回归轨迹检查语义漂移。
- 评估覆盖 17 个模型，使用冻结的 2024-2025 市场数据，范围包括美国股票、加密货币和中国 A 股，并把质量分和成本效益一起报告。

## 结果
- 论文报告了 17 个模型、12 个策略的结果。
- 表现最好的模型至少达到 91.7% 的有效性，综合得分在 7.29-7.85 之间。
- 基于证据的迭代会提升质量，但也会带来收敛：生成代码在 Iter2 时达到 95.4% 的相似度，到 Iter3 时变成字节级一致。
- 这个基准使用 5 个必需的有效性门槛，再加上至少 95% 的审计完整性；任何一项不通过的提交都不会进入 D1-D4 评分。
- 论文里的样本外评估范围有限：D4 只用了抽样的 10 条 bar 测试窗口和零交易成本，而 2025 年完整测试集、0.1-20 bps 成本扫描的评估被推迟，因为 1020 次回测大约需要 450 个 CPU 小时。
- 主要的实证结论是，大语言模型适合快速原型开发和浅层 bug 修复，而对需要多样化解和更强鲁棒性的关键策略，仍然需要人工量化研究员。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04812v1](http://arxiv.org/abs/2604.04812v1)
