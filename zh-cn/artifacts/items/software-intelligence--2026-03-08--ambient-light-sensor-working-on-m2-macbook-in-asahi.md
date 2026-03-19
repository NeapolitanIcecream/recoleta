---
source: hn
url: https://github.com/AsahiLinux/docs/issues/248
published_at: '2026-03-08T23:09:58'
authors:
- cromka
topics:
- asahi-linux
- ambient-light-sensor
- macbook-m2
- linux-driver
- auto-brightness
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# Ambient Light Sensor working on M2 MacBook in Asahi

## Summary
这是一份面向 Asahi Linux 社区的实现说明，展示了 M2 MacBook 上的环境光传感器如何在 Linux 下工作，并补齐自动亮度调节链路。其价值在于把苹果硬件上的一个依赖专有校准数据的传感器，变成可在 Asahi Fedora 上实际可用的功能。

## Problem
- 需要让 **M2 MacBook 的环境光传感器（ALS）** 在 Asahi Linux 上正常工作，否则自动亮度等用户体验功能无法实现。
- 该传感器依赖 **macOS 中的出厂校准数据**；没有这份固件时，驱动虽然可加载，但传感器会返回 **0 lux**，功能等于不可用。
- KDE Plasma 6.6.0 在 Asahi 上 **没有内建 ALS 自动亮度支持**，因此即便底层读到光照值，桌面端也缺少完整联动。

## Approach
- 启用/使用 Asahi 的 fairydust 内核分支中的 **AOP ALS 驱动**（`CONFIG_IIO_AOP_SENSOR_ALS=m`），作为硬件访问基础。
- 从 macOS 导出 `ioreg` XML，再用脚本从 `AppleSPUVD6286` 节点的 `CalibrationData` 中提取校准 blob，生成 `aop-als-cal.bin` 并放到 Linux 固件目录中。
- 配套内核补丁（PR #457）把 **校准固件改为可选**，使驱动即使缺少固件也能先完成 probe，改善可部署性与调试体验；但若无校准，读数仍会是 0 lux。
- 为桌面侧补了一个轻量自动亮度守护进程：通过 **D-Bus** 从 `iio-sensor-proxy` 读取 lux，再调用 KDE `ScreenBrightness` 接口平滑调节亮度。
- 守护进程使用 **rolling average + hysteresis**，以最简单方式抑制亮度抖动和频繁闪烁。

## Results
- 在 **MacBook Air 15" M2 (J415)**、**VD6286** 传感器、**Asahi Fedora 42**、**KDE Plasma 6.6.0**、**kernel 6.18.10-402.asahi.fairydust.fc42.aarch64+16k** 上，作者声明 ALS 已“**fully working**”。
- 明确给出关键失败/成功条件：**没有校准固件时传感器报告 0 lux**；加入从 macOS 提取的校准数据后可正常提供 lux 读数。
- 在桌面体验上，作者实现了可工作的 **auto-brightness daemon**，并通过平滑调节、滚动平均和滞回来减少闪烁，但**未提供亮度稳定性、响应时间或误差等量化指标**。
- 兼容性声明：除已测试的 **15" M2 Air** 外，作者认为也**应可用于**其他带 **VD6286** 的 M2 机型，如 **13" MacBook Air** 和 **13" MacBook Pro**，但文中未给出额外实测数据或对比基线。

## Link
- [https://github.com/AsahiLinux/docs/issues/248](https://github.com/AsahiLinux/docs/issues/248)
