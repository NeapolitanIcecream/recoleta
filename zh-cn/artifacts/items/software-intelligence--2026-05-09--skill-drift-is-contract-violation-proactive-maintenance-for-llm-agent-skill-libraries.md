---
source: arxiv
url: https://arxiv.org/abs/2605.10990v1
published_at: '2026-05-09T11:41:53'
authors:
- Linfeng Fan
- Yuan Tian
- Ziwei Li
- Zhiwu Lu
topics:
- llm-agents
- skill-libraries
- software-maintenance
- code-intelligence
- agent-repair
- drift-detection
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Skill Drift Is Contract Violation: Proactive Maintenance for LLM Agent Skill Libraries

## Summary
## 摘要
SkillGuard 将过时的 LLM 智能体技能视为环境契约失效，只检查会影响执行的假设。论文称，这样可以减少误报，同时仍能发现真实的 API、包、URL、配置和 schema 漂移。

## 问题
- LLM 智能体会复用技能库来处理软件任务，但当外部包、API、URL、配置、schema 或认证流程在技能写成之后发生变化时，技能就会失效。
- 现有监控常常盯着原始值，因此会对无害变化报警，比如注释里的版本号或文档重定向。
- 这很重要，因为噪声报警会让长期维护智能体技能变得困难，而漏掉漂移会让智能体继续运行过时流程。

## 方法
- SkillGuard 从技能文档中提取环境提及，包括 URL、版本、导入、API 路径、环境变量、Docker 镜像、GitHub Actions、CLI 标志和配置文件。
- 它把每个提及标记为操作性或附带性。只有操作性提及才会变成需要验证的契约。
- 契约记录类型、角色、值和证据跨度。验证会把这些契约与已知漂移事件或注册表、URL 检查等实时来源进行匹配。
- 失效契约会给修复模型一个局部编辑目标：过时的值、它的位置，以及在可用时的新条件。
- 论文还发布了 DriftBench，这是一个包含受控漂移、真实世界漂移、同一性对、格式硬负例和语义硬负例的 880 对基准。

## 结果
- DriftBench 包含 174 对受控漂移配对、107 对真实世界漂移配对和 599 个负对照；受控拆分的裁定有效率为 99.6%，真实世界拆分的有效率为 100%。
- 不带契约的 CI 探针产生 40% 的误报，而 SkillGuard 在 599 个无漂移和硬负例样本上报告 0 误报，Wilson 95% CI 为 [0%, 0.6%]。
- 在已知漂移验证中，5 个测试骨干模型都达到 100% 精度。Qwen3.6-Plus 的召回率最好，为 76%，95% CI 为 [62%, 88%]。
- 其他已知漂移召回率分别为 DeepSeek-R1 62%、DeepSeek-V3.2 57%、GLM-5.1 54% 和 Qwen3-235B-A22B 24%，精度都为 100%。
- 基线结果显示，Grep/diff 的召回率为 30%；类似 Dependabot 的扫描召回率为 11%，FPR 为 10%；类似 NL2Contract 的抽取召回率为 45%，FPR 为 0%；不带契约的 CI 探针召回率为 30%，FPR 为 40%。
- 在一项预注册的 49 个真实技能实时扫描中，SkillGuard 标记了 14 个技能，其中 12 个真阳性、2 个假阳性、10 个假阴性、25 个真阴性，得到 86% 的保守精度、55% 的召回率和 7% 的 FPR。基于契约的单轮修复成功率为 78%，高于不做定位时的 10%、仅用普通漂移文本时的 60%、三轮 Self-refine 的 80%，也与完整漂移规格下的 78% 持平。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10990v1](https://arxiv.org/abs/2605.10990v1)
