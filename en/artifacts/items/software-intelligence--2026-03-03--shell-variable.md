---
source: hn
url: https://www.johndcook.com/blog/2026/03/01/tilde-dash/
published_at: '2026-03-03T23:27:44'
authors:
- ibobev
topics:
- bash-shell
- shell-variables
- developer-productivity
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Shell Variable

## Summary
This short article introduces a rare but practical path shorthand in the Bash shell, `~-`, which is equivalent to the previous working directory variable `$OLDPWD`. The author uses a common two-directory switching scenario to show how this feature makes operations such as file comparison more convenient.

## Problem
- The problem the article addresses is: when frequently switching back and forth between two directories in the shell, how can you more conveniently refer to files in the "previous working directory" rather than just switching back to it?
- This matters because developers often compare, inspect, or process files with the same name across two directories; if they can only rely on `cd -` to switch, commands become more cumbersome and less efficient.
- The article also incidentally clarifies a usability issue: this feature has existed for a long time, yet many users are unaware of it.

## Approach
- The core mechanism is Bash’s `~-` expansion: it is the shell’s shorthand for the “previous working directory,” essentially equivalent to the variable `$OLDPWD`.
- The simplest way to think about it: if you are currently in directory A and just switched from directory B, then `~-` refers to B.
- The typical usage given by the author is to directly access a same-named file in the previous directory from the current directory, for example: `diff notes.org ~-/notes.org`.
- Unlike `cd -`, `~-` does not perform a directory switch; instead, it directly references the previous directory path in a command argument, making it better suited for operations such as comparing, copying, or viewing files.

## Results
- The article does not provide formal experiments, datasets, or benchmarks, so there are **no quantitative results** to report.
- The strongest concrete conclusion is that `~-` can serve as a shorthand for `$OLDPWD`, used to directly reference the previous working directory.
- The explicit example given in the article is comparing the same-named file `notes.org` in two directories with the command `diff notes.org ~-/notes.org`.
- The author also points out that this feature is **not new**: it has existed since Bash was released in **1989**, and appeared even earlier in the C shell.

## Link
- [https://www.johndcook.com/blog/2026/03/01/tilde-dash/](https://www.johndcook.com/blog/2026/03/01/tilde-dash/)
