---
source: arxiv
url: https://arxiv.org/abs/2606.10244v1
published_at: '2026-06-08T23:21:14'
authors:
- Takehiko Ohkawa
- Jumpei Arima
- Yuki Noguchi
- Masatoshi Tateno
- Makoto Sugiura
- Takuya Okubo
- Kengo Ikeuchi
- Yuma Shin
- Hiroki Nishizawa
- Naoaki Kanazawa
- Yuki Wakayama
- Daiki Fukunaga
- Koshi Makihara
- Tomohiro Motoda
- Floris Erich
- Yukiyasu Domae
- Tatsuya Matsushima
- Yohishiro Okumatsu
- Kei Ota
topics:
- bimanual-manipulation
- robot-data-scaling
- vision-language-action
- umi-interface
- dexterous-manipulation
- cross-embodiment-transfer
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# YUBI: Yielding Universal Bidigital Interface for Bimanual Dexterous Manipulation at Scale

## Summary
## 总结
YUBI 是一个由手指驱动的手持夹爪和数据采集系统，用于大规模双臂机器人操作。论文的核心观点是，更好的操作员人体工学加上 VR 位姿追踪，可以生成大得多的开放式、类似 UMI 的数据集，并训练出能在不同机器人手臂之间迁移的策略。

## 问题
- 开放式机器人学习缺少与私有实验室同等规模的、大型且易获取的双臂精细操作数据集。
- 之前类似 UMI 的手枪式握把设备又重又笨，操作员的手指位置和夹爪夹点错开，影响精细控制、触觉反馈和长时间采集。
- 基于 SLAM 的夹爪追踪会漂移，而把 VR 追踪设备戴在头上会让颈部疲劳，限制单次采集时长。

## 方法
- YUBI 用一种与手指对齐的设计替代了手枪式握把：拇指驱动一侧夹爪，食指和中指驱动另一侧夹爪，因此夹爪会随着操作员的捏合动作开合。
- 夹爪重量为 319 g，其中包括一个 119 g 的 VR 控制器；原始 UMI 为 780 g，带 VR 集成的手枪式握把系统至少为 905 g。
- 除 Quest 3S 追踪系统外，每台设备都可以用 3D 打印部件以低于 200 美元的成本制造。
- 这套装置把基于 Quest 的 VR 追踪器装在夹爪上，把头显固定在桌面采集用的支架上；便携模式则把头显装在胸前，用于家庭任务。
- 数据集保存同步的腕部相机、俯视 RealSense 数据、6 自由度夹爪位姿、夹爪角度、任务文本和子动作标签，然后以 30 Hz 转换为 LeRobot 格式。

## 结果
- 该数据集包含 8434 小时、120 万个 episode、680 万个视频-语言-动作三元组、119 个任务，以及每个任务平均 7.99 个子动作；数据由 179 名操作员在两个月内、22 张桌子上采集。
- 论文中引用的既有 UMI 风格数据集规模更小：原始 UMI 只有 12 小时和 4 个任务，FastUMI 约有 60 小时和 22 个任务。
- 在坚果抓取与放置的灵巧度测试中，10 名新手操作员每种坚果做 50 次试验，YUBI 在 M6 坚果上比 UMI 高 20 个百分点，在 M5 坚果上高 10 个百分点，在 M3 坚果上约高 3 倍；两种设备在 M8-M10 坚果上的成功率都至少达到 94%。
- 在 5 个操作效率任务中，YUBI 比 UMI 更快：多米诺骨牌摆放快 1.37 倍，手机充电任务最快快到 4.19 倍。
- 只用 YUBI 腕部数据训练出的单个基于 pi_0.5 的 VLA 策略，可以迁移到三种双臂机器人平台：UR、Franka 和 Toyota ELEY，且使用的是同一个 YUBI 夹爪末端执行器。
- 每个任务进行 20 次机器人执行时，成功结果分别是：球入篮 20/20、堆杯成金字塔 13/20、展开眼镜 9/20、袜子抓取与放置 18/20、胶带入盒 18/20、杯子放置 11/20。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10244v1](https://arxiv.org/abs/2606.10244v1)
