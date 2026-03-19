---
source: arxiv
url: http://arxiv.org/abs/2603.06107v1
published_at: '2026-03-06T10:05:29'
authors:
- Lucas Berg
- Lukas Krodinger
- Stephan Lukasczyk
- Annibale Panichella
- Gordon Fraser
- Wim Vanhoof
- Xavier Devroey
topics:
- automated-test-generation
- python-c-extensions
- fault-detection
- process-isolation
- unit-testing
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# Real-World Fault Detection for C-Extended Python Projects with Automated Unit Test Generation

## Summary
This paper addresses the problem that automatic unit test generation for Python projects with C extensions is easily interrupted by native code crashes, and proposes a Pynguin execution model based on subprocess isolation. This method allows the test generator to keep working even when it encounters fatal errors such as segmentation faults, and to automatically produce reproducible crash-triggering tests.

## Problem
- Many Python libraries improve performance through C/C++ extensions, but this allows native exceptions to bypass Python’s exception mechanism and directly crash the interpreter.
- Traditional automated test generation tools execute tests within the same interpreter; once a segfault/bus error is triggered, the entire generation process stops, making faults hard to discover and impossible to reproduce and analyze.
- This matters because when these crashes occur on public API calls, they are real software defects that affect reliability and may even introduce security risks.

## Approach
- The core idea is simple: separate “test generation” from “test execution,” so that each generated test runs in an isolated subprocess rather than only in a thread within the same process.
- In this way, if a test triggers a C-extension crash, it only kills that subprocess and does not kill the main process running Pynguin’s search and coverage optimization.
- The authors refactored Pynguin’s observer architecture, splitting observers into main-process observers and remote observers, and collecting coverage, assertions, and execution results through serialization and inter-process communication.
- The system exports pytest tests that trigger crashes and adds a re-execution step to verify whether these crash-revealing tests are reproducible.
- To reduce overhead, the paper also designs three automatic execution-mode selection strategies: heuristic, restart, and combined, switching between thread/subprocess execution for pure Python modules and FFI modules.

## Results
- The authors constructed a new real-world dataset, DS-C, containing **1,648** modules related to C extensions from **21** popular Python libraries.
- After using subprocess execution, the system automatically generated **120,176** tests for these libraries and identified **213** unique crash causes.
- Through manual analysis of these crashes, the authors confirmed **32** previously unknown real faults and have reported them to the corresponding development teams.
- The abstract claims that subprocess execution enables automated testing to cover “up to **56.53685674547984** more modules”; the original excerpt does not provide a clearer unit or comparison baseline, but the meaning is that compared with non-subprocess execution, it can successfully test more modules.
- The qualitative breakthrough is that the method not only prevents the test generator itself from crashing, but also continues exploring non-crashing code regions while producing reproducible crash tests to support debugging and fault localization.

## Link
- [http://arxiv.org/abs/2603.06107v1](http://arxiv.org/abs/2603.06107v1)
