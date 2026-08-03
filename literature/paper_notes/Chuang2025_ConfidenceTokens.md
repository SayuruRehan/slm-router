# Paper Notes — Chuang2025_ConfidenceTokens

> File: `Chuang2025_ConfidenceTokens.md`
> Priority: **High** (most recent confidence-routing baseline)

---

**Full Citation:**
```bibtex
@inproceedings{chuang2025confidencetokens,
  author    = {Chuang, Yu-Neng and Sarma, Prathusha Kameswara and Gopalan, Parikshit and
               Boccio, John and Bolouki, Sara and Hu, Xia and Zhou, Helen},
  title     = {Learning to Route {LLMs} with Confidence Tokens},
  booktitle = {Proceedings of the 42nd International Conference on Machine Learning (ICML)},
  series    = {Proceedings of Machine Learning Research},
  volume    = {267},
  pages     = {10859--10878},
  year      = {2025},
  eprint    = {2410.13284},
  archivePrefix = {arXiv},
  url       = {https://proceedings.mlr.press/v267/chuang25b.html},
}
```

**Date Read:** Not yet read
**Reading Time:** —

---

## First Impressions (write these BEFORE reading in detail)

*Read the abstract and introduction only. What do you expect this paper to be about?*

This paper studies whether LLMs can reliably signal their own confidence, and proposes "Self-REF" — a lightweight training method that adds explicit confidence tokens to the model, from which a confidence score can be read off directly, instead of relying on verbalized confidence ("I'm 80% sure...") or raw token probabilities. I expect the core contrast to be: confidence tokens vs. verbalized confidence vs. token-probability thresholds, tested on routing and rejection-learning tasks. This is directly useful for the "raw model confidence isn't the same as correctness" argument in our proposal's problem statement.

---

## Detailed Notes

### Problem Statement
In high-stakes settings it matters whether an LLM's output can be trusted, so a system can decide to route the query elsewhere or fall back to a safe default. But getting a *reliable* confidence signal out of an LLM is hard — existing signals (token probabilities, verbalized confidence) can be unstable or poorly calibrated.

### Related Work They Reference
*(fill in after reading — likely covers verbalized-confidence and token-probability confidence estimation literature; check overlap with "Factual Confidence of LLMs" in our tracker)*

### Technical Approach
Self-Reflection with Error-based Feedback (Self-REF): a lightweight training strategy that teaches the model to emit dedicated confidence tokens, separate from its normal output, from which a confidence score can be extracted directly rather than inferred indirectly from token probabilities or a free-text confidence statement.

### Key Innovation
Treating confidence as a learned, explicit signal (a token) rather than an emergent byproduct of generation — this reframes calibration as something you train for directly, which is closer to how TriRoute's risk estimator is designed (a trained, calibrated multi-head predictor) than to post-hoc confidence extraction methods.

### Experimental Setup
Evaluated on four datasets and two base LLMs (per abstract), on routing and rejection-learning tasks specifically. Need exact dataset names and model names from the full text.

### Results — TBD after reading
Per abstract: confidence tokens show significant improvements over both verbalized confidence and standard token-probability methods on downstream routing and rejection tasks. Need the actual comparison numbers.

### Limitations Acknowledged by Authors
*(fill in after reading)*

### My Critical Assessment
Per our tracker: this motivates using learned confidence features rather than raw token-probability thresholds — directly supports our proposal's Section 4 argument that "token probabilities, verbalised confidence, and other uncertainty measures may be unstable or miscalibrated." Worth checking while reading whether Self-REF's confidence tokens are trained per-action or just for a single accept/reject decision — if it's the latter, that's a clear structural difference from TriRoute's action-specific (ACCEPT/REPAIR/REGENERATE) risk heads, worth naming explicitly.

### Relevance to My/Our TriRoute Work
1. **Confidence-signal baseline:** cite as an alternative learned-confidence approach to compare our calibrated risk estimator against.
2. **Motivates learned features over raw probabilities:** strengthens our problem-statement argument about confidence instability.
3. **Rejection-learning framing:** worth checking whether their "reject" option maps onto our "abstain/unresolved" case, since that's a similar idea from a different angle.

### Follow-up Papers to Read
- Factual Confidence of LLMs (Mahaut et al.) — compares confidence estimators more broadly; read alongside this one to build the full confidence-and-calibration picture for our proposal's Section 6.2.
- A Unified Approach to Routing and Cascading — since it argues quality/confidence estimators are the critical factor in routing success generally.

---

## Second Read Notes *(optional)*

*Date of second read:*
*What new things did you notice?*
*Did your understanding change?*
