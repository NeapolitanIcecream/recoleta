---
source: hn
url: https://codeberg.org/readeck/readeck
published_at: '2026-03-02T23:54:23'
authors:
- Curiositry
topics:
- self-hosted-app
- read-it-later
- web-archiving
- bookmark-manager
- privacy-first
relevance_score: 0.12
run_id: materialize-outputs
---

# Readeck – open-source, self-hosted read-it-later app with full content archiving

## Summary
Readeck 是一个开源、自托管的“稍后读/书签归档”Web 应用，重点是把网页的可读内容与相关资源长期、私密地完整保存下来。它不是研究型模型论文，而是一个强调简洁架构、快速响应和长期归档能力的软件系统。

## Problem
- 现有稍后读或书签工具常常**不能完整保存网页内容**，尤其是图片等相关资源，导致以后再看时内容缺失。
- 网页内容具有**易失性**：今天在线的文章，未来可能被删除、改版或失效，因此长期保存很重要。
- 很多现代Web应用依赖复杂前后端分离和繁重部署栈，增加了**安装、维护和贡献门槛**。

## Approach
- 核心机制很简单：用户保存一个链接后，Readeck 会立即抓取并存储该网页的**可读内容及资源**；对图片和视频页面会做对应适配处理。
- 每个书签都被保存为一个**不可变的单一 ZIP 文件**，其中包含 HTML、图片等内容；应用按需直接提供这些内容，或转换成网页/EPUB。
- 系统采用**简单数据库模式**，推荐用 SQLite，减少部署和维护复杂度。
- 技术栈选择**Go + 服务端渲染**，并用 Stimulus/Turbo 提供少量交互，避免重型单页应用和复杂后台进程。
- 在隐私设计上，除视频外，保存后浏览器读取内容时**不需要再向外部网站发请求**，以支持私密阅读与长期归档。

## Results
- 提供了明确的功能结果：支持**全文搜索、标签、收藏、归档、高亮、集合、浏览器扩展、EPUB 导出、OPDS 访问**等完整阅读归档工作流。
- 架构上给出具体实现信号：代码主要为 **Go 74.9%**，辅以 **HTML 13.3%**、**JavaScript 6.5%**、**SCSS 3.3%**、**Python 1%**。
- 部署结果较直接：可通过单条容器命令在 **8000** 端口运行，也支持**单一二进制文件**启动，降低安装成本。
- 文本没有提供严格的基准测试、数据集或与竞品的定量对比，因此**没有可验证的性能数字**；最强的具体主张是“快速响应”“平滑体验”以及“长期、私密、完整归档”。

## Link
- [https://codeberg.org/readeck/readeck](https://codeberg.org/readeck/readeck)
