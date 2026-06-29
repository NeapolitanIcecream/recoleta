---
source: arxiv
url: https://arxiv.org/abs/2606.11863v1
published_at: '2026-06-10T09:38:40'
authors:
- Yufu Wang
- He Jiang
- Hao Lin
- Peiyu Zou
- Ang Jia
- Xiaochen Li
- Zhilei Ren
topics:
- code-translation
- code-intelligence
- llm-agents
- semantic-augmentation
- software-reliability
- automated-testing
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Enhancing LLM-Based Code Translation with Verified Multi-Semantic Representations

## Summary
## 总结
Multisage 通过从源代码中提取语义指导并在提示翻译器之前检查这些指导，来提升 LLM 代码翻译效果。
它面向 HumanEval-X 上的功能正确性，报告的成功率提升最高可达 2.22×。

## 问题
- LLM 代码翻译器可能生成能够编译、但会改变控制流、数据处理、类型或 API 行为的目标代码。
- 测试用例、文档和规范可以减少这类错误，但许多真实代码库没有这些资源。
- 论文指出，许多失败属于可以干预的语义错误；在轻量级模型中，模型特定错误只占失败的 10%–23%。

## 方法
- Multisage 先用静态分析解析源代码，提取控制流结构、函数输入/输出类型和外部 API 调用。
- 随后，它基于这些解析信号生成多种语义视图：代码摘要、函数级测试用例、API 描述和 API 级测试用例。
- 它使用 XLCoST 和 XCodeEval 等数据集训练一个多任务语义增强模型，并采用受 FAMO 和 MFTCoder 启发的自适应任务加权。
- 它通过执行验证、保持语义不变的代码变异和跨视图一致性测试来检查生成的语义，然后过滤较弱或相互冲突的指导。
- 校准后的语义指导和原始源代码一起放入提示词中，供目标语言 LLM 翻译。

## 结果
- 在 HumanEval-X 上，Multisage 在测试的各个主干模型中，相比普通提示，报告的翻译成功率提升最高可达 2.22×。
- 与 Chain-of-Thought 和单阶段语义提示等语义增强基线相比，它在小模型上的成功率最高提升 1.42×，在中等规模模型上提升 1.28×，在大模型上提升 1.17×。
- 论文将评估模型分为三类：参数少于 10B 的轻量级模型、10B–100B 参数的中等规模模型，以及超过 100B 参数的高性能大模型。
- 在相同评估设置下，与 TransCoder 相比，Multisage 的 CodeBLEU 更高，同时保持了有竞争力的执行成功率；摘要没有给出具体的 CodeBLEU 数值。
- 报告中的相对增益在较小模型上最大，这说明当主干模型容量有限时，新增的语义指导最有帮助。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.11863v1](https://arxiv.org/abs/2606.11863v1)
