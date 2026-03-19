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
- subprocess-isolation
- software-testing
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Real-World Fault Detection for C-Extended Python Projects with Automated Unit Test Generation

## Summary
This paper addresses the problem that automated unit test generation for Python projects with C extensions is easily interrupted by native-code crashes, and proposes a subprocess-isolated Pynguin execution model. Its core value is enabling the test generator to continue operating on real-world C-extension libraries, detect crashes, and produce reproducible crash-triggering test cases.

## Problem
- Many Python libraries call C/C++ code through FFI for performance, but native exceptions (such as segmentation faults) can bypass Python’s exception mechanism and crash the interpreter directly.
- Traditional automated test generation executes tests within the same interpreter; once the SUT crashes, the entire generation process stops, making it impossible to continue covering other code and difficult to stably reproduce and analyze faults.
- This matters because when such crashes occur through public API calls, they are real defects that affect software reliability and safety in scientific computing, data analysis, and the machine learning ecosystem.

## Approach
- The authors decouple Pynguin’s "test generation" and "test execution": each generated test is no longer run only in a thread, but is instead executed in an isolated subprocess.
- Put simply: if a test triggers a C-extension crash, it kills only that subprocess rather than the main test generator; after detecting the crash, the main process saves the test and continues searching for other tests.
- To support cross-process execution, the authors refactored the observer architecture: they separated observers that only need to be maintained in the main process from remote observers that must collect coverage/assertion information during remote execution, and transfer them between processes via serialization.
- The system also adds crash-test export and re-execution mechanisms to confirm the reproducibility of crash-revealing tests, making it easier for developers to debug and fix issues.
- To balance robustness and overhead, the authors add three automatic execution-mode selection strategies: heuristic (choose subprocess after detecting FFI), restart (use threads first, switch after a crash), and combined (a combination of both).

## Results
- The authors constructed a new dataset, DS-C, containing **1,648** modules with C-extensions from **21** popular Python libraries.
- After using subprocess execution, they automatically generated **120,176** tests and found **213** unique crash causes.
- Among these, manual analysis identified **32** previously unknown real defects, which have already been reported to the corresponding development teams.
- The paper abstract states that subprocess execution enabled automated testing to cover "up to **56.53685674547984** more modules"; the excerpt does not further explain the unit/baseline of this value, but its core meaning is that compared with non-isolated execution, more modules can be tested successfully.
- In a specific case, the generated crash test revealed that SciPy’s `idd_reconid` performs insufficient parameter validation, and invalid input can lead to a segmentation fault.
- The excerpt does not provide complete table values for coverage increase/decrease, but it clearly states that for modules containing FFI, subprocess execution can prevent the overall generation process from crashing and continue testing the non-crashing parts.

## Link
- [http://arxiv.org/abs/2603.06107v1](http://arxiv.org/abs/2603.06107v1)
