---
source: arxiv
url: https://arxiv.org/abs/2605.14859v2
published_at: '2026-05-14T14:05:58'
authors:
- Zheng Yan
- Jingxiang Weng
- Charles Chen
- Dengyun Peng
- Ethan Qin
- Jiannan Guan
- Jinhao Liu
- Qiming Yu
- Yixin Yuan
- Fanqing Meng
- Carl Che
- Mengkang Hu
topics:
- coding-agents
- least-privilege
- authorization
- code-intelligence
- agent-safety
- benchmark
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Do Coding Agents Understand Least-Privilege Authorization?

## Summary
## 摘要
这篇论文研究编码代理在执行前能否为终端任务选择文件级权限。论文引入 AuthBench，并提出一种两步式策略生成方法；在报告的测试中，该方法提高了任务成功率，并减少了攻击路径。

## 问题
- 编码代理现在会读取文件、编写代码并运行 shell 命令，因此宽泛的默认权限可能暴露密钥、不安全脚本和其他敏感文件。
- 这项任务很难，因为代理必须授予完成任务所需的每一项权限，同时避免授予会打开攻击路径的权限。
- 现有评估通常假定权限策略已经存在；这篇论文测试模型能否根据任务和环境推断该策略。

## 方法
- 论文定义了权限边界推断：给定任务指令和终端环境，模型输出基于 POSIX 路径模式的读取、写入和执行允许列表。
- 论文构建了 AuthBench，包含 120 个终端任务：80 个标准任务和 40 个敏感任务，并配有人审权限标签、实用性验证器和攻击验证器。
- 该基准先用精确率、召回率和 F1 评估静态权限匹配，然后在生成的策略下运行固定的 GPT-5 执行代理，以衡量任务成功率。
- 论文提出的充分性-紧致性分解（Sufficiency-Tightness Decomposition）先要求模型通过模拟可能的任务流程生成较宽的策略，然后审计每项权限，移除缺少任务依据或会暴露敏感内容的条目。

## 结果
- 在标准任务上，Full-Access 达到 83.3% TSR，Golden-Permission 达到 77.1% TSR。最佳生成策略是 Gemini 3.1 Pro，TSR 为 75.4%，读取 F1 为 78.0，写入 F1 为 85.3，执行 F1 为 49.0。
- 在敏感任务上，Full-Access 达到 94.0% TSR，但 ASR 为 65.8%。Golden-Permission 达到 81.7% TSR，ASR 为 0.0%。
- 在生成策略中，Gemini 3.1 Pro 的敏感任务 TSR 最高，为 85.8%，SER 为 34.8%，ASR 为 28.3%。
- GPT-5.4 的敏感暴露低于 Gemini，SER 为 21.1%，ASR 为 19.4%，但其敏感任务 TSR 为 61.1%。
- 论文报告称，更多推理时计算会把模型推向各自特定的权限风格：Gemini 往往授予更宽的访问权限，而 GPT-5.4 和 Claude Opus 4.6 往往生成更紧的策略，并漏掉所需权限。
- 该分解方法在偏紧策略模型上最高将敏感任务成功率提高 15.8%，在所有测试模型上降低攻击成功率，并在标准任务上最高将执行维度 F1 提高 16.7%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14859v2](https://arxiv.org/abs/2605.14859v2)
