---
source: hn
url: https://jsdev.space/toggleevent-source-dialog-closedby/
published_at: '2026-03-05T23:20:19'
authors:
- javatuts
topics:
- web-apis
- javascript
- dialog
- popover
- declarative-ui
relevance_score: 0.19
run_id: materialize-outputs
language_code: en
---

# JavaScript Note: ToggleEvent.source and Dialog.closedBy

## Summary
This article introduces two new Web platform capabilities: `ToggleEvent.source` and `<dialog closedby>`, which make it easier and more declarative to track the trigger source and control the closing behavior of dialogs/popovers. The core value is reducing handwritten JavaScript by pushing common UI behavior down into native HTML/API.

## Problem
- Traditionally, it has been difficult for developers to directly know **which element** triggered the opening or closing of a dialog/popover, often requiring extra event bindings or manual state management.
- Dialog closing strategies (such as closing by clicking the backdrop, pressing `Esc`, or allowing only explicit button-based closing) previously often depended on custom JavaScript, increasing implementation complexity and reliance on framework hooks.
- Multi-layer dialogs also have a backdrop stacking/darkening problem, while CSS currently cannot directly select the topmost element in the browser dialog stack.

## Approach
- `ToggleEvent.source` provides a read-only `source` reference on the `toggle` event, directly indicating which `Element` triggered the visibility change of a popover/dialog; if triggered programmatically, it is `null`.
- `<dialog closedby="...">` declaratively specifies the allowed closing methods in HTML: `any`, `closerequest`, and `none`, covering backdrop clicks, platform actions (such as `Esc`), and explicit developer control, respectively.
- The article uses an example of a dialog closed by multiple buttons to show that, after listening for `toggle`, you can read which button closed the dialog through `event.source.dataset`.
- For the backdrop stacking issue in multi-layer dialogs, the article provides a pragmatic JavaScript solution: use `MutationObserver` to track changes to the `open` attribute and add the `active` class only to the topmost dialog, so that only one backdrop is shown.

## Results
- The article **does not provide benchmark tests or experimental quantitative metrics** (such as latency, throughput, accuracy, or user study numbers).
- Clear capability improvements include: `ToggleEvent.source` can directly return the element that triggered the toggle; if triggered programmatically, it returns `null`.
- `closedby` provides **3** closing modes: `any`, `closerequest`, and `none`; among them, the default behavior for dialogs opened with `showModal()` is `closerequest`, otherwise the default is `none`.
- In terms of browser support, the article claims that both capabilities are supported by **most major browsers**, while Safari currently makes them available behind an **experimental flag**.
- The strongest concrete claim is that these APIs can reduce the extra JavaScript required to implement dialog closing logic and trigger-source identification, while pushing UI behavior toward a declarative model.

## Link
- [https://jsdev.space/toggleevent-source-dialog-closedby/](https://jsdev.space/toggleevent-source-dialog-closedby/)
