# Paper Notes — Huang2024_CannotSelfCorrect

> File: `Huang2024_CannotSelfCorrect.md`
> Priority: **High** (motivation and risk analysis for TriRoute)

---

**Full Citation:**
```bibtex
@inproceedings{huang2024cannotselfcorrect,
  author    = {Huang, Jie and Chen, Xinyun and Mishra, Swaroop and Zheng, Huaixiu Steven and
               Yu, Adams Wei and Song, Xinying and Zhou, Denny},
  title     = {Large Language Models Cannot Self-Correct Reasoning Yet},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2024},
  eprint    = {2310.01798},
  archivePrefix = {arXiv},
  url       = {https://openreview.net/forum?id=IkmD3fKBPQ},
}
```

**Date Read:** Not yet read
**Reading Time:** —

---

## First Impressions (write these BEFORE reading in detail)

*Read the abstract and introduction only. What do you expect this paper to be about?*

This is the "risk" paper in our list — a critical look at self-correction that pushes back on the optimism in a lot of the self-refinement literature. The key term is "intrinsic self-correction": the model tries to fix its own answer using only its own capabilities, with no external feedback at all. From the abstract, their headline claim is that on reasoning tasks, LLMs largely fail to self-correct this way, and performance can even get *worse* after "correcting." I expect this to be our strongest citation for why TriRoute doesn't rely on unaided self-correction and instead routes through an external stronger model with either preserved structure (REPAIR) or a fresh attempt (REGENERATE).

---

## Detailed Notes

### Problem Statement
Self-correction has been proposed as a fix for LLM inaccuracy, but the paper questions whether this actually works when the model has no external feedback to draw on — i.e., is self-correction really improving reasoning, or is it just noise/regression dressed up as "correction"?

### Related Work They Reference
*(fill in after reading — likely engages directly with SELF-REFINE, Reflexion, and other intrinsic self-correction methods being challenged)*

### Technical Approach
Defines "intrinsic self-correction" precisely: the model attempts to fix its initial response using only its own inherent capabilities, without any external feedback signal. This is important because high-quality external feedback isn't always available in real deployments, so understanding what the model can do *unaided* matters on its own.

### Key Innovation
Empirically challenging the assumption (common across a lot of prior self-refinement work) that LLMs reliably improve their own reasoning when asked to reconsider — showing that in most cases studied, performance doesn't improve, and sometimes actively degrades, when there's no external signal involved.

### Experimental Setup
*(fill in after reading — need the specific reasoning benchmarks and models tested, and how many self-correction rounds were attempted)*

### Results — TBD after reading
Per the paper's own framing: in most instances, performance after self-correction does not improve, and at times, performance degrades. Need the actual per-benchmark numbers and how consistent this finding is across model sizes.

### Limitations Acknowledged by Authors
*(fill in after reading)*

### My Critical Assessment
Per our tracker: this directly justifies TriRoute's use of independent (external) validators and a controlled correction policy, rather than trusting the SLM (or even the stronger model) to fix things purely through self-reflection. Worth being precise in our report about scope: this paper studies *intrinsic* self-correction specifically — it's not a claim that correction never works, just that it doesn't work reliably *without* external feedback. That's an important distinction to get right, since TriRoute's REPAIR action always includes external validator evidence, so this paper is evidence for why that design choice matters, not evidence against repair working at all.

### Relevance to My/Our TriRoute Work
1. **Core motivation citation** for why TriRoute avoids relying on unaided self-correction.
2. **Risk framing:** useful for the problem statement — self-correction can silently make things worse, which is exactly the kind of hidden risk a calibrated risk estimator is meant to catch before it happens.
3. **Contrast with CRITIC/verifier papers:** this paper is the "without external feedback" baseline that CRITIC and the strong-verifier paper argue against — worth citing all three together to show the full picture.

### Follow-up Papers to Read
- CRITIC — the natural counterpoint, since it shows correction *can* work when tool-based external feedback is added.
- Small Language Models Need Strong Verifiers — extends this exact question (does self-correction work?) specifically to small models and ties the answer to verifier strength.

---

## Second Read Notes *(optional)*

*Date of second read:*
*What new things did you notice?*
*Did your understanding change?*
