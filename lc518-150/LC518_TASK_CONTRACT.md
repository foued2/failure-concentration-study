# LC518 Task Contract: Coin Change II

**Study package:** lc518-150
**Status:** New, standalone task contract for the 150-body construction study.
**Contract source:** [Official LeetCode problem 518, Coin Change II](https://leetcode.com/problems/coin-change-ii/description/).

## 1. Repository separation

The existing frozen file `engineered-study/03_TASK_SPEC.md` specifies `paren7_min_insertions`, a seven-character parenthesis problem. It is not LC518. This new study must remain separate. Do not edit, replace, reinterpret, or reuse the parenthesis-task contract, its input banks, its family definitions, or its results as LC518 evidence.

## 2. Problem semantics

Given an array of distinct positive integer coin denominations and a non-negative target amount, return the number of distinct combinations that sum to the target. Each denomination may be used an unlimited number of times. The order in which coins are selected does not distinguish combinations. If no combination makes the target, return zero.

Important consequences:

- The input coin denominations are distinct.
- The input array is not guaranteed to be sorted. A correct solver must not rely on input order.
- Reordering the same denomination set must not change the answer.
- The empty combination is the unique combination for amount zero, so amount zero has answer one.
- The result is an exact integer count, not a boolean indicating reachability.

## 3. Official input and output constraints

- Number of coin denominations: 1 through 300 inclusive.
- Each denomination: 1 through 5,000 inclusive.
- Denominations are all unique.
- Target amount: 0 through 5,000 inclusive.
- The answer is guaranteed to fit in a signed 32-bit integer.

All diagnostic and held-out inputs must satisfy these constraints. Invalid-input behavior is outside this study's contract.

## 4. Study execution interface

The study language is Python 3.11 or later, with the exact interpreter version to be pinned in a separate execution protocol before any solver execution.

Every solver body must expose the standard judge interface:

    class Solution:
        def change(self, amount: int, coins: list[int]) -> int:
            ...

The adapter will instantiate Solution and call change(amount, coins). The returned value must have exact Python type int; bool is not accepted as an integer result. No printing, network access, external package imports, or reads of unrelated files are permitted by the study harness.

Each execution receives a fresh copy of the input list. The study records any observed input mutation separately; the correctness contract is determined by the returned answer.

## 5. Correctness predicate

For a valid input x = (amount, coins), a solver output is correct exactly when:

1. the call completes under the separately pinned execution conditions;
2. the returned object has exact type int; and
3. its integer value equals the reference combination count for x.

A timeout or resource-limit breach can be classified only after the execution environment and its resource budget have been declared. The LeetCode statement supplies no study-specific wall-clock or memory cutoff. Do not invent one or treat an inefficient implementation as an observed timeout before that budget exists.

An observation that cannot be classified because the harness or oracle did not produce sufficient evidence must be recorded as unresolved, not silently converted into pass or fail.

## 6. Oracle requirements

The study package must contain:

- A primary iterative dynamic-programming oracle using the coin-outer, increasing-amount recurrence.
- A cross-check oracle from a materially different formulation, such as a two-dimensional coin-index/amount dynamic-programming table.
- Exhaustive multiplicity enumeration for small cases only, used to cross-check both implementations on a bounded small-input set.

Record the recurrence, source hash, test domain and cross-check results. These are algorithmically distinct formulations, not independent authorship: if the same agent writes them, do not describe them as independently authored or externally certified.

## 7. Scope limitations

This contract defines correctness only for LC518 under the stated input domain and the study's pinned execution and observation protocol. It does not define correctness for arbitrary programs, other tasks, malformed inputs, concurrent execution, external I/O, floating-point behavior, or every possible resource environment.

A result on the study's finite held-out bank applies to that bank and its declared sampling/weighting design. It does not automatically generalize to all LeetCode submissions or all possible LC518 inputs.