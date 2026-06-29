---
source: arxiv
url: http://arxiv.org/abs/2604.03986v1
published_at: '2026-04-05T06:12:49'
authors:
- Anh T. V. Dau
- Shin Hwei Tan
- Jinqiu Yang
- Nghi D. Q. Bui
- Anh Tuan Nguyen
topics:
- cobol-code-generation
- legacy-language-llm
- code-translation
- domain-adaptation
- code-intelligence
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# COBOL-Coder: Domain-Adapted Large Language Models for COBOL Code Generation and Translation

## Summary
COBOL-Coder is a COBOL-specialized LLM built by fine-tuning Qwen2.5-Coder on a curated mix of real COBOL code, synthetic translation data, and COBOL documentation. The paper claims large gains over general-purpose and open-source baselines on COBOL code generation and COBOLJava translation, plus better ratings from experienced COBOL developers.

## Problem
- Existing LLMs do well on common languages but perform poorly on COBOL, even though COBOL still runs critical systems in banking, insurance, and government.
- Public COBOL data is scarce, noisy, and often uncompilable, which makes domain adaptation hard and leaves current benchmarks narrow.
- This matters for code generation and modernization tasks such as translating between COBOL and Java, where weak model performance slows maintenance and migration of legacy systems.

## Approach
- The authors build a COBOL training pipeline with three data sources: public GitHub COBOL files, synthetic JavaCOBOL translations, and COBOL/mainframe documentation.
- They use compiler-in-the-loop validation with GnuCOBOL and GPT-4o-based repair to turn noisy COBOL files and translated programs into compilable samples; from 40,829 cleaned GitHub files they keep 31,492 compilable programs.
- For synthetic data, they translate Java from Stack-v2-dedup-Java into COBOL, then filter pairs with two checks: LLM similarity scoring with threshold 0.6 and back-translation plus AST/CodeBERTScore filtering with threshold 0.7. This yields 173,042 validated translation pairs and 172,759 descriptioncode pairs.
- They convert code and documentation into instruction-tuning data, then fine-tune Qwen2.5-Coder 7B and 14B models into COBOL-Coder. They also introduce COBOL-JavaTrans, a benchmark for bidirectional COBOLJava translation.

## Results
- On COBOLEval code generation, COBOL-Coder-14B reaches 73.95% compilation success rate and 49.33 Pass@1, versus GPT-4o at 41.8% CSR and 16.4 Pass@1.
- On the same task, COBOL-Coder-7B gets 73.80% CSR and 44.70 Pass@1. The paper says most open-source baselines such as CodeGemma, CodeLlama, StarCoder2, and DeepSeek-R1-Distill-Qwen score 0% CSR and 0% Pass@1 on COBOLEval and COBOLCodeBench.
- On COBOLCodeBench, COBOL-Coder-14B is the only model with non-trivial reported performance: 26.09% CSR and 4.35 Pass@1.
- On COBOL-to-Java translation in COBOL-JavaTrans, COBOL-Coder reaches 97.9% CSR and up to 83.91 Pass@1, which the paper says approaches much larger general-purpose LLMs.
- On Java-to-COBOL translation, COBOL-Coder-7B gets 63.64% CSR and 27.27 Pass@1, while COBOL-Coder-14B gets 72.03% CSR and 34.93 Pass@1; the paper says general-purpose LLMs are near zero on this direction.
- In a developer study, experienced COBOL developers rank COBOL-Coder first on all Java-to-COBOL tasks and first or tied for first on most COBOL generation tasks. The excerpt does not provide numeric survey scores.

## Link
- [http://arxiv.org/abs/2604.03986v1](http://arxiv.org/abs/2604.03986v1)
