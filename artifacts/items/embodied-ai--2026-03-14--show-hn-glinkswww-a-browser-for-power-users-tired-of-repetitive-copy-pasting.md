---
source: hn
url: https://github.com/rio719/gLinksWWW-browser
published_at: '2026-03-14T22:37:19'
authors:
- glinkswww
topics:
- web-browser
- productivity-tools
- privacy
- clipboard-manager
relevance_score: 0.01
run_id: materialize-outputs
---

# Show HN: GLinksWWW – A browser for power users tired of repetitive copy-pasting

## Summary
这不是一篇研究论文，而是一个面向高频网页操作用户的浏览器项目介绍。它主打多槽剪贴板、搜索引擎快速切换和隐私保护，但未提供系统性实验或学术评测结果。

## Problem
- 解决重度网页用户反复复制粘贴、频繁切换搜索引擎、管理站点数据繁琐的问题。
- 强调隐私需求：常见浏览器会保存历史和持续积累 cookie，增加暴露与管理成本。
- 之所以重要，是因为这些高频小操作会持续消耗效率，且隐私泄露风险与本地痕迹积累相关。

## Approach
- 提出一个**多槽剪贴板浏览器**：提供最多 18 个并发槽位，并通过快捷键将复制、剪切、粘贴直接绑定到指定槽位。
- 内置剪贴板管理器，让用户查看和管理各槽位中的文本片段或链接，而不是只依赖单一系统剪贴板。
- 提供界面内的**搜索引擎一键切换**，覆盖 Google、Bing、Yahoo、Startpage、Yandex、Perplexity 等。
- 采用“**无历史存储**”的零足迹思路：浏览历史不写入本地磁盘，关闭会话后不保留浏览轨迹。
- 支持**按网站粒度的 Cookie 管理**，可对特定站点进行查看、编辑和销毁，而不影响其他站点。

## Results
- 文本给出的具体功能数字包括：**18 个并发剪贴板槽位**、说明中也提到 **9-Slot Multi-Copy & Paste**，两者表述存在不一致。
- 浏览器支持**最多 7 个标签页**，并宣称支持 **Windows、Linux（AppImage/DEB）、MacOS** 跨平台运行。
- 提供了明确快捷键映射：复制为 **Ctrl+Shift+0~9/F1~F8**，剪切为 **Alt+Shift+0~9/F1~F8**，粘贴为 **Ctrl+Alt+0~9/F1~F8**。
- **没有提供量化实验结果**：没有速度基准、用户研究、隐私评测、与其他浏览器的对比指标，也没有数据集或标准 benchmark。
- 最强的具体主张是：通过多槽剪贴板减少重复复制粘贴，通过无历史策略降低本地痕迹，通过站点级 cookie 管理增强控制力。

## Link
- [https://github.com/rio719/gLinksWWW-browser](https://github.com/rio719/gLinksWWW-browser)
