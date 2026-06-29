---
source: arxiv
url: https://arxiv.org/abs/2605.04107v1
published_at: '2026-05-04T15:35:45'
authors:
- Furkan Sakizli
topics:
- tool-calling
- agentic-llms
- schema-compression
- prompt-compression
- mcp
- llm-agents
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# TSCG: Deterministic Tool-Schema Compilation for Agentic LLM Deployments

## Summary
TSCG compiles JSON tool schemas into compact structured text so LLM agents can choose tools more accurately while using fewer input tokens. The paper reports large gains on small and frontier models when tool catalogs become long.

## Problem
- Production agent APIs send tool definitions as JSON schemas, which consume 3,000–25,000 input tokens per call and grow linearly with tool count.
- Small models lose tool-use accuracy as catalog size grows; the paper reports 0–49% accuracy beyond 15 tools in JSON-schema settings.
- This matters because schema overhead raises cost and blocks many local 4B–14B models from reliable tool calling.

## Approach
- TSCG is a deterministic compiler at the API boundary: it turns JSON schemas into structured text before the model sees them.
- It uses eight fixed operators, including tokenizer-aligned delimiters, constraint-first layout, causal ordering, filler removal, structural compression, and selective anchor duplication.
- It needs no model weights, fine-tuning, search, or runtime model calls; the implementation is a zero-dependency 1,200-line TypeScript package with sub-millisecond compilation.
- The method keeps the full tool catalog visible while reducing repeated JSON syntax and schema boilerplate.

## Results
- The main benchmark uses about 19,000 calls across 12 models and 5 core scenarios, plus BFCL and GSM8K checks.
- On frontier models, TSCG text beats native function calling in all reported Scenario A/B cells: Claude Sonnet 4 gains +11.2 pp and +5.0 pp with 50.1% token savings; GPT-4o gains +1.0 pp and +9.7 pp with 6.2% savings; GPT-5.2 gains +29.7 pp and +9.2 pp with 11.4% savings.
- On BFCL with Claude Sonnet 4, TSCG improves accuracy from 85.7% to 93.2%, tool selection from 86.7% to 95.0%, and parameter F1 from 84.2% to 91.7%, while saving 46.8% tokens.
- For small models, conservative TSCG raises Mistral 7B from 35.0% to 80.0% at 20 tools and from 30.0% to 75.3% at 50 tools; Gemma 3 4B rises from 24.3% to 87.5% at 50 tools.
- The abstract claims Phi-4 14B recovers from 0% to 84.4% accuracy at 20 tools and reaches 90.3% at 50 tools.
- The paper claims a formal compression bound of at least 51% on well-formed schemas, 52–57% token savings on heavy MCP schemas, and a +5.0 pp accuracy advantage at about 10,500 input tokens.

## Link
- [https://arxiv.org/abs/2605.04107v1](https://arxiv.org/abs/2605.04107v1)
