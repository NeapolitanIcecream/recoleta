---
source: hn
url: https://play.thomaskidane.com/
published_at: '2026-03-14T23:01:53'
authors:
- meneliksecond
topics:
- gui-agent
- mobile-ui-control
- real-world-demo
- natural-language-agent
relevance_score: 0.3
run_id: materialize-outputs
---

# Show HN: I let the internet control my iPad with AI

## Summary
这是一个让公众通过自然语言远程控制真实 iPad 的 AI 代理演示系统，展示了 AI 在移动端图形界面上的实时规划与执行能力。它更像产品/演示而非学术论文，但体现了面向真实设备的 GUI agent 可行性。

## Problem
- 目标问题是：如何让 AI 理解自然语言指令，并在**真实 iPad** 上自主完成图形界面操作。
- 这很重要，因为真实移动设备控制比纯文本或模拟环境更接近实际人机交互，也更能检验代理的感知、规划与执行闭环能力。
- 难点在于多步 UI 导航、实时执行、共享排队使用，以及在真实硬件约束下保证基本可用性与安全性。

## Approach
- 系统提供一个排队式网页入口，用户输入英文自然语言命令，轮到后由 AI 代理在真实 iPad 上执行。
- 核心机制可简单理解为：AI 先把一句话目标拆成若干 UI 操作步骤，再在屏幕上移动光标、点击图标/按钮、滚动页面，直到完成目标或超时。
- 当前能力聚焦于基础触控 GUI 操作：打开/关闭/切换应用、点击 UI 元素、上下滚动、返回主屏幕，以及完成简单多步指令。
- 为控制风险与复杂度，系统显式限制了文本输入、复杂手势、通知/控制中心/锁屏、需登录应用等高难或敏感交互。

## Results
- 提供了**真实 iPad 实时控制**演示：用户可下达如“Open Safari”或“Open Goodnotes then close it”之类命令，并观看代理执行。
- 支持的已声明能力包括 **5 类**：打开/关闭/切换应用、点击按钮/图标/UI 元素、应用内滚动、从任意位置回到主屏幕、执行多步指令。
- 明确列出的当前限制也有 **5 类**：**不支持**文本输入、主屏幕跨页滑动、双指/缩放等手势、通知/控制中心/锁屏交互、登录/认证类应用。
- 文本中**没有提供定量实验结果**，没有成功率、任务完成时间、基准数据集、对比方法或消融实验，因此无法验证相对 SOTA 或研究性突破。
- 最强的具体主张是：该系统能让“来自世界各地的人”轮流向真实 iPad 发送自然语言命令，并由 AI 代理自主执行，形成公开可见的实时演示闭环。

## Link
- [https://play.thomaskidane.com/](https://play.thomaskidane.com/)
