---
source: hn
url: https://www.macrumors.com/2026/03/11/apple-ios-16-7-15-release/
published_at: '2026-03-12T23:32:50'
authors:
- mgh2
topics:
- apple-security-update
- ios
- ipad-os
- legacy-device-support
- mobile-security
relevance_score: 0.0
run_id: materialize-outputs
---

# Apple Releases New Versions of iOS for Older iPhones

## Summary
这篇文章介绍了苹果为无法升级到较新系统的旧款 iPhone 和 iPad 发布了 iOS/iPadOS 15.8.7 与 16.7.15 安全更新，重点是修复已披露的 Coruna 高级漏洞利用。其意义在于说明苹果继续为老设备提供长期安全支持，但这不是一篇机器人或 AI 研究论文。

## Problem
- 旧款 iPhone 和 iPad 无法运行最新的 iOS/iPadOS 版本，但仍面临已知安全漏洞风险。
- Google 上周披露的复杂 **Coruna exploit** 需要被修补，否则老设备用户会持续暴露在攻击面前。
- 设备长期安全支持很重要，因为大量用户仍在使用多年以前发布的硬件。

## Approach
- 苹果发布了 **iOS 16.7.15、iPadOS 16.7.15、iOS 15.8.7、iPadOS 15.8.7**，专门面向无法升级到更新主版本的旧设备。
- 核心机制很简单：把此前已在 **iOS 16 / iOS 17** 中修复的安全补丁，回移植到旧系统分支上。
- 用户可通过 **Settings > General > Software Update** 手动安装，或等待自动更新推送。
- 苹果将这些版本定位为包含“重要安全修复”的维护更新，而非功能更新。

## Results
- 发布了 **4 个** 面向旧设备的软件更新版本：**iOS 16.7.15、iPadOS 16.7.15、iOS 15.8.7、iPadOS 15.8.7**。
- 苹果明确表示这些更新修复了与 **Coruna exploit** 相关的问题；这些问题此前已在多个 **iOS 16 / iOS 17** 更新中修复，现在同步带给旧设备。
- 文章给出的长期支持数字包括：苹果承诺自设备发布后至少提供 **5 年** 安全更新；并举例称 **iPhone 5s 在发布 13 年后** 仍收到更新。
- 没有提供传统研究论文中的实验指标、数据集、基线模型或性能提升百分比；最强的具体主张是苹果正在把已知关键安全修复扩展到无法升级新系统的旧设备。

## Link
- [https://www.macrumors.com/2026/03/11/apple-ios-16-7-15-release/](https://www.macrumors.com/2026/03/11/apple-ios-16-7-15-release/)
