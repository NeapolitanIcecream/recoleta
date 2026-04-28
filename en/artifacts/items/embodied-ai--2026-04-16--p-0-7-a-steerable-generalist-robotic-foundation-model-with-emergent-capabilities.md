---
source: arxiv
url: http://arxiv.org/abs/2604.15483v2
published_at: '2026-04-16T19:18:07'
authors:
- Physical Intelligence
- Bo Ai
- Ali Amin
- Raichelle Aniceto
- Ashwin Balakrishna
- Greg Balke
- Kevin Black
- George Bokinsky
- Shihao Cao
- Thomas Charbonnier
- Vedant Choudhary
- Foster Collins
- Ken Conley
- Grace Connors
- James Darpinian
- Karan Dhabalia
- Maitrayee Dhaka
- Jared DiCarlo
- Danny Driess
- Michael Equi
- Adnan Esmail
- Yunhao Fang
- Chelsea Finn
- Catherine Glossop
- Thomas Godden
- Ivan Goryachev
- Lachlan Groom
- Haroun Habeeb
- Hunter Hancock
- Karol Hausman
- Gashon Hussein
- Victor Hwang
- Brian Ichter
- Connor Jacobsen
- Szymon Jakubczak
- Rowan Jen
- Tim Jones
- Gregg Kammerer
- Ben Katz
- Liyiming Ke
- Mairbek Khadikov
- Chandra Kuchi
- Marinda Lamb
- Devin LeBlanc
- Brendon LeCount
- Sergey Levine
- Xinyu Li
- Adrian Li-Bell
- Vladislav Lialin
- Zhonglin Liang
- Wallace Lim
- Yao Lu
- Enyu Luo
- Vishnu Mano
- Nandan Marwaha
- Aikys Mongush
- Liam Murphy
- Suraj Nair
- Tyler Patterson
- Karl Pertsch
- Allen Z. Ren
- Gavin Schelske
- Charvi Sharma
- Baifeng Shi
- Lucy Xiaoyang Shi
- Laura Smith
- Jost Tobias Springenberg
- Kyle Stachowicz
- Will Stoeckle
- Jiaming Tang
- Jimmy Tanner
- Shalom Tekeste
- Marcel Torne
- Kyle Vedder
- Quan Vuong
- Anna Walling
- Haohuan Wang
- Jason Wang
- XuDong Wang
- Chris Whalen
- Samuel Whitmore
- Blake Williams
- Charles Xu
- Sukwon Yoo
- Lili Yu
- Wuming Zhang
- Zhuoyang Zhang
- Ury Zhilinsky
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- cross-embodiment-transfer
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# $π_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities

## Summary
$\pi_{0.7}$ is a 5B-parameter generalist vision-language-action model for robot control that uses richer prompts to learn from mixed-quality, multi-source data. The paper claims this prompt design gives stronger zero-shot generalization across tasks, environments, and robot embodiments, with out-of-the-box performance on dexterous long-horizon tasks.

## Problem
- Prior robot foundation models struggle with compositional generalization: they often fail to combine learned skills for new tasks and may need task-specific fine-tuning even on tasks close to training data.
- Training on large, diverse robot data is hard because trajectories differ in strategy and quality; if trained naively, the model can average across good and bad behaviors and produce weak actions.
- This matters because useful robot foundation models need to work in unseen homes, follow varied language instructions, transfer across robots, and benefit from failures, autonomous rollouts, and non-robot data instead of discarding them.

## Approach
- The core idea is to condition the robot policy on a richer prompt that says both **what to do** and **how to do it**. The prompt can include a task instruction, a step-level subtask instruction, episode metadata, control mode, and subgoal images.
- Episode metadata labels each trajectory with attributes such as speed, quality score from 1 to 5, and whether a segment contains a mistake. This lets the model train on failures, suboptimal demonstrations, and autonomous rollouts without treating them as targets to imitate blindly.
- Subgoal images show a desired near-future scene state. A separate world model, initialized from BAGEL, generates these images from the current observation and subtask text, giving the action model a more concrete target than language alone.
- The base policy is a flow-matching VLA built on a Gemma3 4B vision-language backbone, MEM-style video history encoding, and an 860M action expert, for about 5B parameters total.
- During training, prompt parts are randomly dropped so the model can run with any subset at test time. Subgoal images are used on 25% of training examples; metadata is dropped entirely 15% of the time; individual metadata fields are dropped with 5% probability.

## Results
- The model has about **5B parameters**: a **4B** Gemma3 VLM backbone plus an **860M** action expert.
- The paper claims strong out-of-the-box performance on dexterous long-horizon tasks such as **operating an espresso machine, folding laundry, taking out a trash bag, folding a box, and peeling vegetables**, without task-specific post-training.
- It claims **zero-shot cross-embodiment transfer**, including **t-shirt folding on a robot with no laundry-folding training**, and states this **matches expert teleoperators on their initial attempts**.
- It claims instruction following in **unseen kitchen and bedroom environments** and compositional generalization to new tasks such as **loading a sweet potato into an air fryer**.
- The abstract states espresso-machine performance matches **specialized RL-finetuned models**, and the introduction says the system can sometimes outperform RL-trained or single-task post-trained policies on dexterous tasks by learning from diverse and suboptimal data.
- The provided excerpt does **not include task tables, success rates, or benchmark numbers**, so the quantitative evidence available here is limited to model and training setup numbers rather than evaluation metrics.

## Link
- [http://arxiv.org/abs/2604.15483v2](http://arxiv.org/abs/2604.15483v2)
