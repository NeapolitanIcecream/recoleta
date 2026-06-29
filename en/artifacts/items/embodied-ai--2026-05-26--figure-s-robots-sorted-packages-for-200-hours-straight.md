---
source: hn
url: https://sherwood.news/tech/figures-robots-just-sorted-packages-for-200-hours-straight/
published_at: '2026-05-26T22:52:27'
authors:
- hochmartinez
topics:
- humanoid-robots
- package-sorting
- robot-autonomy
- multi-robot-operation
- logistics-automation
relevance_score: 0.55
run_id: materialize-outputs
language_code: en
---

# Figure's robots sorted packages for 200 hours straight

## Summary
Figure reports that a team of Figure 03 humanoid robots ran an autonomous package-sorting demo for 200 hours and sorted 249,560 packages. The strongest claim is endurance in a logistics task, not a new research method or benchmarked robot policy.

## Problem
- The task targets warehouse package sorting, where robots must identify a barcode and place the package face-down on a conveyor.
- It matters because useful humanoid robots need to perform paid industrial work for long periods, not only short demonstrations.
- The article does not describe a scientific problem statement, formal benchmark, or failure model.

## Approach
- Figure used Figure 03 humanoid robots on a package-sorting line.
- Each robot located the barcode on a small package and placed the package face-down on the conveyor.
- Multiple robots worked as a team: when one robot's battery ran low after about 3 to 4 hours, it stepped away to recharge and another robot took over.
- Brett Adcock said the run was autonomous with no humans in the loop.
- The post credits Helix models, but the excerpt gives no details on model architecture, training data, control policy, sensing stack, or evaluation setup.

## Results
- The demo ran for 200 hours, equal to 8 days and 8 hours or 25 human 8-hour shifts.
- The livestream count showed 249,560 packages sorted over the 200-hour run.
- In the earlier 10-hour human-versus-robot challenge, the human intern sorted 12,924 packages and the Figure 03 robot sorted 12,735 packages.
- The reported rates were 2.79 seconds per package for the human and 2.83 seconds per package for the robot.
- The article claims the 200-hour run had no failures and no humans in the loop, but it gives no independent audit, error rate, uptime breakdown, or comparison to an existing warehouse automation baseline.

## Link
- [https://sherwood.news/tech/figures-robots-just-sorted-packages-for-200-hours-straight/](https://sherwood.news/tech/figures-robots-just-sorted-packages-for-200-hours-straight/)
