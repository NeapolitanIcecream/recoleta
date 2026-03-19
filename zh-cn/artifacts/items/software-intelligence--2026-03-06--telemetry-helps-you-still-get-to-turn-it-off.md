---
source: hn
url: https://ritter.vg/blog-telemetry.html
published_at: '2026-03-06T23:44:30'
authors:
- birdculture
topics:
- telemetry
- browser-engineering
- privacy-engineering
- software-reliability
- security-rollout
relevance_score: 0.34
run_id: materialize-outputs
language_code: zh-CN
---

# Telemetry helps. you still get to turn it off

## Summary
这篇文章主张：遥测并非“没用的监控”，而是在浏览器工程中持续提升稳定性、安全性、性能和发布安全的重要技术手段；同时作者明确支持用户按自身威胁模型关闭遥测。

## Problem
- 文章反驳一种常见说法：**遥测没有实际价值，只是收集数据**。
- 对浏览器这类复杂软件而言，如果没有真实世界信号，开发者很难发现测试未覆盖的问题、评估兼容性风险，或判断是否能安全移除危险/低使用率功能。
- 这很重要，因为错误的发布、性能退化或安全加固导致的大面积兼容性破坏，会直接影响海量真实用户。

## Approach
- 核心机制很简单：**让软件把技术性运行信号发回开发方**，例如性能、功能使用、卡顿堆栈、崩溃报告与兼容性表现，用于工程决策而非只做产品点击统计。
- 作者区分了“遥测”与其他联网行为：更新检查、Remote Settings、证书/插件/驱动黑名单、captive portal 检测等并不都属于他所讨论的遥测。
- 在 Firefox 中，这些信号被用于发现真实世界中的异常路径、验证高风险安全改动不会“炸”Nightly、比较不同实现的实际速度、以及衡量某些特性的真实使用率。
- 文中还强调隐私保护设计：如常规遥测立即丢弃 IP、OHTTP 让服务器看不到 IP、Prio 做隐私保护计算，以及数据自动删除、分段与去关联存储；但用户仍应保留关闭权。

## Results
- **无系统性基准实验或统一量化表格**；这是开发者经验性案例总结，而非学术论文，因此没有标准数据集/统一指标上的完整对比数字。
- 在“canvas anti-fingerprinting noise”实现选择上，遥测帮助得出具体工程结论：**有 SHA 指令扩展时用 SHA-256 更快；没有时用 SipHash 更快；或者输入小于约 2.5KB 时用 SipHash**。作者强调该差异在“**billions of calls**”规模下很重要。
- 在移除父进程中的 `eval` 改造中，第一次上线到 **Nightly** 后“立即导致 Nightly 出问题”，随后作者称通过多轮遥测找出真实世界里仍在使用 `eval` 的路径以及用户自定义脚本生态，从而才能安全重做并减少破坏。
- **Background Hang Reporter (BHR)** 捕获预发布渠道卡顿堆栈，作者据此重构代码后，声称“**hang graphs dropped**”，即卡顿图表明显下降，但文中未提供具体百分比。
- 在 **Fission/site isolation** 与数据最小化工作中，遥测被用来确认移除跨源与设备标识信息时没有破坏用户工作流；在 **jar:** Web 暴露关闭上，遥测显示“**real-web usage was basically nonexistent**”，从而支持直接收缩攻击面。
- 文章还声称遥测推动了 **CRLite、TLS/HTTPS-First/Certificate Transparency rollout、OS sandbox 加固、XSLT 去功能化论证、Android font allowlist、Resist Fingerprinting 用户规模判断** 等决策，但除“约 2.5KB”阈值外未给出更多具体数字。

## Link
- [https://ritter.vg/blog-telemetry.html](https://ritter.vg/blog-telemetry.html)
