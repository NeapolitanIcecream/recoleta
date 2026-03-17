---
source: arxiv
url: http://arxiv.org/abs/2603.09290v1
published_at: '2026-03-10T07:19:43'
authors:
- Shimin Di
- Xujie Yuan
- Hanghui Guo
- Chaoqian Ouyang
- Zhangze Chen
- Ling Yue
- Libin Zheng
- Jia Zhu
- Shaowu Pan
- Jian Yin
- Min-Ling Zhang
- Yong Rui
topics:
- llm-agents
- tool-standardization
- model-context-protocol
- multi-agent-systems
- scientific-ai
- software-reuse
relevance_score: 0.93
run_id: materialize-outputs
---

# ToolRosetta: Bridging Open-Source Repositories and Large Language Model Agents through Automated Tool Standardization

## Summary
ToolRosetta提出一个自动化框架，把GitHub上的异构开源代码仓库和API转换成可被LLM代理直接调用的MCP标准工具，以减少人工封装与复现实验的成本。其核心价值是在开放工具生态中按需发现、标准化并安全执行长尾专业工具，从而显著提升科学任务完成率。

## Problem
- 现有高价值工具大多埋在异构代码仓库中，缺少统一、可执行的标准接口，LLM很难可靠调用。
- 把仓库手工改造成MCP工具需要理解代码、配置环境、重写接口和调试服务，人工成本高且难以扩展。
- 固定且人工整理的工具库覆盖面有限，面对跨学科或OOD任务时常因“没有合适工具”而失败。

## Approach
- 使用分层多代理流程：Planning代理规划工具链，Tool-search代理检索并评估相关仓库，MCP-construction代理自动完成克隆、语义分析、环境配置和MCP服务生成。
- 将“仓库/API → MCP工具”视为统一翻译问题，把异构实现自动包装为标准化、可执行、可被LLM调用的服务接口。
- 引入Review-Revise-Fix迭代修复机制：当验证失败时，Review代理做根因分析并生成修复计划，循环改进直到测试通过或停止。
- 增加Security Agent，在工具生成与执行阶段检查隐私泄露、恶意逻辑和安全风险，降低开放源码直接执行的风险。
- 生成后的标准化工具不仅供ToolRosetta自身使用，也可注入其他代理系统，作为可迁移基础设施复用。

## Results
- 自动标准化规模：成功将**122个GitHub仓库**中的**1580个工具**转换为标准化可执行接口，覆盖**6个领域**与**35个子学科**。
- 仓库转换成功率：首轮成功率**53.0%**，高于GPT-4o仅生成`MCP_service.py`的基线**49.6%**；若让GPT-4o一次性生成完整仓库到MCP栈，成功率仅**3.3% (4/122)**；人工工程师为**82.9%**。
- 转换效率：平均每仓库**210.1秒**，相比人工**1589.4秒（26.5分钟）**，时间减少**86.8%**，约**7.6×**加速。
- 迭代修复收益：经三轮RRF后，领域宏平均成功率从**54.2%**升至**69.3%**（**+15.1个百分点**），加权基准成功率从**53.0%**升至**68.4%**；最大单领域提升出现在Scientific Community & Society，达**+24.4个百分点**。
- 下游任务表现：在六大科学类别上，ToolRosetta的宏平均任务完成准确率为**55.6%**，在35个子学科上平均为**52.1%**；在**5/6**个类别中排名第一。相对“最强基线”声称**超过31%**的宏平均准确率提升。
- OOD与迁移增强：在**21个OOD子领域**上，ToolRosetta平均准确率**57.4%**，显著高于SciToolAgent **11.7%**、ChemCrow **3.3%**、RepoMaster **24.0%**、OpenAgents **21.5%**；把其标准化工具注入RepoMaster后，宏平均从**24.2%→34.8%（+10.6）**，注入OpenAgents后从**22.0%→35.4%（+13.4）**。案例中还报告发现一种**铅含量降低50%**的钙钛矿配方，湿实验验证PCE为**17%**，接近预测区间**16%–19%**。

## Link
- [http://arxiv.org/abs/2603.09290v1](http://arxiv.org/abs/2603.09290v1)
