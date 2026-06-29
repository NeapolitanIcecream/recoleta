---
source: arxiv
url: https://arxiv.org/abs/2605.28148v1
published_at: '2026-05-27T08:31:21'
authors:
- Aditya Pujara
- Xiaogang Zhu
- Hsiang-Ting Chen
topics:
- model-context-protocol
- code-generation
- api-evolution
- code-intelligence
- software-agents
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# DeltaMCP: Incremental Regeneration via Spec-Aware Transformation for MCP servers

## Summary
DeltaMCP updates existing MCP server tools when an OpenAPI spec changes, instead of regenerating the whole server. It matters because enterprise MCP servers often contain custom logging, safeguards, and adapter code that full regeneration can overwrite.

## Problem
- MCP servers expose API actions as callable tools for LLM agents, so they must stay aligned with changing backend APIs.
- Existing tools such as AutoMCP generate complete MCP servers again for each spec update, which can waste compute and remove hand-written enterprise logic.
- Large OpenAPI diffs can exceed 500,000 tokens, so direct whole-spec regeneration is hard to run and hard to control.

## Approach
- DeltaMCP takes three inputs: existing Python MCP server code, the old OpenAPI spec, and the new OpenAPI spec.
- It resolves OpenAPI references, uses Oasdiff to find schema and endpoint changes, then splits the diff into endpoint-level change units.
- Each unit pairs the old tool code with the relevant spec change, so the model only rewrites the affected MCP tool.
- The authors fine-tune StarCoder2-7B, CodeLlama-7B, and Phi-3-Mini-4k-Instruct with LoRA on more than 2,000 structured samples from Microsoft.Storage Azure REST API specs.
- The generated tool patches are inserted back into the existing MCP server through adapter logic, which keeps unrelated custom code in place.

## Results
- On Microsoft.Resources as unseen evaluation data, DeltaMCP averaged about 0.1% CPU use during updates, compared with about 3.0% CPU use for AutoMCP.
- DeltaMCP used about 10.5 to 12.5 MB of memory, while AutoMCP averaged about 30 MB.
- The paper reports that DeltaMCP touched far fewer tools per version update than AutoMCP, but the excerpt does not provide exact tool-count values from Figure 4.
- Code quality was scored on a 100-point normalized scale using syntax checks, MCP agent execution, and OpenAPI schema alignment; the excerpt says DeltaMCP stayed more consistent than AutoMCP, but it does not provide exact scores from Figure 5.
- Training used a 2,048-token context window for 3 epochs with 4-bit quantization and FlashAttention on an NVIDIA GH200 GPU with 480 GB of memory.

## Link
- [https://arxiv.org/abs/2605.28148v1](https://arxiv.org/abs/2605.28148v1)
