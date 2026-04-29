---
source: arxiv
url: http://arxiv.org/abs/2604.21017v1
published_at: '2026-04-22T19:05:17'
authors:
- Open-H-Embodiment Consortium
- ':'
- Nigel Nelson
- Juo-Tung Chen
- Jesse Haworth
- Xinhao Chen
- Lukas Zbinden
- Dianye Huang
- Alaa Eldin Abdelaal
- Alberto Arezzo
- Ayberk Acar
- Farshid Alambeigi
- Carlo Alberto Ammirati
- Yunke Ao
- Pablo David Aranda Rodriguez
- Soofiyan Atar
- Mattia Ballo
- Noah Barnes
- Federica Barontini
- Filip Binkiewicz
- Peter Black
- Sebastian Bodenstedt
- Leonardo Borgioli
- Nikola Budjak
- "Benjamin Calm\xE9"
- Fabio Carrillo
- Nicola Cavalcanti
- Changwei Chen
- Haoxin Chen
- Sihang Chen
- Qihan Chen
- Zhongyu Chen
- Ziyang Chen
- Shing Shin Cheng
- Meiqing Cheng
- Min Cheng
- Zih-Yun Sarah Chiu
- Xiangyu Chu
- Camilo Correa-Gallego
- Giulio Dagnino
- Anton Deguet
- Jacob Delgado
- Jonathan C. DeLong
- Kaizhong Deng
- Alexander Dimitrakakis
- Qingpeng Ding
- Hao Ding
- Giovanni Distefano
- Daniel Donoho
- Anqing Duan
- Marco Esposito
- Shane Farritor
- Jad Fayad
- Zahi Fayad
- Mario Ferradosa
- Filippo Filicori
- Chelsea Finn
- "Philipp F\xFCrnstahl"
- Jiawei Ge
- Stamatia Giannarou
- Xavier Giralt Ludevid
- Frederic Giraud
- Aditya Amit Godbole
- Ken Goldberg
- Antony Goldenberg
- Diego Granero Marana
- Xiaoqing Guo
- "Tam\xE1s Haidegger"
- Evan Hailey
- Pascal Hansen
- Ziyi Hao
- Kush Hari
- Kengo Hayashi
- Jonathon Hawkins
- Shelby Haworth
- Ortrun Hellig
- S. Duke Herrell
- Zhouyang Hong
- Andrew Howe
- Junlei Hu
- Ria Jain
- Mohammad Rafiee Javazm
- Howard Ji
- Rui Ji
- Jianmin Ji
- Zhongliang Jiang
- Dominic Jones
- Jeffrey Jopling
- Britton Jordan
- Ran Ju
- Michael Kam
- Luoyao Kang
- Fausto Kang
- Siddhartha Kapuria
- Peter Kazanzides
- Sonika Kiehler
- Ethan Kilmer
- Ji Woong
- Kim
- "Przemys\u0142aw Korzeniowski"
- Chandra Kuchi
- Nithesh Kumar
- Alan Kuntz
- Federico Lavagno
- Yu Chung Lee
- Hao-Chih Lee
- Hang Li
- Zhen Li
- Xiao Liang
- Xinxin Lin
- Jinsong Lin
- Chang Liu
- Fei Liu
- Pei Liu
- Yun-hui Liu
- Wanli Liuchen
- "Eszter Luk\xE1cs"
- Sareena Mann
- Miles Mannas
- Brett Marinelli
- Sabina Martyniak
- Francesco Marzola
- Lorenzo Mazza
- Xueyan Mei
- Maria Clara Morais
- Luigi Muratore
- Chetan Reddy Narayanaswamy
- "Micha\u0142 Naskr\u0119t"
- David Navarro-Alarcon
- Cyrus Neary
- Chi Kit Ng
- Christopher Nguan
- David Noonan
- Ki Hwan Oh
- Tom Christian Olesch
- Allison M. Okamura
- Justin Opfermann
- Matteo Pescio
- Doan Xuan Viet Pham
- Tito Porras
- Hongliang Ren
- Ariel Rodriguez Jimenez
- Ferdinando Rodriguez y Baena
- Septimiu E. Salcudean
- Asmitha Sathya
- Preethi Satish
- Lalithkumar Seenivasan
- Jiaqi Shao
- Yiqing Shen
- Yu Sheng
- Lucy XiaoYang Shi
- "Zoe Soul\xE9"
- Stefanie Speidel
- Mingwu Su
- Jianhao Su
- Idris Sunmola
- "Krist\xF3f Tak\xE1cs"
- Yunxi Tang
- Patrick Thornycroft
- Yu Tian
- Jordan Thompson
- Mehmet K. Turkcan
- Mathias Unberath
- Pietro Valdastri
- Carlos Vives
- Quan Vuong
- Martin Wagner
- Farong Wang
- Wei Wang
- Lidian Wang
- Chung-Pang Wang
- Guankun Wang
- Junyi Wang
- Erqi Wang
- Ziyi Wang
- Tanner Watts
- Wolfgang Wein
- Yimeng Wu
- Zijian Wu
- Hongjun Wu
- Luohong Wu
- Jie Ying Wu
- Junlin Wu
- Victoria Wu
- Kaixuan Wu
- "Mateusz W\xF3jcikowski"
- Yunye Xiao
- Nan Xiao
- Wenxuan Xie
- Hao Yang
- Tianqi Yang
- Yinuo Yang
- Menglong Ye
- Ryan S. Yeung
- Nural Yilmaz
- Chim Ho Yin
- Michael Yip
- Rayan Younis
- Chenhao Yu
- Sayem Nazmuz Zaman
- Milos Zefran
- Han Zhang
- Yuelin Zhang
- Yidong Zhang
- Yanyong Zhang
- Xuyang Zhang
- Yameng Zhang
- Joyce Zhang
- Ning Zhong
- Peng Zhou
- Haoying Zhou
- Xiuli Zuo
- Nassir Navab
- Mahdi Azizian
- Sean D. Huver
- Axel Krieger
topics:
- medical-robotics
- vision-language-action
- world-model
- surgical-robotics
- robot-datasets
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Open-H-Embodiment: A Large-Scale Dataset for Enabling Foundation Models in Medical Robotics

## Summary
## 摘要
Open-H-Embodiment 是一个大型开放式医疗机器人数据集，用来支持跨多种机器人平台和任务的基础模型。论文用它训练了一个手术视觉-语言-动作策略模型和一个动作条件世界模型，并展示了它们在缝合任务和跨平台评估中的提升。

## 问题
- 医疗机器人学习缺少带有同步视频和机器人运动学数据的大型开放数据集，这阻碍了手术及相关医疗任务中的基础模型训练。
- 早期数据集规模小且范围窄：JIGSAWS 约 3 小时，Expanded CRCD 约 7 小时，SutureBot 约 6 小时，ImitateCholec 约 20 小时，而且每个都只覆盖单一平台。
- 这很重要，因为手术策略需要处理可变形组织、长任务序列和严格的错误容忍要求，而在非医疗数据上训练的通用机器人 VLA 在手术基准上的表现一直较差。

## 方法
- 作者构建了 **Open-H-Embodiment**，这是一个跨具身数据集，包含 **770 小时**、**124,019 个 episode**、**119 个数据集**、**49+ 家机构**、**20 个机器人平台**和 **33 个任务家族**。每个数据集都将视频与同步运动学数据配对。
- 该数据集覆盖手术、机器人超声和内镜，场景包括仿真、台架、离体、活体和临床环境。它包含 **da Vinci**、**dVRK**、**Versius**、**MIRA**、**BiTrack** 和 **Maestro** 等主要系统。
- 他们在 Open-H 上对 NVIDIA 的 **GR00T-N1.6** 进行后训练，得到 **GR00T-H**，论文将其描述为首个面向医疗机器人的开放基础视觉-语言-动作模型。
- 他们还将 **Cosmos-Predict 2.5** 微调为 **Cosmos-H-Surgical-Simulator**，这是一个 **20 亿参数** 的动作条件世界模型。它以单帧图像加运动学动作作为输入，能够通过一个 checkpoint 预测 **九个机器人平台** 上未来的手术视频。

## 结果
- **数据集规模：** Open-H 有 **770 小时**，而此前公开的手术运动学数据集大约分别为 **3 小时、7 小时、6 小时和 20 小时**。它覆盖 **20 个平台**；前述数据集各自只覆盖 **1 个平台**。
- **端到端缝合（SutureBot）：** **GR00T-H 完成了 20 次试验中的 5 次（25%）**。**ACT、GR00T-N1.6 和 LingBot-VA 均为 20 次中的 0 次**。在 throw 阶段，GR00T-H 保留了 **12/20** 次试验，而 ACT 为 **4/20**，GR00T-N1.6 为 **4/20**，LingBot-VA 为 **1/20**。
- **分布外泛化（未见过的伤口 + 光照变化）：** GR00T-H 的平均子任务成功率达到 **54%**，相比之下 GR00T-N1.6 为 **30%**，ACT 为 **5%**。在 pickup 和 handover 上，它达到 **70%**，GR00T-N1.6 为 **40%**；在 throw 和 extract 上，分别为 **42.5%** 和 **5%**。
- **SutureBot 上的数据效率：** 使用 **33%** 的微调数据（约 **2 小时**）时，GR00T-H 和 ACT 的平均成功率都约为 **47%**，而 GR00T-N1.6 约为 **20%**。使用 **100%** 数据（约 **6 小时**）时，GR00T-H 达到约 **73%**，ACT 约 **50%**，GR00T-N1.6 约 **37%**。
- **跨具身评估：** 在 **dVRK-Si、Versius 和 MIRA** 上，GR00T-H 的表现都优于基础模型 GR00T-N1.6，论文报告其总体平均成功率提升具有统计显著性（**p < 0.001**）。这些平台测试的训练数据包括 Versius 上的 **5.2 小时**、MIRA 上的 **22 分钟** 和 dVRK-Si 上的 **6 小时**。
- **猪腹部离体缝合：** GR00T-H 在 **29 个子任务** 上达到 **64% 的平均成功率**（**总 n=290，每个子任务 10 次试验**）。多个子任务达到 **10/10**，包括 needle pickup、set-down needle 和三个打结步骤；而 cutting 相关子任务较弱，分别为 **2/10** 和 **3/10**。
- **世界模型：** 论文称这是首个多具身手术动作条件世界模型，使用来自 **9 个平台** 和 **32 个数据集** 的数据训练。文中报告使用 **L1** 和 **SSIM** 对 **72 个生成帧** 和 **3 个种子** 进行评估，但摘要片段没有给出具体数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21017v1](http://arxiv.org/abs/2604.21017v1)
