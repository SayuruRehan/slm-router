# Paper Notes — Chen2021_FinQA

> File: `Chen2021_FinQA.md`
> Priority: **Critical** (primary candidate numerical-reasoning dataset)

---

**Full Citation:**
```bibtex
@inproceedings{chen2021finqa,
  author    = {Chen, Zhiyu and Chen, Wenhu and Smiley, Charese and Shah, Sameena and
               Borova, Iana and Langdon, Dylan and Moussa, Reema and Beane, Matt and
               Huang, Ting-Hao and Routledge, Bryan R. and Wang, William Yang},
  title     = {{FinQA}: A Dataset of Numerical Reasoning over Financial Data},
  booktitle = {Proceedings of the 2021 Conference on Empirical Methods in Natural
               Language Processing (EMNLP)},
  pages     = {3697--3711},
  year      = {2021},
  eprint    = {2109.00122},
  archivePrefix = {arXiv},
  url       = {https://aclanthology.org/2021.emnlp-main.300/},
  note      = {Code: https://github.com/czyssrs/FinQA},
}
```

**Date Read:** Not yet read
**Reading Time:** —

---

## First Impressions (write these BEFORE reading in detail)

*Read the abstract and introduction only. What do you expect this paper to be about?*

This is our primary candidate dataset for the numerical-reasoning half of TRACER's experiments (alongside DebugBench on the code side). From the abstract, FinQA pairs financial-report text and tables with questions that require multi-step numerical reasoning, and — crucially for us — includes annotated "reasoning programs," meaning there's an executable/checkable ground truth for each answer, not just a final number. I expect the paper to describe: how questions were collected/annotated, what the reasoning-program format looks like, and how far models fall short of expert humans (their headline finding per the abstract).

---

## Detailed Notes

### Problem Statement
Financial reports are long and dense, making manual analysis hard, and there wasn't a good benchmark that combined real financial documents (text + tables) with multi-step numerical reasoning that has an explicit, checkable reasoning trace — most QA benchmarks either aren't numerical/financial or don't require multi-step reasoning programs.

### Related Work They Reference
*(fill in after reading — worth comparing framing against TAT-QA, the other financial-QA dataset in our tracker)*

### Technical Approach
Expert-annotated question-answer pairs are built from real financial reports (text and tables together), with each answer accompanied by an explicit multi-step reasoning program (the sequence of arithmetic/lookup operations needed to reach the answer) rather than just a final numeric value. This program-level annotation is what makes execution-based correctness checking possible.

### Key Innovation
The reasoning-program annotations, which let correctness be checked by execution rather than exact-match string comparison or free-text judgment — directly relevant to TRACER's requirement for objective, reproducible correctness checks without relying on an LLM-as-judge.

### Experimental Setup
8,281 expert-annotated QA pairs total, following roughly a 75/10/15 train/dev/test split (6,251 / 883 / 1,147 — per a follow-up paper that reports these numbers; need to confirm against the original FinQA paper directly). Baselines are evaluated with "execution accuracy" as the primary metric.

### Results — TBD after reading
Per abstract: even strong pretrained models fall well short of expert-human performance on the finance-knowledge and multi-step-reasoning combination this dataset requires. Need the actual accuracy gap numbers from the results tables.

### Limitations Acknowledged by Authors
*(fill in after reading)*

### My Critical Assessment
Per our tracker: this is our primary candidate dataset for the "numerical reasoning" arm of TRACER's evaluation, parallel to DebugBench on the code side. Worth checking while reading: does the "reasoning program" format make it straightforward to build a validator that gives TRACER's REPAIR action intermediate feedback (e.g., which step in the program went wrong), similar to failed-test output for code? If so, that's a nice methodological parallel between our two task domains worth calling out explicitly in the methods section.

### Relevance to My/Our TRACER Work
1. **Primary reasoning dataset:** likely candidate for our objective numerical-reasoning experiments.
2. **Execution accuracy metric:** gives us a precedent for defining "incorrect" cleanly under our proposal's operational definitions (Section 3.1).
3. **Program-level ground truth:** potential source of structured validator evidence for the REPAIR action, not just a binary correct/incorrect signal.
4. **Report/methods section:** cite when justifying our dataset and correctness-checking choices for the reasoning domain.

### Follow-up Papers to Read
- TAT-QA (in our tracker as an optional secondary dataset) — a hybrid tabular-text financial QA benchmark, worth comparing against FinQA if we need a generalization test.
- ConvFinQA (mentioned in several citing papers) — a conversational extension of FinQA, useful if we ever want multi-turn numerical reasoning, though likely out of scope for our three-month timeline.

---

## Second Read Notes *(optional)*

*Date of second read:*
*What new things did you notice?*
*Did your understanding change?*
