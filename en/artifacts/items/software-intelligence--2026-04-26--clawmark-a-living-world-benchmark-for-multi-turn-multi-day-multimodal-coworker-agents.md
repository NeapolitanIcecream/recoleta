---
source: arxiv
url: http://arxiv.org/abs/2604.23781v1
published_at: '2026-04-26T16:05:02'
authors:
- Fanqing Meng
- Lingxiao Du
- Zijian Wu
- Guanzheng Chen
- Xiangyan Liu
- Jiaqi Liao
- Chonghe Jiang
- Zhenglin Wan
- Jiawei Gu
- Pengfei Zhou
- Rui Huang
- Ziqi Zhao
- Shengyuan Ding
- Ailing Yu
- Bo Peng
- Bowei Xia
- Hao Sun
- Haotian Liang
- Ji Xie
- Jiajun Chen
- Jiajun Song
- Liu Yang
- Ming Xu
- Qionglin Qiu
- Runhao Fu
- Shengfang Zhai
- Shijian Wang
- Tengfei Ma
- Tianyi Wu
- Weiyang Jin
- Yan Wang
- Yang Dai
- Yao Lai
- Youwei Shu
- Yue Liu
- Yunzhuo Hao
- Yuwei Niu
- Jinkai Huang
- Jiayuan Zhuo
- Zhennan Shen
- Linyu Wu
- Cihang Xie
- Yuyin Zhou
- Jiaheng Zhang
- Zeyu Zheng
- Mengkang Hu
- Michael Qizhe Shieh
topics:
- agent-benchmarks
- multimodal-agents
- multi-turn-evaluation
- dynamic-environments
- coworker-agents
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# ClawMark: A Living-World Benchmark for Multi-Turn, Multi-Day, Multimodal Coworker Agents

## Summary
ClawMark is a benchmark for AI coworker agents that work across multiple days, multiple turns, and multiple data types while the environment changes outside the agent's control. It measures a gap that earlier agent benchmarks mostly miss: staying useful when files, emails, calendars, and other tools keep changing between workdays.

## Problem
- Existing agent benchmarks usually test one static session, but real coworker agents face work that continues across days.
- In real office settings, the world changes between turns: new emails arrive, calendar entries move, records get edited, and evidence may appear in PDFs, images, audio, video, or spreadsheets.
- This matters because an agent that looks strong in a frozen episode may fail when it must refresh state, track progress over time, and act on raw multimodal evidence.

## Approach
- The paper introduces **ClawMark**, a benchmark with **100 tasks across 13 professional scenarios**. Each task spans **2 to 6 turns** (mean **3.6**), with one turn per in-universe workday.
- Tasks run in a dynamic sandbox with **five stateful services**: filesystem, email, calendar, knowledge base, and spreadsheet. The environment changes between turns through announced "loud events" and unannounced "silent mutations."
- Evidence is multimodal and untranscribed. The release includes **1,072 raw artifacts** such as PDFs, images, audio, video, and spreadsheets.
- Scoring is fully rule-based. The benchmark uses **1,537 deterministic Python checkers**, including **55 red-line constraints**, and does **not** use LLM-as-judge scoring.
- The authors evaluate **seven frontier agent systems** under a common harness to compare how current models handle long, stateful coworker workflows.

## Results
- ClawMark claims a distinct benchmark setting relative to prior work: among the listed benchmarks, it is the only one with **multi-day tasks = yes**, **dynamic environment = yes**, **full multimodal input = yes**, and **rule-based verification**.
- On the 100-task benchmark, the top **weighted score** is **75.8** from **Claude Sonnet 4.6**. The next best are **Claude Opus 4.6 at 74.6** and **GPT-5.4 at 72.0**.
- On the stricter **Task Success** metric, the best model is **Claude Opus 4.6 at 20.0%**, followed by **Claude Sonnet 4.6 at 14.0%** and **GPT-5.4 at 9.0%**. This shows that partial progress is common, but full end-to-end completion is still rare.
- Red-line failure rates vary by model: **3.6%** for Claude Sonnet 4.6, **5.5%** for Claude Opus 4.6, **3.6%** for GPT-5.4, **14.5%** for Qwen 3.6 Plus, and **9.1%** for Kimi K2.5.
- Turn-level analysis on **73 three-turn tasks** shows that **6 of 7 models** drop on Day 2 after the first external environment update. The reported gap between **Claude Sonnet 4.6** and **GPT-5.4** narrows from **+6.5 points on Day 1** to **+4.0 points on Day 3**.
- The main empirical claim is that current frontier agents can often make partial progress in dynamic office workflows, but they still struggle to fully complete multi-day tasks once the outside world changes.

## Link
- [http://arxiv.org/abs/2604.23781v1](http://arxiv.org/abs/2604.23781v1)
