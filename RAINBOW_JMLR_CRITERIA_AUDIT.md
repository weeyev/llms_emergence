# Rainbow JMLR Criteria Audit

Date: 2026-06-22  
Workspace: `/Users/vihantiwari/Documents/emergence_llms`

Paper audited:

Florentin Guth, Brice Menard, Gaspar Rochette, and Stephane Mallat. **A Rainbow in Deep Network Black Boxes.** Journal of Machine Learning Research, 25(350):1-59, 2024.

Public source: <https://www.jmlr.org/papers/v25/23-1573.html>

## Executive Verdict

This paper **does satisfy several of our criteria for paper-defined emergence by the compression / novel-basis route**, but only in a **provisional and scoped** way.

Best classification:

> **PROVISIONAL_PAPER_DEFINED_EMERGENCE for CNN internal compression / novel-basis evidence; not evidence for the exact Guth/Menard double-descent claim; not evidence for LLM emergent intelligence.**

## Criteria Count

Using the seven core checks from `GOAL.md`:

| Count Style | Satisfied | Criteria |
|---|---:|---|
| Strict full-pass count, for the scoped Rainbow compression/novel-basis claim | **4 / 7** | Core 0, Core 1, Core 2, Core 4 |
| Full plus provisional pass count | **5 / 7** | Core 0, Core 1, Core 2, Core 4, Core 5 |
| Including partial/provisional support | **7 / 7** | Core 0 through Core 6 all have at least partial support |
| For the exact Guth/Menard double-descent claim | **0 / 7 as verification of that exact claim** | The paper is public and relevant, but it does not test that claim |

My working verdict is therefore:

> **4 full passes, 1 provisional pass, 2 partial passes.**

This is why the support level is **PROVISIONAL_PAPER_DEFINED_EMERGENCE**, not **STRONG_PAPER_DEFINED_EMERGENCE**.

The reason is subtle but important. *Rainbow* is a real, public, peer-reviewed paper with a serious reduced-description result: learned networks can be described through aligned weight distributions and, in the Gaussian case, through layerwise weight covariance matrices. Those covariances are low-rank, define informative subspaces, and can be used to sample networks that recover much of the trained network's performance in some settings.

That is exactly the kind of internal coarse-graining our rubric was looking for.

But the paper does **not** show the target paper's separate Guth/Menard 2025 claim: a double-descent peak at which covariance spectra move from exponential to scale-free. In fact, *Rainbow* often emphasizes exponential low-rank regimes in weight covariances and power-law-like activation spectra, not a double-descent-linked exponential-to-scale-free phase transition.

## What The Paper Actually Claims

The supported claims are:

1. Deep trained networks can be modeled through a "rainbow" random-feature construction.
2. In the infinite-width limit, rainbow networks define deterministic hierarchical kernels.
3. Trained CNNs approximately satisfy parts of the rainbow hypothesis.
4. In the Gaussian rainbow special case, network behavior is specified by layerwise weight covariance matrices.
5. These covariances are often low-rank.
6. Their eigenvectors can be interpreted as learned features or informative subspaces.
7. Low-dimensional projections of these covariances can preserve classification performance.
8. In some settings, newly sampled rainbow networks recover much of the performance of the original trained networks.
9. The strongest Gaussian rainbow result is mainly shown for scattering networks on CIFAR-10, with more limited applicability to practical ImageNet-scale CNNs.

Claims it does **not** establish:

1. It does not establish a double-descent peak as the control point.
2. It does not establish a scale-free transition at that peak.
3. It does not establish broad LLM emergence.
4. It does not establish emergent intelligence.
5. It does not fully establish causal sufficiency of the reduced variables across architectures and tasks.

## Step-By-Step Rubric Audit

### Core 0 - Source Validity

Verdict: **PASS.**

The source is public, peer-reviewed in JMLR, full text is available, and code is linked by the paper. The local extracted full text is available at `research_sources/txt/guth_2024_rainbow_jmlr.txt`.

Reflection: this is not like the Guth/Menard 2025 double-descent example, which is in preparation / personal communication. *Rainbow* is inspectable and should be allowed into the evidence pool.

### Core 1 - Claim Match

Verdict: **PASS for compression / novel-basis claims; FAIL for exact double-descent claim; OUT OF SCOPE for LLM intelligence.**

For our route B/C criteria, the match is strong. The paper is centrally about replacing individual trained weights with a lower-dimensional, aligned statistical description: learned distributions, covariance matrices, low-rank eigenspaces, rainbow kernels, and data-dependent RKHS descriptions.

For the target paper's exact Guth/Menard example, the match fails. The exact claim in the target paper is about a double-descent peak and covariance spectra changing from exponential to scale-free. *Rainbow* does not test that stated transition.

Reflection: this is where the earlier confusion came from. The citation is real and relevant, but it supports a nearby claim, not the exact in-prep claim.

### Core 2 - Behavioral Or Organizational Effect

Verdict: **PASS.**

The paper shows real internal organization:

- aligned activations and weight distributions across trained networks,
- low-rank learned weight covariances,
- convergence of covariance estimates with width,
- informative covariance eigenspaces shared across training runs,
- dimensionality contractions through learned covariances and re-expansions through random features/nonlinearities,
- sampled rainbow networks preserving substantial performance in some settings.

Reflection: this is much stronger than a mere benchmark jump. It identifies organization inside the model and connects it to function.

### Core 3 - Method And Robustness

Verdict: **PARTIAL / GOOD BUT SCOPED.**

Strengths:

- The paper combines theory and numerical validation.
- It analyzes trained CNNs, not only toy networks.
- It checks multiple initializations, widths, covariance estimates, projections, and sampled rainbow networks.
- It includes CIFAR-10 and ImageNet-facing evidence.
- It compares informative covariance bases against random bases and discusses non-trained kernel baselines.

Limitations:

- The cleanest Gaussian rainbow validation is for scattering networks on CIFAR-10.
- The paper states that the Gaussian rainbow approximation is inadequate for the practical ImageNet scattering setting at the widths tested.
- Some assumptions are verified only at second-order moment level.
- Conditional independence and full training dynamics are not fully established.
- It is not a double-descent study.
- It is not an LLM study.

Reflection: method quality is high, but scope is narrow. This makes it provisional, not strong.

### Core 4 - Internal Mechanism / Coarse-Graining

Verdict: **PASS.**

This is the paper's strongest match to our rubric.

The proposed coarse variables are:

- aligned weight distributions,
- layerwise weight covariance matrices,
- covariance eigenspaces,
- low-dimensional informative subspaces,
- deterministic rainbow kernels,
- data-dependent hierarchical RKHS descriptions.

The paper argues that, in the Gaussian rainbow case, the covariance matrices are enough to specify the network's functional behavior up to the relevant approximation.

Reflection: this is a genuine coarse-graining candidate. It replaces individual neuron weights with a lower-dimensional statistical object that still carries functional information.

### Core 5 - Reduced Predictive Description

Verdict: **PROVISIONAL PASS.**

The paper provides real reduced-description evidence:

- Projecting weights onto leading covariance components can preserve performance.
- KPCA of activations gives a close-to-optimal low-dimensional approximation to learned covariance structure in some layers.
- Sampled Gaussian rainbow networks can recover most of the trained scattering network's CIFAR-10 performance at large width.
- The reduced description is not merely descriptive; it is used to generate working networks and preserve classification accuracy.

Why this is not a full strong pass:

- The strongest result is model-class dependent.
- The reduced description does not fully screen off all microscopic details in all tested architectures.
- The ImageNet/practical-width setting is weaker.
- The paper does not show broad independent replication.
- The causal/intervention status is suggestive rather than decisive.

Reflection: among the sources we looked at, this is one of the better examples of the "reduced predictive description" criterion. It deserves more credit than a generic representation-geometry paper.

### Core 6 - Alternative Explanations And Controls

Verdict: **PARTIAL.**

The paper does address some alternatives:

- random bases are compared against covariance/KPCA bases,
- non-trained kernel baselines are discussed,
- performance is measured on held-out test data,
- width dependence is analyzed,
- limitations of Gaussianity are stated,
- the paper explicitly notes that deviations from Marchenko-Pastur should not simply be interpreted as power-law weight distributions.

Remaining alternatives:

- The effect may rely heavily on CNN/scattering architecture priors.
- It may be specific to natural-image structure.
- Low-rank covariance may be compression without a phase-transition-like emergence.
- The paper does not establish a double-descent control parameter.
- The Gaussian rainbow approximation is not broadly valid at practical ImageNet scale.

Reflection: the paper is careful and self-critical, but not exhaustive. Controls are good enough for provisional status, not strong status.

## Route Labels

Assign:

- **Route B - Compression / Coarse-Grained Internal Model:** yes, strongly.
- **Route C - Novel Bases / Manifolds:** yes, strongly.
- **Route F - Counterclaim / Control:** yes, partially, because it clarifies what the public evidence can and cannot support.

Do not assign as primary:

- **Route A - Scaling / Criticality:** not for this paper alone. It does not test a double-descent transition or critical point.
- **Route D - World Models / Causal State:** no.
- **Route E - Generalization / Analogy / Reuse:** only weakly/indirectly; not the main result.

## Final Classification

| Question | Verdict | Reason |
|---|---|---|
| Does *Rainbow* satisfy our emergence criteria at all? | **Yes, provisionally** | It gives credible internal coarse-graining plus reduced predictive structure. |
| Does it verify the exact Guth/Menard 2025 double-descent example? | **No** | It does not test the double-descent peak or an exponential-to-scale-free transition at that peak. |
| Does it support the target paper's "novel bases/manifolds" lane? | **Yes** | Covariance eigenspaces and rainbow kernels are plausible reduced bases. |
| Does it support the target paper's "compression" lane? | **Yes** | Low-rank covariances and sampled rainbow networks are reduced-description evidence. |
| Is it strong evidence for LLM emergence? | **No** | It is CNN/image-domain evidence, useful by analogy and as a mechanistic standard. |
| Is it evidence for broad emergent intelligence? | **No** | It does not show broad abstraction reuse across qualitatively different domains. |

## Practical Consequence For Our Final Set

This paper should not be dismissed.

It should be treated as:

> **A high-quality non-LLM mechanistic exemplar for the compression / novel-basis route.**

But it should not be counted as:

> **A verified Guth/Menard double-descent phase-transition paper.**

If we keep a separate non-LLM methodological/context tier, *Rainbow* belongs near the top. If the final set is restricted to LLM emergence candidates, it should be cited as background / criterion-calibration evidence rather than as one of the final LLM-positive papers.

## What Would Promote It To Strong

To move from provisional to strong under our rubric, we would need:

1. independent reproduction of the rainbow approximation;
2. broader success on standard CNNs and practical ImageNet-scale models;
3. clearer causal interventions on covariance eigenspaces showing functional necessity/sufficiency;
4. stronger evidence that the reduced covariance description screens off microscopic weight details;
5. training-dynamics theory showing when the rainbow assumptions arise;
6. if used for the target paper's criticality claim, a separate dense double-descent sweep showing the claimed representational transition.

Final one-line verdict:

> *Rainbow* passes our compression / novel-basis criteria **provisionally**, but it does **not** verify the unpublished Guth/Menard double-descent emergence example.
