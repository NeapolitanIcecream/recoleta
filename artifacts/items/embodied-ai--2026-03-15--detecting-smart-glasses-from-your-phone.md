---
source: hn
url: https://nearby-glasses-alert.pages.dev/
published_at: '2026-03-15T23:21:21'
authors:
- modexapps
topics:
- ble-detection
- smart-glasses
- privacy-preserving
- mobile-app
- background-scanning
relevance_score: 0.05
run_id: materialize-outputs
---

# Detecting Smart Glasses from your phone

## Summary
这不是一篇学术论文，而是一个面向消费者的手机应用说明页。它提出用手机端 BLE 持续扫描来检测附近带摄像头的智能眼镜，并以本地隐私保护方式实时告警。

## Problem
- 解决的问题：附近的 Meta Ray-Ban、Snap Spectacles 等智能眼镜外观接近普通眼镜，但可能携带摄像头，旁人难以及时察觉。
- 重要性：如果能在手机上实时发现这类设备，用户可更早获得隐私风险提示，而不需要专用硬件或云端服务。
- 挑战在于：移动操作系统会限制后台扫描与耗电，且 BLE 广播信号噪声大，容易误报或漏报。

## Approach
- 核心机制很简单：手机持续进行 BLE 扫描，匹配厂商 BLE ID、service UUID 和设备名称关键词，发现疑似智能眼镜后立即通知用户。
- 为降低误报，系统把 manufacturer IDs、service UUIDs、RSSI 和 name keywords 组合成一个 confidence score，只在“有意义的匹配”时告警。
- 为提高后台稳定性，应用声称使用硬件级 BLE 扫描过滤器，以绕过 Android 激进的电池优化，并支持 Doze、后台运行和重启后自动恢复扫描。
- 为提升可用性，提供 Strict/Balanced/Relaxed 三档精度-召回权衡、按设备冷却时间（20 秒到 5 分钟）以及基于 RSSI 的距离估计。
- 为保护隐私，所有检测在本地完成，原始蓝牙标识符不存储，仅做单向哈希；联网仅用于 OTA 检测规则更新。

## Results
- 文本**没有提供正式实验、数据集、基线或量化评测结果**，因此无法验证检测准确率、召回率、误报率、能耗或后台存活率。
- 最具体的功能性声明包括：可在后台持续扫描；即使关屏也能即时通知；在 Android Doze 和重启后继续工作；支持每设备 20s–5min 告警冷却。
- 距离相关的定量声明是：基于修正的室内 path-loss 公式估计距离，范围从“sub-1m 到 200m”；但未给出误差、测试环境或对比基线。
- 产品层面的具体信息包括：售价 $1.99，支持 Android 和 iOS，无账号，无云分析，仅使用互联网进行规则更新。
- 因缺少可重复实验结果，所谓“detects when other apps go silent”“hardware-level filters bypass optimizer”等突破性说法目前更像工程宣称，而非已验证研究结论。

## Link
- [https://nearby-glasses-alert.pages.dev/](https://nearby-glasses-alert.pages.dev/)
