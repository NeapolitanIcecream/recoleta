---
source: hn
url: https://jsdev.space/toggleevent-source-dialog-closedby/
published_at: '2026-03-05T23:20:19'
authors:
- javatuts
topics:
- web-apis
- dialog
- popover
- javascript
- declarative-ui
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# JavaScript Note: ToggleEvent.source and Dialog.closedBy

## Summary
This article introduces two new Web platform capabilities: `ToggleEvent.source` and the `closedby` attribute on `<dialog>`. They make it easier for developers to know what triggered a popover/dialog state change and to declaratively control how a dialog can be closed, reducing the need for extra JavaScript.

## Problem
- Traditionally, it has been difficult for developers to directly know **which element** triggered the opening/closing of a popover or dialog, often requiring handwritten event-tracking logic.
- How a dialog can be closed (clicking the backdrop, pressing `Esc`, closing via button) has often depended on custom JavaScript, increasing implementation complexity and weakening the benefits of declarative HTML.
- When multiple dialogs are open at the same time, their translucent backdrops can **stack and grow darker** layer by layer; meanwhile, CSS currently cannot directly select the “topmost dialog.”

## Approach
- `ToggleEvent.source` provides a read-only `Element` reference on the `toggle` event that directly indicates **what triggered the visibility change**; if triggered programmatically, it returns `null`.
- `<dialog closedby="...">` allows developers to declare in HTML which closing methods are permitted: `any`, `closerequest`, and `none`, covering backdrop clicks, platform actions (such as `Esc`), and explicit/programmatic closing respectively.
- The article uses buttons together with modern attributes like `commandfor` / `command` and `popovertarget` to show how popover and dialog interactions can be implemented with less JS.
- To address the backdrop stacking issue with multiple dialogs, it offers a practical workaround: use `MutationObserver` to track changes to the `open` attribute and add an `active` class only to the topmost dialog so that only it shows a backdrop.

## Results
- No benchmarks, datasets, or formal experimental metrics are provided; the article is an API explanation and development-practice summary rather than a quantitative research paper.
- The clear functional takeaway is that `ToggleEvent.source` simplifies “identifying the triggering button” to directly reading `event.source`, and that this value is `null` for programmatic toggles.
- `closedby` provides **3** closing strategies: `any`, `closerequest`, and `none`; for dialogs opened with `showModal()`, the default is `closerequest`, otherwise the default is `none`.
- Regarding browser support, the article claims that both capabilities are supported by **most major browsers**, while Safari still requires an experimental flag.
- For the multi-dialog issue, the article claims its `MutationObserver` approach ensures that **only the topmost dialog** displays a backdrop, avoiding the visual darkening caused by stacked overlays.

## Link
- [https://jsdev.space/toggleevent-source-dialog-closedby/](https://jsdev.space/toggleevent-source-dialog-closedby/)
