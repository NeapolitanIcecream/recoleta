---
source: hn
url: https://llama-cpp.com/
published_at: '2026-06-13T23:50:55'
authors:
- doener
topics:
- llm-inference
- c-cpp
- quantization
- local-deployment
- cross-platform
relevance_score: 0.77
run_id: materialize-outputs
language_code: zh-CN
---

# Llama.cpp – Run LLM Inference in C/C++

## Summary
## 摘要
Llama.cpp 是一个用于在本地硬件上运行 LLM 推理的 C/C++ 运行时，开销低，平台支持范围广。它之所以重要，是因为它让量化模型可以在 CPU 和常见 GPU 上使用，而不需要额外的运行时栈。

## 问题
- 运行 LLM 往往需要大型运行时、GPU 和按平台单独配置的环境。
- 许多用户希望在 CPU、笔记本、手机和混合硬件上进行本地推理。
- 模型文件和执行路径需要在不同系统和加速器之间保持可移植。

## 方法
- 它加载 GGUF 格式的模型，这是一种单文件可移植格式，保存权重、分词器数据和元数据。
- 它会自动检测 CPU 特性和可用 GPU，然后为当前机器选择执行路径和内核。
- 它使用量化权重、优化后的注意力机制和键值缓存进行推理。
- 在有 GPU 时，它可以把部分层卸载到 GPU，并在生成时流式输出 token。
- 它支持 C++11 构建，除可选的加速器 SDK 外，没有外部运行时依赖。

## 结果
- 摘要中没有基准测试表或准确率数据。
- 它声称可以在本地推理中实时生成响应。
- 它支持许多目标平台：Linux、macOS、Windows、Android、iOS、FreeBSD、x86、ARM、CUDA、ROCm、Metal、Vulkan、OpenCL 和 SYCL。
- 它声称以 GGUF 形式运行 7B-13B 参数模型时，实际模型大小大约在 2-10 GB。
- 小模型可以在低至 4 GB 内存下运行，更广泛使用则需要 16 GB 以上内存和 AVX2。

## Problem

## Approach

## Results

## Link
- [https://llama-cpp.com/](https://llama-cpp.com/)
