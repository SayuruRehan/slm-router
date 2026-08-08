# Paper Notes — Ong2025_RouteLLM

> File: `Ong2025_RouteLLM.md`
> Priority: **Critical** (modern learned-routing baseline)

---

**Full Citation:**
```bibtex
@inproceedings{ong2025routellm,
  author    = {Ong, Isaac and Almahairi, Amjad and Wu, Vincent and Chiang, Wei-Lin and
               Wu, Tianhao and Gonzalez, Joseph E. and Kadous, M. Waleed and Stoica, Ion},
  title     = {{RouteLLM}: Learning to Route {LLMs} with Preference Data},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2025},
  eprint    = {2406.18665},
  archivePrefix = {arXiv},
  url       = {https://arxiv.org/abs/2406.18665},
  note      = {Code: https://github.com/lm-sys/RouteLLM},
}
```

**Date Read:** Not yet read
**Reading Time:** —

---

## First Impressions (write these BEFORE reading in detail)

*Read the abstract and introduction only. What do you expect this paper to be about?*

RouteLLM trains a router that picks between a weak and strong LLM before generation, learning from human preference data (Chatbot Arena style) rather than task-specific labels. I expect the paper to cover: how preference data gets turned into training labels for the router, what router architectures they compare (their blog mentions a few, e.g. similarity-weighted / matrix-factorization / BERT-classifier variants), and their headline result of roughly halving cost without hurting quality, plus a section on transfer — whether a router trained on one model pair generalizes to a different pair.

---

## Detailed Notes

### Problem Statement
Choosing which LLM to use per query is a cost/quality tradeoff. RouteLLM frames this as training an efficient router that decides, before any generation happens, whether a query should go to a stronger or weaker model.

### Related Work They Reference
*(fill in after reading — worth checking how they position themselves against FrugalGPT and Hybrid LLM specifically)*

### Technical Approach
A training framework for router models that uses human preference data plus data augmentation to improve router quality, so the router doesn't need large amounts of hand-labelled routing data. The router only ever sees the query — it never observes an actual model output before deciding, which is the key structural difference from AutoMix and from TRACER.

### Key Innovation
Learning routing decisions from preference data (rather than correctness labels) and demonstrating that the resulting router transfers reasonably well even when the underlying strong/weak model pair changes at test time — this transfer result is the part most worth digging into, since it speaks to how much a router "learns the task" vs. "learns the specific models."

### Experimental Setup
*(fill in after reading — need exact benchmarks, model pairs used for training vs. transfer testing, and router architectures compared)*

### Results — TBD after reading
Per the abstract: cost reductions "over 2 times in certain cases" without compromising response quality on standard benchmarks. Need the actual numbers per benchmark and per router variant from the results tables.

### Limitations Acknowledged by Authors
*(fill in after reading)*

### My Critical Assessment
Per our tracker: RouteLLM is an important learned-routing baseline, but it routes *before* seeing the SLM response — it can't observe anything about the actual generated output, so it's fundamentally a different point in the pipeline from TRACER (which reacts to a completed SLM response). Worth stating explicitly in the report: RouteLLM answers "which model should generate this?" while TRACER answers "given what the small model already generated, what should we do with it?" These aren't competing approaches so much as different pipeline stages, and could in principle be combined (route pre-generation with RouteLLM's approach, then apply TRACER's action-risk estimator post-generation).

### Relevance to My/Our TRACER Work
1. **Modern routing baseline:** cite as the current standard for learned, preference-trained routers.
2. **Preference-data framing:** worth considering whether any part of our own risk-estimator training could benefit from preference-style labels instead of pure correctness labels.
3. **Transfer results:** relevant if we ever test whether TRACER's risk estimator generalizes across different SLM/LLM pairs.
4. **Code availability:** they released code (lm-sys/RouteLLM) — could be useful as an implementation reference for router training infrastructure even though the routing point differs.

### Follow-up Papers to Read
- Hybrid LLM — the other major pre-generation query-routing baseline, useful to read back-to-back with this one.
- A Unified Approach to Routing and Cascading — formalizes routing and cascading (including approaches like RouteLLM's) under one framework.

---

## Second Read Notes *(optional)*

*Date of second read:*
*What new things did you notice?*
*Did your understanding change?*
