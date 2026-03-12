---
source: arxiv
url: http://arxiv.org/abs/2603.04245v1
published_at: '2026-03-04T16:33:35'
authors:
- Jialiang Wei
- Ali Ebrahimi Pourasad
- Walid Maalej
topics:
- human-ai-interaction
- ui-feedback
- multimodal-generation
- image-editing
- mobile-apps
relevance_score: 0.7
run_id: materialize-outputs
---

# LikeThis! Empowering App Users to Submit UI Improvement Suggestions Instead of Complaints

## Summary
本文提出 **LikeThis!**，用生成式 AI 帮助普通 App 用户把模糊抱怨转成可视化、可操作的 UI 改进建议。核心价值在于改善用户—开发者之间的反馈质量，让开发团队更容易理解并采纳真实需求。

## Problem
- 用户提交的移动应用反馈常常**含糊、破坏性强或缺少细节**，开发者难以理解并采取行动。
- 仅靠文字评论很难准确表达具体的 UI 改进想法，普通用户又**不会使用专业设计工具**制作 mockup。
- 现有 GenAI/AI4SE 工作多聚焦于**生成代码或全新 UI**，而不是帮助用户**编辑现有界面并提交原位改进建议**。

## Approach
- 提出一个两阶段流程：输入**用户评论 + 当前界面截图**，先生成多个文本化的**解决方案规格**，再据此编辑原始 UI 图像，产出多个改进候选图。
- 第一步由多模态大模型生成若干替代性设计建议，每个建议包含简短标题和具体修改说明，同时生成当前界面的描述。
- 第二步把“用户问题 + 界面描述 + 方案规格 + 原截图（可选 mask）”送入图像编辑模型，生成对应的改进后 UI。
- 用户从 3 个候选方案中选择最符合自己意图的一个，再连同原始问题一起提交给开发者，从而把“抱怨”转化为“建议”。
- 作者还实现了一个 **iOS 原型**；实证中采用 GPT-4o 做建议生成，GPT-Image-1 做 UI 编辑，并研究了 mask 与去除中间步骤的影响。

## Results
- 在基于 **UICrit** 的模型基准测试中，作者从 **300** 个 critique/screen 构造评测集，其中 **120** 张用于模型对比；双标注者在 **120 tasks** 上共形成 **240 annotations**，一致率 **80.42%**。
- **GPT-Image-1** 明显优于 Flux、Gemini、Bagel：在用户偏好中获得 **214** 次 rank-1，而其他模型仅 **14 / 8 / 4** 次；其平均问题解决分数约 **2.74–2.75**，而其他模型为 **1.38–1.83**；平均保真度 **2.83**，鲁棒性 **2.88–2.89**。论文称这些优势在相关比较上达到统计显著（**Wilcoxon-Mann-Whitney, p ≤ 0.05**）。
- 按计数看，GPT-Image-1 在 **240** 次注释中有 **200** 次被评为“完全解决问题”，而 Flux/Gemini/Bagel 分别为 **58/73/32**；这也支持作者所述其他模型仅能在约 **25%–53%** 的界面上至少部分解决问题。
- 用户研究覆盖 **10** 个生产 App、**15** 名用户；参与者认为 **85.5%** 的生成建议是“多数准确”或“非常准确”。
- 开发者评估表明，带有生成改进图的反馈相比不带改进图的反馈，**更易理解、也更可执行**；摘要与引言给出的是方向性结论，节选中未提供更细的开发者侧量化数值。
- 消融结论显示，中间的 **Suggestion Generation** 步骤对高质量 UI 改进是关键；mask 仅在**问题区域较小**时更有帮助，较大区域时会降低保真度并更容易引入新问题。

## Link
- [http://arxiv.org/abs/2603.04245v1](http://arxiv.org/abs/2603.04245v1)
