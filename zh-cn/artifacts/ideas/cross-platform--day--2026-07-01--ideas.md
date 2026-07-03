---
kind: ideas
granularity: day
period_start: '2026-07-01T00:00:00'
period_end: '2026-07-02T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- AI coding agents
- Flutter
- Agent Development Kit
- developer skills
- frontend generation
tags:
- recoleta/ideas
- topic/ai-coding-agents
- topic/flutter
- topic/agent-development-kit
- topic/developer-skills
- topic/frontend-generation
language_code: zh-CN
---

# 可审查的 Flutter 生成工作流

## Summary
这个案例给为 ADK agent 构建 Flutter 客户端的团队提供了一个实用模式：让编码 agent 在写代码前创建可审查的接口、用法、架构和设计文件，再把每次失败运行的修复写入可复用技能。最明确的构建目标是一个小型 ADK Flutter 客户端工作流，并带有生成后检查，覆盖平台权限、markdown、流式事件、Web 网络和工具调用显示。

## 为 ADK 客户端生成 Flutter 代码前使用分阶段规划文件
为 ADK agent 构建 Flutter 客户端的团队，可以要求编码 agent 在编写 UI 代码前先产出四个可审查文件：`AGENT_INTERFACE_NOTES.md`、`FRONTEND_USAGE_NOTES.md`、`FRONTEND_ARCHITECTURE_NOTES.md` 和 `FRONTEND_DESIGN_NOTES.md`。这样开发者能在修改成本还低时，检查后端接口、预期用户行为、状态模型和视觉方案。

有用的采用方式是在编码 agent 工作流中加入一道关卡。agent 读取 ADK 代码库，起草这些笔记，暂停等待审查，然后才生成 Flutter 应用。一个低成本测试方法是：把该工作流用于两个已有但没有前端的 ADK agent，检查这些笔记是否在生成代码前正确识别流式行为、API、工具调用和所需客户端状态。

### Evidence
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): 文章列出了四个规划文件，并说明了它们在代码生成前的作用。
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): 作者使用第二个 Antigravity 对话，在更新工作流前检查笔记、规格说明和代码结构。

## 针对 ADK Flutter 客户端故障模式的生成后检查
面向 ADK agent 的可复用 Flutter 前端技能，应包含一份生成后检查清单，针对应用在真实目标平台运行时出现的故障。清单可以覆盖 macOS 和 iOS 网络权限、使用 `flutter_markdown` 渲染 markdown、lint 和格式化规则、sealed 消息类型、聊天自动滚动、用于 Web 构建的 `package:http` 网络代码、部分流式事件聚合，以及工具调用显示。

这是生成式客户端的一层具体支持。编码 agent 可以运行格式化和 lint 检查，扫描面向 Web 的网络代码中是否有 `dart:io`，验证 entitlements，并加入一个小型流式事件测试：先组装 ADK 的部分事件，再把完成的消息加入会话列表。这些检查针对的是单次代码生成可能漏掉的错误。

### Evidence
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): 迭代日志列出了权限、markdown、lint、消息类型、滚动、Web 网络、部分事件和工具调用显示方面的具体故障与修复。
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): 摘要确认，部分 ADK 流式事件通过累积 `event.partial` 片段处理，并将完成的事件加入会话列表。

## 把人工 Flutter 修复转成技能更新的审查循环
在不熟悉的 ADK 后端上使用编码 agent 的开发者，可以为可复用技能保留一个单独的审查循环。一个 agent 运行当前工作流并生成产物。第二个对话和开发者一起审查这些产物，记录缺口，并更新技能。更新后，删除生成的前端，再次运行工作流。

当开发者阅读生成的笔记和源文件、运行应用，并直接修复重复出现的故障时，这个流程效果最好。下一条提示会询问 Antigravity 如何把这些修复写入技能，让下一次生成的客户端从新学到的规则开始。这个工作流适合需要在 agent 会话结束后仍能解释和维护生成代码的团队。

### Evidence
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): 作者描述了安装已有技能、启动重复工作流、评估输出、更新指导、删除生成产物并重新运行的过程。
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): 文章说，作者研究了反复出现的故障，修改了笔记和代码，然后询问 Antigravity 如何更新技能，使未来生成结果符合这些修复。
