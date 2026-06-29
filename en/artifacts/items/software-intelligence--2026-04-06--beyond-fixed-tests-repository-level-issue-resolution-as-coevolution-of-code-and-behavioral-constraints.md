---
source: arxiv
url: http://arxiv.org/abs/2604.04580v1
published_at: '2026-04-06T10:26:46'
authors:
- Kefan Li
- Yuan Yuan
- Mengfei Wang
- Shihao Zheng
- Wei Wang
- Ping Yang
- Mu Li
- Weifeng Lv
topics:
- program-repair
- multi-agent-systems
- test-generation
- repository-level-reasoning
- swe-bench
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints

## Summary
Agent-CoEvo treats repository-level bug fixing as a joint search over code patches and test patches, instead of assuming tests are fixed and correct. On SWE-bench Lite and SWT-bench Lite, it reports higher repair and test-generation performance than prior agent-based and agentless systems.

## Problem
- Repository-level issue resolution often starts with incomplete or wrong behavioral constraints, because tests may miss assumptions or encode the bug poorly.
- Most LLM repair systems keep tests fixed and use them as a final filter, which can reward overfitted patches and reject valid fixes.
- This matters because real software repair depends on changing both the implementation and the tests that define the intended behavior.

## Approach
- The paper proposes **Agent-CoEvo**, a multi-agent coevolution system with a `CodeAgent` for code patches and a `TestAgent` for test patches.
- A `LocationAgent` first turns the issue description into a reproduction script, runs it, and localizes likely faulty files and lines.
- The system keeps populations of candidate code patches and test patches, then runs every test candidate against every code candidate to build a pass/fail execution matrix.
- Code fitness depends on how many tests it passes and how much its behavior agrees with other code candidates; test fitness depends on whether it is passed by high-fitness code candidates.
- New candidates are produced with LLM-based semantic crossover, and elite candidates are kept across iterations. Test candidates are filtered early so they must fail on the buggy repository.

## Results
- On **SWE-bench Lite (300 issues)**, Agent-CoEvo reports **41.33% resolved**, beating **DARS: 37.00%**, **KGCompass: 36.67%**, **Moatless Tools (DeepSeek-V3): 30.67%**, and **Agentless 1.5: 32.00%**.
- On **SWT-bench Lite (276 issues)**, Agent-CoEvo reports **46.4% resolved**, beating **AssertFlip: 38.0%**, **AEGIS: 36.0%**, **OpenHands setup: 28.3%**, and **SWE-Agent+: 18.5%**.
- For test quality on **SWT-bench Lite**, Agent-CoEvo reports **56.0% ΔC**, above **OpenHands setup: 52.4%**, **AssertFlip: 44.2%**, and **AEGIS: 44.2%**.
- The method uses **population size 10** and **5 evolutionary iterations** with **DeepSeek-V3-0324** as the backbone model.
- The excerpt claims consistent gains over code-only, test-only, and generalist agent baselines, but the provided text does not include ablation numbers for the individual components discussed in the research questions.

## Link
- [http://arxiv.org/abs/2604.04580v1](http://arxiv.org/abs/2604.04580v1)
