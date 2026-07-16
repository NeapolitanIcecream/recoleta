---
kind: ideas
granularity: week
period_start: '2026-06-29T00:00:00'
period_end: '2026-07-06T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- AI coding agents
- Antigravity
- Flutter
- ADK
- agent skills
- cross-platform development
tags:
- recoleta/ideas
- topic/ai-coding-agents
- topic/antigravity
- topic/flutter
- topic/adk
- topic/agent-skills
- topic/cross-platform-development
language_code: zh-CN
---

# agent 生成的 Flutter 代码检查

## 摘要
这组材料中的 Antigravity 工作指向两类可用做法：面向 ADK 前端的可复用 skill，以及面向 Flutter 游戏逻辑的检查辅助工具。共同的采用阻碍是对生成代码的信任：当平台行为、流式事件或对时序敏感的物理逻辑在 prompt 之外失败时，团队需要能检查和验证代码。

## 用于 ADK agent 的 Flutter 前端可复用 Antigravity skill
在 Google Agent Development Kit 上构建演示或内部工具的团队，可以把每一次前端失败转成一次 Antigravity skill 更新。可用的模式很具体：要求 agent 在生成代码前产出接口说明、使用说明、架构说明和设计说明；审查这些产物；更新 `SKILL.md` 和参考文件；删除生成的前端；然后重新运行工作流。

这适合已有 Python ADK agent、但没有客户端团队立即接入 Flutter 的团队。这个案例经过 13 次迭代后，得到一个可分享的 `flutter_frontend_for_adk` skill。修复内容是跨项目常见的前端集成问题：macOS 和 iOS 网络权限、markdown 渲染、lint、sealed 消息类型、聊天滚动、`dart:io` 导致的 Web 崩溃、ADK partial event 聚合，以及工具调用显示。

一个低成本测试是用这个 skill 跑两个不同的 ADK 示例 agent，检查第二次运行是否需要更少的手动修复。验收线应包括一次 Web 构建、一个移动端目标、一条流式响应路径和一条工具调用显示路径，因为报告中的失败集中在这些地方。

### 资料来源
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): 概述可重复的 Antigravity 工作流、分阶段产物、双 agent 审查循环、13 次迭代，以及反复出现的 ADK 前端修复。
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): 点名 `flutter_frontend_for_adk` skill，以及代码生成前产出的规划文档。
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): 列出后续的具体修复，包括平台网络权限、markdown、lint、Web 网络、滚动和 ADK partial event。

## agent 生成前端代码的审查暂停和重新运行
agent 生成的前端工作需要在代码生成前设置明确的停止点。Antigravity ADK 案例在早期阶段后加入强制审查步骤，让人类开发者能在 agent 继续之前检查说明和计划。这个小的工作流改动很有用，因为开发者还要通过这个过程学习后端接口，而不只是拿到写好的文件。

可构建的版本是一个 Antigravity skill 仓库模板，它在发现、使用、架构和设计阶段后强制设置审查门。每个审查门都应在仓库中留下一个具名文件，并要求批准后才能继续生成。重新运行步骤应重置生成文件，让改进沉淀在 skill 中，而不是停留在某一次会话的本地偶然结果里。

这对维护内部 agent 模板的开发者赋能团队有用。它让团队能在工作推进时记录平台规则和项目约定，包括一些小但代价高的遗漏，例如 `frontend/lib` 文件被忽略，或缺少 macOS 和 iOS entitlement。

### 资料来源
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): 描述安装现有 Google Cloud 和 Flutter skill，然后建立由 coder agent 和 author agent 组成的迭代循环。
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): 展示一次具体更新：加入审查暂停并修复 gitignore 行为，随后清理文件并重新运行。
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): 把 skill 描述为开发者所学内容的记录，并报告经过 13 次迭代达到可分享版本。

## agent 构建的 Flutter 游戏的调试 overlay 和回放 checkpoint
使用 coding agent 的 Flutter 和 Flame 游戏团队，应在生成游戏逻辑时要求加入检查工具。在 DashLander 中，只阅读生成的数学代码不足以信任物理和碰撞行为。一个由键盘开启的调试模式显示地形数据、表面倾角和 hitbox，让开发者能指示 agent 修正错误计算。

回放逻辑需要第二层支持。Challenge Mode 使用过去高分的 ghost，避开了实时多人基础设施。测试暴露出毫秒级漂移：重放的着陆器在大部分运行过程中看起来正确，但接近结尾时会坠毁。修复方法是在 thruster event 处存储完整的 lander 状态，并把实时回放与这些 checkpoint 对比。

一个实用的采用测试是要求每个由 agent 构建的游戏原型，在添加更多内容前都带有碰撞和物理状态的调试 overlay，以及确定性回放检查。这样生成代码出错时，人类审查者能拿到证据，尤其是那些视觉输出直到运行后期都看似合理的地方。

### 资料来源
- [Vibe once, run anywhere with Antigravity and Flutter](../Inbox/2026-06-29--vibe-once-run-anywhere-with-antigravity-and-flutter.md): 报告最初的 Flutter 和 Flame 游戏、后续的 prompt 数量，以及为让代码可理解而进行重构和添加测试的需要。
- [Vibe once, run anywhere with Antigravity and Flutter](../Inbox/2026-06-29--vibe-once-run-anywhere-with-antigravity-and-flutter.md): 描述带有地形数据、相对倾角和碰撞 hitbox overlay 的调试模式，并引入回放不同步 bug。
- [Vibe once, run anywhere with Antigravity and Flutter](../Inbox/2026-06-29--vibe-once-run-anywhere-with-antigravity-and-flutter.md): 解释毫秒级调度漂移，以及使用 thruster event 处完整物理状态 checkpoint 的修复方法。
