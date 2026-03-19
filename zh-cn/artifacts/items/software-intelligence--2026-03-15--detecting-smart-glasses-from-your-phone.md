---
source: hn
url: https://nearby-glasses-alert.pages.dev/
published_at: '2026-03-15T23:21:21'
authors:
- modexapps
topics:
- ble-detection
- smart-glasses
- mobile-privacy
- background-scanning
relevance_score: 0.2
run_id: materialize-outputs
language_code: zh-CN
---

# Detecting Smart Glasses from your phone

## Summary
这是一款通过手机后台蓝牙低功耗扫描来检测附近带摄像头智能眼镜的应用，目标是在不上传数据到云端的前提下提供实时提醒。其核心价值在于帮助用户发现看似普通但可能正在拍摄的智能眼镜，从而提升隐私感知与环境透明度。

## Problem
- 带摄像头的智能眼镜（如 Meta Ray-Ban、Snap Spectacles）外观接近普通眼镜，周围人往往难以及时察觉自己可能正被拍摄。
- 现有手机系统对后台蓝牙扫描、电池优化、Doze 模式和重启恢复等机制较严格，持续可靠检测并不容易实现。
- 隐私防护类工具若依赖云端、账号体系或持久标识存储，反而可能引入新的数据泄露与跟踪风险。

## Approach
- 使用手机上的连续 BLE 扫描，在后台持续寻找与智能眼镜相关的蓝牙信号，即使应用关闭、屏幕关闭或设备重启后也尽量保持检测能力。
- 检测规则基于多个蓝牙特征组合：manufacturer BLE IDs、service UUIDs、设备名称关键词，以及 RSSI 信号强度，而不是依赖单一特征。
- 将上述特征综合为一个 confidence score，只在达到“有意义匹配”时触发通知，以平衡误报与漏报。
- 提供 Strict、Balanced、Relaxed 三种检测策略，并用每设备冷却时间（20 秒到 5 分钟）减少重复告警。
- 隐私设计上坚持本地处理：扫描与判断均在手机端完成，原始蓝牙标识不存储，仅做单向哈希；联网仅用于 OTA 检测规则更新。

## Results
- 文本未提供论文式基准测试、公开数据集结果或与其他方法的定量对比，因此没有可验证的精度/召回率/F1 等数字结果。
- 宣称可在后台“一键”持续 BLE 扫描，并在检测到相机型智能眼镜时“立即通知”，即使屏幕关闭也可工作。
- 宣称通过硬件级 BLE 扫描过滤器绕过 Android 激进省电策略，在其他应用静默时仍可检测；但未给出功耗、成功率或设备覆盖率数字。
- 宣称可基于修正后的室内路径损耗公式估计距离，范围从亚 1 米到 200 米；但未报告距离估计误差或验证实验。
- 提供每设备 20 秒到 5 分钟的可配置告警冷却时间，以及重启后自动恢复扫描，强调“保护不会意外关闭”；但没有稳定性或长期运行统计。

## Link
- [https://nearby-glasses-alert.pages.dev/](https://nearby-glasses-alert.pages.dev/)
