---
source: hn
url: https://hackaday.com/2026/03/04/neither-android-nor-ios-diy-smartphone-runs-on-esp32/
published_at: '2026-03-04T23:18:51'
authors:
- HardwareLust
topics:
- open-hardware
- diy-smartphone
- esp32
- 4g-modem
- embedded-systems
relevance_score: 0.02
run_id: materialize-outputs
---

# Neither Android nor iOS: DIY Smartphone Runs on ESP32

## Summary
这篇文章介绍了一款基于 ESP32-S3 自制的 4G 智能手机原型，强调用户对硬件与软件的完全控制以及未来开源计划。它不是学术论文，而是一个偏黑客/DIY 的开放硬件项目展示。

## Problem
- 现有智能手机大多基于封闭、受限的商业硬件与软件生态，用户很难真正“拥有”和控制设备。
- 即便是替换操作系统（如 Linux 发行版），通常也仍运行在可能带有后门风险的商业手机硬件上。
- 因此需要一种从硬件到软件都可自主掌控、可修改、可开源的手机方案，这对隐私、可修复性和技术自治有意义。

## Approach
- 核心方法很简单：用 **ESP32-S3** 作为主控，自行拼装一个模块化 4G 手机，而不是依赖现成手机 SoC 平台。
- 通信部分使用 **A7682E simcom 4G modem**，实现打电话和发短信等基础手机功能。
- 多媒体与交互部分加入 **OV2640 Arducam** 摄像头、**3.5 英寸触摸屏**，并保留 **3.5 mm 音频接口**。
- 当前版本是由多层模块堆叠成的 alpha 原型；后续计划做成更薄的 **四层 PCB**，并集成 **SD 卡适配器**。
- 作者承诺在下一版完成后**开源硬件和软件设计**，并提供文档。

## Results
- 原型已经实现了明确的手机能力：**4G 连接、打电话、发短信、拍照、网页浏览**。
- 硬件配置包括 **ESP32-S3** 主控、**A7682E** 4G 模块、**OV2640** 摄像头、**3.5"** 触摸屏，以及 **3.5 mm** 耳机孔。
- 文章未提供标准化定量评测结果，**没有**报告如性能跑分、续航、延迟、吞吐、相机质量等具体数字。
- 最强的具体主张是：该设备已经是一个可工作的 **alpha 版 DIY 4G smartphone**，并计划演进到更薄的开源四层 PCB 设计。
- 文中同时明确承认其性能**明显弱于旗舰手机**，但优势在于开放性、可控性与自制硬件路线。

## Link
- [https://hackaday.com/2026/03/04/neither-android-nor-ios-diy-smartphone-runs-on-esp32/](https://hackaday.com/2026/03/04/neither-android-nor-ios-diy-smartphone-runs-on-esp32/)
