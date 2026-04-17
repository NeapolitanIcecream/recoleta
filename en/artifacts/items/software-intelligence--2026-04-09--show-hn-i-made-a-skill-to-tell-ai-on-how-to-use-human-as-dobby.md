---
source: hn
url: https://github.com/LittleLittleCloud/Dobby
published_at: '2026-04-09T23:01:07'
authors:
- BigBigMiao
topics:
- human-ai-interaction
- agent-workflow
- task-delegation
- prompt-skill
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Show HN: I made a skill to tell AI on how to use human as Dobby

## Summary
This is a prompt skill for assigning simple support tasks to a human helper called "Dobby." It frames the human as a low-skill executor for chores such as file moving, manual testing, information gathering, formatting, and copy-paste work.

## Problem
- The project targets a coordination problem: how an AI or operator should give simple, bounded tasks to a human helper.
- It matters for human-AI workflows because many software tasks still need manual execution, browsing, testing, or formatting outside the model's direct control.
- The excerpt does not define a measured research gap, formal task, or evaluation setting.

## Approach
- The core method is a reusable "Skill" that users install with `npx skills add littlelittlecloud/dobby`.
- The skill gives behavioral instructions for managing a human assistant named Dobby and sets a sharp task boundary: Dobby handles simple physical or clerical work, while coding and architecture stay with the main agent or user.
- The examples of allowed work are concrete: moving files, manual testing, collecting materials, organizing formats, and copying and pasting.
- The mechanism is prompt-level role assignment rather than a trained model, new algorithm, or system with autonomous planning.

## Results
- No quantitative results are provided in the excerpt.
- No benchmark, dataset, accuracy, task success rate, latency, or comparison against a baseline is reported.
- The strongest concrete claim is functional scope: the skill is meant to help an AI instruct a human to do simple execution tasks and avoid assigning high-intelligence work such as coding or architecture design.
- The artifact appears to be installable through `npx skills add littlelittlecloud/dobby`, but the excerpt gives no usage metrics or outcome data.

## Link
- [https://github.com/LittleLittleCloud/Dobby](https://github.com/LittleLittleCloud/Dobby)
