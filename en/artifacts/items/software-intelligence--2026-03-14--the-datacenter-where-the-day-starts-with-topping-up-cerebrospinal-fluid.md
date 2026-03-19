---
source: hn
url: https://www.theregister.com/2026/03/14/cortical_labs_biological_cloud/
published_at: '2026-03-14T22:43:59'
authors:
- spzb
topics:
- biological-computing
- neuromorphic-cloud
- brain-computer-interface
- wetware-systems
- experimental-computing
relevance_score: 0.17
run_id: materialize-outputs
language_code: en
---

# The datacenter where the day starts with topping up cerebrospinal fluid

## Summary
This article introduces Cortical Labs' launch of a cloud service composed of CL1 biological computing devices powered by living neurons, enabling external users to remotely access this new type of computing resource via API, Jupyter Notebook, and Python code. Its significance lies in advancing biological computing, which is still highly experimental, from a laboratory demonstration to a rentable infrastructure stage.

## Problem
- The problem the article addresses is: **although biological computing is claimed to have learning capabilities, potential low energy consumption, and computational properties different from traditional AI, it is currently extremely difficult to obtain, deploy, and maintain, making it almost impossible for external researchers to use in practice.**
- This matters because without a cloud-like delivery model, biological computing would remain confined to a small number of laboratories, unable to support reproducible experiments, application exploration, or an industry ecosystem.
- Another core obstacle is the supply chain and operations: cell sources are scarce, custom cell lines are required, and the living environment involving fluid, oxygen, nitrogen, and carbon dioxide must be continuously managed.

## Approach
- Cortical Labs centrally deploys its CL1 biological computers in a datacenter, building a "biological cloud" that lets users submit jobs much like calling cloud compute resources.
- Each machine is centered on a biological neural network placed on a high-density microelectrode array, connecting silicon-based systems and living neurons through **electrical stimulation and electrical signal recording**. Put simply, it "uses electronic devices to send signals to neurons, then reads back the neurons' responses."
- The user-side interface is presented in a more familiar software form: users can create Jupyter Notebooks or upload Python code and run experiments on the biological computing devices through an API.
- Before execution, specific cell lines must be prepared according to the task, and the "cerebrospinal-fluid-like" nutrient solution and a gas environment of about **5% oxygen** must be manually maintained; currently, the preparation cycle for each task is about **one week**.
- Its technical origins can be traced to the 2022 paper *In vitro neurons learn and exhibit sentience when embodied in a simulated game-world*, which demonstrated that in vitro neurons learned to play Pong; this was later engineered into CL1 and further used to learn to play DOOM.

## Results
- The article itself **does not provide a rigorous benchmark table or peer-reviewed quantitative cloud performance data**, so its actual advantages in throughput, accuracy, or cost relative to traditional computing cannot be confirmed.
- The clearly disclosed infrastructure scale is that Cortical Labs has deployed **120 CL1 units** as part of the cloud service.
- Explicitly disclosed operational parameters include: the nutrient solution is **replaced/replenished every 24 hours**; the gas environment around the devices is maintained at about **5% oxygen**; and the machine preparation time for each user job is about **1 week**.
- For typical user configurations, the company says most users will rent **3 to 4 CL1s** to conduct repeated experiments and set up control groups.
- The cited prior capability demonstrations are that the in vitro neuron system in the 2022 paper learned to play **Pong**; Cortical Labs later claimed its machines also learned to play **DOOM**, but this article provides no quantitative comparison in terms of score, sample efficiency, or against classical algorithms/LLMs.
- The company's strongest claims are that neurons can learn and form new strategies in simulated environments, may learn faster than classical computers, use less energy than traditional datacenters, and do more than simply recombine existing information as LLMs do; however, these claims are **not supported by quantitative evidence** in the excerpt provided.

## Link
- [https://www.theregister.com/2026/03/14/cortical_labs_biological_cloud/](https://www.theregister.com/2026/03/14/cortical_labs_biological_cloud/)
