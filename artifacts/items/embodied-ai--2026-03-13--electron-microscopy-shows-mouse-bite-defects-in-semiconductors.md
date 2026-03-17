---
source: hn
url: https://news.cornell.edu/stories/2026/03/electron-microscopy-shows-mouse-bite-defects-semiconductors
published_at: '2026-03-13T23:30:08'
authors:
- hhs
topics:
- electron-microscopy
- semiconductor-defects
- electron-ptychography
- chip-failure-analysis
relevance_score: 0.01
run_id: materialize-outputs
---

# Electron microscopy shows 'mouse bite' defects in semiconductors

## Summary
这项工作利用高分辨率三维电子显微成像，首次直接看到现代半导体晶体管中原子尺度的界面缺陷（“mouse bites”）。其意义在于为芯片研发和失效分析提供了一种此前几乎无法实现的原子级调试工具。

## Problem
- 现代晶体管已缩小到约 **15–18 个原子宽**，器件性能会被原子级界面粗糙和缺陷显著影响。
- 传统表征多依赖投影图像，难以直接恢复复杂三维结构中的原子排布，因此很难定位导致性能下降的真实缺陷。
- 随着半导体从平面结构走向复杂三维结构，制造步骤多达数百到上千步，缺陷调试与工艺优化变得更关键也更困难。

## Approach
- 使用 **electron ptychography（电子叠层相位成像）**：让电子穿过晶体管后，由高精度像素阵列探测器记录散射图样。
- 通过比较不同扫描位置上的散射变化，进行计算重建，得到极高分辨率的三维原子结构图像。
- 关键硬件是研究团队共同开发的 **EMPAD** 探测器，它能精确测量电子散射信号，从而支持超高分辨率成像。
- 在与 **TSMC、ASM** 合作下，对由 **Imec** 制备的现代半导体样品进行成像，并逐原子追踪界面位置与粗糙度。

## Results
- 论文声称 **首次** 检测到会破坏芯片性能的 **原子尺度缺陷**，并直接观察到晶体管沟道界面的粗糙缺陷“**mouse bites**”。
- 研究指出这些粗糙缺陷来源于器件 **优化生长过程** 中形成的界面问题，为制造流程中的缺陷来源提供了直接证据。
- 文中给出的器件尺度是晶体管沟道仅 **约 15–18 个原子宽**，说明该方法已能工作在当前最前沿的原子级器件尺度。
- 文中未提供具体的定量性能指标（如分辨率数值、误差、良率提升或与基线方法的数值比较）。最强的具体主张是：该方法能在开发阶段对芯片进行原子级 **debugging / fault-finding**，并有望影响手机、汽车、AI 数据中心和量子计算芯片等广泛应用。

## Link
- [https://news.cornell.edu/stories/2026/03/electron-microscopy-shows-mouse-bite-defects-semiconductors](https://news.cornell.edu/stories/2026/03/electron-microscopy-shows-mouse-bite-defects-semiconductors)
