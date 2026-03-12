---
source: hf_daily
url: https://huggingface.co/papers/2603.07980
published_at: null
authors: []
topics:
- agent-benchmark
- language-agents
- professional-reasoning
- evaluation
- tool-use
relevance_score: 0.88
run_id: fa4f5d9d-bee2-47ee-b80f-c690622f57d0
---

# \$OneMillion-Bench: How Far are Language Agents from Human Experts?

## Summary
### TL;DR: 该论文提出 **$OneMillion-Bench**，一个面向法律、金融、医疗、工业和自然科学等高价值专业场景的 400 题基准，用来衡量语言代理距离“人类专家级可靠执行复杂真实工作”还有多远。

### Problem:
- 现有大模型/代理基准大多停留在考试题、结构化问答或短程推理，难以反映真实专业工作中的多步决策、证据检索和规则应用能力。
- 在高风险行业里，模型不仅要“答对”，还要能处理权威来源、冲突证据、合规约束和实际可执行性，因此传统只看最终答案的评测不够用。
- 缺少一个统一、跨行业、面向经济价值和专家级任务难度的评测集，导致难以判断语言代理是否已接近可落地的专业生产力工具。

### Approach:
- 构建了 **400 个由专家策划的真实专业任务**，覆盖 **Law、Finance、Industry、Healthcare、Natural Science** 五大领域。
- 每个任务都要求代理完成更接近真实工作的流程：**检索权威资料、消解相互冲突的证据、应用领域规则、做出受约束的决策**。
- 采用 **rubric-based evaluation**，从 **事实准确性、逻辑一致性、实践可行性、专业合规性** 等维度打分，而不只看最终答案是否匹配。
- 基准强调 **expert-level problems**，目标是拉开不同代理系统在专业深度、可靠性和实际 readiness 上的差距。
- 该基准还引入“**任务市场价值**”视角：社区解读显示任务依据真实专业工资进行了定价，总价值超过 **100 万美元**。

### Results:
- 论文的核心产出是一个新基准，而不是提出新的代理方法；**给定摘录中未提供具体模型排行榜、准确率、胜率或相对基线提升数字**。
- 明确给出的规模信息：**400 个任务**，覆盖 **5 个行业/学科领域**。
- 数据集构建投入很高：社区信息称由真实领域专家耗时 **2000+ 小时** 策划整理。
- 任务总经济价值被定价为 **超过 100 万美元**，这是其命名的重要来源，也凸显了评测目标是“高价值专业劳动”而非普通问答。
- 最强具体主张是：该基准比既有评测更能衡量代理在 **长程推理、工具使用、证据解析、专业合规与实际决策** 上的真实职业能力与可靠性。

## Links
- Canonical: https://huggingface.co/papers/2603.07980
