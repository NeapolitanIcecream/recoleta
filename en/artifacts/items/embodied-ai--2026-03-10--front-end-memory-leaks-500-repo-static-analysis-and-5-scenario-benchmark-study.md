---
source: hn
url: https://stackinsight.dev/blog/memory-leak-empirical-study/
published_at: '2026-03-10T22:56:26'
authors:
- nadis
topics:
- frontend-memory-leaks
- static-analysis
- benchmarking
- react-vue-angular
- javascript-gc
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Front End Memory Leaks: 500-Repo Static Analysis and 5-Scenario Benchmark Study

## Summary
This study used cross-framework AST static analysis spanning React, Vue, and Angular to scan 500 high-impact frontend repositories, and used 5 controlled benchmarks to quantify the cost of frontend memory leaks caused by “missing cleanup.” The core conclusion is: this kind of problem is extremely common in production code, and its memory growth is approximately linear and can be reproduced consistently.

## Problem
- The paper aims to answer: how common are “chronic” memory leaks in frontend single-page applications, and how much retained heap growth does each missed cleanup during component mount/unmount actually cause.
- This matters because such leaks usually do not throw errors immediately, but instead gradually cause stuttering, frame drops, freezes, or even tabs being killed by the system during long sessions, frequent navigation, or in mobile and Electron scenarios.
- Existing lint/tools do not fully cover these issues. Common cases are often missed, such as missing cleanup in `useEffect`, failing to unsubscribe from `.subscribe()`, or not saving the stop handle from `watch()`.

## Approach
- The author built Babel-based AST detectors for React, Vue, and Angular respectively, matching whether “resource acquisition” and “resource release” appear in pairs, such as `addEventListener/removeEventListener`, `subscribe/unsubscribe`, `watch/stop`, and `requestAnimationFrame/cancelAnimationFrame`.
- The detectors were run on 500 public and mature repositories, covering 714,217 files, with findings categorized by leak type, context, and severity.
- To quantify the real cost, the author designed 5 controlled benchmark scenarios: React event listeners, Vue timers, Angular subscriptions, Vue watchers, and RAF; each scenario ran 100 mount/unmount cycles, 50 independent repetitions, with forced GC before every measurement.
- Simply put, the method was: first find “forgotten cleanup” patterns in large-scale real-world code, then measure in small controlled experiments how much extra memory each missed cleanup retains.

## Results
- Static analysis found that 430 of the 500 repositories had at least 1 missing-cleanup pattern, for a prevalence of **86.0%**; in total, **55,864** potential leak instances were found across **714,217** files.
- Among the main patterns, `setTimeout/setInterval`-related issues were the most common; `setTimeout` alone accounted for **40%** of all findings, with **10,616** cases of unremoved event listeners; Vue `watch` without a saved stop handle appeared **3,360** times, `watchEffect` **629** times; and missing `cancelAnimationFrame` appeared **1,230** times.
- The results across the 5 benchmark scenarios were highly consistent: after **100 cycles**, the BAD versions without cleanup retained about **804–819 KB** of heap, or roughly **~8 KB/cycle**; the properly cleaned-up GOOD versions retained only **2.4–2.6 KB total**, close to the noise floor.
- In the React `useEffect` scenario: BAD averaged **807 KB**, GOOD **2.4 KB**, with a standard deviation of about **±37 KB**; the author says the 95% CI and SEM indicate stable results, with SEM at **5.2 KB**.
- In terms of statistical significance, all scenarios reported **p < 0.001**; effect sizes were extremely large, for example **Cohen’s d = 21.8** in the React scenario and **d = 820.3** in the Angular subscription scenario, indicating that the BAD and GOOD distributions were almost completely separated.
- The author claims that the 5 benchmarked patterns correspond to **53,313 / 55,864 = 95.4%** of the scan findings, and summarizes the takeaway as: missing cleanup is not an edge case, but a predictable, linearly accumulating engineering problem that usually requires only a “one-line fix.”

## Link
- [https://stackinsight.dev/blog/memory-leak-empirical-study/](https://stackinsight.dev/blog/memory-leak-empirical-study/)
