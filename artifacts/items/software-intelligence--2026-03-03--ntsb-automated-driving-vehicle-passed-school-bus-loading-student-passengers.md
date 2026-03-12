---
source: hn
url: https://www.ntsb.gov:443/investigations/Pages/HWY26FH007.aspx
published_at: '2026-03-03T23:30:19'
authors:
- Animats
topics:
- autonomous-driving-safety
- ads-failure-analysis
- remote-assistance
- school-bus-compliance
- transportation-investigation
relevance_score: 0.12
run_id: materialize-outputs
---

# NTSB: Automated Driving Vehicle Passed School Bus Loading Student Passengers

## Summary
这不是一篇研究论文，而是NTSB对一起Waymo自动驾驶车辆在学校巴士停靠上下学生时违法通过事件的初步调查通报。其核心价值在于揭示了ADS在校车场景识别与远程协助决策链上的安全缺陷。

## Problem
- 该通报关注的问题是：**自动驾驶系统在学校巴士开启红灯和伸出停车臂、正在上下学生时，未能持续停车并最终违法通过**，这直接威胁儿童乘客安全。
- 之所以重要，是因为该车辆为**无人驾驶、SAE Level 4**系统，本应在限定运行域内独立处理安全关键场景；若在高风险校车场景失效，说明系统边界和安全保障可能不足。
- 事件还暴露出**远程协助误判**问题：车辆主动询问“这是不是一辆激活信号的校车？”，远程协助人员回答“No”，随后车辆恢复行驶并通过校车。

## Approach
- 这份材料的“方法”不是提出新算法，而是**基于事故调查**重建事件经过：使用车辆/道路环境描述、视频证据、校车外部摄像头记录以及运营方信息来分析系统行为。
- 调查重点放在**ADS感知—停车—请求远程协助—远程答复—恢复行驶**这一决策链，识别系统在校车法规遵循与异常场景处理上的薄弱环节。
- 通报同时将单次事件置于**更广泛的模式**中审视：Austin ISD报告自2025/2026学年开始已出现多起Waymo车辆通过停靠校车事件，说明这可能不是孤立失效。
- 相关监管动作包括**NHTSA缺陷初步评估（PE25013）**及Waymo对**3,067辆搭载第5代ADS车辆的软件召回（25E-084）**，表明问题已进入系统性安全审查。

## Results
- **2026年1月12日 7:55 a.m. CST**，一辆**2024 Jaguar I-Pace**、搭载Waymo**第5代ADS**的无人车，在德州奥斯汀**East Oltorf Street**上通过了一辆正在上下学生的校车；当时校车**红灯闪烁且停车臂已伸出**。
- 视频显示该ADS车辆起初是**第一个停车**的车辆，但在请求远程协助并收到“**No**”答复后，**在校车停车臂仍伸出时恢复行驶并通过**校车。
- 事件中**共有6辆车**在校车停靠期间通过，其中包括该ADS车辆及其后方一辆乘用车；**未发生碰撞**。
- Austin ISD报告称，自**2025/2026学年开始**已发生**多起**Waymo ADS车辆通过停靠校车事件；文中明确提到除1月12日外，还有**2026年1月14日**另一起涉及特殊需求路线校车的事件。
- Waymo已于**2025年12月10日**向NHTSA通报，对**3,067辆**搭载其**第5代ADS**的车辆进行软件召回更新；NHTSA缺陷调查办公室于**2025年10月17日**启动初步评估**PE25013**。
- 该文本**没有提供学术基准、实验数据或性能指标**；最强的具体结论是：真实道路中出现了**ADS+远程协助链条未能正确识别/遵守校车停车法规**的安全事件，并已触发联邦调查与软件召回。

## Link
- [https://www.ntsb.gov:443/investigations/Pages/HWY26FH007.aspx](https://www.ntsb.gov:443/investigations/Pages/HWY26FH007.aspx)
