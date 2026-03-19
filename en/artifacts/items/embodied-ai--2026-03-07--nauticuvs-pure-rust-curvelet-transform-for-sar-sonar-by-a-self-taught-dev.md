---
source: hn
url: https://news.ycombinator.com/item?id=47292406
published_at: '2026-03-07T23:15:21'
authors:
- NautiDogSV
topics:
- curvelet-transform
- sar-sonar
- rust
- signal-processing
- image-denoising
relevance_score: 0.05
run_id: materialize-outputs
language_code: en
---

# Nauticuvs – pure-Rust curvelet transform for SAR sonar, by a self-taught dev

## Summary
Nauticuvs is a pure-Rust implementation of a Fast Discrete Curvelet Transform (FDCT) library for SAR sonar image processing. Its core value is using curvelets' more efficient representation of curved edges to support denoising, edge enhancement, and downstream analysis in maritime search and rescue.

## Problem
- Side-scan sonar images often contain curved structures such as hull shadows, seafloor targets, and debris, and traditional wavelets are not efficient enough at representing these curved edges.
- In search-and-rescue scenarios, better sonar denoising and edge enhancement directly affect target discovery, search planning, and decision-making efficiency, so this has real practical significance.
- Related tools are not sufficiently accessible in civilian/volunteer search-and-rescue systems, and the author wants to build open-source signal-processing infrastructure that can be freely used.

## Approach
- This work implements **Fast Discrete Curvelet Transform (FDCT via wrapping)**, corresponding to the curvelet transform scheme of Candès/Donoho 2006.
- The core mechanism can be understood simply as decomposing an image into a set of basis functions organized by **scale, orientation, and position**, where curvelets follow **parabolic scaling** (width ≈ length²), making them especially good at representing curved edges.
- Compared with wavelets, curvelets can preserve more important structural information in images containing curved contours using fewer or the same number of coefficients.
- From an engineering perspective, the library is implemented in **pure Rust** and serves as a low-level module for the larger CESARops system, aimed at search-and-rescue workflows such as drift prediction, search planning, and sonar analysis.

## Results
- The text **does not provide paper-style quantitative experimental results**; it gives no datasets, PSNR/SSIM, detection rates, runtime, or numerical comparisons with baseline methods.
- The strongest technical claim is that curvelets, because they satisfy **width ≈ length²** parabolic scaling, are "significantly more efficient than wavelets" for images with curved edges.
- The strongest application claim is that in **side-scan sonar** scenarios, it can achieve **better denoising and edge enhancement** under the "**same coefficient budget**," for target structures such as hull shadows, seafloor targets, and debris.
- It also claims that the library has been **published to crates.io** and is positioned as the signal-processing foundation of the open-source search-and-rescue platform **CESARops**, but no benchmark figures are reported.

## Link
- [https://news.ycombinator.com/item?id=47292406](https://news.ycombinator.com/item?id=47292406)
