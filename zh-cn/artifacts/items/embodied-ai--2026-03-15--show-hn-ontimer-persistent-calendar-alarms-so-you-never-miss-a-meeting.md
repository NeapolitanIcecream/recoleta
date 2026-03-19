---
source: hn
url: https://www.ontimer.app
published_at: '2026-03-15T22:26:38'
authors:
- ethangarr
topics:
- calendar-app
- persistent-alarms
- meeting-reminders
- iphone-productivity
- time-to-leave
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: OnTimer – persistent calendar alarms so you never miss a meeting

## Summary
OnTimer 是一款 iPhone 日历提醒应用，把普通、容易被忽略的日历通知变成更响亮且持续显示的闹钟，以减少错过会议和迟到。它面向依赖日程安排、但经常漏看提醒的用户，支持 Google 和 Microsoft 多日历。

## Problem
- 它解决的问题是：iPhone 上常规日历提醒通常是被动通知，出现时间短、容易被划掉或忽略，导致用户错过会议、通话或预约。
- 这件事重要，因为对忙碌专业人士、连续会议用户、以及有时间盲倾向或 ADHD 倾向的人来说，漏掉提醒会直接带来迟到、缺席和工作中断。
- 现有日历应用更偏向“展示通知”，而不是在关键时刻真正抓住用户注意力。

## Approach
- 核心机制很简单：连接用户的 Google 或 Microsoft 日历，自动监测即将到来的事件，并为这些事件预先生成提醒闹钟。
- 与普通通知不同，OnTimer 在事件开始前触发“响亮、持续、需要手动关闭”的提醒，让提醒更难被忽略。
- 对带地点的事件，它还提供基于路程时间和交通状况的 Time To Leave 出发提醒，帮助用户判断何时该离开；这是付费功能。
- 它不替代原有日历，而是在现有日程之上增加一层更强的提醒执行机制，并支持多个日历账户统一接入。

## Results
- 提供的内容没有给出任何定量实验结果、用户研究指标或对比基线数据，因此无法报告准确的提升幅度、召回率或迟到率下降数字。
- 最强的具体产品声明是：支持 **2 类**主流日历生态（Google、Microsoft）以及多账户/多日历接入。
- 最强的具体功能声明是：可对日历事件自动准备闹钟，并让提醒保持“响亮且持续可见”，直到用户手动关闭；相比标准通知，目标是让会议和预约“更难错过”。
- 另一个具体声明是：对有地点的事件提供基于出行时间和交通的 Time To Leave 提醒，但文本仅说明这是付费功能，没有提供准确率、覆盖率或效果数字。

## Link
- [https://www.ontimer.app](https://www.ontimer.app)
