---
source: hn
url: https://www.theregister.com/2026/03/14/cortical_labs_biological_cloud/
published_at: '2026-03-14T22:43:59'
authors:
- spzb
topics:
- biological-computing
- neuromorphic-cloud
- in-vitro-neurons
- brain-computer-interface
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# The datacenter where the day starts with topping up cerebrospinal fluid

## Summary
This article describes Cortical Labs' attempt to turn “biological computers” based on living neurons into a rentable cloud service. Its core selling point is to let cultured neurons learn tasks in simulated environments and be invoked remotely via APIs like cloud compute.

## Problem
- The problem the article addresses is how to turn biological computing, which is currently highly experimental and dependent on cell culture and manual maintenance, into a computing platform accessible to external users.
- This matters because the company claims biological neurons may learn certain simulated tasks faster than traditional computers, use less energy, and potentially generate more “original” strategies rather than merely recombining existing information like LLMs.
- The current bottleneck is that biological computing infrastructure is extremely immature: it requires specific cell sources, daily replacement of a cerebrospinal fluid-like culture medium, regulation of the gas environment, and the industry still lacks a standardized supply system analogous to a “cell foundry/TSMC.”

## Approach
- Cortical Labs places biological neural networks cultured from human and rodent stem cells on high-density microelectrode arrays, allowing silicon-based systems to interact bidirectionally with neurons through electrical stimulation and recording.
- Put simply, the method is to connect living neurons to electronic interfaces, encode simulated environment states into electrical signals as inputs, read out their firing activity as action outputs, and let them learn tasks in a closed loop.
- The company productized this approach as the CL1 device and further “cloudified” it: deploying 120 CL1 units and providing APIs, Jupyter Notebook, and Python code upload interfaces so users can remotely run experiments on biological computers.
- Before each job, cell lines still need to be prepared according to customer requirements, and the oxygen, nitrogen, carbon dioxide, and nutrient solution environment must be configured; the article says users typically rent 3–4 machines for repeat experiments and controls.
- The article also links this platform to the method from a 2022 paper, which showed in vitro neurons learning Pong in a simulated game world; the company later extended this to learning DOOM, ultimately resulting in the CL1 product.

## Results
- At the infrastructure level: the company has deployed **120 CL1 units** in a Melbourne datacenter and opened cloud access interfaces; this is the most concrete productization scale data in the article.
- At the operations level: the culture medium must be replaced **every 24 hours**, the operating atmosphere is maintained at about **5% oxygen**, and preparing a machine for each customer task takes about **1 week**.
- At the usage level: the company says most users rent **3–4** CL1 units to conduct repeat experiments and control groups.
- At the capability-claim level: the article cites a 2022 paper saying in vitro neurons learned to play **Pong**, and mentions the company later demonstrated its machines learning **DOOM**; however, this article does not provide quantitative metrics, dataset scores, baseline comparisons, or statistically significant results for these tasks.
- At the performance-claim level: the CEO claims such systems can learn challenges in simulated environments “faster” than classical computers and use less power than traditional datacenters, but the article does not provide verifiable numerical results or experimental controls.

## Link
- [https://www.theregister.com/2026/03/14/cortical_labs_biological_cloud/](https://www.theregister.com/2026/03/14/cortical_labs_biological_cloud/)
