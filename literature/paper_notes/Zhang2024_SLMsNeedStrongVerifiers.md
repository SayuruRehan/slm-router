# Paper Notes — Zhang2024_SLMsNeedStrongVerifiers

> File: `Zhang2024_SLMsNeedStrongVerifiers.md`
> Priority: **Critical** (direct evidence for SLM–LLM correction dynamics)

---

**Full Citation:**
```bibtex
@inproceedings{zhang2024slmverifiers,
  author    = {Zhang, Yunxiang and Khalifa, Muhammad and Logeswaran, Lajanugen and
               Kim, Jaekyeom and Lee, Moontae and Lee, Honglak and Wang, Lu},
  title     = {Small Language Models Need Strong Verifiers to Self-Correct Reasoning},
  booktitle = {Findings of the Association for Computational Linguistics: ACL 2024},
  pages     = {15637--15653},
  year      = {2024},
  eprint    = {2404.17140},
  archivePrefix = {arXiv},
  url       = {https://aclanthology.org/2024.findings-acl.924/},
}
```

**Date Read:** Not yet read
**Reading Time:** —

---

## First Impressions (write these BEFORE reading in detail)

*Read the abstract and introduction only. What do you expect this paper to be about?*

This is the paper most directly relevant to TRACER's REPAIR action, since it studies whether small models (≤13B) can self-correct reasoning with minimal help from a stronger model. From the abstract, they build a pipeline that has smaller models generate their own self-correction training data — first using correct solutions to guide critiquing of incorrect ones, then fine-tuning on the filtered critiques — and find real gains, especially when paired with a strong (GPT-4-based) verifier, but weaknesses when the verifier is itself weak. I expect the "weak self-verifier" failure mode to be the most citable part for us, since it's basically evidence for why TRACER doesn't rely on the SLM's own self-assessment.

---

## Detailed Notes

### Problem Statement
Small (≤13B) language models are known to struggle at self-correcting their own reasoning without help. This paper studies to what extent minimal input from a stronger model can unlock genuine self-correction ability in small models, rather than relying on full distillation from the larger model.

### Related Work They Reference
*(fill in after reading — likely covers SELF-REFINE and GRACE, both mentioned around this work; need to check their positioning against CRITIC and against "Cannot Self-Correct")*

### Technical Approach
A pipeline that: (1) uses correct solutions to help the model critique its own incorrect responses, generating self-correction training data; (2) filters those generated critiques for quality; (3) uses the filtered critiques for supervised fine-tuning of a self-correcting version of the small model. The verifier that decides whether a solution is correct can be the model itself (intrinsic) or an external signal (extrinsic) — this maps closely onto TRACER's distinction between relying on the SLM vs. relying on validator evidence.

### Key Innovation
Showing that a small model's *self-correction ability* can be meaningfully improved via this bootstrapped pipeline — without full reliance on distillation from a much larger teacher model — while also showing this improvement depends heavily on verifier strength.

### Experimental Setup
Evaluated on two model sizes and five datasets spanning math and commonsense reasoning (per abstract). Need exact model names, dataset names, and verifier configurations from the full text.

### Results — TBD after reading
Per abstract: improved self-correction on both models across the five datasets, with the largest gains when paired with a strong (GPT-4-based) verifier — but clear limitations identified when relying on a weak self-verifier to decide *when* to correct.

### Limitations Acknowledged by Authors
*(fill in after reading — the "weak self-verifier" limitation is flagged in the abstract itself; need the specifics of what fails and why)*

### My Critical Assessment
Per our tracker: this is direct evidence that SLM correction quality improves substantially with stronger verification — which is exactly the argument for TRACER's REPAIR action using an external, stronger LLM plus validator evidence, rather than having the SLM try to fix itself. The gap our tracker flags is real: this paper doesn't optimize action-specific risk (accept/repair/regenerate) — it's about *whether self-correction training works at all*, not about *deciding when to trigger it*. That decision layer is TRACER's actual contribution.

### Relevance to My/Our TRACER Work
1. **Core motivating evidence** for why REPAIR should route through a stronger model with validator evidence rather than SLM self-correction.
2. **Weak-verifier failure mode** — strong citation for why TRACER's risk estimator can't just be the SLM grading its own homework.
3. **Correction methodology reference** — their critique-then-refine pipeline is a useful point of comparison for how we design our own REPAIR prompt (preserve valid parts, fix errors).

### Follow-up Papers to Read
- CRITIC and "Large Language Models Cannot Self-Correct Reasoning Yet" — read as a trio, since together they define the boundary of when self/tool-assisted correction works vs. fails.
- Arimbur (2026), cited in our proposal [17] — studies repairability by error category and model scale, a natural extension of this paper's findings.

---

## Second Read Notes *(optional)*

*Date of second read:*
*What new things did you notice?*
*Did your understanding change?*
