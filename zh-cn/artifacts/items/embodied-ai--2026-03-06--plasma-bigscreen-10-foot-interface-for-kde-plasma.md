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
language_code: zh-CN
---

# Plasma Bigscreen – 10-foot interface for KDE plasma

## Summary
Plasma Bigscreen 是一个面向电视、HTPC 和机顶盒的开源 Linux 大屏界面，强调可定制性、开放生态与隐私保护。它本质上是 KDE Plasma 在“10 英尺交互”场景下的电视友好型桌面环境，而不是机器人或基础模型研究论文。

## Problem
- 解决的是电视与机顶盒常见系统封闭、缺乏用户控制、隐私与可信度不足的问题。
- 需要一种适合“沙发距离”操作的 Linux 大屏界面，支持遥控器、CEC、手柄、键鼠、手机等多种输入方式。
- 这件事重要，因为现有 TV 平台多为封闭生态；开放替代方案可让用户和厂商获得更高的可控性、可扩展性与可审计性。

## Approach
- 核心方法是把 KDE Plasma/KWin/KDE Frameworks/Qt/Kirigami 这套开源 Linux 桌面技术栈，封装成一个专为电视大屏优化的桌面环境。
- 界面机制上采用 TV-friendly 设计：可从沙发距离浏览应用、切换任务、修改设置，并通过一键 Home overlay 快速搜索、进入设置、返回主屏或切换应用。
- 交互上支持多输入统一接入，包括 TV remote via CEC、游戏控制器、键盘鼠标，以及通过 KDE Connect 的手机控制。
- 生态上不自建封闭应用商店，而是复用 Linux 发行版包管理器与 Flathub，运行 Steam、Kodi、Jellyfin、VacuumTube 等现有 Linux 应用。
- 产品定位上强调 fully open source、可移植到任意支持 Linux 的设备，并允许社区和厂商共同开发或集成到自身产品中。

## Results
- 文本**没有提供定量实验结果**，没有数据集、指标、基线或数值对比，因此不存在可核验的性能突破数字。
- 最强的具体主张是：该系统可作为标准 Linux 桌面环境安装在受支持设备上，并面向 TV、HTPC、set-top boxes 使用。
- 支持的输入方式明确包括 **4+ 类**：CEC 遥控器、游戏手柄、键盘鼠标、手机（KDE Connect）。
- 提供完整的大屏设置应用，可配置显示、网络、外观等系统选项，并支持遥控器或手柄导航。
- 可访问的应用生态主张包括 Steam、Kodi、Jellyfin、YouTube（经 VacuumTube）以及“thousands more” Linux/Flathub 应用，但文中未给出精确应用数量统计或兼容性测试结果。

## Link
- [https://plasma-bigscreen.org](https://plasma-bigscreen.org)
