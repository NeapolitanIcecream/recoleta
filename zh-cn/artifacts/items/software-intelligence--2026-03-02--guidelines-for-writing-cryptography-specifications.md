---
source: hn
url: https://cfrg.github.io/draft-irtf-cfrg-cryptography-specification/draft-irtf-cfrg-cryptography-specification.html
published_at: '2026-03-02T23:44:02'
authors:
- themaxdavitt
topics:
- cryptography-specification
- technical-writing
- secure-implementation
- interoperability
- threat-modeling
relevance_score: 0.19
run_id: materialize-outputs
language_code: zh-CN
---

# Guidelines for Writing Cryptography Specifications

## Summary
这是一份面向密码学规范作者的指导文档，目标是让规范更清晰、精确、一致且可实现，从而提升安全性与互操作性。它不是提出新密码算法，而是系统总结如何编写高质量的密码协议与原语规范。

## Problem
- 密码学规范若存在歧义、不精确或表示不一致，容易直接导致实现错误、互操作失败和安全漏洞。
- 不同受众（实现者、研究者、协议设计者）对规范的需求不同；如果规范不能同时服务这些群体，软件保证性和安全审查都会受损。
- 数学符号、威胁模型、安全定义、错误处理和测试向量若描述不完整，会造成规范与实际实现之间的偏差，影响部署安全。

## Approach
- 提出一套编写原则：强调**简单性、精确性、一致性**，要求用清晰语言、统一术语、逻辑化结构和明确步骤减少误解。
- 针对密码学特有内容，给出数学表示规范：规范性算法描述必须使用 ASCII；要求建立“Mathematical Operators and Symbols”表，禁止同一符号多重含义，并建议用伪代码、示例和图示辅助解释。
- 强调规范内容本身要可复用和完整：尽量复用已有原语与规范，采用模块化接口，定义所有输入上的行为，尤其覆盖反序列化、错误处理和边界情况。
- 要求明确安全目标、形式化安全定义与威胁模型，并说明残余风险、侧信道考虑以及安全与性能之间的权衡。
- 面向实现者提出可验证性要求：提供覆盖逻辑分支的测试向量、可复现实验步骤，以及持久化的机器可读测试向量（如 JSON）。

## Results
- 文档的主要产出是**规范写作指南与强制性/建议性检查项**，而不是实验性算法结果；摘录中**没有提供量化基准、数据集或性能指标**。
- 它明确声称遵循这些指南可带来：更少歧义、更一致且正确的实现、更容易的安全分析，以及更强的互操作性，但未给出数值化提升幅度。
- 给出若干具体且可操作的规范要求，例如：规范性算法描述**必须使用 ASCII-only**；每个运算符在符号表中都要给出**3项信息**（ASCII 形式、操作描述、常数时间/可变时间说明）。
- 对测试向量提出具体覆盖要求：应覆盖**所有逻辑路径**、有效但退化的错误/提前退出情形，以及**攻击者可控输入**可触发的异常；对概率极低且不可行复现的分支，可注明不提供测试向量。
- 对符号使用提出强约束：例如**不得**在同一规范中复用 `^` 表示两种不同运算；若使用 Unicode 符号，仅可在说明性示例/图中出现，并必须提供 ASCII fallback。

## Link
- [https://cfrg.github.io/draft-irtf-cfrg-cryptography-specification/draft-irtf-cfrg-cryptography-specification.html](https://cfrg.github.io/draft-irtf-cfrg-cryptography-specification/draft-irtf-cfrg-cryptography-specification.html)
