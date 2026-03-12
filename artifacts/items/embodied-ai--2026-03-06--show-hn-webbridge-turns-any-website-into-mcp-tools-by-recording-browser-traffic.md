---
source: hn
url: https://github.com/jalabulajunx/WebBridge
published_at: '2026-03-06T23:29:40'
authors:
- nonstopnonsense
topics:
- mcp-tools
- browser-automation
- traffic-recording
- api-reverse-engineering
- privacy-audit
relevance_score: 0.06
run_id: materialize-outputs
---

# Show HN: WebBridge turns any website into MCP tools by recording browser traffic

## Summary
WebBridge把用户在Chrome中记录到的网站网络流量，自动转换成可被MCP客户端调用的工具服务器，目标是在**无需写代码、无需网站配合**的情况下把任意网站接入AI工作流。它还扩展到隐私/合规审计：通过“全量抓包”把真实网络请求作为证据交给模型分析。

## Problem
- 许多网站没有官方API、SDK或现成MCP集成，导致把网站能力接入Claude/Cursor等MCP客户端通常需要手写逆向代码，门槛高、耗时长。
- 网站自动化不仅要理解请求结构，还要处理认证、会话、字段映射、测试、安装和后续API变更维护，这些步骤碎片化且容易出错。
- 对隐私/合规团队而言，文档声明与应用真实发出的网络流量可能不一致；仅看隐私政策无法验证实际数据共享行为。

## Approach
- 用Chrome扩展通过 **Chrome DevTools Protocol** 录制用户正常操作时的API流量；利用浏览器现有登录态，通过cookies/脚本桥接认证，而不是保存密码或令牌。
- 让Claude读取录制结果，识别其中的API操作，询问工具名称和关键字段，然后自动生成**带类型的MCP server**，通过标准MCP/JSON-RPC over stdio 暴露给任意兼容客户端。
- 提供端到端流水线：`record -> read_recordings -> write_server -> test -> install -> update`，并内置常见错误自检，如ESM配置、错误的bridge模式、低层MCP API误用。
- 通过原生宿主和Unix socket在Chrome与生成的服务器之间转发请求；支持HAR导入、增量更新（只重生成受影响工具）、以及某些站点的后台标签页保活来维持JS会话。
- “Full Dump”模式不用于生成工具，而是抓取全部网络请求（含分析、追踪器、失败请求、SSE等），让Claude生成结构化隐私/合规报告，并可结合法律插件核对DPA、隐私政策与真实传输是否一致。

## Results
- 宣称**从录制到可用工具约 10 分钟**，且**无需手写代码**；这是文中最核心的效率结果，但不是基于标准学术基准的系统评测。
- 给出的案例：为 **York Region 9家公共图书馆** 生成集成，能够一次搜索 **全部9个目录**，并产出至少 **3个工具**：`search_york_region_libraries`、`search_specific_library`、`list_york_region_libraries`。
- 该图书馆案例据称只需**录制一次** BiblioCommons 搜索流量，再由Claude分析并生成MCP server，**整个过程少于10分钟**。
- 系统支持**增量更新**：当网站API变化时，重新录制相关动作并运行 `webbridge_update`，只重生成受影响工具，而非重写整个server；文中未给出成功率或耗时统计。
- 自验证生成会在写出server后立即检查 **3类常见错误**（ESM语法、错误bridge模式、低层MCP API模式），并触发自动再生成；但未报告具体错误率下降数字。
- 没有提供学术式定量指标，如成功率、覆盖网站数、与Playwright/手写抓包方案的对比基线、隐私审计准确率等。最强的具体主张是：**任意网站、无代码、无站点配合、约10分钟生成MCP工具**，外加可对全量流量做基于真实网络证据的合规分析。

## Link
- [https://github.com/jalabulajunx/WebBridge](https://github.com/jalabulajunx/WebBridge)
