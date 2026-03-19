---
source: hn
url: https://play.thomaskidane.com/
published_at: '2026-03-14T23:01:53'
authors:
- meneliksecond
topics:
- gui-agent
- mobile-automation
- human-ai-interaction
- real-device-control
- natural-language-interface
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: I let the internet control my iPad with AI

## Summary
这是一个让互联网用户用自然语言远程控制真实 iPad 的 AI 代理演示系统，重点展示了语言到图形界面操作的实时执行能力。它更像交互式产品原型而非正式论文，但清晰体现了面向消费设备的代理式 UI 自动化。

## Problem
- 目标是解决“普通人如何用自然语言让 AI 直接操作真实移动设备”的问题，而不需要手写脚本或手动点击。
- 这很重要，因为它是通往通用设备代理、GUI 自动化和更自然的人机交互的关键一步。
- 移动端真实环境复杂，存在排队共享、实时执行、界面导航和安全约束等工程挑战。

## Approach
- 用户先排队获取回合，然后直接输入自然语言命令，例如“Open Safari”。
- AI 代理把命令分解为若干界面动作步骤，并在真实 iPad 上自主执行，如移动光标、点击图标、切换应用和滚动。
- 系统通过直播方式公开执行过程，用户可实时观看代理如何完成目标或在超时后结束回合。
- 当前能力集中于基础 GUI 操作：打开/关闭/切换应用、点击 UI 元素、滚动、回到主屏，以及执行简单多步任务。
- 系统显式限制高风险或高复杂度能力，如文本输入、复杂手势、通知/锁屏交互和需要登录的应用。

## Results
- 提供的是公开可玩的真实 iPad 在线演示，而不是带标准数据集评测的研究论文；文段中**没有给出正式定量指标**，如成功率、延迟、任务完成率或基线对比。
- 已宣称可完成的任务类型包括：打开/关闭/切换应用、点击按钮和图标、应用内上下滚动、从任意位置返回主屏。
- 已宣称支持简单多步指令，例如“Open Goodnotes then close it”，说明代理具备基础任务分解与顺序执行能力。
- 运行机制上支持多人共享访问：用户排队、按回合执行、超时自动切换到下一位，这表明系统已处理最基本的并发使用流程。
- 明确未支持的能力包括文本输入、主屏翻页、双指/多指手势、通知与控制中心、锁屏及登录场景，说明当前结果更偏“受限环境中的可运行原型”而非通用移动代理突破。

## Link
- [https://play.thomaskidane.com/](https://play.thomaskidane.com/)
