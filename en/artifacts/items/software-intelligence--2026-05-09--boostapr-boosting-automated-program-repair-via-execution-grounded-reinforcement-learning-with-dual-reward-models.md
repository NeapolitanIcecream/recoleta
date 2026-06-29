---
source: arxiv
url: https://arxiv.org/abs/2605.09134v3
published_at: '2026-05-09T19:31:02'
authors:
- Yuanhao Li
- Hongbo Wang
- Xiaotang Shang
- Xunzhu Tang
- Yiming Cao
- Xuhong Chen
topics:
- automated-program-repair
- reinforcement-learning
- code-intelligence
- reward-modeling
- execution-feedback
- software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# BoostAPR: Boosting Automated Program Repair via Execution-Grounded Reinforcement Learning with Dual Reward Models

## Summary
BoostAPR trains a code repair model with execution feedback and line-level reward assignment, so PPO can learn which edits in a patch helped. It targets automated program repair on real repository bugs and Java/Python repair benchmarks.

## Problem
- LLM-based automated program repair gets sparse execution feedback: a patch passes all tests or fails, so RL gets weak training signal.
- Sequence-level rewards give one score to a whole multi-line diff, which makes it hard to assign credit to the edits that fixed or broke the program.
- This matters because better repair models can reduce debugging and maintenance work on real codebases, especially when pass@1 quality is the main user-visible outcome.

## Approach
- The base policy is Qwen2.5-Coder-32B-Instruct, trained only on SWE-Gym. Stage I runs supervised fine-tuning on Claude 3.5 Sonnet demonstrations that include reasoning traces and execution-verified patches; about 35% of generated patches pass the filter.
- Stage II trains a sequence reward model, Rseq, on sampled patches and execution-derived scores that combine patch application success, test pass rate, and a diff-size penalty. Its loss combines score regression with pairwise preference ranking.
- Stage II also trains a line reward model, Rline, over contiguous edited-line spans in unified diffs. Passing patches provide positive spans; failing patches provide negative or lower-credit spans from stack traces, function-level heuristics, or a uniform fallback.
- Stage III runs PPO for 300 steps. Rseq gives the patch-level score, and Rline distributes that score across tokens inside edited-line spans. Malformed diffs receive deterministic format penalties.

## Results
- SWE-bench Verified: 40.7% pass@1 on 500 tasks, +22.9 percentage points over Qwen2.5-Coder-32B base at 17.8%, and +2.4 points over PPO with Rseq only at 38.3%. SWE-RL reports 41.0% with a 70B backbone.
- Defects4J v2.0: 24.8% on 835 Java bugs after training on SWE-Gym, +13.5 points over base at 11.3%, and +5.6 points over Rseq-only PPO at 19.2%.
- HumanEval-Java: 84.5% on 164 tasks, +20.5 points over base at 64.0%, and +5.1 points over Rseq-only PPO at 79.4%.
- QuixBugs: 95.0% on 40 bugs, +5.0 points over base at 90.0%, with no gain over Rseq-only PPO at 95.0%.
- Stage I SFT alone reaches 23.4% on SWE-bench Verified, 14.9% on Defects4J, 73.1% on HumanEval-Java, and 92.5% on QuixBugs.

## Link
- [https://arxiv.org/abs/2605.09134v3](https://arxiv.org/abs/2605.09134v3)
