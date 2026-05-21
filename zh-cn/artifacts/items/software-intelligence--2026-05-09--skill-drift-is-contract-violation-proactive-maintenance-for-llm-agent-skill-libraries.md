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
SkillGuard 将过时的 LLM 智能体技能视为环境契约失效，并且只检查会影响执行的假设。论文声称，这种方法减少了误报，同时仍能发现真实的 API、软件包、URL、配置和 schema 漂移。

## 问题
- LLM 智能体会复用用于软件任务的技能库，但如果外部软件包、API、URL、配置、schema 或认证流程在技能写成后发生变化，技能就可能失效。
- 现有监控器通常监控原始值，因此会对注释中的版本号或文档重定向这类无害变化发出告警。
- 这会带来维护问题：噪声告警会让长期使用的智能体技能难以维护，而漏检的漂移可能导致智能体运行过时流程。

## 方法
- SkillGuard 从技能文档中抽取环境提及项，包括 URL、版本、import、API 路径、环境变量、Docker 镜像、GitHub Actions、CLI 标志和配置文件。
- 它将每个提及项标注为操作性或偶然性。只有操作性提及项会变成需要验证的契约。
- 契约记录类型、作用、值和证据片段。验证过程会将这些契约与已知漂移事件或实时来源匹配，例如注册表和 URL 检查。
- 失效契约会给修复模型一个局部编辑目标：过时值、它的位置，以及可用时的新条件。
- 论文还发布了 DriftBench，这是一个包含 880 对样本的基准，覆盖受控漂移、真实世界漂移、同一性样本对、格式化困难负例和语义困难负例。

## 结果
- DriftBench 包含 174 对受控漂移、107 对真实世界漂移和 599 个负对照；受控划分报告的裁定有效率为 99.6%，真实世界划分报告的有效率为 100%。
- 无契约 CI 探针产生 40% 的误报，而 SkillGuard 在 599 个无漂移和困难负例中报告 0 个误报，Wilson 95% CI 为 [0%, 0.6%]。
- 在已知漂移验证中，全部五个测试骨干模型都达到 100% 精确率。Qwen3.6-Plus 的召回率最高，为 76%，95% CI 为 [62%, 88%]。
- 其他报告的已知漂移召回率为 DeepSeek-R1 62%、DeepSeek-V3.2 57%、GLM-5.1 54%、Qwen3-235B-A22B 24%，精确率均为 100%。
- 基线结果为：Grep/diff 的召回率为 30%；Dependabot 风格扫描的召回率为 11%，FPR 为 10%；NL2Contract 风格抽取的召回率为 45%，FPR 为 0%；无契约 CI 探针的召回率为 30%，FPR 为 40%。
- 在一项预注册的 49 个真实技能实时扫描中，SkillGuard 标记了 14 个技能，其中 12 个真阳性、2 个假阳性、10 个假阴性、25 个真阴性，对应 86% 的保守精确率、55% 的召回率和 7% 的 FPR。契约引导的一轮修复成功率达到 78%，相比之下，无定位为 10%，仅使用普通漂移文本为 60%，三轮 Self-refine 为 80%，使用完整漂移规格为 78%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10990v1](https://arxiv.org/abs/2605.10990v1)
