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
relevance_score: 0.04
run_id: materialize-outputs
language_code: en
---

# Show HN: OxiMedia – Pure Rust Reconstruction of FFmpeg and OpenCV

## Summary
OxiMedia is a unified multimedia/computer vision framework that reconstructs FFmpeg and OpenCV in pure Rust, emphasizing freedom from patent constraints, memory safety, and zero system-level C/Fortran dependencies. It aims to converge traditionally fragmented and complex media processing and vision capabilities into a production-grade ecosystem that can be added directly with `cargo add`.

## Problem
- Existing **FFmpeg** and **OpenCV**, while de facto standards, depend on C/C++, complex build chains, and large numbers of system libraries, creating deployment difficulty, high maintenance costs, and security risks.
- FFmpeg often involves patent-restricted codecs such as **H.264/H.265/AAC**; the project emphasizes that this creates obstacles for licensing, distribution, and commercialization.
- For developers and product teams, there is a lack of an integrated alternative that simultaneously covers media processing and computer vision while also being **memory-safe + pure Rust + patent-free**.

## Approach
- Reconstruct the core capabilities of FFmpeg and OpenCV with a **clean-room pure Rust implementation**, and unify codec support, packaging, streaming, transcoding, filter graphs, CV, quality analysis, and related capabilities into the same framework.
- Adhere to **`#![forbid(unsafe_code)]`**, default to **no C/Fortran dependencies**, and use a **Tokio-based async-first** architecture, replacing traditional C/C++ multimedia stacks with compile-time safety and concurrency capabilities.
- At the codec layer, support only royalty-free formats such as **AV1, VP9, VP8, Theora, Opus, Vorbis, FLAC**, and explicitly reject patent-restricted formats such as **H.264/H.265/H.266/AAC/AC-3/DTS**.
- Use a modular crate architecture to connect media infrastructure, processing pipelines, CV/analysis, and the CLI/Python/WASM/server application layers into a single ecosystem.

## Results
- The project claims to have reached a **production-grade framework at v0.1.1 (2026-03-10)**, and reports an ecosystem scale of **97 crates** and about **1.49M SLOC**.
- Its claimed feature coverage spans both multimedia and vision: support for codecs (such as **AV1/VP9/Opus/FLAC**), containers (**MP4/MKV/MPEG-TS/OGG**), protocols (**HLS/DASH/RTMP/SRT/WebRTC/SMPTE 2110**), as well as detection, tracking, stabilization, denoising, calibration, VMAF/PSNR/SSIM, and forensics.
- The engineering constraints present clear, verifiable claims: **zero unsafe code** (under default features), **zero warnings**, default **100% Pure Rust**, buildable as a **single binary**, and support for **Python (`pip install oximedia`)**, **WASM (`npm install @cooljapan/oximedia`)**, and CLI distribution.
- The text **does not provide standard benchmark tests or accuracy/speed comparison figures**, so there is no evidence that it already surpasses FFmpeg/OpenCV in performance, compression efficiency, vision-task metrics, or stability; the strongest concrete claims are mainly about architectural completeness, dependency purity, and breadth of support.

## Link
- [https://github.com/cool-japan/oximedia](https://github.com/cool-japan/oximedia)
