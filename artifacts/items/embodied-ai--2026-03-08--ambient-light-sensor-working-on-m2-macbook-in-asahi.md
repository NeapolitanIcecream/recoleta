---
source: hn
url: https://github.com/AsahiLinux/docs/issues/248
published_at: '2026-03-08T23:09:58'
authors:
- cromka
topics:
- linux-driver
- ambient-light-sensor
- asahi-linux
- macbook-m2
- auto-brightness
relevance_score: 0.02
run_id: materialize-outputs
---

# Ambient Light Sensor working on M2 MacBook in Asahi

## Summary
这是一份关于在 Asahi Linux 上启用 M2 MacBook 环境光传感器（ALS）的实现说明，而不是传统学术论文。它解决了 M2 机型在 Linux 下无法正常读取环境光并驱动自动亮度的问题，提供了驱动、校准提取和用户态守护进程的完整方案。

## Problem
- 解决的问题是：M2 MacBook 在 Asahi Linux 上的 VD6286 环境光传感器默认无法完整工作，缺少工厂校准数据时会一直报告 **0 lux**。
- 这很重要，因为没有 ALS，系统无法根据环境光自动调节屏幕亮度，影响可用性、功耗体验和桌面集成度。
- 另外，KDE Plasma 6.6.0 在 Asahi 上也没有现成的 ALS 自动亮度支持，需要额外的用户态组件来打通整条链路。

## Approach
- 核心方法很简单：让内核驱动先能识别并加载 ALS，再从 macOS 中提取出苹果出厂校准数据供 Linux 使用。
- 具体机制是从 macOS 的 `ioreg` 导出中解析 `AppleSPUVD6286` 节点里的 `CalibrationData`，生成 `aop-als-cal.bin` 固件文件，并放到 `/lib/firmware/apple/` 下供驱动读取。
- 配合一个内核补丁（PR #457），即使没有校准固件也允许驱动先 probe，不再因为缺固件而完全不起作用；只是没有校准时读数会是 0 lux。
- 在用户态，作者编写了一个轻量自动亮度 daemon：通过 D-Bus 从 `iio-sensor-proxy` 读取 lux，再通过 KDE `ScreenBrightness` API 平滑调整亮度。
- 为避免屏幕亮度来回跳动，该 daemon 使用了 rolling average 和 hysteresis 来抑制闪烁。

## Results
- 作者声称已在 **MacBook Air 15" M2 (J415)** 上将 **VD6286 ALS fully working**，系统环境为 **Asahi Fedora 42 + KDE Plasma 6.6.0**。
- 使用的内核版本为 **6.18.10-402.asahi.fairydust.fc42.aarch64+16k**，并依赖配置项 **`CONFIG_IIO_AOP_SENSOR_ALS=m`**。
- 文中给出的最明确定量现象是：**没有工厂校准数据时，传感器输出为 0 lux**；加入提取出的校准文件后即可正常工作。
- 提供了一个内核补丁 **PR #457**，其作用是让校准固件变为“可选”，从而驱动即使缺文件也能 probe 成功。
- 适配验证硬件明确列出为 **15 英寸 M2 Air**，并声称**应当也适用于**其他带 **VD6286** 的 M2 机器，如 **13 英寸 MacBook Air** 和 **13 英寸 MacBook Pro**。
- 没有提供标准化基准测试、误差指标、延迟数据或与其他方法的定量对比，因此突破性结果主要是工程落地：从“0 lux/不可用”到“完整可用+自动亮度链路打通”。

## Link
- [https://github.com/AsahiLinux/docs/issues/248](https://github.com/AsahiLinux/docs/issues/248)
