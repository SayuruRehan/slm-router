# Paper Notes — Gou2024_CRITIC

> File: `Gou2024_CRITIC.md`
> Priority: **High** (validator-assisted correction design)

---

**Full Citation:**
```bibtex
@inproceedings{gou2024critic,
  author    = {Gou, Zhibin and Shao, Zhihong and Gong, Yeyun and Shen, Yelong and
               Yang, Yujiu and Duan, Nan and Chen, Weizhu},
  title     = {{CRITIC}: Large Language Models Can Self-Correct with
               Tool-Interactive Critiquing},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2024},
  eprint    = {2305.11738},
  archivePrefix = {arXiv},
  url       = {https://openreview.net/forum?id=Sx038qxjek},
}
```

**Date Read:** Not yet read
**Reading Time:** —

---

## First Impressions (write these BEFORE reading in detail)

*Read the abstract and introduction only. What do you expect this paper to be about?*

CRITIC is about giving LLMs external tools (like a search engine for facts or a code interpreter for debugging) so they can check and revise their own output, rather than revising purely from internal self-reflection. I expect this to be the most directly useful paper for designing TriRoute's REPAIR action's validator step — the framing of "starting with an initial output, interact with tools to evaluate it, then revise based on that feedback" maps almost exactly onto what our proposal describes for REPAIR (original task + SLM response + validator evidence → corrected response).

---

## Detailed Notes

### Problem Statement
LLMs are prone to hallucinating facts, generating flawed code, or producing other flawed output, and they're essentially "black boxes" with no built-in way to check their own work against ground truth. Humans handle this by using external tools (search engines, code interpreters) to verify and fix their own output — the paper asks whether LLMs can do the same.

### Related Work They Reference
*(fill in after reading — check how they position against SELF-REFINE and other purely-intrinsic self-correction methods, since our proposal explicitly separates validator-assisted correction from those)*

### Technical Approach
Starting from an initial LLM output, CRITIC has the model interact with appropriate external tools (e.g., a search engine, a code interpreter) to evaluate specific aspects of that output, then revises the output based on the feedback those tools provide — a tool-in-the-loop critique-and-revise cycle rather than pure self-reflection.

### Key Innovation
Grounding self-correction in *external, verifiable* tool feedback instead of the model's own (potentially unreliable) judgment of its own output — directly supports using execution/validator evidence rather than confidence scores as the input to a correction step.

### Experimental Setup
*(fill in after reading — need task types covered, which tools were used for which tasks, and how many revision rounds were allowed)*

### Results — TBD after reading
*(fill in from paper)*

### Limitations Acknowledged by Authors
*(fill in after reading)*

### My Critical Assessment
Per our tracker: CRITIC supports the case for validator-assisted correction, but TriRoute's contribution goes a step further — deciding *whether* correction is even worth attempting (via a calibrated risk estimate) before spending the cost of a repair call, rather than always running the critique-and-revise loop. Worth checking while reading whether CRITIC allows multiple revision rounds — our proposal explicitly restricts REPAIR to a single attempt (Section 3.2), specifically to stay distinct from iterative self-repair research, so I should note clearly if CRITIC's design is iterative and by how much that differs from ours.

### Relevance to My/Our TriRoute Work
1. **REPAIR design reference:** the closest existing template for how to structure our own validator-plus-revision prompt.
2. **Supports validator-over-confidence framing:** strengthens the argument that external evidence beats self-assessment for correction.
3. **Contrast point:** helps us clearly state that TriRoute adds an economic decision layer (should we even repair?) on top of what CRITIC-style methods do (how do we repair?).

### Follow-up Papers to Read
- Small Language Models Need Strong Verifiers — read together with this one, since both are about the role of verification/tool feedback in correction quality.
- "Is Self-Repair a Silver Bullet for Code Generation?" (cited in our proposal [16]) — studies when repair gains are/aren't worth the cost, which is exactly the decision layer TriRoute adds on top of CRITIC-style tool-assisted repair.

---

## Second Read Notes *(optional)*

*Date of second read:*
*What new things did you notice?*
*Did your understanding change?*
