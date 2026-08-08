# Paper Notes — Dekoninck2025_UnifiedRoutingCascading

> File: `Dekoninck2025_UnifiedRoutingCascading.md`
> Priority: **Critical** (theoretical framing for TRACER's router)

---

**Full Citation:**
```bibtex
@inproceedings{dekoninck2025unified,
  author    = {Dekoninck, Jasper and Baader, Maximilian and Vechev, Martin},
  title     = {A Unified Approach to Routing and Cascading for {LLMs}},
  booktitle = {Proceedings of the 42nd International Conference on Machine Learning (ICML)},
  series    = {Proceedings of Machine Learning Research},
  volume    = {267},
  pages     = {12987--13010},
  year      = {2025},
  eprint    = {2410.10347},
  archivePrefix = {arXiv},
  url       = {https://proceedings.mlr.press/v267/dekoninck25a.html},
}
```

**Date Read:** Not yet read
**Reading Time:** —

---

## First Impressions (write these BEFORE reading in detail)

*Read the abstract and introduction only. What do you expect this paper to be about?*

This is the most theory-heavy paper on our list. From the abstract, the authors point out that routing (pick one model per query) and cascading (run models in increasing size order until satisfied) are usually treated as separate strategies, each without a formal optimality proof, and they introduce "cascade routing" as a unified framework that provably combines both. I expect a fair amount of formal notation — optimal stopping / decision-theoretic framing — and I expect their central empirical finding to be about quality estimators being the deciding factor in whether routing/cascading helps at all, which directly matters for how we justify TRACER's calibrated risk estimator.

---

## Detailed Notes

### Problem Statement
Existing routing and cascading strategies for combining LLMs of different costs (1) lack formal proofs that they're actually optimal, (2) don't clearly say when each strategy helps vs. doesn't, and (3) can't be combined with each other for further gains.

### Related Work They Reference
*(fill in after reading)*

### Technical Approach
They first derive a new optimal cascading strategy and prove an existing routing strategy is already optimal, then unify both into "cascade routing" — a single framework claimed to be theoretically optimal across both paradigms.

### Key Innovation
The headline empirical claim (per the abstract) is that **quality estimators are the critical factor** determining whether routing and/or cascading actually improve the cost-performance tradeoff — not the routing/cascading algorithm itself. This is directly relevant to TRACER's core bet: that a well-calibrated, action-specific risk estimator is what makes the ACCEPT/REPAIR/REGENERATE decision good, more so than the decision rule on top of it.

### Experimental Setup
*(fill in after reading — need the specific benchmarks/model sets used to demonstrate cascade routing "consistently outperforms" the individual approaches)*

### Results — TBD after reading
*(fill in from paper — one secondary source claims a 2–3x speedup while maintaining accuracy; needs verification against the actual results section, not a third-party summary)*

### Limitations Acknowledged by Authors
*(fill in after reading)*

### My Critical Assessment
Per our tracker: this is the theoretical foundation we should lean on when justifying action-outcome routing and the quality/cost tradeoffs TRACER makes. Since the paper's central claim is that estimator quality — not algorithm choice — drives the benefit, this gives us a strong citation for why TRACER invests specifically in a calibrated multi-head risk estimator rather than a simpler heuristic router. Worth checking during reading: does their formal optimality proof assume binary actions (route/don't-route, escalate/don't-escalate), and if so, does it extend cleanly to TRACER's three-action setting (accept/repair/regenerate), or is that a genuine theoretical gap we're filling?

### Relevance to My/Our TRACER Work
1. **Theoretical backbone:** cite when framing why calibration matters more than routing-policy sophistication.
2. **Cost-quality formalism:** useful notation/framing for our own methodology section when defining tolerance-based routing (accept when risk < tolerance).
3. **Strong baseline:** cascade routing itself is worth comparing against empirically if time allows, since it claims to already be optimal within its (likely binary) action space.

### Follow-up Papers to Read
- RouteLLM and AutoMix — both are examples of the routing/cascading paradigms this paper tries to unify.
- SATER — a more recent (2025) paper that also directly compares pre-generation routing and cascade routing on efficiency grounds.

---

## Second Read Notes *(optional)*

*Date of second read:*
*What new things did you notice?*
*Did your understanding change?*
