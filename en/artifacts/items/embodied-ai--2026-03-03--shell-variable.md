---
source: hn
url: https://www.johndcook.com/blog/2026/03/01/tilde-dash/
published_at: '2026-03-03T23:27:44'
authors:
- ibobev
topics:
- bash-shell
- command-line
- shell-variables
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Shell Variable

## Summary
This is not a research paper, but a short article about a Bash shell tip introducing `~-` as a shorthand for the previous working directory (`$OLDPWD`). Its value lies in improving the efficiency of switching between two directories and comparing files on the command line.

## Problem
- The problem the article addresses is that users often switch back and forth between two directories, but do not know how to more conveniently refer directly to the "previous working directory."
- This matters because frequently changing directories and comparing files with the same name are common command-line workflow needs, and small syntax improvements can reduce typing and the chance of errors.
- The article also clarifies a misconception: `~-` is not a new feature, but one that Bash has supported since 1989.

## Approach
- The core mechanism is very simple: `~-` is shell expansion syntax, equivalent to the variable `$OLDPWD`, meaning "the previous working directory."
- Users can normally use `cd -` to return to the previous directory, while `~-` allows that directory path to be referenced directly in command arguments.
- The most straightforward use is comparing files with the same name across two directories, for example: `diff notes.org ~-/notes.org`.
- The article explains through a personal usage scenario that this syntax is especially suitable for reducing path typing when repeatedly switching between two directories.

## Results
- The article provides no experiments, benchmarks, or quantitative evaluation results, so there are no paper-style metrics, datasets, or baseline comparisons to report.
- The strongest concrete conclusion is that `~-` can serve as shorthand for `$OLDPWD` and be used to directly reference the previous working directory.
- The specific example given is that running `diff notes.org ~-/notes.org` in the current directory compares the file `notes.org` in the current directory with the one in the previous directory.
- The article states that this feature was not added recently: it has existed since Bash was released in 1989, and originated earlier in C shell.

## Link
- [https://www.johndcook.com/blog/2026/03/01/tilde-dash/](https://www.johndcook.com/blog/2026/03/01/tilde-dash/)
