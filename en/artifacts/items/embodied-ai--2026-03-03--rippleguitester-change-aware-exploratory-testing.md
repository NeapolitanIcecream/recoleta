---
source: arxiv
url: http://arxiv.org/abs/2603.03121v1
published_at: '2026-03-03T15:56:49'
authors:
- Yanqi Su
- Michael Pradel
- Chunyang Chen
topics:
- gui-testing
- change-impact-analysis
- llm-based-testing
- differential-testing
- regression-detection
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# RippleGUItester: Change-Aware Exploratory Testing

## Summary
RippleGUItester is a GUI exploratory testing system for code changes. It uses LLMs to analyze change impact, generate and execute scenarios, and then detect user-visible regressions through differential analysis between pre-change and post-change versions. It mainly addresses the limitation of traditional regression testing, which covers fixed paths and struggles to uncover side effects induced by changes.

## Problem
- The paper addresses the problem that **user-visible defects introduced by code changes at the GUI layer are difficult to detect early**; this is important because the authors found that among **97,347** PRs in Firefox, **11,910 (12.2%)** still introduced new bugs, showing that even with testing, CI, and code review, change-induced defects remain common.
- These defects are hard to test because triggering them often requires **diverse event sequences**, **specific test data**, and **cross-scenario side effects**, rather than simply rerunning existing regression test cases.
- Even when a problem is triggered, the **test oracle for GUI defects is hard to formalize**; many abnormal manifestations are unstructured visual or behavioral differences that are difficult to enumerate in advance.

## Approach
- The core mechanism can be understood simply as: **treat a code change as the “epicenter of a ripple”**, first infer which user scenarios it may affect, then run the pre-change and post-change versions separately through the GUI, and finally compare the differences to find bugs.
- The system is divided into three parts: **Scenario Generator** uses an LLM to combine change intent with the code patch for change-impact analysis and generate initial test scenarios; it then uses a knowledge base built from historical issues/PRs to expand **alternative event sequences** and fill in executable **concrete test data**.
- **Scenario Executor** translates high-level natural-language steps into structured UI actions (such as click, input, scroll, and **11** other action types) and executes them in a containerized environment on both the pre-change and post-change versions.
- **Bug Detector** performs differential analysis on the execution results of the two versions, compares visual changes in GUI screenshots, and combines them with the **change intent** expressed in natural language to determine whether those changes are expected updates or unintended bugs, i.e., it uses **multimodal bug detection**.
- One distinctive design is the use of **preceding change intents**: through code tracing, it identifies prior PRs/issues that modified the same code region and uses them as prompts for relevant old scenarios to discover cross-scenario side effects.

## Results
- The approach is evaluated on **4** real software systems: **Firefox, Zettlr, JabRef, and Godot**; the test subjects are **hundreds of real-world code changes**, and the abstract does not provide a more precise total number of PRs.
- RippleGUItester identified **26** previously unknown bugs that still exist in the latest versions; these bugs had **not been detected by existing test suites, CI pipelines, or code review**.
- After reporting, their status was: **16** fixed, **2** confirmed, **6** still under discussion, and **2** marked as intended behavior.
- In terms of cost, each PR requires on average **54.8 minutes** and **5.99 USD**, indicating the method is effective but relatively expensive.
- The paper claims its key breakthrough is that it is, according to the authors, the **first change-aware GUI testing system**, capable of systematically exploring the ripple effects of code changes rather than only covering predefined paths or performing unguided random exploration.
- Beyond the figures above, the provided excerpt does not include standardized metrics (such as precision/recall) or quantitative comparison tables with specific baseline methods.

## Link
- [http://arxiv.org/abs/2603.03121v1](http://arxiv.org/abs/2603.03121v1)
