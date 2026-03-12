---
source: hn
url: https://plasma-bigscreen.org
published_at: '2026-03-06T23:59:16'
authors:
- PaulHoule
topics:
- linux-desktop
- tv-interface
- open-source
- kde-plasma
- human-computer-interaction
relevance_score: 0.12
run_id: materialize-outputs
---

# Plasma Bigscreen – 10-foot interface for KDE plasma

## Summary
Plasma Bigscreen 是一个面向电视、HTPC 和机顶盒的开源 Linux 大屏界面，强调可定制性、开放生态与隐私友好。它并不是研究型模型或算法论文，而是一个产品/平台介绍，核心价值在于提供替代封闭电视系统的开放方案。

## Problem
- 现有电视和机顶盒平台通常是**封闭生态**，开放性、可控性和可验证性不足。
- 这类系统往往在**隐私与用户信任**方面存在问题，用户难以真正掌控设备与软件栈。
- 电视场景需要适合“10-foot interface”的交互方式：可远距离操作、适配遥控器/手柄等输入，并兼顾应用启动、设置管理和多任务切换。

## Approach
- 采用一个**面向电视的大屏 Linux 桌面环境**：把 KDE Plasma/Qt/KWin/Kirigami 等开放技术栈组合成适合客厅场景的 TV UI。
- 核心机制可以简单理解为：**把 Linux 桌面重新包装成适合电视的界面**，让用户能在沙发上用遥控器、CEC、手柄、键鼠或手机完成日常操作。
- 提供**TV-friendly settings** 与一键呼出的 home overlay，使应用搜索、设置访问、返回主页和任务切换更适合大屏远距交互。
- 通过 Linux 发行版包管理器和 Flathub 接入现有应用生态，并支持 Steam、Kodi、Jellyfin、VacuumTube 等应用，强调可扩展和可定制。
- 以**完全开源、社区协作开发**为基础，允许发行版和厂商直接采用，也允许用户自由修改和部署。

## Results
- 文本**没有提供量化实验结果**，没有出现准确率、延迟、用户研究分数、基准测试或与竞品的数值比较。
- 最强的具体主张是：该系统可作为**标准 Linux 桌面环境**安装，并面向电视、HTPC、机顶盒设备使用。
- 支持**多种输入方式**：TV remote via CEC、游戏控制器、键盘鼠标、以及通过 KDE Connect 的手机控制。
- 支持从大屏界面直接完成**应用启动、设置调整、任务切换**，并提供完整的 TV-friendly 设置应用。
- 兼容**开放应用生态**，可安装 Steam、Kodi、Jellyfin、YouTube（经 VacuumTube）以及“thousands more” Linux/Flathub 应用，但原文未给出精确数量统计或覆盖率指标。

## Link
- [https://plasma-bigscreen.org](https://plasma-bigscreen.org)
