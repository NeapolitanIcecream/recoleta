---
source: arxiv
url: https://arxiv.org/abs/2605.19633v1
published_at: '2026-05-19T10:18:12'
authors:
- Lakshya A Agrawal
- Donghyun Lee
- Shangyin Tan
- Wenjie Ma
- Karim Elmaaroufi
- Rohit Sandadi
- Sanjit A. Seshia
- Koushik Sen
- Dan Klein
- Ion Stoica
- Joseph E. Gonzalez
- Omar Khattab
- Alexandros G. Dimakis
- Matei Zaharia
topics:
- llm-optimization
- code-intelligence
- agent-architecture-search
- prompt-optimization
- multi-task-search
- automated-software-production
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# optimize_anything: A Universal API for Optimizing any Text Parameter

## Summary
## 总结
optimize_anything 把许多优化任务变成同一个循环：编辑一个文本工件，打分，把诊断反馈送给 LLM，再尝试更好的工件。论文声称，这一套 API 适用于提示词、代码、智能体、调度策略、CUDA kernel、圆打包、图像和数值求解器。

## 问题
- 现有的 LLM 优化工具通常只适用于一种工件类型，比如代码、提示词或智能体图，所以处理相关搜索问题时，用户得用不同系统。
- 许多评估器会产出有用的诊断信息，比如堆栈跟踪、性能分析数据、轨迹、成本明细或图像，但以前的工具把这些反馈放在任务专用的管线里。
- 共享一个优化器有意义，因为软件和工程工作常常可以归结为：针对自动化测试或分数，改进一个可序列化工件。

## 方法
- 用户提供一个种子字符串或自然语言目标、一个评估器、可选的训练/验证数据，以及可选的背景知识。
- 评估器返回一个标量分数和一个包含诊断信息的 side_info 字典；LLM 提议器读取这些反馈并写出一个修订候选。
- 默认后端把 GEPA 风格的 Pareto 搜索扩展到任意文本工件，保留在某个样本、任务或指标上最好的候选，而不只保留平均分最高的候选。
- 它支持单任务搜索、跨相关任务的多任务搜索，以及在同一 API 下对留出样本的泛化。
- 工程组件包括用于修复格式错误生成结果的 refiner、内容寻址的评估缓存、类型化的侧信息、图像反馈和后端适配器。

## 结果
- ARC-AGI 智能体架构搜索：Gemini Flash 准确率从 32.5% 提升到 89.5%，提高了 57 个百分点。
- 云调度：CloudCast 相比 Dijkstra routing 将成本降低 40.2%；Can’t Be Late 将成本降低 7.8%；ADRS 总分为 96.6，OpenEvolve 为 92.9，ShinkaEvolve 为 72.0。
- CUDA KernelBench：生成的 kernel 中有 87% 与 PyTorch 基线持平或更好，论文还声称多任务搜索在预算匹配的单任务运行上表现更好。
- 提示词优化：GPT-4.1-mini 在 AIME-2025 上的准确率从 46.67% 提升到 60.00%，提高了 13.33 个百分点。
- Bleve 上的编码智能体技能：Haiku 4.5 的通过率从 79.3% 提升到 98.3%；Sonnet 4.5 从 94.8% 提升到 100%；解决时间减少 47%。
- 消融实验报告称，可执行的侧信息让收敛速度比只看分数反馈快 4–6 倍，并且最终分数更高；圆打包在 n=26 时超过 AlphaEvolve，附录中的数学优化在 10 次对比中赢了 Optuna 的 7 次。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.19633v1](https://arxiv.org/abs/2605.19633v1)
