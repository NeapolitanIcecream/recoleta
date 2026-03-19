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
- multimodal-benchmark
- geo-temporal-reasoning
- visual-localization
- temporal-inference
relevance_score: 0.37
run_id: materialize-outputs
language_code: zh-CN
---

# TimeSpot: Benchmarking Geo-Temporal Understanding in Vision-Language Models in Real-World Settings

## Summary
TimeSpot 是一个面向视觉语言模型的真实世界地理-时间理解基准，要求模型仅凭图像同时判断“在哪里”和“什么时候”。论文表明，当前最强VLM即使有不错的粗粒度地理识别能力，在时间推断和地理-时间一致性上仍明显不足。

## Problem
- 现有图像地理定位基准大多只评估“地点”，很少要求模型显式预测“时间”（季节、月份、当地时间、昼夜阶段）或检查两者是否物理一致。
- 这很重要，因为灾害响应、交通规划、导航、环境监测和世界建模都依赖同时正确理解地点与时间；只会猜国家但不会判断季节/时间，可能导致不可信甚至不安全的决策。
- 现有评测也常偏向地标、文字或检索式指标，难以测出模型是否真正利用阴影、植被、气候和建筑等细微信号进行物理落地推理。

## Approach
- 提出 **TimeSpot**：包含 **1,455** 张地面真实图像，覆盖 **80** 个国家，强调非地标、少文字、依赖细微物理线索的场景。
- 任务要求输出一个 **9字段结构化模式**：4个时间属性（season, month, local time, daylight phase）+ 5个地理属性（continent, country, climate zone, environment type, latitude/longitude）。
- 标注采用“程序化生成 + 人工核验”：月份、季节、昼夜阶段、当地时间由时间戳、时区和太阳星历计算；国家、气候区、坐标由地理元数据映射，并由人工检查视觉一致性与异常样本。
- 评测不仅看分类准确率，还看 **时间1小时窗准确率、时间MAE、坐标误差、地理大圆距离**，并检查跨字段物理一致性，如月份-季节-半球是否匹配、时间与昼夜阶段是否兼容。
- 作者还进行监督微调（SFT）作为诊断性干预，用于测试显式监督能否提升地理-时间理解，但摘要指出改进后仍不足。

## Results
- 数据集规模与覆盖：**1,455** 张图像、**80** 个国家；纬度范围 **-54.80 到 71.96**，经度范围 **-173.24 到 170.31**，具备全球分布。
- 论文核心结论：即使最强模型，**country accuracy 最高仅 77.59%**（Gemini-2.5-Flash-Thinking），但 **median geodesic error 仍达 892.54 km**，说明粗粒度定位正确并不代表真实空间推断可靠。
- 时间理解更弱：**time-of-day accuracy 最高仅 33.74%**（GLM-4.1V-9B-Thinking，按 **±1小时窗口**），对应 **time MAE 最好约 3:58**；说明模型很难从视觉线索稳定推断具体时间。
- 其他代表性结果：**season accuracy 最高 65.81%**（o4-mini），**month accuracy 最高 48.20%**（o4-mini），**daylight-phase accuracy 最高 64.09%**（Qwen-VL2.5-7B-Instruct）。
- 地理字段上，**continent accuracy 最高 90.51%**（Gemini-2.5-Flash），**country accuracy 最高 77.59%**（Gemini-2.5-Flash-Thinking），但最优 **mean distance** 仍接近 **892.54 km**，显示精细定位依旧很差。
- 摘要未给出SFT的具体增益数字；最强具体主张是：**监督微调虽有改善，但整体结果仍不足以支持稳健、物理落地的地理-时间理解**。

## Link
- [http://arxiv.org/abs/2603.06687v1](http://arxiv.org/abs/2603.06687v1)
