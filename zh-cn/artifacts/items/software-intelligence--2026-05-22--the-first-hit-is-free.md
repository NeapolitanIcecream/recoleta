---
source: hn
url: https://whattotelltherobot.com/p/the-first-hit-is-free
published_at: '2026-05-22T22:28:04'
authors:
- stefie10
topics:
- human-ai-interaction
- ai-assisted-coding
- ai-policy
- robotics-software
- research-automation
relevance_score: 0.64
run_id: materialize-outputs
language_code: zh-CN
---

# The First Hit Is Free

## Summary
## 摘要
文章主张开放使用 AI，但人类要保留主导权：让 AI 写作、写代码和起草内容，再由有能力的人对结果负责。它的主要价值在于为 AI 辅助的研究、教学和机器人工作提供了一种可操作的政策立场。

## 问题
- AI 可以生成论文、幻灯片、代码和演示，这带来一个具体问题：谁对成果的质量、准确性和许可负责？
- 作者说，AI 帮助之所以重要，是因为它能加快研究沟通和软件工作，但领域知识不足会让使用者接受错误修正或糟糕的研究想法。
- 课程政策需要在允许真实使用 AI 的同时，保留学生处理难题所需的专业能力。

## 方法
- 核心方法是人主导的 AI 使用：让 Claude Code 等工具起草、翻译、实现和修复内容，再由人审阅并重新指引工具。
- 作者把这种模式用在真实任务上，包括 LaTeX 数学写作、Python 实现、Kalman 滤波器修改、ROS1 到 ROS2 的迁移、幻灯片生成和视频演示生成。
- 控制机制是领域判断。在 AIBO 项目中，Claude 提议修改源文件，而作者识别出 package.xml 可能才是构建问题，并引导工具调整方向。
- 这项政策在精神上接近 Linux 内核的立场：允许 AI 生成的贡献，但必须由明确的人审查、检查许可，并承担责任。

## 结果
- 文章没有报告基准测试、数据集或受控评估。
- Claude Code 完成了数学撰写支持、LaTeX 生成、Python 算法实现和错误修复，而这项任务作者尝试了 10 多年都没做成。
- 作者要求把扩展卡尔曼滤波器改成无迹卡尔曼滤波器，工具完成了修改。
- Claude 帮助把一个旧的 ROS1 程序转换为 ROS2，用于 AIBO 外联项目；作者说这个修复比自己单独做更快，但没有给出时间数据。
- 在 Brown 的一门课程里，某学期允许学生在所有课程作业中使用 AI，包括演示；有几名学生把它用于幻灯片、代码和视频演示。
- 当工具面对作者实验室的近期论文并被要求提出新研究想法时，它给出的想法很差，作者据此认为专家审查仍然必要。

## Problem

## Approach

## Results

## Link
- [https://whattotelltherobot.com/p/the-first-hit-is-free](https://whattotelltherobot.com/p/the-first-hit-is-free)
