---
source: hn
url: https://github.com/rio719/gLinksWWW-browser
published_at: '2026-03-14T22:37:19'
authors:
- glinkswww
topics:
- web-browser
- privacy
- clipboard-manager
- power-user-tools
- search-switching
relevance_score: 0.24
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: GLinksWWW – A browser for power users tired of repetitive copy-pasting

## Summary
gLinksWWW 是一个面向高效重度用户的隐私浏览器，主打多槽剪贴板、快速切换搜索引擎、零历史存储和按站点 Cookie 管理。其价值主要在于减少重复复制粘贴和增强本地隐私控制，但更像产品功能说明而非研究论文。

## Problem
- 解决浏览器中**重复复制粘贴低效**的问题：传统剪贴板通常一次只保存一个内容，频繁切换文本或链接会打断工作流。
- 解决**隐私与会话痕迹残留**的问题：常规浏览器会保存历史和站点数据，给重视本地隐私的用户带来负担。
- 解决**搜索入口切换和站点数据控制不便**的问题：用户往往需要手动切换搜索引擎，且难以按网站精细管理 Cookie。

## Approach
- 核心机制是一个**多槽剪贴板系统**：用户可把不同文本或链接复制/剪切到指定编号槽位，再从对应槽位粘贴，避免反复覆盖单一系统剪贴板。
- 提供**18 个并发槽位**（文本中同时提到 9-Slot 与 18 Concurrent Slots，表述略有不一致），并通过快捷键将复制、剪切、粘贴直接映射到槽位编号。
- 在浏览器界面内集成**一键搜索引擎切换**，支持 Perplexity、Google、Bing、Yahoo、Startpage、Yandex 等，减少手动改配置或改地址栏操作。
- 采用**零历史存储**策略：浏览历史不落盘，关闭会话后轨迹即消失，以最简单直接的方式提升本地隐私。
- 提供**按网站 Cookie 管理器**和最多 **7 标签页**的多标签系统，兼顾站点隔离、数据控制和基础多任务浏览。

## Results
- 文本**未提供正式实验、基准测试或学术评测结果**，没有准确的吞吐、延迟、用户研究或与 Chrome/Firefox/Edge 的量化对比。
- 最明确的功能性结果是：支持**18 个并发剪贴板槽位**，并可通过 `Ctrl+Shift` / `Alt+Shift` / `Ctrl+Alt` 加数字键或 `F1-F8` 实现定向复制、剪切、粘贴。
- 支持**最多 7 个标签页**的多标签浏览，并宣称具备“high-speed performance”，但没有给出启动时间、内存占用或页面加载速度数字。
- 隐私方面的具体声明是**不保存浏览历史到本地磁盘**，并在关闭会话后清除痕迹；但没有给出威胁模型、安全审计或隐私验证结果。
- 跨平台方面声称支持**Windows、Linux（AppImage/DEB）、MacOS**，这是部署覆盖面的具体卖点，但不是经过量化验证的研究突破。

## Link
- [https://github.com/rio719/gLinksWWW-browser](https://github.com/rio719/gLinksWWW-browser)
