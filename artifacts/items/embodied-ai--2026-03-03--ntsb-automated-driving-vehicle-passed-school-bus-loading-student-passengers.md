---
source: hn
url: https://www.ntsb.gov:443/investigations/Pages/HWY26FH007.aspx
published_at: '2026-03-03T23:30:19'
authors:
- Animats
topics:
- automated-driving-safety
- school-bus-compliance
- remote-assistance
- ads-incident-investigation
- waymo
relevance_score: 0.14
run_id: materialize-outputs
---

# NTSB: Automated Driving Vehicle Passed School Bus Loading Student Passengers

## Summary
这是一份NTSB关于Waymo自动驾驶车辆在得州一辆校车上下学生时违法通过的初步调查通报。它揭示了ADS在识别校车停靠信号与远程协助决策链路上的安全缺陷，对无人驾驶公共道路部署具有直接安全意义。

## Problem
- 该事件关注的问题是：**L4自动驾驶车辆在校车红灯闪烁、停车臂伸出时，未能依法保持停车并最终通过校车**，这会直接危及上下车学生。
- 之所以重要，是因为校车场景属于高风险、强规则约束的交通场景；如果ADS在这类少见但关键的安全情境下失效，说明其感知、规则理解或人机协同仍存在漏洞。
- 该问题并非单一偶发事件：Austin ISD报告自**2025/2026学年开始已发生多起**Waymo车辆通过停靠校车的类似事件，促使NTSB和NHTSA同时介入调查与缺陷评估。

## Approach
- 这不是一篇算法论文，而是一份**事故/事件调查通报**；核心机制是基于**视频证据、车辆行为记录、远程协助交互**来还原事件经过并识别可能失效环节。
- 事件链条可简化为：ADS车辆先在对向车道停车 → 车辆向远程协助发出提示“**is this a school bus with active signals?**” → 远程协助人员回答“**No**” → 车辆恢复行驶并在校车停车臂仍伸出时通过。
- 通报特别指出该车运行的是**Waymo第5代ADS（SAE L4）**，且当时车内无人，这说明系统应在限定ODD内独立处理驾驶与安全关键决策。
- NTSB的目标是继续调查**1月12日事件及其他类似事件**，确定可能原因，并提出安全建议以避免再次发生。

## Results
- 已确认的关键结果是：**2026年1月12日7:55 a.m.**，一辆**2024 Jaguar I-Pace**搭载Waymo第5代ADS，在Austin一辆**2025 Thomas Built**校车上下学生时违法通过；**未发生碰撞**。
- 现场条件为：道路限速**35 mph**，**白天、晴天、干燥路面**；校车当时**红灯闪烁且两侧停车臂伸出**，说明环境并不恶劣，失效并非由明显天气/能见度问题触发。
- 视频证据显示：ADS车辆最初是**第一辆停车**的车，但在远程协助回复“**No**”后重新起步；最终**共有6辆车**在校车停靠期间通过，其中包括该ADS车辆及其后方一辆乘用车。
- Austin ISD称自**2025/2026学年开始**已出现**多起**Waymo车辆通过停靠校车事件；文中明确提到除1月12日外，还有**1月14日**一起涉及**2023 International**特殊需求路线校车的事件。
- 监管层面的具体进展包括：NHTSA缺陷调查办公室于**2025年10月17日**开启初步评估**PE25013**；Waymo于**2025年12月10日**通知NHTSA进行安全召回**25E-084**，涉及**3,067辆**搭载其**第5代ADS**的车辆软件更新。
- 文本**没有提供正式性能指标、基准对比或统计显著性结果**；最强的具体主张是：NTSB已识别出重复发生的校车通过事件，并正调查其可能原因以形成安全建议。

## Link
- [https://www.ntsb.gov:443/investigations/Pages/HWY26FH007.aspx](https://www.ntsb.gov:443/investigations/Pages/HWY26FH007.aspx)
