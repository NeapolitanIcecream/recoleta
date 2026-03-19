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
- cli-toolkit
- simpleitk
- mmengine
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# ITKIT: Feasible CT Image Analysis based on SimpleITK and MMEngine

## Summary
ITKIT is an open-source toolkit for CT image analysis, focusing on providing a complete reproducible pipeline from DICOM/volume data preprocessing to 3D segmentation training, inference, and evaluation. Its core selling point is not proposing a new segmentation model, but integrating SimpleITK and MMEngine into a low-barrier, CLI-first, configurable engineering pipeline.

## Problem
- Medical CT segmentation is often constrained by engineering issues such as chaotic data preprocessing, inconsistent formats, nonstandard orientation/spacing, and missing or inconsistent labels, all of which directly limit the upper bound of model performance.
- Although existing frameworks are powerful, they often provide insufficient support for CLI workflows and beginner friendliness, making it difficult for clinical users or users with weak programming skills to quickly complete the full process from data organization to training and deployment.
- There is a need for a standardized, reproducible, low-compute infrastructure that connects data preparation, training, evaluation, and deployment, which is important for real clinical adoption and multi-center collaboration.

## Approach
- Uses a **pair-centric** standard data model: images and labels are paired by fixed directories and filenames, with metadata such as spacing, size, and orientation centrally maintained in `meta.json`/`crop_meta.json`.
- Provides a CLI toolchain covering key steps, including metadata inspection, orientation adjustment, resampling, patch splitting, augmentation, label extraction/remapping, data structure conversion, and segmentation evaluation; metadata is automatically synchronized after data changes.
- The deep learning component is based on OneDL-MMEngine, supporting 2D/3D segmentation, sliding-window inference, configuration-driven training, and integration with multiple classic networks (such as MedNeXt, UNETR, SegFormer3D, and Mamba-series models).
- Compatible with MONAI, TorchIO, and 3D Slicer, supports native/MMEngine and ONNX inference backends, and enables visualization deployment through a 3D Slicer front-end/back-end decoupling extension.
- The core mechanism can be understood simply as packaging the most common but scattered engineering steps in CT segmentation into a unified data specification plus command-line commands, then connecting them to mature training frameworks and inference interfaces.

## Results
- The paper reports **12 typical experiments** to verify that ITKIT can cover most basic scenarios, but the experiments mainly validate toolchain usability and end-to-end operation under different backend configurations, rather than proposing a new SOTA model.
- On **AbdomenCT1K**, **TorchIO backend + SegFormer3D** achieved the best result: **Dice 94.08, IoU 89.50, Recall 94.91, Precision 93.29**.
- On the same dataset, **TorchIO + MedNeXt** achieved: **Dice 88.25, IoU 80.88, Recall 85.94, Precision 91.36**.
- Under the **Native backend**, **SegFormer3D** achieved **Dice 87.25**, outperforming **MedNeXt 83.41**; the corresponding IoU values were **79.84 vs 75.98**.
- Results under the **MONAI backend** were significantly lower: **MedNeXt Dice 45.52**, **SegFormer3D Dice 41.63**; much lower than the best **TorchIO + SegFormer3D (94.08)**.
- The paper’s strongest concrete claim is that ITKIT can connect the full CT segmentation workflow from data preprocessing to training/inference/visualized deployment through a unified CLI and configurable approach, and can deliver a runnable end-to-end baseline on at least one public dataset.

## Link
- [http://arxiv.org/abs/2603.14255v1](http://arxiv.org/abs/2603.14255v1)
