---
source: hn
url: https://alexalejandre.com/programming/interview-with-ngoldbaum/
published_at: '2026-03-12T23:24:34'
authors:
- birdculture
topics:
- python-free-threading
- gil-removal
- cpython-abi
- scientific-python
- rust-bindings
relevance_score: 0.42
run_id: materialize-outputs
language_code: en
---

# Lobsters Interview with Ngoldbaum

## Summary
This is an interview centered on Nathan Goldbaum, with the core discussion focused on the engineering practice, challenges, and roadmap for migrating the Python ecosystem toward a no-GIL/free-threading build. It is not an academic paper, but rather an experience-based summary of Python scientific computing, extension ABI, thread-safety testing, and trends in Rust adoption.

## Problem
- Python’s GIL causes **CPU-bound Python orchestration code** to become a scalability bottleneck on multicore machines. Even if the underlying native code can already run in parallel, overall scalability remains constrained.
- The existing Python/C extension ecosystem has long assumed the presence of the GIL, hiding many **thread-safety issues, global state issues, and ABI assumptions**, which obstruct the adoption of a no-GIL interpreter.
- Although multiprocessing can work around the GIL, it introduces **data copying, pickle overhead, and usage complexity in environments such as Jupyter**, reducing the efficiency of scientific computing and data-processing workflows.

## Approach
- The core mechanism is advancing **PEP 703’s free-threaded CPython** into practice: allowing Python threads to no longer depend on the global interpreter lock, so multicore parallelism can be genuinely utilized.
- Supporting work is concentrated on **ecosystem compatibility and low-level refactoring**: adding support for free-threaded build in key foundational packages such as NumPy, Cython, setuptools, PyO3, and cffi.
- Key technical points include **reworking the CPython ABI and object layout**: under a free-threaded build, the `PyObject` layout changes and introduces mechanisms such as per-object locks, so extension layers that depend on the old ABI need to be rewritten or adapted, especially PyO3/FFI.
- For thread-safety validation, methods such as **pytest-run-parallel** are used to run tests concurrently and repeatedly in multithreaded pools, in order to expose implementation flaws that depend on global state, supplemented by explicit multithreaded testing patterns.
- The long-term direction also includes **driving adoption of Rust/PyO3 in Python extensions** to replace implementations in the more error-prone C/C++/Cython space.

## Results
- The article does not provide a rigorous benchmark table or paper-style quantitative results, so there is **a lack of reproducible performance metrics, datasets, and baseline numerical comparisons**.
- A key milestone: **PEP 703 was approved in October 2023**, marking the CPython project’s official acceptance of the free-threading path.
- Ecosystem timeline: the author says that in **March 2024** they began focusing on foundational projects such as NumPy, Cython, and setuptools, so that the free-threaded interpreter would be usable from the “bottom of the stack.”
- Staffing: the Steering Council required Meta to fund **2 full-time equivalents (2 FTE)** to support the ecosystem migration; the author mentions having made **about 1,500 GitHub contributions in 2025**, indicating a high level of engineering intensity.
- In terms of support status, the interview claims to have advanced compatibility progress in key projects such as **NumPy, PyO3, cffi, and Greenlet (experimental)**, and specifically notes that PyO3/cryptography-related support was prioritized to make large parts of the web stack usable.
- Future outlook: the author expects free-threading may become a more mainstream or even the only build target around **Python 3.16 or 3.17**, but clearly states that the community still needs to continue testing and fixing GC pauses and extension compatibility issues.

## Link
- [https://alexalejandre.com/programming/interview-with-ngoldbaum/](https://alexalejandre.com/programming/interview-with-ngoldbaum/)
