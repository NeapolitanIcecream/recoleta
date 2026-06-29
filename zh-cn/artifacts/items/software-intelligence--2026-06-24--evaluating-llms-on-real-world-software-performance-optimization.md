---
source: arxiv
url: https://arxiv.org/abs/2606.25530v1
published_at: '2026-06-24T08:07:41'
authors:
- "Ezgi Sar\u0131kayak"
- Wenchao Gu
- Hesham Ghonim
- Chunyang Chen
topics:
- llm-code-optimization
- software-benchmarking
- repository-level-code
- performance-engineering
- memory-profiling
- code-intelligence
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Evaluating LLMs on Real-World Software Performance Optimization

## Summary
## 摘要
SWE-Pro 是一个仓库级基准，用来测试 LLM 能否针对运行时间和内存优化真实 Python 代码。论文发现，当前 LLM 经常能应用补丁，有时能通过测试，但很少带来可测量的性能提升。

## 问题
- 现有 LLM 代码优化基准通常只测试孤立函数、单一工作负载，或只测试运行时间，因此会漏掉仓库依赖、输入敏感性、内存成本和测量噪声。
- 这一点很重要，因为生成代码可能给真实软件系统增加性能债务：执行更慢、内存使用更高、计算成本更高。
- 性能优化需要的不只是通过单元测试；补丁必须保持行为不变，并在多个工作负载上改善资源使用，且信号要足以超过噪声。

## 方法
- 作者用 `pandas`、`scikit-learn` 和 `xarray` 中 102 个专家编写的优化 pull request 构建了 SWE-Pro。
- 每个任务向模型提供真实仓库状态、正确性测试，以及参数化性能测试；这些性能测试会改变输入大小、数据属性和执行选项。
- 该基准测量运行时间、峰值内存和 Time-Weighted Memory Usage (TWMU)，其中 TWMU 捕捉一段时间内持续的内存压力。
- 测量在全新的 Docker 容器中运行，并使用校准、预热、自适应采样和 Signal-to-Noise Ratio 过滤；只有 SNR 高于 2 的效果才会计入。
- 评估在 oracle context 和 BM25 检索下测试六个 LLM：GPT-5.2、Claude Sonnet 4.6、Kimi K2.5、Gemini 3.1 Flash-Lite、GLM-5.1 和 MiniMax M2.7。

## 结果
- 专家 gold patches 平均实现 15.48× 运行时间加速、171.31× 峰值内存降低和 619.22× TWMU 降低。
- Gold patches 在 91.2% 的任务上显示出可复现的运行时间改进，在 65.7% 的任务上显示出峰值内存收益，在 52.0% 的任务上显示出 TWMU 收益；另一个数据集验证视角报告称，93.1% 的任务有可检测的运行时间效果，70.6% 有峰值内存效果，55.9% 有 TWMU 效果。
- 在 oracle context 下，LLM 补丁应用率范围为 30.4% 到 97.1%，正确率范围为 18.6% 到 79.4%，因此许多可应用的补丁仍会破坏行为。
- 在 oracle context 下，Gemini 3.1 Flash 的可检测运行时间通过率最高，为 12.7%，IF 为 1.27×；Claude Sonnet 4.6 的运行时间通过率较低，为 2.0%，但 IF 更高，为 6.67×。
- GPT-5.2 在 oracle context 下出现退化，运行时间 IF 为 0.69×，TWMU IF 为 0.85×。
- LLM 带来的内存收益很少：Claude Sonnet 4.6 在 oracle context 下达到 16.61× 峰值内存 IF 和 28.82× TWMU IF，在 BM25 下达到 3556.03× TWMU IF，但论文称这些收益来自一个实例，而不是广泛的任务成功。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.25530v1](https://arxiv.org/abs/2606.25530v1)
