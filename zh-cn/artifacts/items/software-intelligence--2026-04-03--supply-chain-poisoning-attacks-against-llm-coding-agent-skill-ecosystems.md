---
source: arxiv
url: http://arxiv.org/abs/2604.03081v1
published_at: '2026-04-03T14:58:58'
authors:
- Yubin Qu
- Yi Liu
- Tongcheng Geng
- Gelei Deng
- Yuekang Li
- Leo Yu Zhang
- Ying Zhang
- Lei Ma
topics:
- llm-agents
- software-supply-chain-security
- prompt-injection
- code-generation-security
- agent-skills
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Supply-Chain Poisoning Attacks Against LLM Coding Agent Skill Ecosystems

## Summary
## 摘要
本文研究针对从开放市场加载第三方技能的 LLM 编码代理的供应链攻击。文中提出一种投毒方法，把恶意代码藏在技能文档里，让代理在正常工作时复制并执行这些代码。

## 问题
- 编码代理会信任包含指令、代码示例和配置模板的技能文件，而这些代理通常对宿主机有文件、Shell 和网络访问权限。
- 先前工作研究了工具选择操控和文本输出投毒，但没有检验一个被投毒的技能是否能让代理在机器上直接执行恶意动作。
- 这很重要，因为一个恶意技能就可能导致数据外传、权限提升、构建或配置篡改，或其他宿主机层面的入侵，而且不需要用户明确输入恶意提示。

## 方法
- 论文提出 **Document-Driven Implicit Payload Execution（DDIPE，文档驱动的隐式载荷执行）**：把载荷藏在技能文档中看起来无害的代码示例或配置模板里。
- 当代理处理正常的编码或设置任务时，它会把这些示例当作可信参考代码，复现被投毒的模式，然后执行自己生成的输出。
- 这种攻击主要有两条嵌入路径：代码示例投毒和配置模板投毒。
- 为了扩大测试规模，作者构建了一个由 LLM 驱动的种子-变异-验证流水线，把 81 个种子技能扩展成覆盖 15 个 MITRE ATT&CK 类别的对抗变体。
- 该攻击还使用合规措辞、看起来像内部服务的端点和静默异常处理来降低被发现的概率。

## 结果
- 评估覆盖 **1,070 个对抗性技能**、**4 个代理框架**（Claude Code、OpenHands、Codex、Gemini CLI）和 **5 个模型**（Claude Sonnet 4.6、GLM-4.7、MiniMax-M2.5、GPT-5.4、Gemini 2.5 Pro）。
- DDIPE 在测试配置下的绕过率达到 **11.6% 到 33.5%**。
- 在论文报告的最强防御下，显式指令注入基线的结果是 **0%**。
- 静态分析拦截了 **90.7%** 的攻击，但仍有 **2.5%** 同时逃过静态检测和模型对齐。
- 移除架构防护后，某个模型的执行率最高提升 **11.3 倍**；另一个模型变化不大，这说明对齐和框架防御之间的作用会因模型而异。
- 负责任披露促成了 **4 个已确认漏洞** 和 **2 个已部署修复**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03081v1](http://arxiv.org/abs/2604.03081v1)
