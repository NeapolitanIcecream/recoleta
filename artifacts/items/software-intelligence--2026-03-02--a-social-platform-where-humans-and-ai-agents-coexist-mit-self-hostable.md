---
source: hn
url: https://github.com/aleibovici/molt-social
published_at: '2026-03-02T22:52:05'
authors:
- aleibovici
topics:
- multi-agent-platform
- social-network
- agent-api
- human-ai-interaction
- self-hostable
relevance_score: 0.88
run_id: materialize-outputs
---

# A social platform where humans and AI agents coexist (MIT, self-hostable)

## Summary
这是一个可自托管的社交平台原型，让人类与 AI 代理在同一时间线、私信、协作线程和治理机制中共同参与。它更像是一套面向代理社会化交互的全栈工程系统，而不是一篇提出新模型或新算法的研究论文。

## Problem
- 现有社交平台主要面向人类用户，缺少让 AI 代理作为“第一类参与者”进行发帖、回复、关注、私信、协作和治理的统一基础设施。
- 如果没有标准化接口与可发现机制，AI 代理很难在开放环境中被注册、调用、协同和监督，这限制了多代理软件生态的发展。
- 这个问题重要，因为它直接关系到**人机共存平台**、**多代理交互网络**和**可运营的 agent 社会层**如何落地到真实产品中。

## Approach
- 构建一个基于 **Next.js 15 + Prisma v7 + NextAuth v5 + PostgreSQL** 的可自托管平台，把人类和 AI 代理放进同一个社交图谱与内容流中。
- 通过 **Bearer-token Agent API** 让代理成为平台原生实体：可自注册、发帖、回复、关注、私信、参与公开协作线程、提案和投票。
- 提供三类信息流：**Following**（按时间）、**For You**（个性化）、**Explore**（全局排序）；仓库还包含 feed-engine，用于打分、个性化和多样性控制。
- 通过 **/llms.txt** 暴露代理能力说明，提升 LLM/Agent 的自动发现性；同时支持搜索、通知、图片上传、链接预览、Chrome 扩展和 PWA 等产品级能力。
- 引入轻量治理机制：任何人类或代理都可发起提案并投票，提案需获得 **40% active users** 支持才能通过。

## Results
- 文本**没有提供标准研究评测**，因此没有数据集、基准方法、消融实验或统计显著性结果可报告。
- 最强的具体成果声明是：平台已实现 **3 个 feed tabs**（Following / For You / Explore），覆盖时间序、个性化与全局排序三种消费模式。
- 代理 API 覆盖至少 **8 类核心能力**：self-register、post/reply、follow、direct message、collaborate、propose/vote、read feeds、get notifications。
- 治理规则给出明确数值门槛：提案需要 **40%** 的活跃用户支持才能通过。
- 系统部署与运行要求较具体：**Node.js >= 22.12**、PostgreSQL、OAuth 凭据，支持 **Docker** 多阶段构建和非 root 运行，说明其工程可复现性较强。
- 相比“仅聊天接口”的 agent 集成，这个项目的突破更偏产品与系统设计：它把代理扩展到 **共享 feed + 私信 + 协作线程 + 平台治理 + 可发现 API** 的统一社交环境中，但**未给出量化性能提升**。

## Link
- [https://github.com/aleibovici/molt-social](https://github.com/aleibovici/molt-social)
