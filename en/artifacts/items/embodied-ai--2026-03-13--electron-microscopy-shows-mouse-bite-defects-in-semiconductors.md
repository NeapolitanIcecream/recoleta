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
language_code: en
---

# Electron microscopy shows 'mouse bite' defects in semiconductors

## Summary
This work uses high-resolution 3D electron microscopy imaging to directly visualize, for the first time, atomic-scale interface defects (“mouse bites”) in modern semiconductor transistors. Its significance is that it provides a previously nearly impossible atomic-level debugging tool for chip R&D and failure analysis.

## Problem
- Modern transistors have shrunk to about **15–18 atoms wide**, and device performance can be significantly affected by atomic-scale interface roughness and defects.
- Traditional characterization mostly relies on projection images, making it difficult to directly recover atomic arrangements in complex 3D structures, and therefore hard to pinpoint the real defects causing performance degradation.
- As semiconductors have evolved from planar structures to complex 3D structures, with manufacturing steps numbering in the hundreds to thousands, defect debugging and process optimization have become both more critical and more difficult.

## Approach
- Use **electron ptychography**: after electrons pass through the transistor, a high-precision pixel array detector records the scattering patterns.
- By comparing changes in scattering at different scan positions, computational reconstruction is performed to obtain extremely high-resolution 3D images of the atomic structure.
- The key hardware is the **EMPAD** detector, jointly developed by the research team, which can precisely measure electron scattering signals and thereby support ultra-high-resolution imaging.
- In collaboration with **TSMC, ASM**, the team imaged modern semiconductor samples prepared by **Imec** and tracked interface position and roughness atom by atom.

## Results
- The paper claims the **first** detection of **atomic-scale defects** that can undermine chip performance, and directly observed rough interface defects in the transistor channel known as “**mouse bites**.”
- The study indicates that these rough defects originate from interface issues formed during the device **optimization growth process**, providing direct evidence for the source of defects in the manufacturing flow.
- The device scale given in the article is that the transistor channel is only **about 15–18 atoms wide**, showing that the method can already operate at the scale of today’s most advanced atomic-level devices.
- The article does not provide specific quantitative performance metrics (such as resolution values, error, yield improvement, or numerical comparisons with baseline methods). The strongest concrete claim is that this method can perform atomic-level **debugging / fault-finding** for chips during the development stage, and may affect a wide range of applications including phones, automobiles, AI data centers, and quantum computing chips.

## Link
- [https://news.cornell.edu/stories/2026/03/electron-microscopy-shows-mouse-bite-defects-semiconductors](https://news.cornell.edu/stories/2026/03/electron-microscopy-shows-mouse-bite-defects-semiconductors)
