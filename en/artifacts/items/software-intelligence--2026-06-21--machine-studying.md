---
source: hn
url: https://jacobxli.com/blog/2026/machine-studying/
published_at: '2026-06-21T23:26:12'
authors:
- meander_water
topics:
- machine-studying
- agent-evaluation
- code-intelligence
- rag
- continual-learning
- software-agents
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Machine Studying

## Summary
Machine Studying defines a test for whether an agent can turn a new document corpus into usable expertise before it sees the exam. The paper adds StudyBench and reports early evidence that search, long context, and simple fine-tuning do not reliably create that expertise.

## Problem
- Agents often face new codebases, papers, manuals, and private corpora after training, and task-specific RL data or labeled examples may be unavailable.
- RAG and long-context search give access to documents, but they do not guarantee that the agent knows what to search for, which priors to distrust, or how to use found evidence efficiently.
- This matters for software agents and research agents because stale or missing domain knowledge can produce wrong APIs, poor configuration choices, and weak literature coverage even when the right evidence exists in the corpus.

## Approach
- The paper defines expertise as the weighted area under a performance curve as inference tokens increase. Higher expertise means better answers at lower token cost, with the corpus still available at test time.
- A studying algorithm can change model weights, prompts, tools, indexes, notes, or other harness state using only the corpus, before downstream tasks are known.
- StudyBench pairs a corpus with a hidden exam across three domains: DSPy code, OpenClaw code, and recent machine-learning literature.
- Agents run in a ReAct harness with grep, glob, and read_file tools. The evaluation compares direct answering, up to 5 tool iterations, up to 20 tool iterations, and forced 20 iterations.
- The paper tests early baselines including continual pre-training with LoRA on raw corpus text and synthetic supervised fine-tuning from generated question-answer pairs.

## Results
- StudyBench currently includes 3 tasks: Studying-DSPy with 30 coding questions, Studying-OpenClaw with 20 questions, and Studying-Literature built from about 50,000 full-text ICLR, CVPR, ICML, and NeurIPS papers from 2018 to 2025.
- The expertise metric uses log-token budgets where x=0 equals 3k generated tokens and each +1 is a 10x token increase. The paper uses exponential decay w(x)=(ln 10)10^-x, so each doubling of compute halves the budget weight.
- In a worked example with 5k, 10k, 20k, and 100k token budgets scoring 10%, 20%, 30%, and 40%, the estimated expertise is about 10.8%. The measured-budget weights sum to 0.60, so even perfect scores at those measured budgets would cap expertise at 60% because the sub-5k region gets zero.
- GPT-5.4-mini beats GPT-5.1 at every tested inference budget on DSPy, a library that grew popular after 2024. On OpenClaw, which postdates both models' cutoffs, the advantage disappears and both models remain barely above 10% even with more search.
- For Qwen3.5-9B on DSPy before studying, forcing the full 20 search iterations raises the lenient score from 9.6 to 29.4, about a 3.1x gain, which shows that reachable evidence often remains unused without better study behavior.
- The reported studying baselines are preliminary. The excerpt claims that simple self-supervised or supervised adaptations often improve raw models less than hoped and do not yet give a reliable jump in agent expertise.

## Link
- [https://jacobxli.com/blog/2026/machine-studying/](https://jacobxli.com/blog/2026/machine-studying/)
