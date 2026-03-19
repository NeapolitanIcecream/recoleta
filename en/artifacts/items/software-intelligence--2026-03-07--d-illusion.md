---
source: hn
url: https://d-illusion.com/
published_at: '2026-03-07T23:56:48'
authors:
- TimeKeeper
topics:
- digital-scarcity
- attention-economy
- gamified-market
- social-referral
- interactive-art
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# D-Illusion

## Summary
D-Illusion proposes an interactive system that discretizes the 86,400 seconds in a day and “sells/allocates” them to participants, combining time position, rising prices, drift, and invitation-based growth into a mechanism of scarcity and dissemination. It is more like a conceptual apparatus for time assetization and social propagation than a traditional academic algorithm paper.

## Problem
- The problem it attempts to address is whether “time,” which is shared by everyone and cannot be stored or owned, can be transformed into a positional resource that individuals can claim and compete over.
- Its significance lies in exploring how digital scarcity, the attention economy, and social propagation jointly shape “value,” mapping abstract time into a social object that can be traded/displayed.
- From a systems design perspective, it also examines how simple rules can drive user participation, invitation-driven spread, and positional competition.

## Approach
- The core mechanism is to divide a day into **86,400** second-level positions; each time a participant makes a purchase, they are assigned the “next available moment,” at which point their name and message are displayed for that second and then disappear.
- Participants **cannot choose their second slot themselves**; instead, slots are assigned sequentially. With each new participant, the price increases by **£0.01**, so joining later costs more.
- The system introduces two opposing forces: **drift** gradually moves a user’s second slot toward an earlier time, representing that “time loses value when it is not shared”; **recruitment**, when someone joins through you, moves both your second and theirs toward a later time, representing that “time gains value when it is shared.”
- The optimization objective is very direct: get as close as possible to **midnight** (the last second of the day), because later positions are more valuable and no one can move beyond midnight.

## Results
- The excerpt **does not provide any experiments, user studies, or quantitative evaluation results**, so standard academic metrics, datasets, or baseline comparisons cannot be reported.
- The strongest concrete claim is that the system defines a fixed total of **86,400 seconds/day** and creates a monotonically increasing cost of entry through a **£0.01 price increase for each additional participant**.
- It also explicitly asserts a dynamic value model: if no action is taken, positions move forward due to **drift**; when a new participant is successfully invited, both parties’ positions move backward, closer to **midnight**.
- Its “breakthrough” lies more in its conceptual and mechanism design: binding time, price, propagation, and ranked competition into a unified interactive rule, rather than surpassing existing methods on performance metrics.

## Link
- [https://d-illusion.com/](https://d-illusion.com/)
