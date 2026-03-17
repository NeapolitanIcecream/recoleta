---
source: hn
url: https://www.macrumors.com/2026/03/11/apple-ios-16-7-15-release/
published_at: '2026-03-12T23:32:50'
authors:
- mgh2
topics:
- ios-security
- legacy-device-support
- software-update
- apple-ecosystem
relevance_score: 0.05
run_id: materialize-outputs
---

# Apple Releases New Versions of iOS for Older iPhones

## Summary
这是一则产品与安全更新新闻，而不是研究论文。内容主要说明苹果为无法升级到较新系统的旧款 iPhone 和 iPad 发布了 iOS/iPadOS 15 与 16 的安全补丁更新。

## Problem
- 旧款设备无法运行较新的 iOS/iPadOS 版本，但仍面临已披露漏洞的安全风险。
- 若旧设备得不到补丁，已知漏洞（如文中提到的 Coruna exploit 相关问题）可能持续暴露用户。
- 长期维护旧设备的安全性很重要，因为设备生命周期往往超过主版本系统支持周期。

## Approach
- 苹果发布了针对旧设备的点版本更新：iOS 16.7.15、iPadOS 16.7.15、iOS 15.8.7、iPadOS 15.8.7。
- 核心机制很简单：把此前已在较新 iOS 16 / iOS 17 更新中修复的安全问题，回补到无法升级到 iOS 17 或更高版本的旧设备上。
- 更新通过系统“设置 -> 通用 -> 软件更新”分发，也可由自动更新机制在未来几天内安装。
- 苹果说明这些版本包含重要安全修复，且安全说明显示其与 Google 上周披露的复杂 Coruna exploit 有关。

## Results
- 发布了 **4 个**更新版本：**iOS 16.7.15、iPadOS 16.7.15、iOS 15.8.7、iPadOS 15.8.7**。
- 苹果称这些更新包含“**重要安全修复**”，并将此前在 **iOS 16** 和 **iOS 17** 中已修复的问题带到旧设备。
- 文中给出的长期支持信号：苹果承诺 iPhone 自发布后至少提供 **5 年**安全更新；同时举例称 **iPhone 5s** 在发布 **13 年**后今年早些时候仍获得更新。
- 未提供漏洞修复效果的量化指标、测试数据集、基线对比或性能数字，因此**没有可报告的研究型定量结果**。
- 最强的具体主张是：这些补丁针对已披露的 **Coruna exploit** 相关问题，并覆盖无法升级到 iOS 17+ 的旧设备用户。

## Link
- [https://www.macrumors.com/2026/03/11/apple-ios-16-7-15-release/](https://www.macrumors.com/2026/03/11/apple-ios-16-7-15-release/)
