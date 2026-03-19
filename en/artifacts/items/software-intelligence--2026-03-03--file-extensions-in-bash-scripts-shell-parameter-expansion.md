---
source: hn
url: https://www.johndcook.com/blog/2026/02/28/file-extensions-bash/
published_at: '2026-03-03T23:27:59'
authors:
- ibobev
topics:
- bash-scripting
- shell-parameter-expansion
- file-extension-handling
relevance_score: 0.14
run_id: materialize-outputs
language_code: en
---

# File extensions in bash scripts – shell parameter expansion

## Summary
This article introduces a shell parameter expansion technique in Bash for handling file extensions, showing how to use a minimal script to map a `.tex` filename to the corresponding `.dvi` and `.svg` filenames.

## Problem
- It addresses the common shell scripting problem of generating corresponding output filenames from an input filename, such as turning `foo.tex` into `foo.dvi` and `foo.svg`.
- This matters because file extension replacement is a frequent operation in automation scripts; if written in a verbose or fragile way, it reduces script readability and reliability.
- The article emphasizes that although shell syntax may look brief or even cryptic, it can solve this kind of common task very directly.

## Approach
- The core method is to use Bash parameter expansion `${parameter%word}`, which removes the **shortest** part matching the pattern `word` from the end of a variable’s value.
- In the example, when the input argument `$1` is `foo.tex`, `${1%.tex}` evaluates to `foo`.
- Then, based on this “filename with the extension removed,” new extensions are appended to produce `${1%.tex}.dvi` and `${1%.tex}.svg`.
- The full script given in the article first runs `latex "$1"`, then runs `dvisvgm --no-fonts "${1%.tex}.dvi" -o "${1%.tex}.svg"`.

## Results
- It provides a concrete working example: given the input `foo.tex`, the script constructs the two target filenames `foo.dvi` and `foo.svg`.
- The post does not provide formal experiments, datasets, or benchmarks, nor does it include quantitative metrics.
- The strongest specific claim is that Bash’s `${parameter%word}` can perform common file extension replacement tasks in a very concise way.
- The article also claims that shell parameter expansion can be “fancier/more powerful,” but here it only demonstrates the basic use of removing a trailing extension.

## Link
- [https://www.johndcook.com/blog/2026/02/28/file-extensions-bash/](https://www.johndcook.com/blog/2026/02/28/file-extensions-bash/)
