---
source: hn
url: https://hackaday.com/2026/03/04/neither-android-nor-ios-diy-smartphone-runs-on-esp32/
published_at: '2026-03-04T23:18:51'
authors:
- HardwareLust
topics:
- open-hardware
- esp32
- diy-smartphone
- embedded-systems
- mobile-device
relevance_score: 0.22
run_id: materialize-outputs
---

# Neither Android nor iOS: DIY Smartphone Runs on ESP32

## Summary
这是一款基于 ESP32-S3 自制的 4G 智能手机原型，目标是提供对手机硬件与软件更完整的所有权和开放性。它展示了在极低端算力平台上实现通话、短信、拍照和网页浏览等基础手机功能的可行性。

## Problem
- 现有主流智能手机通常是封闭生态，用户很难真正控制硬件、软件与可修改性，这削弱了“拥有”设备的意义。
- 即便是可替代操作系统（如移动 Linux）方案，很多仍运行在商业现成硬件上，无法解决底层硬件可信性与开放性问题。
- 因此需要一种从硬件到软件都更开放、可自制、可文档化的手机方案，证明完全 DIY 手机不是空想。

## Approach
- 以 **ESP32-S3** 作为主控，构建一台可独立工作的手机，而不是在现成手机硬件上刷第三方系统。
- 通过 **A7682E Simcom 4G modem** 提供蜂窝通信能力，实现打电话和发短信。
- 集成 **OV2640 Arducam** 摄像头、**3.5 英寸触摸屏** 和 **3.5 mm 耳机孔**，覆盖拍照、交互和音频等核心功能。
- 当前为分层模块堆叠的 alpha 原型，后续计划改为更薄的 **四层 PCB**，并加入 **SD 卡适配器**。
- 作者计划在下一阶段同时开源**硬件与软件**并提供文档，从而提升可复现性与社区扩展能力。

## Results
- 原型已实现多项核心手机功能：**4G 通话、短信、拍照、网页浏览**。
- 硬件配置明确：主控为 **ESP32-S3**，蜂窝模块为 **A7682E**，摄像头为 **OV2640**，屏幕为 **3.5 英寸触摸屏**，并保留 **3.5 mm 音频接口**。
- 文中**没有提供标准化量化评测结果**，例如性能跑分、续航时间、网络吞吐、延迟、摄像质量或与 Android/iPhone 的基准对比。
- 最强的具体主张是：该设备已经在**非商用手机主板**上实现了接近基础智能手机的关键能力，并计划进一步缩小体积、增加 **四层 PCB + SD 卡** 支持以及完整开源发布。
- 文中同时明确指出其性能**明显弱于旗舰手机**，因此贡献主要在开放性、可控性与 DIY 可行性，而非性能突破。

## Link
- [https://hackaday.com/2026/03/04/neither-android-nor-ios-diy-smartphone-runs-on-esp32/](https://hackaday.com/2026/03/04/neither-android-nor-ios-diy-smartphone-runs-on-esp32/)
