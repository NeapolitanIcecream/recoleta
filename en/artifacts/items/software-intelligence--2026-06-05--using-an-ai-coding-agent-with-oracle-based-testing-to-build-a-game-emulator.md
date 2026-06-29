---
source: hn
url: https://keanw.com/2026/03/a-diary-of-an-agentic-retro-gamer-part-1.html
published_at: '2026-06-05T23:43:13'
authors:
- throwaway_2494
topics:
- coding-agents
- test-oracles
- emulation
- code-intelligence
- human-ai-collaboration
- automated-software-production
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Using an AI coding agent with oracle-based testing to build a game emulator

## Summary
A guided AI coding agent built a working Intellivision emulator in 36 hours when paired with a jzintv-derived test oracle. The piece matters for code intelligence because it shows how reference-based tests can constrain agent output on a hardware-accurate programming task.

## Problem
- The existing Intellivision emulator broke after OS updates, so the author wanted a new emulator that he could maintain.
- Building an emulator requires exact CPU, memory, timing, video, sound, and controller behavior, so small mistakes can stop games from booting or running correctly.
- An unguided coding agent produced a parser with two major flaws, which showed that the agent needed human direction and strong tests.

## Approach
- The author first wrote much of the CP-1610 CPU core by hand.
- He extracted the CPU implementation from jzintv and used it as a test oracle.
- Unit tests compared each new instruction against jzintv on registers, flags, RAM, and cycle counts.
- After the oracle was in place, the author guided the coding agent through bus, video, sound, ROM loading, controls, and runtime features.
- A debugger port let the AI inspect emulator state and control the running game during live play.

## Results
- Before using the agent, the author had spent time until mid-March and had a mostly working CP-1610 CPU core, with no bus, video, or sound.
- By hour 5 with the guided agent, the emulator showed its first pixels and color test bars.
- By hour 10, the rendering pipeline was in place; by hour 21, the first cartridge ROM booted.
- By hour 28, all 204 ROMs in the author's collection booted.
- By hour 32, games had on-screen movement; by hour 36, the full Intellivision system ran with controller input and sound.
- In the following days, the author added a debugger port, AI-driven game control, code-location support for collision or death events, and controller buzz on player death.

## Link
- [https://keanw.com/2026/03/a-diary-of-an-agentic-retro-gamer-part-1.html](https://keanw.com/2026/03/a-diary-of-an-agentic-retro-gamer-part-1.html)
