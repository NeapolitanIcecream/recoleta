---
source: arxiv
url: http://arxiv.org/abs/2603.06687v1
published_at: '2026-03-04T07:27:35'
authors:
- Azmine Toushik Wasi
- Shahriyar Zaman Ridoy
- Koushik Ahamed Tonmoy
- Kinga Tshering
- S. M. Muhtasimul Hasan
- Wahid Faisal
- Tasnim Mohiuddin
- Md Rizwan Parvez
topics:
- vision-language-models
- geo-temporal-reasoning
- benchmarking
- image-geolocation
- temporal-inference
relevance_score: 0.46
run_id: materialize-outputs
language_code: zh-CN
---

# TimeSpot: Benchmarking Geo-Temporal Understanding in Vision-Language Models in Real-World Settings

## Summary
TimeSpot 是一个用于评测视觉语言模型真实世界地理-时间理解能力的基准，要求模型仅凭图像同时预测“在哪里”和“什么时候”。论文显示，当前最强VLM即使在粗粒度地理定位上看似不错，但在时间推断和跨字段物理一致性上仍明显不足。

## Problem
- 现有视觉地理定位基准大多只评估**地点**，很少要求模型显式预测**季节、月份、当地时间、昼夜阶段**等时间属性。
- 这很重要，因为灾害响应、交通规划、具身导航、世界模型等应用不仅需要知道“在哪里”，还需要知道“何时”，否则会产生物理上不合理的判断。
- 论文还指出，仅靠检索式定位指标会掩盖问题：模型可能国家猜对了，但坐标误差很大、时间判断很差，且地理与时间字段彼此矛盾。

## Approach
- 提出 **TimeSpot**：一个包含 **1,455 张**地面图像、覆盖 **80 个国家** 的基准，强调非地标、少文字、依赖阴影、植被、建筑、气候等细微物理线索。
- 每张图要求输出一个**9字段结构化模式**：4个时间属性（season, month, local time, daylight phase）和5个地理属性（continent, country, climate zone, environment type, latitude, longitude）。
- 标注采用**程序化生成 + 人工核验**：月份/季节/昼夜阶段/当地时间由时间戳、时区和太阳天文信息确定；国家、大陆、气候带等由坐标和地理数据库映射得到，再由人工审核边界样本。
- 评测不仅看分类准确率，还看**时间1小时窗口准确率、时间MAE、经纬度误差、地表大圆距离误差**，并加入**跨字段一致性**与可信度诊断。
- 论文还进行了**监督微调（SFT）**作为诊断性干预，以检验显式监督能否提升地理-时间理解。

## Results
- 基准规模为 **1,455** 张图像，覆盖 **80** 个国家；摘要中称数据来自 **80 countries**，统计表中列出 **82 unique countries**，文本存在轻微数字不一致。
- 最强国家分类结果达到 **77.59% country accuracy**（**Gemini-2.5-Flash-Thinking**），但其**中位/文中强调的地理距离误差**仍高达 **892.54 km**，说明“国家猜对”不代表精确定位可靠。
- 时间推断明显更难：**time-of-day accuracy** 最高只有 **33.74%**（**GLM-4.1V-9B-Thinking**，按 ±1 小时窗口），对应 **3:58** 的时间MAE；摘要也明确指出时间表现整体很低。
- 在地理字段上，较强模型如 **Gemini-2.5-Flash-Thinking** 达到 **90.31% continent accuracy、77.59% country accuracy、70.86% climate accuracy、64.47% environment accuracy**，但时间字段仅有 **51.13% season、24.26% month、22.19% time accuracy、36.56% daylight-phase accuracy**。
- 某些模型在粗分类上强，但坐标级误差依旧大。例如 **Gemini-2.5-Flash-Thinking** 的纬度/经度 MAE 为 **3.04° / 9.85°**，距离误差 **892.54 km**；**GLM-4.5V-106B-MoE** 国家准确率 **69.68%**，但距离误差仍有 **1280.87 km**。
- 论文的核心结论是：即便经过评测和监督微调，当前SOTA VLM 仍缺乏稳健、物理落地的联合地理-时间理解能力，尤其在时间 grounding 和 geo-temporal consistency 上不足；文段未给出 SFT 的完整量化提升数字。

## Link
- [http://arxiv.org/abs/2603.06687v1](http://arxiv.org/abs/2603.06687v1)
