---
source: arxiv
url: http://arxiv.org/abs/2603.10621v1
published_at: '2026-03-11T10:33:14'
authors:
- Juan M. Murillo
- "Ignacio Garc\xEDa Rodr\xEDguez de Guzm\xE1n"
- Enrique Moguel
- "Javier Romero-\xC1lvarez"
- Jaime Alvarado-Valiente
- "\xC1lvaro M. Aparicio-Morales"
- Jose Garcia-Alonso
- "Ana D\xEDaz Mu\xF1oz"
- "Eduardo Fern\xE1ndez-Medina"
- Francisco Chicano
- Carlos Canal
- "Jos\xE9 Daniel Viqueira"
- "Sebasti\xE1n Villarroya"
- "Eduardo Guti\xE9rrez"
- "Adri\xE1n Romero-Flores"
- "Alfonso E. M\xE1rquez-Chamorro"
- Antonio Ruiz-Cortes
- Cyrille YetuYetu Kesiku
- "Pedro S\xE1nchez"
- "Diego Alonso C\xE1ceres"
- "Lidia S\xE1nchez-Gonz\xE1lez"
- Fernando Plou
topics:
- quantum-software-engineering
- quantum-computing
- software-engineering
- nisq
- hybrid-systems
relevance_score: 0.44
run_id: materialize-outputs
language_code: en
---

# QuantumX: an experience for the consolidation of Quantum Computing and Quantum Software Engineering as an emerging discipline

## Summary
This article summarizes QuantumX, the first conference track focused on the intersection of quantum computing and quantum software engineering, reviewing representative work, shared themes, and open challenges from relevant Spanish research groups. Its core value lies in promoting quantum software engineering from fragmented research toward the construction of a more systematic engineering discipline.

## Problem
- Quantum computing is moving from theory to practice, but quantum software still lacks mature software engineering methods to ensure **quality, maintainability, testability, governance, and reusability**.
- Existing quantum hardware is constrained by NISQ conditions, cloud queuing, high error rates, and high costs, making large-scale development, testing, and deployment very difficult.
- Without unified engineering abstractions, quality models, orchestration mechanisms, and toolchains, quantum technology will struggle to truly enter industrial-grade software production and service-oriented scenarios, which is critical for both disciplinary development and industrial adoption.

## Approach
- The paper itself does not propose a single new algorithm, but rather a **systematic review/synthesis** of multiple works presented at the QuantumX conference, organized by research groups and themes, extracting common issues and future directions in quantum software engineering.
- The core mechanisms identified include transferring classical software engineering principles to the quantum domain, such as **quality models, service engineering, automatic code generation, static analysis, testing and mutation testing, orchestration and governance, and reusable abstractions**.
- At the execution and operations level, related work explores **quantum task scheduling, orchestration across multiple NISQ cloud providers, and hybrid quantum-classical SaaS governance** to reduce costs, decrease failed executions, and improve availability.
- At the programming and modeling level, related work proposes **higher-level abstractions** (such as quantum integer and Locus), automated circuit generation, QML benchmarking tools, and reproducible experimental frameworks for hybrid/simulation environments.

## Results
- As a survey paper, it **does not provide a single unified experimental metric**; however, it summarizes representative results and specific figures from multiple works presented at the conference.
- QCRAFT Scheduler reports that, compared with executing tasks individually, quantum circuit grouping and combined scheduling can **reduce average cost by about 84%** and **reduce the number of tasks by about 84%**.
- The quantum mutation testing work reports that, in IBM Quantum scenarios, by planning and executing quantum circuit mutants in combined jobs, **cost can be reduced by up to about 94%**, and it claims to demonstrate the feasibility of large-scale quantum testing in the NISQ era.
- The quantum service engineering work evaluated **40 quantum algorithm implementations** and found clear differences in quality attributes (such as analyzability), based on which it proposed recommendations for continuous improvement.
- The clinical text classification work of eVIDA claims that, on the **MIMIC-III/IV** datasets, a hybrid model combining 1D CNN, quantum BiLSTM, and quantum attention outperformed classical baselines on **F1 and MCC**, but the abstract does not provide specific values.
- The remaining contributions are mostly qualitative or methodological claims, such as higher-level quantum programming abstractions, tensor networks improving QML simulation efficiency, improved trainability of variational circuits, multi-cloud quantum orchestration, and a quantum database roadmap; in the provided text, most **do not offer unified numerical comparisons that can be independently verified**.

## Link
- [http://arxiv.org/abs/2603.10621v1](http://arxiv.org/abs/2603.10621v1)
