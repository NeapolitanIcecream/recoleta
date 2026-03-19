---
source: hn
url: https://plasma-bigscreen.org
published_at: '2026-03-06T23:59:16'
authors:
- PaulHoule
topics:
- linux-tv-interface
- kde-plasma
- open-source-desktop
- 10-foot-ui
- htpc
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Plasma Bigscreen – 10-foot interface for KDE plasma

## Summary
Plasma Bigscreen is an open-source Linux big-screen interface for TVs, HTPCs, and set-top boxes, emphasizing customizability, an open ecosystem, and privacy protection. It is essentially a TV-friendly desktop environment based on KDE Plasma for the "10-foot interface" scenario, rather than a robotics or foundation-model research paper.

## Problem
- It addresses the common issues of closed systems, lack of user control, and insufficient privacy and trustworthiness in TVs and set-top boxes.
- There is a need for a Linux big-screen interface suited to "couch-distance" use, supporting multiple input methods such as remotes, CEC, game controllers, keyboard and mouse, and phones.
- This matters because existing TV platforms are mostly closed ecosystems; an open alternative can provide users and manufacturers with greater controllability, extensibility, and auditability.

## Approach
- The core approach is to package the open-source Linux desktop stack of KDE Plasma/KWin/KDE Frameworks/Qt/Kirigami into a desktop environment optimized specifically for large TV screens.
- In terms of interface design, it adopts a TV-friendly approach: users can browse apps, switch tasks, and change settings from couch distance, and use a one-button Home overlay to quickly search, open settings, return to the home screen, or switch apps.
- For interaction, it supports unified access for multiple input methods, including TV remote via CEC, game controller, keyboard and mouse, and phone control through KDE Connect.
- For the ecosystem, it does not build its own closed app store, but instead reuses Linux distribution package managers and Flathub to run existing Linux apps such as Steam, Kodi, Jellyfin, and VacuumTube.
- In product positioning, it emphasizes being fully open source, portable to any Linux-supported device, and allowing both the community and manufacturers to develop or integrate it into their own products.

## Results
- The text **does not provide quantitative experimental results**; there are no datasets, metrics, baselines, or numerical comparisons, so there are no verifiable performance breakthrough figures.
- The strongest concrete claim is that the system can be installed as a standard Linux desktop environment on supported devices and is intended for use with TVs, HTPCs, and set-top boxes.
- The supported input methods explicitly include **4+ categories**: CEC remote, game controller, keyboard and mouse, and phone (KDE Connect).
- It provides a complete big-screen settings app for configuring system options such as display, network, and appearance, with navigation supported by remote or controller.
- The accessible app ecosystem is claimed to include Steam, Kodi, Jellyfin, YouTube (via VacuumTube), and "thousands more" Linux/Flathub apps, but the text does not provide precise app-count statistics or compatibility test results.

## Link
- [https://plasma-bigscreen.org](https://plasma-bigscreen.org)
