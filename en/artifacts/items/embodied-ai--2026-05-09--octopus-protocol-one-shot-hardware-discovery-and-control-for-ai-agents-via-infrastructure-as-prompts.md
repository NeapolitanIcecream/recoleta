---
source: arxiv
url: https://arxiv.org/abs/2605.09055v1
published_at: '2026-05-09T16:57:11'
authors:
- Quilee Simeon
- Justin M. Wei
- Yile Fan
topics:
- hardware-discovery
- mcp-tools
- robot-control
- agentic-robotics
- self-healing-systems
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Octopus Protocol: One-Shot Hardware Discovery and Control for AI Agents via Infrastructure-as-Prompts

## Summary
Octopus Protocol uses a coding agent to discover connected hardware, generate MCP tools, and deploy a live hardware server from one bootstrap command. The paper targets the driver and SDK work that blocks agents from controlling new devices.

## Problem
- Agentic robotics systems such as Code-as-Policies and VLA policies usually assume existing ROS nodes, SDKs, drivers, or action APIs.
- New hardware bring-up still requires humans to inspect devices, write glue code, install dependencies, expose control primitives, and repair failures.
- This matters because hardware integration can dominate the engineering cost before an AI agent can act in the physical world.

## Approach
- The system runs a five-stage pipeline: probe OS devices, identify capabilities, generate typed MCP tool schemas, write a FastMCP server, then deploy an HTTP/SSE endpoint.
- A coding agent compiles markdown hardware specifications and live probe results into platform-specific driver code at setup time.
- The generated tools can include actions such as `set_servo_angle` and `capture_image`, with typed inputs exposed to any MCP-compliant client.
- A persistent daemon watches logs, repairs generated code or dependencies after failures, and uses generated camera tools to summarize physical state.

## Results
- One bootstrap command onboarded hardware in about 10-15 minutes and exposed up to 30 MCP tools, depending on the detected platform and devices.
- The same markdown specification worked on 3 hosts: Windows/WSL PC, Apple Silicon macOS, and Raspberry Pi 4.
- The Raspberry Pi setup typically exposed about 18 tools; the Mac setup reached close to the 30-tool cap.
- On a benchtop SO-ARM101 6-DOF arm with USB camera feedback, an MCP client performed closed-loop visual-motor control by capturing an image, observing pose, moving a joint, and verifying with a second capture.
- The self-healing stage handled 3 induced failures: missing Python dependency, USB arm hot-unplug/replug, and deliberate generated-server corruption.
- The orchestrator passed 14 of 14 integration tests and used about 640 lines of Python plus about 560 lines of markdown specifications; the runtime MCP server was generated during setup.

## Link
- [https://arxiv.org/abs/2605.09055v1](https://arxiv.org/abs/2605.09055v1)
