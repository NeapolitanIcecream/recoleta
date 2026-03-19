---
source: hn
url: https://www.johndcook.com/blog/2026/02/28/file-extensions-bash/
published_at: '2026-03-03T23:27:59'
authors:
- ibobev
topics:
- bash
- shell-scripting
- parameter-expansion
- file-extensions
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# File extensions in bash scripts – shell parameter expansion

## Summary
This article introduces the Bash parameter expansion syntax used to handle file extensions, showing how an extremely small script can convert a `.tex` filename into the corresponding `.dvi` and `.svg` filenames. Its core value is using a concise, native shell mechanism to solve the very common scripting problem of rewriting filenames.

## Problem
- The problem the article addresses is: in a Bash script, how can you efficiently replace the extension of an input filename with target extensions, for example turning `foo.tex` into `foo.dvi` and `foo.svg`.
- This matters because file extension conversion is a high-frequency need in automation scripts; if handling it is cumbersome or error-prone, it reduces the maintainability and practicality of shell scripts.
- The author emphasizes that although shell syntax may look brief or even “cryptic,” it is highly efficient in these scenarios precisely because it is so compressed for common tasks.

## Approach
- The core method is to use Bash parameter expansion `${parameter%word}`, which removes the **shortest** suffix matching the given pattern from the end of the variable’s value.
- In the example, if the input argument `$1` is `foo.tex`, then `${1%.tex}` yields `foo`, and appending `.dvi` or `.svg` generates the new filenames.
- The example script first calls `latex "$1"` to generate the DVI, then calls `dvisvgm --no-fonts "${1%.tex}.dvi" -o "${1%.tex}.svg"` to generate the SVG.
- Put simply: first “remove the old suffix,” then “add the new suffix,” without needing extra tools or complex string processing.

## Results
- The article does not provide formal experiments, datasets, or benchmark tests, so there are **no quantitative results** to report.
- The most specific result stated is: when the input is `foo.tex`, `${1%.tex}` expands to `foo`, which then yields `foo.dvi` and `foo.svg`.
- The complete script shown needs only **2 commands** (`latex` and `dvisvgm`) and **1** Bash parameter expansion pattern to automatically convert a LaTeX source filename into an SVG output filename.
- The author’s strongest concrete claim is: for common tasks like handling file extensions, Bash parameter expansion is extremely concise, enough to make a shell script more direct in some cases than switching to Python.

## Link
- [https://www.johndcook.com/blog/2026/02/28/file-extensions-bash/](https://www.johndcook.com/blog/2026/02/28/file-extensions-bash/)
