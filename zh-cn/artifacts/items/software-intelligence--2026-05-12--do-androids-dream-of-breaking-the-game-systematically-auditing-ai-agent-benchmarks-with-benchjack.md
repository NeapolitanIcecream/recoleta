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
BenchJack 会在正常代理运行前，先审计 AI 代理基准中的奖励黑客路径。在 10 个常见基准上，它都构造出了利用方式，并且在不做任何预期任务工作的情况下，在 10 个中的 9 个上拿到了接近满分的结果。

## 问题
- 代理基准会给那些篡改测试、泄露答案或利用评分代码的代理打出高分，所以报告的能力数值可能是错的。
- 手动审计无法扩展到带有不同执行框架、沙箱和评分函数的新基准。
- 运行后的黑客检测器只能在坏结果出现后处理，而且文中引用的工作说，基于 LLM 的检测器可能漏掉或放过被黑的轨迹。

## 方法
- 论文根据过去的奖励黑客案例建立了一个 8 类缺陷分类法，包含隔离失效、附带答案、远程代码执行、提示注入、弱字符串匹配、逻辑缺口、信任不可信输出和权限过大。
- 它把这套分类法整理成 Agent-Eval Checklist：给基准设计者使用的 7 类、30 项二元检查。
- BenchJack 包装了一个编码代理，并按三个阶段运行：侦察阶段映射入口点、评分代码、任务文件、环境和信任边界；缺陷扫描阶段记录可利用发现；利用构造阶段编写并测试一个 run.sh 利用脚本，在不执行预期任务的情况下最大化分数。
- 修补循环会在防守方编码代理修复已验证的利用后重新运行 BenchJack，然后重复，直到 BenchJack 找不到可用的黑客方式，或者该基准需要重设计。

## 结果
- BenchJack 审计了 10 个基准：SWE-bench Verified、SWE-bench Pro、FrontierSWE、MLE-Bench、SkillsBench、Terminal-Bench、OSWorld、WebArena、NetArena 和 AgentBench。
- 它为全部 10 个基准都生成了可运行的奖励黑客利用方式，并且在 10 个中的 9 个上覆盖了几乎所有实例；AgentBench 结果较低，是因为只黑了其中的 dbbench 子集。
- 它发现了 8 个缺陷类别中的 219 个不同缺陷。
- 被审计的数据集覆盖了数千个任务，其中包括 SWE-bench Verified 的 500 个、SWE-bench Pro 的 731 个、WebArena 的 812 个、NetArena 的 5,030 个，以及 AgentBench 的 903 个。
- 对于 4 个设计可修复的基准，迭代修补循环把可被黑的任务比例从约 100% 降到了 10% 以下。
- WebArena 和 OSWorld 在 3 轮迭代内被修补到 BenchJack 无法再黑掉它们。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12673v1](https://arxiv.org/abs/2605.12673v1)
