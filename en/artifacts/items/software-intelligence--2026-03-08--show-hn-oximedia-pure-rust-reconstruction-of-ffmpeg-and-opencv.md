---
source: hn
url: https://github.com/cool-japan/oximedia
published_at: '2026-03-08T22:56:39'
authors:
- kitasan
topics:
- rust
- multimedia-framework
- computer-vision
- ffmpeg-replacement
- opencv-replacement
- memory-safety
relevance_score: 0.36
run_id: materialize-outputs
language_code: en
---

# Show HN: OxiMedia – Pure Rust Reconstruction of FFmpeg and OpenCV

## Summary
OxiMedia is a unified multimedia/computer vision framework that reconstructs FFmpeg and OpenCV in pure Rust, emphasizing freedom from patent burdens, memory safety, and zero system-level C/Fortran dependencies. It aims to replace the problems of complex builds, patent risk, and security vulnerabilities in traditional C/C++ multimedia stacks.

## Problem
- Existing multimedia and vision infrastructure mainly depends on **FFmpeg (C)** and **OpenCV (C++)**, with common pain points including memory safety vulnerabilities, complex build chains, and heavy system library dependencies.
- Traditional stacks are also often tied to **patent-encumbered codecs** (such as H.264/H.265/AAC), increasing legal, licensing, and distribution costs.
- For developers and deployers, installation, cross-platform release, browser execution, and unified media + CV workflows are all cumbersome, creating demand for a safer and easier-to-integrate alternative.

## Approach
- Using a **clean-room pure Rust implementation**, it integrates FFmpeg-style media processing capabilities and OpenCV-style computer vision capabilities into a unified framework.
- The core mechanism is straightforward: it provides a **modular crate system + DAG filtering/transcoding pipeline**, allowing codec processing, packaging, streaming protocols, analysis, detection, enhancement, and other capabilities to work together within the same processing graph.
- The design adheres to **`#![forbid(unsafe_code)]`, Tokio async-first, no C/Fortran dependencies by default, single-binary distribution, and WASM support**, reducing the build and security problems of traditional native media stacks at the root.
- On the media side, it covers royalty-free codecs such as AV1/VP9/Opus/FLAC, containers such as MP4/MKV/OGG, and protocols such as HLS/DASH/RTMP/SRT/WebRTC; on the vision side, it covers detection, tracking, stabilization, denoising, shot analysis, color management, quality assessment, and forensics.

## Results
- The project states that it has reached a **production-grade framework at v0.1.1 (2026-03-10)**.
- In terms of code scale, the author claims to maintain **97 stable crates** and about **1.49M SLOC**, covering the foundation layer, transcoding graph, audio/video, CV, quality analysis, services, and binding layers.
- In terms of engineering constraints, it explicitly requires **zero unsafe code** (under default features), **zero clippy warnings**, and **pure Rust default dependencies**, while providing multi-entry integration through Rust/Python/WASM/npm/CLI.
- In terms of claimed functionality, it supports **AV1/VP9/VP8/Theora, Opus/Vorbis/FLAC/MP3**, containers **MP4/MKV/MPEG-TS/OGG**, protocols **HLS/DASH/RTMP/SRT/WebRTC/SMPTE 2110**, as well as quality analysis capabilities such as **PSNR/SSIM/VMAF**.
- The paper excerpt **does not provide benchmark tests, accuracy, throughput, latency, or direct quantitative comparisons with FFmpeg/OpenCV**, so the current “breakthrough results” are mainly claims about scope and engineering completeness rather than quantitatively validated performance/SOTA metrics.
- It also explicitly states that it will **never support** several patent-encumbered formats: **H.264, H.265, H.266, AAC, AC-3/E-AC-3, DTS**, and positions “patent freedom” as a key differentiator.

## Link
- [https://github.com/cool-japan/oximedia](https://github.com/cool-japan/oximedia)
