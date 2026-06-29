---
source: arxiv
url: http://arxiv.org/abs/2604.15663v1
published_at: '2026-04-17T03:35:35'
authors:
- Jiahui Geng
- Qing Li
- Fengyu Cai
- Fakhri Karray
topics:
- multimodal-code-retrieval
- code-search
- retrieval-augmented-generation
- vision-language-code
- benchmark-datasets
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# CodeMMR: Bridging Natural Language, Code, and Image for Unified Retrieval

## Summary
CodeMMR is a multimodal code retriever that puts natural language, code, and images into one embedding space so the same model can retrieve across all three. The paper also introduces MMCoIR, a benchmark for this setting, and shows that standard multimodal retrievers miss much of the visual meaning in code artifacts.

## Problem
- Existing code retrieval models mostly treat code as text and miss visual outputs tied to code, such as web pages, charts, SVGs, diagrams, and UML.
- This matters for code search and code RAG because developers often need to retrieve code from an image, retrieve images from code, or combine text and visuals when editing or generating code.
- Before this work, there was no broad benchmark for multimodal multilingual code retrieval across domains, languages, and retrieval directions.

## Approach
- The paper builds **MMCoIR**, a benchmark covering 5 visual domains, 8 programming languages, and 11 libraries, with tasks such as text-to-code, image-to-code, code-to-image, and composed queries like text+image-to-code.
- It trains **CodeMMR**, a single retriever initialized from a pretrained vision-language model and adapted to encode text, code, and images into a shared semantic space.
- Each query includes an instruction that states the retrieval intent, such as retrieving code that matches an image. The model embeds the query plus instruction and matches it against candidate targets.
- Training uses a contrastive InfoNCE objective: matched query-target pairs are pulled together, while in-batch and hard negative examples are pushed apart.
- The design aims to generalize across modalities, programming languages, and unseen retrieval settings used in editing and repair tasks.

## Results
- On **MMCoIR**, **CodeMMR (2B)** gets **68.0 nDCG@10 average**, beating **VLM2Vec-v2 (2B)** at **58.0**, **GME (7B)** at **53.8**, and **GME (2B)** at **51.5**. The abstract states an average gain of about **10 absolute nDCG@10 points** over strong baselines such as UniIR, GME, and VLM2Vec.
- On **Hit@1** over MMCoIR, **CodeMMR (2B)** reaches **65.4 average**, ahead of **VLM2Vec-v2 (2B)** at **53.3** and **GME (7B)** at **49.5**.
- Strong per-dataset numbers include **99.8 nDCG@10** on **Chart2Code image-to-code**, **98.6** on **Web2Code image-to-code**, **97.8/97.0** on **DATIKZv3 code-to-image / image-to-code**, and **100.0/100.0** on **PlantUML code-to-image / image-to-code**.
- The task remains hard on SVG-heavy settings: on **MMSVG**, CodeMMR reports **11.2**, **12.3**, **9.4**, and **58.2 nDCG@10** across the listed retrieval directions, which is still much better than several baselines but far below its scores on WebUI, charts, and UML.
- For downstream generation with retrieval, the paper claims gains on unseen image-to-code tasks: **+10.0 points in Execution Rate** on **ChartMimic Direct** and **+9.4 points in Visual Accuracy** on **WebCode2M-Mid** over a non-retrieval baseline, while also beating RAG systems that use baseline retrievers.

## Link
- [http://arxiv.org/abs/2604.15663v1](http://arxiv.org/abs/2604.15663v1)
