---
source: hn
url: https://news.cornell.edu/stories/2026/03/electron-microscopy-shows-mouse-bite-defects-semiconductors
published_at: '2026-03-13T23:30:08'
authors:
- hhs
topics:
- electron-microscopy
- semiconductor-defects
- 3d-imaging
- electron-ptychography
- chip-debugging
relevance_score: 0.09
run_id: materialize-outputs
language_code: zh-CN
---

# Electron microscopy shows 'mouse bite' defects in semiconductors

## Summary
这项工作首次用高分辨率三维电子成像直接看到了先进半导体晶体管中的原子级界面缺陷，即所谓的“mouse bites”。其意义在于为芯片开发阶段的失效分析、工艺调试和下一代器件优化提供了此前几乎不可替代的直接观测工具。

## Problem
- 现代晶体管已经缩小到原子尺度，沟道宽度仅约 **15–18 个原子**，此时“每一个原子的位置”都会影响性能。
- 现有故障分析长期难以直接看清三维晶体管内部的原子级粗糙度和缺陷，只能依赖投影图像间接推断。
- 这些缺陷会破坏载流通道、拖慢器件表现，并影响从手机、汽车到 AI 数据中心和量子计算芯片的可靠性与性能。

## Approach
- 使用 **electron ptychography（电子叠层成像）**：让电子穿过晶体管，再记录不同扫描位置下电子散射图样的变化。
- 借助 **EMPAD 像素阵列电子探测器** 高精度采集散射数据，再通过计算重建出高保真三维原子结构图像。
- 在与 **TSMC、ASM** 合作下，对现代半导体样品进行成像，并对原子位置进行跟踪分析。
- 由此直接测量晶体管沟道界面粗糙度，识别出在优化生长过程中形成的原子级缺陷“mouse bites”。

## Results
- **首次** 在计算机芯片中检测到会破坏性能的 **原子尺度缺陷**，这是文中最核心的突破性结论。
- 在现代晶体管的沟道界面中直接观察到粗糙缺陷“**mouse bites**”，并将其归因于优化生长工艺中形成的界面缺陷。
- 文中给出的器件尺度信息显示：晶体管沟道仅约 **15–18 个原子宽**，说明该方法已能在这一极端尺度上进行有效表征。
- 文章未提供标准 benchmark 式的定量指标（如误差率、吞吐、与基线方法数值对比）；最具体的性能声明是该探测与成像体系曾实现“**世界最高分辨率图像**”级别的原子成像能力，并支持对制程步骤后的结构变化进行直接观察与调试。

## Link
- [https://news.cornell.edu/stories/2026/03/electron-microscopy-shows-mouse-bite-defects-semiconductors](https://news.cornell.edu/stories/2026/03/electron-microscopy-shows-mouse-bite-defects-semiconductors)
