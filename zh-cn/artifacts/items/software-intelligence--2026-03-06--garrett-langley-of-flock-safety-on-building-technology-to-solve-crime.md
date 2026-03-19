---
source: hn
url: https://cheekypint.substack.com/p/garrett-langley-of-flock-safety-on
published_at: '2026-03-06T23:56:28'
authors:
- hhs
topics:
- public-safety
- computer-vision
- real-time-systems
- sensor-fusion
- drone-systems
relevance_score: 0.22
run_id: materialize-outputs
language_code: zh-CN
---

# Garrett Langley of Flock Safety on building technology to solve crime

## Summary
这是一篇关于 Flock Safety 如何把车牌识别、跨机构数据共享、911 实时接入、视频检索与无人机整合为公共安全操作系统的访谈，而非严格意义上的学术论文。核心价值主张是：把原本低效、碎片化、事后响应的执法流程，变成更实时、可协同、可搜索的系统，从而提升破案与抓捕效率。

## Problem
- 许多犯罪是机会型且跨社区/跨城市发生，传统安防系统往往只能**记录犯罪发生**，却难以**快速锁定嫌疑人并协同追踪**。
- 美国执法体系高度地方化，机构之间历史上依赖电话、传真、CSV/FTP 等方式交换信息，导致实时协作差、追踪滞后，尤其不适合跨辖区案件。
- 城市 911、视频监控、车牌数据、无人机等数据源彼此割裂，人工分发和检索成本高，很多线索会因为时间延误而变成冷案。

## Approach
- 以**社区/城市级公共安全操作系统**为核心，而不是单户安防：先用可自供电、5G 回传的摄像头在道路侧捕获车辆/车牌，再扩展到城市范围内的多类视频与事件流整合。
- 建立实时数据管道：接入 FBI 的 NCIC 热名单、本地“hot list”、911 呼叫流以及第三方/私人摄像头，让系统在事件发生时立即联动搜索。
- 用简单的计算机视觉与检索能力做“可操作线索提取”：例如按车牌、车辆外观、异常车牌匹配、人物着装（如白色 Converse 鞋）进行搜索，而不是只做被动存档。
- 通过 FlockOS 把多机构、多州、多部门放到同一协作层中，并把结果分发给前线警员与无人机系统，实现从报警到定位、追踪、抓捕的闭环。
- 在硬件侧强调基础设施无依赖部署：太阳能、5G、边缘侧有限算力设计，以适应道路口等缺少供电/光纤的位置。

## Results
- 访谈声称：**上一年帮助“clear”超过 100 万起犯罪**，并称约占**美国报告犯罪的 7%**；这里的“help clear”被定义为参与了破案/逮捕流程，而非独立完成全部执法工作。
- 部署规模方面，声称已覆盖**6000+ 城市**，覆盖**超过 50% 的美国人口**；公司业务从 0 增长到约**5 亿美元 ARR（7 年内）**。
- 在实时处置案例中，作者给出一个具体数字：某起未公开城市的恶性案件，从**911 呼叫到嫌疑人被捕约 17 分钟**，依赖 911 实时接入、视频调取和基于外观描述的检索。
- 在跨机构协同案例中，声称一次**跨 4 个州**的人口贩运行动中，**逮捕 76 人**，由多个地方警局、州机构和联邦机构在 Flock 上协同完成。
- 在失踪人口相关场景中，声称上一年帮助处理了**1000+ 起 Amber/Silver Alert** 案件。
- 这些结果均来自创始人口述与案例描述，**未提供可复现的实验设置、公开基准数据集或与学术/工业基线的严格对照评测**。相关最强主张是“把原本需数周/数月甚至无法侦破的案件，压缩到分钟级响应与跨机构实时协作”。

## Link
- [https://cheekypint.substack.com/p/garrett-langley-of-flock-safety-on](https://cheekypint.substack.com/p/garrett-langley-of-flock-safety-on)
