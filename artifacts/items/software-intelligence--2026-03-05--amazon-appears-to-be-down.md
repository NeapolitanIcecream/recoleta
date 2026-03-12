---
source: hn
url: https://arstechnica.com/gadgets/2026/03/amazon-appears-to-be-down-with-over-20000-reported-problems/
published_at: '2026-03-05T23:12:32'
authors:
- samizdis
topics:
- service-outage
- software-deployment
- incident-report
- site-reliability
relevance_score: 0.27
run_id: materialize-outputs
---

# Amazon Appears to Be Down

## Summary
这不是一篇研究论文，而是一则关于 Amazon 服务中断的事件报道。核心信息是：一次与**软件代码部署**相关的问题导致 Amazon 网站与应用在 2026 年 3 月 5 日出现大规模故障，随后已恢复。

## Problem
- 文章描述的问题是 Amazon 电商网站与应用发生可见的大规模中断，影响用户浏览商品、访问首页和完成结账。
- 这很重要，因为 Amazon 是关键大型在线零售与云服务平台，故障会直接影响交易转化、用户体验和平台可靠性认知。
- 从工程角度看，事件指出一次软件代码部署即可触发广泛生产事故，说明发布安全与故障隔离至关重要。

## Approach
- 这篇文章**没有提出研究方法**；它主要基于 Downdetector 报告、媒体实测以及 Amazon 后续声明来描述事故经过。
- 最接近“机制”的信息是 Amazon 事后说明：问题与一次**software code deployment**有关，即生产环境代码发布引发网站和应用异常。
- 报道通过时间线整理事故演化：1:41 p.m. ET 开始报障上升，3:32 p.m. ET 达到峰值，4:10 p.m. ET 后开始回落，晚间基本恢复。
- 文章还按故障类型拆分用户受影响场景，例如结账、移动端和商品页面问题，以帮助定位影响范围。

## Results
- Downdetector 显示，报障自 **1:41 p.m. ET** 开始上升，到 **2:26 p.m. ET** 已达到 **18,320** 份报告。
- 报障在 **3:32 p.m. ET** 达到峰值 **20,804**，说明影响范围较大。
- 故障分布上，约 **50%** 的报告与**结账**有关，**21%** 来自**移动应用**用户，**17%** 指向**商品页面**问题。
- Ars Technica 实测确认：部分商品页无法正常加载，Amazon 首页有时也无法加载。
- 到 **4:10 p.m. ET**，Downdetector 报告开始下降；到 **5:55 p.m. ET** 已显著回落。
- 到 **9:05 p.m. ET**，报障降至 **435**；Amazon 随后声明问题已解决，并明确原因为一次**软件代码部署**相关故障。

## Link
- [https://arstechnica.com/gadgets/2026/03/amazon-appears-to-be-down-with-over-20000-reported-problems/](https://arstechnica.com/gadgets/2026/03/amazon-appears-to-be-down-with-over-20000-reported-problems/)
