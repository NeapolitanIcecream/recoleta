---
source: hn
url: https://alexalejandre.com/programming/interview-with-ngoldbaum/
published_at: '2026-03-12T23:24:34'
authors:
- birdculture
topics:
- python-free-threading
- gil-removal
- scientific-python
- numpy
- pyo3
- rust-in-python
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Lobsters Interview with Ngoldbaum

## Summary
This is not a robotics or machine learning research paper, but an interview with Nathan Goldbaum. Its core topics are Python’s removal of the GIL through free-threading, compatibility across the scientific Python ecosystem, Rust adoption, and open source maintenance practices.
It discusses why free-threaded Python should be advanced, the ABI and thread-safety issues encountered during ecosystem migration, and views on NumPy, PyO3, Cython, testing, and community governance.

## Problem
- The core problem the article addresses is that Python’s GIL limits the scalability of CPU-bound multithreading, causing pure Python coordination code to eventually become a bottleneck on multicore machines.
- This matters because the Python ecosystem for scientific computing, data processing, and Web/AI heavily depends on concurrency and native extensions; if threads cannot work efficiently, performance, developer experience, and ecosystem evolution are all constrained.
- The article also emphasizes related issues: many historical C/Cython extensions are not thread-safe, and old ABI assumptions, global state, and insufficient testing obstruct the rollout of free-threading.

## Approach
- The core mechanism is to advance CPython’s free-threaded build (in the direction of PEP 703), so that the interpreter no longer relies on the global interpreter lock to serialize thread execution.
- To make this mechanism truly usable, the author’s team has been incrementally refactoring foundational ecosystem components such as NumPy, Cython, setuptools, PyO3, and cffi, fixing issues related to global state, ABI compatibility, and thread safety.
- At the implementation level, the article explains that free-threading requires changes to PyObject layout, reference counting, and object lock design, so extension modules must adapt to the new ABI rather than simply “removing one lock.”
- At the validation level, the team uses tools such as `pytest-run-parallel` to expose implementations that depend on global state or are not thread-safe by repeatedly running tests concurrently.
- The article also advocates gradually replacing new C/Cython native code with Rust/PyO3 to reduce memory-unsafety issues and improve long-term maintainability.

## Results
- The article does not provide standard paper-style quantitative experimental results, benchmark datasets, or a unified performance table, so there are **no strict quantitative results that can be extracted**.
- Clear project milestones include: PEP 703 was approved in **October 2023**; the author says that in **March 2024** they began pushing foundational packages such as NumPy, Cython, and setuptools to adapt to the free-threaded interpreter.
- The author mentions having approximately **1,500 GitHub contributions in 2025** to illustrate the breadth of the ecosystem migration work, but this is not a research performance metric.
- The article claims that key components already advanced or helped toward support include **NumPy, PyO3, cffi, cryptography**, and that Greenlet also has “experimental support.”
- The strongest concrete claim about practical benefits is that free-threading can allow workflows that previously depended on multiprocessing to switch to multithreading, avoiding the extra overhead of data copying and pickle, while making better use of threads on multicore machines; however, the author also explicitly states that it is **not yet recommended to rely on it directly as a production default**.
- As for the future timeline, the author predicts that free-threaded Python may become more mainstream or even the only build around **3.16 or 3.17**, but this remains a forecast rather than a validated result.

## Link
- [https://alexalejandre.com/programming/interview-with-ngoldbaum/](https://alexalejandre.com/programming/interview-with-ngoldbaum/)
