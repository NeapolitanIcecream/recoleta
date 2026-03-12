---
source: hn
url: https://ritter.vg/blog-telemetry.html
published_at: '2026-03-06T23:44:30'
authors:
- birdculture
topics:
- telemetry
- browser-engineering
- privacy-preserving-measurement
- security-rollout
- performance-optimization
relevance_score: 0.03
run_id: materialize-outputs
---

# Telemetry helps. you still get to turn it off

## Summary
这是一篇经验性技术文章，核心论点是：遥测在尊重用户可关闭权利的前提下，依然对浏览器的稳定性、安全性、性能优化和安全发布非常有用。文章主要基于 Firefox 的真实工程案例，说明“遥测无用”的说法并不成立。

## Problem
- 文章要解决的问题是：**如何判断软件遥测是否真的对产品改进有实际价值**，以及为何它值得在隐私约束下被保留为可选机制。
- 这很重要，因为浏览器这类复杂软件需要在真实世界异构环境中发现**崩溃、卡顿、兼容性回归和安全上线风险**，仅靠测试集和内部 dogfooding 往往不够。
- 文章也回应了一个常见争议：很多用户认为遥测只是“监视”且“没用”，作者试图用工程实例反驳“没用”这一点，而不是否认用户关闭它的权利。

## Approach
- 核心方法很简单：**收集来自真实用户环境的技术信号**，如性能、功能使用、崩溃、卡顿、硬件特征和实验 rollout 数据，用它来指导修复、回滚、兼容性处理和特性取舍。
- 作者区分了不同“回传”类型：真正的 telemetry 是把测量结果发回发布方；而更新检查、Remote Settings、证书/驱动黑名单等更多是为了给用户下发数据，不完全算遥测。
- 在隐私机制上，文章提到 Firefox 使用了如**立即丢弃 IP 的常规遥测、OHTTP、Prio、数据自动删除、分段和去链接存储**等方式，以降低隐私风险，但并不声称这是完美方案。
- 文章主要采用**案例论证**而非形式化实验：通过多个 Firefox 工程实例说明遥测如何帮助定位 hangs、验证危险安全变更、评估低使用率特性是否可移除、以及选择更快实现路径。

## Results
- **未提供系统化论文式定量实验结果**；没有统一 benchmark、数据集、消融实验或总体指标表。最强证据是多个真实工程案例和局部阈值/规模描述。
- 在“**anti-fingerprinting canvas noise**”实现选择中，作者声称通过遥测确定：**有 SHA 指令扩展时 SHA-256 更快；无扩展时 SipHash 更快；或当输入小于约 2.5KB 时 SipHash 更优**。该选择会影响**billions of calls（数十亿次调用）**规模下的总体性能。
- 在“**kill eval in parent process**”案例中，第一次上线到 **Nightly** 后即导致真实用户环境严重破坏；后续作者加入多轮遥测，定位到野外残余 eval 使用及 userChromeJS 社区依赖，从而实现更安全的兼容迁移。文中**未给出故障率或回归百分比**。
- 在“**Background Hang Reporter**”案例中，作者表示遥测发现了其代码导致的特定交互卡顿，重构后“**hang graphs dropped**”，但**未给出下降幅度**。
- 在“**jar: URI**”与“**XSLT**”案例中，作者称使用遥测证明真实网页使用率**极低/基本不存在**，因此可以合理关闭攻击面或推动弃用；但**未提供具体使用占比数字**。
- 在“**Resist Fingerprinting**”案例中，遥测帮助证明该功能的手动启用用户虽然反馈很响亮，但只是“**minute portion of the population**（总体中极小一部分）**”，从而避免被管理层直接封禁；同样**没有精确比例数字**。

## Link
- [https://ritter.vg/blog-telemetry.html](https://ritter.vg/blog-telemetry.html)
