# Paper Notes — Aggarwal2024_AutoMix

> File: `Aggarwal2024_AutoMix.md`
> Priority: **Critical** (closest conceptual predecessor to TRACER)

---

**Full Citation:**
```bibtex
@inproceedings{aggarwal2024automix,
  author    = {Aggarwal, Pranjal and Madaan, Aman and Anand, Ankit and
               Potharaju, Srividya Pranavi and Mishra, Swaroop and Zhou, Pei and
               Gupta, Aditya and Rajagopal, Dheeraj and Kappaganthu, Karthik and
               Yang, Yiming and Upadhyay, Shyam and Faruqui, Manaal and Mausam},
  title     = {{AutoMix}: Automatically Mixing Language Models},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume    = {37},
  year      = {2024},
  eprint    = {2310.12963},
  archivePrefix = {arXiv},
  url       = {https://arxiv.org/abs/2310.12963},
}
```

**Date Read:** 03.08.2026
**Reading Time:** 30 mins

---

## First Impressions (write these BEFORE reading in detail)

*Read the abstract and introduction only. What do you expect this paper to be about?*

This is our closest predecessor and the central comparison point for TRACER, so I expect to spend the most time on this one. From the abstract, AutoMix lets a small model answer first, then uses a few-shot self-verification step to estimate whether that answer is likely correct, and feeds that estimate into a POMDP-based router that decides whether to escalate to a larger model. I expect the paper to describe: how self-verification is prompted (framed as an entailment problem), how the POMDP handles noisy verification signals, and how much it saves in compute while matching or beating baselines. Key thing I need to nail down while reading: exactly where the accept/escalate boundary sits, since TRACER's whole contribution is splitting "escalate" into repair vs. regenerate.

---

## Detailed Notes

### Problem Statement
Multiple LLMs of different sizes and costs are available via API, but there's no simple way to combine them to get good performance without paying for the largest model every time. AutoMix aims to route queries to a larger model only when the smaller model's output is likely wrong, using self-verification rather than a trained external router.

### Related Work They Reference
*(fill in after reading — the abstract references adaptive computation and black-box routing methods, but I need the actual related-work section to map this against FrugalGPT, Hybrid LLM, and RouteLLM)*

### Technical Approach
Two main components:
1. **Few-shot self-verification** — the smaller model (or the same model) is prompted to judge whether its own answer is likely correct, framed as an entailment-style check rather than a raw confidence score.
2. **POMDP-based router** — since self-verification is noisy, the router treats correctness as a partially observable state and uses a POMDP formulation to decide whether to accept the small model's answer or escalate to the larger model, needing only ~50 samples to train.

No architectural changes are required and the method assumes only black-box API access to both models — worth comparing against TRACER's assumption that we also see validator evidence (test failures, etc.), not just the response itself.

### Key Innovation
An ideal router should (a) judge query difficulty from the small model's own confidence, (b) route hard queries up and easy queries down, and — importantly — (c) avoid escalating queries that neither model can solve, since that wastes cost for no benefit. This third point (recognizing "unsolvable" queries) is worth comparing against TRACER's "unresolved/abstain" case.

### Experimental Setup
*(fill in after reading — the paper reports evaluation across five language models and five datasets; need exact datasets, model pairs, and cost metric definitions from the full text)*

### Results — TBD after reading
*(fill in table/numbers from the paper — abstract-level source claims AutoMix "reduces computational cost by over 50% for comparable performance" against strong baselines; needs verifying against the actual results table and exact baselines used)*

### Limitations Acknowledged by Authors
*(fill in after reading)*

### My Critical Assessment
Per our tracker: AutoMix is the primary predecessor and central comparison for TRACER. The main gap I need to articulate clearly in the report is that AutoMix's action space is binary (accept small-model output vs. escalate to large model), while TRACER splits escalation into two distinct actions — repair (edit using the SLM's response as a starting point) vs. regenerate (solve independently) — each with its own calibrated risk estimate. AutoMix's self-verification signal is also purely intrinsic (the model judging itself), whereas TRACER additionally uses external validator evidence (e.g. failed test output) as an input to the risk estimator, which should make our risk signal harder to game and less coupled to the SLM's own blind spots.

### Relevance to My/Our TRACER Work
1. **Core baseline:** this is the single most important comparison in our proposal — cite this paper first when framing what TRACER extends.
2. **POMDP router:** worth understanding well enough to explain why TRACER uses a supervised, calibrated multi-head risk estimator instead of a POMDP — is it a design choice, or does it solve a different problem?
3. **Cost-quality tradeoff framing:** useful language and metrics for how we report our own cost/latency numbers later in the project.
4. **Report/related work section:** this is likely the paper we spend the most words distinguishing ourselves from.

### Follow-up Papers to Read
- RouteLLM and A Unified Approach to Routing and Cascading — both cite AutoMix directly as the output-aware routing lineage.
- Resample or Reroute (cited in our proposal, [10]) — extends the "what to do after the SLM has already answered" framing.

---

## Second Read Notes *(optional)*

*Date of second read:*
*What new things did you notice?*
*Did your understanding change?*
