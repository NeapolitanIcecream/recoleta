---
source: hn
url: https://unsloth.ai/docs/models/qwen3.5
published_at: '2026-03-07T23:32:17'
authors:
- Curiositry
topics:
- local-llm
- model-quantization
- llama-cpp
- qwen
- tool-calling
- agentic-coding
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# How to run Qwen 3.5 locally

## Summary
This is an engineering-oriented local deployment guide explaining how to run the full Qwen3.5 model family on llama.cpp, LM Studio, and llama-server, while using Unsloth dynamic quantization to lower the barrier for local inference.
It is not a standard academic paper, but more like a product/system documentation page focused on runnability, quantization configuration, inference mode switching, and resource requirements.

## Problem
- The problem it addresses is: **how to efficiently run Qwen3.5 models ranging from 0.8B to 397B on local devices**, while minimizing memory usage and preserving reasoning, coding, long-context, and tool-calling capabilities.
- This matters because large models usually require very high VRAM/memory; if they can be run locally through quantization and backend adaptation, that enables offline use, lower-cost deployment, private data processing, and local agent/coding workflows.
- The document also implicitly addresses an engineering problem: different “thinking / non-thinking” modes, tool-calling templates, quantization formats, and inference backends are easy to misconfigure, which affects real-world usability.

## Approach
- The core method is to **use Unsloth Dynamic 2.0 GGUF dynamic quantization**, combining low-bit quantization such as 4-bit with upcasting key layers to 8/16-bit to maintain performance while keeping model size as small as possible.
- The runtime workflow is straightforward: first download the GGUF quantized file for the corresponding Qwen3.5 variant, then load it with **llama.cpp / llama-server / LM Studio**, and switch between “thinking” and “non-thinking” modes depending on the task.
- The document provides local hardware recommendations, context length, sampling parameters, and command-line settings for different model sizes; for small models, reasoning is disabled by default and must be explicitly enabled with `enable_thinking=true`.
- For the ultra-large 397B model, the method relies on **MoE offloading + quantization**, allowing it to run in an environment with a single 24GB GPU plus large system memory, rather than requiring a purely high-end multi-GPU cluster.
- It also fixes a **tool-calling chat template bug** and updates `imatrix` data and the quantization algorithm to improve chat, coding, long-context, and tool-calling performance.

## Results
- The document claims Qwen3.5 supports **256K context** and can be extended to **1M** via **YaRN**; it covers **201 languages**.
- In terms of local resource requirements: **27B can run on about 18GB RAM/Mac**, **35B-A3B can run on roughly 22–24GB** devices, **9B near full precision requires about 12GB RAM/VRAM**, and **122B-A10B requires about 70GB**.
- For **397B-A17B**: the full checkpoint is about **807GB**; **3-bit** quantization can fit into **192GB RAM**, and **4-bit** can fit into **256GB RAM**; its **UD-Q4_K_XL** uses about **214GB** of disk space and can be loaded directly on a **256GB M3 Ultra**; with MoE offloading using **a single 24GB GPU + 256GB system memory**, it is reported to reach **25+ tokens/s**.
- In a third-party 750-prompt mixed evaluation (**LiveCodeBench v6, MMLU Pro, GPQA, Math500**), **Qwen3.5-397B-A17B original weights scored 81.3%**; **UD-Q4_K_XL scored 80.5%** (**-0.8 points**, **+4.3% relative error increase**); **UD-Q3_K_XL scored 80.7%** (**-0.6 points**, **+3.5% relative error increase**). Based on this, the document emphasizes that the performance gap after quantization is **less than 1 percentage point** versus the original model.
- For the 35B series, the document says the updated quantization performs as **SOTA on Pareto Frontier** across **150+ KL Divergence benchmarks** and a total of **9TB GGUFs**, and specifically mentions results such as **UD-Q4_K_XL, IQ3_XXS**, though the excerpt does not provide more complete per-benchmark values.
- Most other results are qualitative claims: the improved quantization algorithm, `imatrix` data, and template fixes can improve performance in **chat, coding, long context, and tool-calling** scenarios; however, aside from the benchmarks above, the excerpt does not provide more detailed numbers that can be independently verified.

## Link
- [https://unsloth.ai/docs/models/qwen3.5](https://unsloth.ai/docs/models/qwen3.5)
