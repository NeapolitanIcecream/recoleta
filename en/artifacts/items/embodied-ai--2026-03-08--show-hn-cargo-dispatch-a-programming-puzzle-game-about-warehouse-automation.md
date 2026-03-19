---
source: hn
url: https://matthuggins.com/lab/cargo-dispatch
published_at: '2026-03-08T23:28:50'
authors:
- matthuggins
topics:
- programming-game
- warehouse-automation
- multi-robot-scheduling
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Show HN: Cargo Dispatch – a programming puzzle game about warehouse automation

## Summary
This is not a robotics research paper, but a programming puzzle game about warehouse automation. Players write control logic in TypeScript or JavaScript to direct robots to move packages and deliver them to the correct trucks within a time limit.

## Problem
- It addresses the question of how to write scheduling and transport strategies for a group of warehouse robots so they can complete pickups and deliveries under conditions where packages continuously spawn and time is limited.
- This problem matters because it abstracts real-world issues in warehouse automation, including multi-robot coordination, task allocation, and path/time management.
- But based on the provided content, the work is more of an educational/entertainment programming game than a proposal of a new research method.

## Approach
- The core mechanic is simple: players write programs in **TypeScript/JavaScript** to directly control the behavior of a fleet of warehouse robots.
- Packages spawn in warehouse aisles, and robots must first pick them up and then deliver them to the correct trucks.
- The overall task is time-limited, so the strategy focuses on scheduling efficiency, managing robot idle time, and choosing among multiple aisles/tasks.
- From the provided excerpt, the system appears to be a discrete warehouse simulator/puzzle environment that evaluates control-program performance through levels and timing mechanics.

## Results
- The provided text **does not include any formal quantitative experimental results**, nor does it provide datasets, baseline methods, or comparisons using academic metrics.
- The only visible interface numbers in the text are “**36s**” and “**0 of 20**,” which look more like game timer/progress displays than research performance metrics.
- The strongest concrete claim is that this is a “**programming puzzle game about warehouse automation**” and that it supports using **TypeScript or JavaScript** to control warehouse robots.
- It does not report research results such as success rate, throughput, path efficiency, sample efficiency, generalization ability, or sim2real.

## Link
- [https://matthuggins.com/lab/cargo-dispatch](https://matthuggins.com/lab/cargo-dispatch)
