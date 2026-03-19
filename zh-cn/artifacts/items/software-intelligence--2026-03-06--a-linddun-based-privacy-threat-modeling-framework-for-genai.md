---
source: arxiv
url: http://arxiv.org/abs/2603.06051v1
published_at: '2026-03-06T09:04:32'
authors:
- Qianying Liao
- Jonah Bellemans
- Laurens Sion
- Xue Jiang
- Dmitrii Usynin
- Xuebing Zhou
- Dimitri Van Landuyt
- Lieven Desmet
- Wouter Joosen
topics:
- privacy-threat-modeling
- generative-ai
- linddun
- ai-agents
- multi-agent-systems
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# A LINDDUN-based Privacy Threat Modeling Framework for GenAI

## Summary
本文提出一个面向生成式AI（GenAI）的、基于 LINDDUN 的隐私威胁建模框架，目标是让缺乏深度GenAI安全经验的软件工程师也能系统识别隐私风险。其核心贡献是把分散的GenAI隐私研究与案例分析整合进可复用的工程化知识库与方法。

## Problem
- 现有通用安全/隐私威胁建模方法对 GenAI 场景不够具体，难以覆盖模型输出泄露、代理调用、RAG/多代理传播等新型隐私风险。
- 组织在将 GenAI 集成到企业系统时，需要满足风险导向的隐私治理与合规要求，但缺少可直接用于系统架构分析的专用框架。
- 这很重要，因为文中引用研究指出，像 GPT-4 和 ChatGPT 这类模型在某些情境下分别有 **39%** 和 **57%** 的概率泄露私人信息，说明实际系统集成会放大隐私暴露风险。

## Approach
- 以 **LINDDUN** 作为基础框架，而不是从零重建；因为它成熟、可扩展，并已有工具支持，适合做 GenAI 隐私威胁的领域化增强。
- 采用双路径构建方法：**自上而下**系统梳理文献中的 GenAI 隐私威胁，**自下而上**对一个代表性的 **HR 聊天机器人**做数据流图（DFD）与隐私威胁分析。
- 文献侧共检索 **65** 篇论文，并在贡献描述中说明系统化纳入了 **58** 篇前沿论文，用来抽取 GenAI 使用范式、攻击者模型和威胁特征，再映射到 LINDDUN 知识库。
- 框架识别出 **4 类** GenAI 系统范式与 **6 个** Common Attacker Models（CAMs），覆盖用户-系统、跨边界、代理交互和系统内部残余泄露等数据流场景。
- 最终对 LINDDUN 的 **7** 类隐私威胁中的 **3 类**进行了扩展，并新增 **100** 个 GenAI 相关威胁示例；随后在一个 **AI Agent / 多代理助手**案例上进行验证，并由学界与工业界专家评审。

## Results
- 论文的主要“突破性结果”是提出了一个可操作的 **GenAI 专用隐私威胁建模框架**，并非一个模型算法，因此结果主要体现为知识库扩展与案例验证，而不是标准ML性能指标。
- 框架基于 **58** 篇前沿论文的系统化整理（方法部分提到初始识别 **65** 篇），并结合一个 **HR chatbot** 案例与一个额外的 **multi-agent GenAI assistant** 验证案例来构建与检验覆盖性。
- 相比原始 LINDDUN，作者声称该框架影响/扩展了 **7** 类隐私威胁中的 **3** 类，并向知识库新增 **100** 个 GenAI 示例，这是文中最明确的量化贡献。
- 文献统计结果给出 6 类 CAM 的出现比例：**CAM2 45%**、**CAM6 24%**、**CAM1 13%**、**CAM5 13%**、**CAM4 4%**、**CAM3 3%**，表明系统到用户泄露与系统内部残余泄露是文献中最常见的风险模式。
- 文中还引用外部基线现象来说明问题严重性：在所引研究中，**GPT-4 39%**、**ChatGPT 57%** 的情境下会泄露私人信息；这不是本文实验结果，但构成该框架的现实动机。
- 提供的摘录中**没有**给出更细的定量对比实验（如与其他威胁建模框架在召回率、覆盖率、时间成本上的直接基线比较），最强的实证主张是：该框架在 AI agent 系统上支持了“更全面的隐私分析”，并经过 **3 名**学术威胁建模专家和 **2 名**行业隐私专家验证。

## Link
- [http://arxiv.org/abs/2603.06051v1](http://arxiv.org/abs/2603.06051v1)
