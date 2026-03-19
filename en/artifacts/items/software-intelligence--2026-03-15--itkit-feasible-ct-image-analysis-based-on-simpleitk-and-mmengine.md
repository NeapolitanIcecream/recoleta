---
source: arxiv
url: http://arxiv.org/abs/2603.14255v1
published_at: '2026-03-15T07:25:06'
authors:
- Yiqin Zhang
- Meiling Chen
topics:
- medical-imaging
- ct-segmentation
- cli-tooling
- simpleitk
- mmengine
- 3d-slicer
relevance_score: 0.21
run_id: materialize-outputs
language_code: en
---

# ITKIT: Feasible CT Image Analysis based on SimpleITK and MMEngine

## Summary
ITKIT is an open-source engineering toolkit for CT medical image analysis, emphasizing a complete pipeline from DICOM to 3D segmentation training and inference, along with a beginner-friendly CLI. It is built on SimpleITK and OneDL-MMEngine, aiming to balance ease of use, configurability, and cross-framework compatibility.

## Problem
- Medical CT segmentation depends not only on model architecture, but is often more constrained by data preprocessing, geometric consistency, label pairing, and the quality of reproducible workflows.
- Although existing tools are powerful, they often lack sufficient CLI support and have a high barrier to entry, making it difficult for clinical users or users with limited programming experience to quickly complete the full process from raw DICOM to trainable data and inference deployment.
- There is a lack of a lightweight and practical solution that integrates data organization, preprocessing, training, evaluation, and visualization while remaining compatible with MONAI/TorchIO/3D Slicer.

## Approach
- Proposes ITKIT: it adopts a strict paired data model, standardizing image/label directories, filename matching, and meta.json / crop_meta.json metadata management to reduce data mismatches and loss of geometric information.
- Provides a CLI covering key steps, including metadata inspection, orientation correction, resampling, patch splitting, augmentation, label extraction/remapping, dataset structure conversion, and segmentation evaluation; metadata is automatically updated when data changes.
- The deep learning component is built on OneDL-MMEngine, supporting 2D/3D segmentation, sliding-window inference, asynchronous H2D/D2H data flow, and configuration-driven training reproducibility.
- Integrates multiple public datasets and representative networks, including CNN, Transformer, and Mamba series; also provides conversion to MONAI and TorchIO and multi-backend data loading.
- Provides a 3D Slicer extension, using QT on the frontend and Flask on the backend to connect ONNX or native models, enabling real-time inference and visualization in an isolated environment.

## Results
- The paper reports **12 typical experiments** to validate ITKIT's usability in basic scenarios, but the quantitative tables in the main text actually show results only on **AbdomenCT1K** with **3 data backends × 2 models**.
- On **AbdomenCT1K**, **TorchIO + SegFormer3D** achieved the best results: **Dice 94.08, IoU 89.50, Recall 94.91, Precision 93.29**.
- On the same dataset, **TorchIO + MedNeXt** reached **Dice 88.25, IoU 80.88, Recall 85.94, Precision 91.36**; **Native + SegFormer3D** achieved **Dice 87.25, IoU 79.84, Recall 84.53, Precision 90.31**; **Native + MedNeXt** achieved **Dice 83.41, IoU 75.98, Recall 83.43, Precision 83.69**.
- The **MONAI backend** performed significantly worse in this baseline: **MedNeXt Dice 45.52** and **SegFormer3D Dice 41.63**, with corresponding IoUs of **38.34** and **35.06**.
- Compared with **Native + SegFormer3D**, **TorchIO + SegFormer3D** improved Dice by **6.83** points (94.08 vs 87.25); compared with **MONAI + SegFormer3D**, the improvement was **52.45** points.
- The paper's main contribution is more focused on **engineering integration and usability validation** rather than proposing a new SOTA segmentation algorithm; it does not provide systematic comparisons against strong external baselines such as nnUNet or native MONAI pipelines.

## Link
- [http://arxiv.org/abs/2603.14255v1](http://arxiv.org/abs/2603.14255v1)
