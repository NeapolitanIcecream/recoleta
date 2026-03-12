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
- privacy
relevance_score: 0.03
run_id: materialize-outputs
---

# Readeck – open-source, self-hosted read-it-later app with full content archiving

## Summary
Readeck 是一个开源、自托管的稍后读与书签归档应用，重点是把网页的可读内容连同图片等资源完整保存到本地以便长期访问。它更像一套面向隐私和长期保存的轻量归档系统，而不是研究论文中的新算法方法。

## Problem
- 它解决的是“网页收藏后内容会失效、丢图、下线或无法长期访问”的问题，这很重要，因为普通书签通常只保存链接，几年后原文和资源可能已经消失。
- 它也解决“用户不想依赖第三方云服务读取个人收藏内容”的隐私问题，尤其是阅读、归档和全文检索场景。
- 从给定材料看，这不是机器人/基础模型方向工作，因此与用户关注主题的直接相关性较低。

## Approach
- 核心机制很简单：用户保存一个链接后，系统立即抓取并存储该网页的可读内容以及图片等资源，避免未来原网页变化或失效带来的损失。
- 每个书签被保存为一个**不可变的单个 ZIP 文件**，其中包含 HTML、图片等内容；应用按需直接提供这些内容，或转换成网页/E-book（EPUB）。
- 系统会识别页面类型（文章、图片、视频）并采用相应处理方式；除视频外，浏览器侧基本不再向外部网站发请求，以增强隐私。
- 工程实现上采用较简单的技术栈：Go 后端、服务端渲染、Stimulus/Turbo 增强交互、简单数据库模式，推荐 SQLite，多数安装可通过单二进制或容器完成。
- 在产品功能层面，支持标签、收藏、归档、高亮、集合、浏览器扩展、全文搜索、EPUB 导出和 OPDS 访问等。

## Results
- 给定文本**没有提供正式的定量评测结果**，没有数据集、基线方法、准确率/召回率/延迟等可比较数字。
- 唯一明确的数字信息主要是代码构成：**Go 74.9%**, **HTML 13.3%**, **JavaScript 6.5%**, **SCSS 3.3%**, **Python 1%**, **Other 1%**。
- 部署接口有一个明确运行示例：默认可通过 **`http://localhost:8000/`** 访问，容器示例映射端口为 **8000:8000**。
- 最强的具体主张是：系统将文本和图片在保存链接时即存入本地实例；**除视频外，不会从浏览器向外部网站发出请求**；并宣称采用简单栈可带来“**very quick response times**”和流畅体验，但文中未给出测速数字或对比基线。

## Link
- [https://codeberg.org/readeck/readeck](https://codeberg.org/readeck/readeck)
