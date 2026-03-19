---
source: hn
url: https://github.com/houqp/kiorg
published_at: '2026-03-07T23:59:44'
authors:
- houqp
topics:
- file-manager
- keyboard-driven-ui
- cross-platform
- vim-keybindings
- developer-tooling
relevance_score: 0.28
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Kiorg – a battery included file manager for keyboard nerds

## Summary
Kiorg 是一个面向键盘重度用户的跨平台文件管理器，强调高性能、单文件分发和开箱即用体验。它结合了 Vim 风格操作、内容预览、内置终端和插件系统，目标是提升文件导航与管理效率。

## Problem
- 传统文件管理器往往对键盘优先用户不够友好，导航与操作效率有限。
- 很多工具要么功能零散、依赖外部组件较多，要么跨平台一致性和可定制性不足。
- 对需要快速浏览目录、预览多种文件内容、并保持低延迟交互的用户来说，这会直接影响日常生产力。

## Approach
- 提供一个**跨平台、性能优先**的文件管理器，基于 egui 构建，强调快速渲染与导航。
- 用**Vim 风格快捷键**作为核心交互机制，并支持通过 TOML 自定义快捷键、主题和布局。
- 内置多种“电池齐全”能力：多标签页、类似 zoxide 的模糊目录跳转、内置终端、书签、状态持久化、撤销/重做文件操作。
- 提供丰富内容预览，覆盖代码高亮、图片、视频、PDF、EPUB 等，并支持语言无关插件扩展。
- 以**单个自包含二进制**形式分发，降低安装和使用门槛。

## Results
- 文本未提供标准基准测试或数据集上的定量结果，因此**没有可核验的性能指标**。
- 明确声称具备“**Lightingly fast rendering and navigation**”，但未给出 FPS、延迟、吞吐或与其他文件管理器的对比数字。
- 测试工具说明中提到 `nextest` 执行测试“**2-3x faster**”于 `cargo test`，但这是开发测试流程的比较，**不是 Kiorg 产品能力本身的评测结果**。
- 具体可验证的产品性结果包括：支持 **Linux/macOS/Windows** 三平台，提供**预构建二进制**，并覆盖多类文件预览与可配置主题/快捷键等完整功能集。

## Link
- [https://github.com/houqp/kiorg](https://github.com/houqp/kiorg)
