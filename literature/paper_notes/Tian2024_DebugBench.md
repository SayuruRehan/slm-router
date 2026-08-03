# Paper Notes — Tian2024_DebugBench

> File: `Tian2024_DebugBench.md`
> Priority: **Critical** (primary candidate code dataset)

---

**Full Citation:**
```bibtex
@inproceedings{tian2024debugbench,
  author    = {Tian, Runchu and Ye, Yining and Qin, Yujia and Cong, Xin and Lin, Yankai and
               Pan, Yinxu and Wu, Yesai and Hui, Haotian and Liu, Weichuan and
               Liu, Zhiyuan and Sun, Maosong},
  title     = {{DebugBench}: Evaluating Debugging Capability of Large Language Models},
  booktitle = {Findings of the Association for Computational Linguistics: ACL 2024},
  pages     = {4173--4198},
  year      = {2024},
  eprint    = {2401.04621},
  archivePrefix = {arXiv},
  url       = {https://aclanthology.org/2024.findings-acl.247/},
  note      = {Code: https://github.com/thunlp/DebugBench},
}
```

**Date Read:** Not yet read
**Reading Time:** —

---

## First Impressions (write these BEFORE reading in detail)

*Read the abstract and introduction only. What do you expect this paper to be about?*

This is a dataset paper rather than a methods paper, and it's a strong candidate for TriRoute's code-debugging experiments since it gives us objective, execution-checkable correctness — exactly what our proposal requires (no reliance on LLM-as-judge). From the abstract: 4,253 buggy code instances across C++, Java, and Python, built by taking real LeetCode submissions and implanting bugs using GPT-4, covering 4 major and 18 minor bug categories. I expect to focus on: how bugs are categorized (this maps to how we might stratify our own risk analysis by bug type), what "zero-shot" evaluation looked like for their baseline models, and whether runtime/test feedback was part of their setup — since that's the validator evidence TriRoute's REPAIR action needs.

---

## Detailed Notes

### Problem Statement
LLM debugging ability (as opposed to code generation ability) was under-evaluated, and prior debugging benchmarks were limited by data leakage risk (models may have seen the exact bugs during training), small scale, and narrow bug-type coverage.

### Related Work They Reference
*(fill in after reading)*

### Technical Approach
Real code snippets are collected from the LeetCode community (i.e., grounded in real problems, not synthetic ones), then GPT-4 is used to implant bugs into the originally-correct code, followed by quality checks. This gives paired (buggy, correct) examples with known ground truth and known bug category — 4 major bug categories, 18 minor types, across three languages.

### Key Innovation
Scale (4,253 instances) and structured bug categorization across three widely-used languages, evaluated with both a "repair" task (fix the code) and a "bug identification" task, plus an explicit comparison between LLM debugging ability and LLM code-generation ability.

### Experimental Setup
Two commercial and four open-source models evaluated zero-shot (per abstract). Need model names, exact split sizes per language/bug-category, and how "runtime feedback" was operationalized in their experiments — this last point matters a lot for us since it's the closest thing to TriRoute's validator evidence.

### Results — TBD after reading
Per abstract: (1) closed-source models beat humans less consistently than expected and open-source models score lower pass rates overall; (2) debugging difficulty varies a lot by bug category; (3) adding runtime feedback helps but not uniformly — sometimes doesn't help. Need the actual pass-rate numbers and which bug categories were hardest, since that's directly useful for picking which TriRoute experiments to prioritize.

### Limitations Acknowledged by Authors
*(fill in after reading)*

### My Critical Assessment
Per our tracker: this is our primary candidate code dataset for measuring accept/repair/regenerate decisions on code failures. The finding that runtime feedback "is not always helpful" is worth digging into carefully — if adding validator evidence sometimes *hurts* debugging performance in their setup, we need to understand why, since TriRoute's REPAIR action is built around using validator evidence as an input. It may be about how the feedback was presented rather than feedback being useless in principle.

### Relevance to My/Our TriRoute Work
1. **Primary code dataset:** likely candidate for our objective, execution-checkable code-debugging experiments.
2. **Bug category structure:** could let us report risk-estimator performance broken down by bug type, which is more informative than a single aggregate number.
3. **Runtime feedback finding:** important cautionary result to address directly when designing our REPAIR validator-evidence pipeline.
4. **Code/data availability:** their GitHub repo means we can actually build our pipeline on top of this without recreating the dataset ourselves.

### Follow-up Papers to Read
- CRITIC — for how to design tool-based (e.g., execution) feedback loops that actually help correction.
- "Is Self-Repair a Silver Bullet for Code Generation?" (cited in our proposal [16]) — directly studies when code repair gains are modest, which pairs well with DebugBench's mixed runtime-feedback finding.

---

## Second Read Notes *(optional)*

*Date of second read:*
*What new things did you notice?*
*Did your understanding change?*
