# Guth & Menard Criteria Audit

Date: 2026-06-22  
Workspace: `/Users/vihantiwari/Documents/emergence_llms`

## Bottom Line

The Guth & Menard example **does not currently satisfy our criteria as a verified paper-defined emergence claim**, because the exact claim cited by the target paper is not publicly inspectable.

The correct classification is:

> **UNVERIFIABLE for the exact double-descent/scale-free-transition claim; PARTIAL/ADJACENT support for the broader novel-bases/compression idea.**

This is not a rejection of the research program. The public Guth/Menard/Guth et al. work is relevant and interesting. It supports parts of our rubric: learned covariances, low-rank structure, universal encodings, dimensionality reduction, and sampled networks recovering much of trained-network performance. But the public papers do **not** verify the exact target-paper claim that a double-descent peak coincides with a transition in covariance spectra from exponential to scale-free.

## Exact Claim Being Audited

The Royal Society version of the target paper says that Guth & Menard 2025, described as **personal communication**, shows:

- neural networks trained on a task,
- the peak of double descent in loss,
- a concomitant qualitative change in neural encoding,
- covariance spectra of weights or learned features moving from exponential to scale-free,
- implying a qualitative change in bases available for the task,
- and therefore evidence for emergence in a CNN as a phase-transition-like representational change.

The local arXiv text says **in prep** rather than **personal communication**.

That wording matters. Our rubric requires inspectable source evidence. A personal communication or in-preparation result cannot verify the claim.

## Source Trail Checked

Checked on 2026-06-22:

1. Target arXiv version: [Large Language Models and Emergence: A Complex Systems Perspective](https://arxiv.org/html/2506.11135v1) describes the exact Guth/Menard double-descent example as **in prep**.
2. Published Royal Society version: [Large language models and emergence: a complex systems perspective](https://royalsocietypublishing.org/rsta/article/384/2320/20250014/481676/Large-language-models-and-emergence-a-complex) describes the exact example as **personal communication**.
3. Public adjacent paper: [A Rainbow in Deep Network Black Boxes](https://www.jmlr.org/papers/v25/23-1573.html), JMLR 2024.
4. Public adjacent paper: [On the Universality of Neural Encodings in CNNs](https://arxiv.org/abs/2409.19460), arXiv/workshop 2024.
5. Local full-text checks: `research_sources/txt/guth_2024_rainbow_jmlr.txt`, `research_sources/txt/guth_2024_universality_neural_encodings.txt`, and `llms_emergence_rs2.txt`.
6. Web search did not surface a public Guth/Menard 2025 manuscript, dataset, code release, or supplement for the exact double-descent peak plus exponential-to-scale-free transition claim.

See `RAINBOW_JMLR_CRITERIA_AUDIT.md` for the separate verdict on the public JMLR paper. That paper is provisionally positive for the compression / novel-basis route, but it does not verify the exact double-descent claim.

## Criterion-By-Criterion Audit

### Core 0 - Source Validity

**Question:** Does the exact source exist and can we inspect it?

**Exact Guth/Menard double-descent claim:** FAIL / UNVERIFIABLE.

I found the claim in the target paper, but the public source for the exact result was not found. The published Royal Society version describes it as personal communication. The local arXiv version describes it as in preparation. Neither gives a public manuscript, data, or methods for the exact result.

**Adjacent public sources:** PASS.

Two public adjacent sources exist:

- Guth, Menard, Rochette, Mallat, **A Rainbow in Deep Network Black Boxes**, JMLR 2024.
- Guth and Menard, **On the Universality of Neural Encodings in CNNs**, arXiv/workshop 2024.

Reflection: this split is the whole case. If we audit the exact cited claim, it fails source validity. If we audit the broader Guth/Menard program, there is real public evidence.

### Core 1 - Claim Match

**Question:** Do the available sources actually test the stated claim?

**Exact claim:** FAIL / UNKNOWN.

The target claim is specifically about double descent and a transition from exponential to scale-free covariance spectra at the double-descent peak. The public Guth/Menard/Guth et al. papers I inspected do not test that exact transition.

**Adjacent claim:** PARTIAL.

The public papers do match a weaker claim:

- CNN weights can be analyzed via aligned covariances.
- Learned covariance eigenvectors and spectra reveal structured encodings.
- Some learned covariance structure is low-rank.
- A universal encoding appears across natural image datasets.
- Weight covariances can be sufficient to generate networks with similar performance in some settings.

Reflection: it matches the paper's **novel bases/manifolds** and **compression/coarse-graining** lane, but not the **double-descent phase transition** lane as stated.

### Core 2 - Behavioral Or Organizational Effect

**Question:** Is there a real effect or organization worth discussing?

**Adjacent public evidence:** PASS / PARTIAL.

The public work shows meaningful organization:

- low-rank learned weight covariances,
- aligned weight/activation structure,
- covariance-based rainbow models,
- universal eigenvectors/encodings across datasets,
- performance retained when sampling from covariance-based models in some conditions.

**Exact double-descent transition:** UNKNOWN.

Because the exact result is unpublished/uninspectable, we cannot confirm whether the claimed transition occurs at the double-descent peak.

Reflection: there is definitely enough public evidence to keep Guth/Menard as an important adjacent source. But there is not enough to verify the specific target-paper example.

### Core 3 - Method And Robustness

**Question:** Are methods, models, datasets, controls, and robustness adequate?

**Adjacent public sources:** PARTIAL.

Strengths:

- JMLR paper is peer-reviewed.
- It contains theory plus numerical validation.
- It uses trained CNNs/scattering networks and image-classification tasks.
- It checks covariance concentration, low-rank structure, and sampled rainbow networks.
- It includes code.

Limitations:

- It is mainly CNN/image-domain evidence, not LLM evidence.
- The strongest Gaussian rainbow results are restricted to some settings.
- The paper itself says assumptions have not been verified in all cases and approximations degrade when width is reduced.
- It is not a direct double-descent-peak study.

Reflection: the public method quality is serious, but the scope is narrower than the target-paper inference.

### Core 4 - Internal Mechanism / Coarse-Graining

**Question:** Does the work identify an internal mechanism or coarse-grained structure?

**Adjacent public sources:** PASS / PARTIAL.

The public work does identify internal structure:

- weight covariance matrices,
- low-rank covariance eigenspaces,
- aligned learned encodings,
- eigenvectors interpreted as learned features,
- rainbow kernels/RKHS descriptions,
- dimensionality reductions between random feature embeddings.

This is much closer to our emergence rubric than benchmark-jump papers are.

**Exact target claim:** UNKNOWN.

We cannot verify whether the specific double-descent peak coincides with the claimed representational reorganization.

Reflection: if the target paper had cited only the public rainbow/universality papers as examples of compressed/novel-basis structure, I would classify this as a strong adjacent candidate. But because the cited example adds a double-descent phase-transition claim, we need the exact source.

### Core 5 - Reduced Predictive Description

**Question:** Does the internal structure provide a reduced description that remains predictive or functionally useful?

**Adjacent public sources:** PARTIAL / PROVISIONAL.

The public JMLR paper is strong here relative to many other sources:

- covariance-based rainbow networks sampled from the learned random-feature model recover similar performance to trained networks in some settings;
- low-dimensional covariance components capture most performance;
- PCA/activation covariance approximations preserve performance in some cases.

But this is still not a full pass for the target claim because:

- it does not verify the double-descent transition,
- it is mostly CNN/image-domain,
- it is not an LLM result,
- the strongest claim is approximate/model-class-dependent,
- the paper reports limitations.

Reflection: this is the criterion where the public work is most impressive. It is real reduced-description evidence. It just does not prove the specific Guth/Menard example in the target paper.

### Core 6 - Alternative Explanations And Controls

**Question:** Are simpler explanations ruled out?

**Adjacent public sources:** PARTIAL.

The work partly addresses alternatives by:

- comparing across initializations,
- aligning representations,
- estimating covariance structure,
- testing sampled rainbow networks,
- comparing across datasets/tasks in the universality paper.

But several alternatives remain:

- low-rank covariance could be useful compression without being emergence in the target paper's stronger sense;
- the observed structure may be a property of CNN inductive bias or natural images, not a general neural-network phase transition;
- no public evidence ties the effect to the double-descent peak;
- no public evidence establishes a phase transition rather than a smooth representational change.

Reflection: controls are respectable for the adjacent claim but insufficient for the exact emergence interpretation.

## Route Labels

Under our final `GOAL.md`, this example receives these route labels:

- **Route A - Scaling / Criticality:** only for the target-paper exact claim; currently unverifiable.
- **Route B - Compression / Coarse-Grained Internal Model:** partially supported by public rainbow/covariance evidence.
- **Route C - Novel Bases / Manifolds:** partially supported by covariance eigenvectors/universal encoding evidence.
- **Route F - Counterclaim / Control:** needed because double descent alone is not emergence and because simple-model/double-descent explanations exist.

It is **not** an LLM result and should not be used as evidence for LLM emergent intelligence.

## Final Verdict

| Question | Verdict | Reason |
|---|---|---|
| Does the exact Guth/Menard 2025 double-descent claim satisfy our criteria? | **No / Unverifiable** | The exact source is personal communication or in preparation; no inspectable public paper was found. |
| Does public Guth/Menard/Guth et al. work support adjacent novel-basis/compression criteria? | **Yes, partially** | Public work shows low-rank covariances, universal encodings, and covariance-based models retaining performance in CNNs. |
| Does it prove paper-defined emergence? | **Not yet** | It lacks public verification of the double-descent transition and full causal/predictive sufficiency for the exact target claim. |
| Should it stay in the audit? | **Yes, as adjacent/provisional evidence** | It is one of the better examples of internal structure and reduced description, but not a verified claim. |

## What Evidence Would Change The Verdict

The exact claim could be promoted if a public Guth/Menard manuscript, dataset, code release, or supplement showed:

1. A dense sweep through the double-descent peak.
2. Test/train loss curves identifying the peak.
3. Covariance spectra before, at, and after the peak.
4. A statistically clear exponential-to-scale-free transition.
5. Evidence that the changed spectrum reflects a new basis or reduced description.
6. Evidence that the reduced description predicts or produces improved performance.
7. Controls against ordinary double-descent explanations from linear/polynomial/simple models.
8. Replication across architectures, seeds, datasets, or tasks.

Until then, the honest classification is:

> **Exact claim: UNVERIFIABLE. Public adjacent work: PARTIAL / PROVISIONAL support for compression and novel-basis routes.**
