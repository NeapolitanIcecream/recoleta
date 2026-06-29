---
source: arxiv
url: https://arxiv.org/abs/2606.26978v1
published_at: '2026-06-25T12:49:59'
authors:
- Zhihao Lin
- Junhua Zhu
- Mingyi Zhou
- Xin Wang
- Zhensu Sun
- Renyu Yang
- David Lo
- Li Li
topics:
- program-repair
- code-agents
- swe-bench
- test-execution
- cost-effectiveness
- code-intelligence
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair

## Summary
## 摘要
论文发现，在所研究的 SWE-bench 任务上，让 LLM 修复代理运行测试对修复准确率帮助很小，却会增加大量 token、时间和环境成本。它的主要结论是，代理应判断执行是否值得付费，而不应默认运行测试。

## 问题
- LLM 程序修复代理常使用一个循环：检查代码、编辑、运行测试、修改补丁。
- 运行项目测试会消耗 token、墙钟时间，并需要为每个仓库设置环境。
- 以往 SWE-bench 结果通常把代理设计变化和执行访问权限混在一起，因此无法单独衡量测试执行本身带来多少帮助。

## 方法
- 研究先分析了 7,745 条公开 SWE-bench 代理轨迹，来源包括 SWE-agent、OpenHands、LiveSWEAgent 和 Mini-SWE-agent，覆盖 12 个 LLM。
- 随后，研究在 200 个 SWE-bench 实例上运行了 3,000 次受控修复尝试：100 个 Lite 和 100 个 Verified。
- 受控运行使用 Claude Code 搭配 Claude Sonnet 4.5、Codex 搭配 GPT-5.2-xhigh，以及 OpenCode 搭配 Qwen2.5-Coder-32B-Instruct。
- 研究人员保持代理和任务不变，只改变执行访问权限：Prohibited、Quota-1、Quota-3、Budget-Guided 和 Unrestricted。
- 他们测量了解决率、token 使用量、墙钟时间、执行次数、定位准确率、单次编辑比例，以及代理运行的测试是否与官方 SWE-bench 评估一致。

## 结果
- 在 7,745 条公开轨迹中，代理平均每个任务运行测试 8.8 次；不同代理-模型组合的范围为每个任务 2.0 到 18.7 次执行。
- 后期执行的通过率高于早期执行；一个报告案例中，使用 Claude-3.5-Sonnet 的 OpenHands 从早期 42% 升至后期 72%，平均执行成功率为 57.9%。
- 在商业代理上，Prohibited 和 Unrestricted 的解决率差距为 1.25 个百分点，按 McNemar 检验统计上不显著（p > 0.05）。
- Claude Code 在无执行时解决 63%，在无限制执行时解决 64%；Prohibited 节省 56% 的 token 和 48% 的墙钟时间。
- 使用 Qwen2.5-Coder-32B 的 OpenCode 在 Prohibited 和 Unrestricted 模式下解决率均为 10%，且无执行时使用的 token 约少 3 倍。
- 对于商业代理，54-66% 的案例在一次编辑内完成，Prohibited 下的定位准确率保持在 95% 以上，并且 81-100% 的失败案例通过了代理自己的验证，但未通过官方 SWE-bench 评估。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.26978v1](https://arxiv.org/abs/2606.26978v1)
