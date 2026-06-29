---
source: hn
url: https://blog.janestreet.com/formal-methods-at-jane-street-index/
published_at: '2026-06-14T23:00:33'
authors:
- dcre
topics:
- formal-methods
- agentic-coding
- programming-languages
- code-verification
- type-systems
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Formal Methods and the Future of Programming

## Summary
## 摘要
Jane Street 说，代理式编程让形式化方法在软件生产中更实用，也更有价值。文中认为，证明工具可以减轻代码评审负担，给代理更好的反馈，并帮助强制执行测试覆盖不到的代码库不变量。

## 问题
- 代理生成的代码在发布前通常需要大量人工审查。
- 测试只覆盖状态空间的一部分，因此会漏掉一些漏洞和不变量违规。
- 对大多数软件来说，完整形式化验证的成本一直太高，所以采用范围一直有限。

## 方法
- 使用代理和模型来降低编写和维护证明的成本。
- 把形式化方法当作编码代理的反馈信号，和测试、基于属性的测试一起使用。
- 扩展编程语言 OxCaml，加入更强的类型级约束、模块化规格和更适合证明的特性。
- 把语言设计和证明工具结合起来，让日常开发里更容易表达和检查保证。

## 结果
- 摘要里没有报告定量实验结果。
- 最强的说法是战略层面的：代理式编程改变了成本和收益的平衡，Jane Street 因此正在组建一个形式化方法团队。
- 文中把 seL4 作为旧式验证的成本基线：验证 8,700 行 C 代码用了 25 人年，每行代码大约对应 23 行证明，并且每行代码大约需要半个人天来验证。
- 文中说，当类型系统里编码了相应约束时，类型已经可以消除数据竞争、跨站脚本这类整类缺陷。
- 文中认为，形式化方法可以减少代理编写代码的验证工作，并提高代理在困难任务上的表现，但没有给出基准数字。

## Problem

## Approach

## Results

## Link
- [https://blog.janestreet.com/formal-methods-at-jane-street-index/](https://blog.janestreet.com/formal-methods-at-jane-street-index/)
