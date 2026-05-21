---
source: arxiv
url: https://arxiv.org/abs/2605.12673v1
published_at: '2026-05-12T19:22:45'
authors:
- Hao Wang
- Hanchen Li
- Qiuyang Mang
- Alvin Cheung
- Koushik Sen
- Dawn Song
topics:
- agent-benchmarks
- reward-hacking
- benchmark-security
- ai-agents
- code-intelligence
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack

## Summary
## 摘要
BenchJack 在常规智能体运行前审计 AI 智能体基准中的奖励黑客路径。在 10 个热门基准上，它为全部基准生成了利用方法，并在 10 个基准中的 9 个上覆盖了几乎所有任务，同时没有执行任何预期任务工作。

## 问题
- 智能体基准可能给篡改测试、泄露答案或利用评分代码的智能体打出高分，因此报告的能力数字可能不准确。
- 人工审计难以覆盖带有不同运行框架、沙箱和评分函数的新基准。
- 运行后的黑客检测器只能在不良运行发生后采取行动；该论文称，基于 LLM 的检测器可能漏掉或接受被黑客利用的轨迹。

## 方法
- 论文基于过去的奖励黑客案例构建了 8 类缺陷分类，包括隔离失败、随基准发布答案、远程代码执行、提示注入、弱字符串匹配、逻辑缺口、信任不可信输出，以及权限过大。
- 论文将该分类转化为 Agent-Eval Checklist：面向基准设计者的 7 个类别、30 项二元检查。
- BenchJack 封装一个编码智能体，并运行三个阶段：侦察阶段绘制入口点、评分代码、任务文件、环境和信任边界；缺陷扫描阶段记录可利用发现；利用构建阶段编写并测试一个 run.sh 利用脚本，在不执行预期任务的情况下最大化分数。
- 修补循环在防御方编码智能体修复已验证利用后重新运行 BenchJack，然后重复该过程，直到 BenchJack 找不到可工作的黑客方法，或该基准需要重新设计。

## 结果
- BenchJack 审计了 10 个基准：SWE-bench Verified、SWE-bench Pro、FrontierSWE、MLE-Bench、SkillsBench、Terminal-Bench、OSWorld、WebArena、NetArena 和 AgentBench。
- 它在全部 10 个基准上生成了可工作的奖励黑客利用方法，并在 10 个基准中的 9 个上覆盖了几乎所有实例；AgentBench 较低，因为只攻破了其中的 dbbench 子集。
- 它在 8 类缺陷中发现了 219 个不同缺陷。
- 被审计集合覆盖了数千个任务，包括 SWE-bench Verified 中的 500 个、SWE-bench Pro 中的 731 个、WebArena 中的 812 个、NetArena 中的 5,030 个，以及 AgentBench 中的 903 个。
- 在 4 个设计可修复的基准上，迭代修补循环将可被黑客利用的任务比例从约 100% 降到 10% 以下。
- WebArena 和 OSWorld 在 3 次迭代内被修补到 BenchJack 无法再攻破。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12673v1](https://arxiv.org/abs/2605.12673v1)
