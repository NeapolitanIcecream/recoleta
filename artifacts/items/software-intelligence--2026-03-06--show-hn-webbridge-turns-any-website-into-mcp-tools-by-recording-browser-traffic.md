---
source: hn
url: https://github.com/jalabulajunx/WebBridge
published_at: '2026-03-06T23:29:40'
authors:
- nonstopnonsense
topics:
- mcp-tools
- browser-traffic-recording
- code-generation
- web-automation
- privacy-audit
relevance_score: 0.89
run_id: materialize-outputs
---

# Show HN: WebBridge turns any website into MCP tools by recording browser traffic

## Summary
WebBridge把网站的真实浏览器流量录制下来，再让Claude自动生成可调用的MCP工具，从而把“任何网站”快速变成可被AI客户端使用的集成。它还扩展到隐私/合规审计，通过完整网络抓包生成基于证据的流量分析报告。

## Problem
- 许多网站没有公开API、没有官方集成，或接入需要大量手工逆向与编写代码，导致把网站能力接入MCP/AI工作流的门槛很高。
- 传统自动化常依赖站点配合、桌面中间层或脆弱脚本；当站点接口变化时，维护成本高。
- 法务与隐私团队通常只能看文档声明，缺少“应用实际发了什么数据”的网络证据来做合规核查。

## Approach
- 用Chrome扩展通过 Chrome DevTools Protocol 录制用户正常操作时的API流量；可选 Full Dump 模式抓取所有请求，用于隐私/合规分析而非工具生成。
- Claude读取录制结果，识别API操作，询问工具命名与关键字段，然后自动写出**强类型** MCP server 代码与配置。
- 生成后的server通过本地 bridge/socket 复用浏览器中的登录态、cookies 和上下文请求能力，因此无需保存密码或令牌，也不需要网站提供官方API。
- 提供 `test / install / update / import_har` 流程：自动测试握手与工具调用、写入Claude配置、基于新旧录制差分只重生成受影响工具，并支持从HAR导入已有流量。
- 内置自校验与错误诊断，自动检查常见生成错误（如ESM配置、错误bridge模式、低层MCP API误用）并促使重新生成。

## Results
- 声称“从录制到可工作的工具”约 **10 分钟**，且**无需手写代码**。
- 给出的实例：York Region 公共图书馆集成可同时搜索 **9** 个图书馆目录（Aurora、East Gwillimbury、Georgina、King Township、Markham、Newmarket、Richmond Hill、Vaughan、Whitchurch-Stouffville）。
- 该实例通过只录制 **1 次** BiblioCommons 搜索流量，即生成了至少 **3** 个工具：`search_york_region_libraries`、`search_specific_library`、`list_york_region_libraries`。
- 生成系统包含约 **10** 个WebBridge插件工具，用于读录制、写server、更新、测试、安装等自动化流程。
- Full Dump 模式可输出结构化隐私报告，覆盖第三方域名、cookie/header、PII泄露、重定向链与 SSE 帧等；但文中**没有提供标准基准数据集上的量化对比结果**，也没有给出成功率、准确率或与现有方案的正式benchmark比较。
- 兼容性上，生成的MCP servers声称可运行于多种MCP客户端，包括 Claude Desktop、Claude Code、Cursor、VS Code、Windsurf、Cline、Continue 等，但这同样是功能性声明而非经论文式实验验证的指标。

## Link
- [https://github.com/jalabulajunx/WebBridge](https://github.com/jalabulajunx/WebBridge)
