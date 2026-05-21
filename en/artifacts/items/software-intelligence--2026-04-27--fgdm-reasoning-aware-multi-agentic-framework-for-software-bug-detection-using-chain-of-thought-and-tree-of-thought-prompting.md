---
source: arxiv
url: https://arxiv.org/abs/2604.24831v1
published_at: '2026-04-27T17:22:15'
authors:
- Srita Padmanabhuni
- Bhargavi Karuturi
- Jerusha Karen Indupalli
- Santhan Reddy Chilla
- Vivek Yelleti
topics:
- software-bug-detection
- program-repair
- multi-agent-systems
- code-intelligence
- chain-of-thought
- flow-graphs
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# FGDM: Reasoning Aware Multi-Agentic Framework for Software Bug Detection using Chain of Thought and Tree of Thought Prompting

## Summary
FGDM is a multi-agent bug detection and repair system that turns source code into flow graphs, localizes faulty nodes, repairs them, and reconstructs code. It targets Python and C programs where bugs depend on control flow, data flow, and cross-block context.

## Problem
- It addresses automated bug detection and repair in large or interconnected programs, where line-by-line ML and DL methods miss dependencies across code blocks.
- This matters because late bug discovery can cause incorrect outputs, operational loss, and slow manual debugging.
- The paper also targets LLM failure modes in code repair, including hallucinated fixes, unstable reasoning, and prompt sensitivity.

## Approach
- FGDM uses four sequential agents: Flow Graph Builder, Semantic Fault Localizer, Graph Repair, and Source Code Reconstruction.
- The system converts code into a flow graph where nodes are code blocks and edges capture containment, data flow, control flow, and function calls.
- Fault localization runs on the graph, tags defective nodes, and checks for broken dependencies and flow mismatches.
- The repair agent changes only faulty areas where possible, then validates graph structure with rules for defect coverage and minimal edge changes.
- Chain-of-Thought and Tree-of-Thought prompts guide the agents, and FAISS retrieval supplies similar historical bugs and fixes.

## Results
- The evaluation used 100 programs from BugsInPy projects: Ansible, Black, FastAPI, Keras, Luigi, Matplotlib, Pandas, Scrapy, SpaCy, and Tornado.
- The authors converted the Python programs into C versions and tested both languages using Gemini 2.5 Flash API agents.
- FGDM claims mean Levenshtein distance reductions of 24.33 for Python and 8.37 for C, compared with the paper's baseline approaches.
- FGDM reports mean cosine similarity of 0.951 for Python and 0.974 for C between repaired outputs and reference representations.
- Example Python table entries include Pandas-102 improving Levenshtein distance from 9 in FGDM-Standard to 1 with FGDM-CoT and 1 with FGDM-ToT, with cosine similarity rising from 0.9892 to 0.9994.

## Link
- [https://arxiv.org/abs/2604.24831v1](https://arxiv.org/abs/2604.24831v1)
