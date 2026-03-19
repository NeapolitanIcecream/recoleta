---
source: hn
url: https://www.danielmoch.com/posts/2025/01/acme/
published_at: '2026-03-14T22:47:21'
authors:
- birdculture
topics:
- text-based-gui
- developer-tools
- plan9
- editor-design
- unix-integration
relevance_score: 0.4
run_id: materialize-outputs
language_code: zh-CN
---

# Plan 9's Acme: The Un-Terminal and Text-Based GUIs

## Summary
这篇文章介绍了 Plan 9 的 Acme 编辑器，并将其定位为一种“非终端”的、文本优先的 GUI 开发环境。核心观点是：比起封闭、各自为政的现代 GUI，Acme 用统一的文本交互和系统工具整合，提供了更简单、更持久的开发体验。

## Problem
- 现代 GUI 应用通常各自重新设计交互方式，缺乏一致性，导致整体使用体验复杂、割裂且学习成本高。
- 传统终端/TUI 之所以受开发者欢迎，并不只是因为“在终端里”，而是因为它们共享了高一致性的文本交互模式，并能方便组合外部工具。
- 常见 IDE/编辑器往往配置项、插件和视觉定制过多，容易让开发者把精力消耗在环境调优上，而不是实际工作上。

## Approach
- Acme 采用文本为中心的 GUI：用户可以在任意窗口中选择文本，并直接将其“管道”给命令行工具，再把输出写回选区或展示到新窗口。
- 它通过 9P 协议暴露内部交互接口，使外部程序能够以非常简单、自由的方式与编辑器通信，形成类似插件/辅助程序的扩展机制。
- 与把“终端嵌入编辑器”的方式不同，Acme 把 CLI 风格的操作深度整合进整个界面，因此任何文本区域都可以成为命令与结果的操作面。
- 它刻意保持极简：几乎没有配置、没有复杂主题系统、默认无语法高亮，借此减少工具链和界面层面的认知负担。

## Results
- 文章不是实验论文，没有提供基准测试、准确率、效率提升百分比或数据集上的量化结果。
- 最强的具体主张是 Acme 已经“优雅地老化”了约 **30 年**，而无需不断追赶新语言、编译器、终端或主题生态。
- 作者声称其核心优势在于更深层的工具整合：相比 VS Code 主要是“在编辑器里打开一个终端”，Acme 支持在 **任意窗口** 中直接执行标准 CLI 式命令并处理结果。
- 文章还声称 Acme 的 9P/辅助程序模型足够简单，扩展甚至“理论上可用 shell 脚本编写”，说明其扩展接口门槛较低。
- 从用户体验角度，作者的结论是：取消语法高亮、主题和大量配置“几乎没有成本”，却显著减少了无意义的环境调优，但这是个人经验性论断而非量化证据。

## Link
- [https://www.danielmoch.com/posts/2025/01/acme/](https://www.danielmoch.com/posts/2025/01/acme/)
