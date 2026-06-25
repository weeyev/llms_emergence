# Level 1 Surprise Audit

Date: 2026-06-22  
Workspace: `/Users/vihantiwari/Documents/emergence_llms`

## Scope

The user asked to search the same way we audited Guth/Menard/Rainbow, but now across all **18 Level 1 direct mechanistic shortlist papers**, and to look for surprising implications relative to the emergence paper.

No local `agent.dm` or project `AGENTS.md` file was found in this workspace. I therefore followed `GOAL.md` as the local agent methodology:

1. inspect the original source;
2. check current version / publication status;
3. look for support, follow-up, code, or independent versions;
4. search for criticism, alternative explanations, or caveats;
5. apply Core 0 through Core 6 from `GOAL.md`.

## Executive Surprise

The surprising pattern is this:

> The Level 1 set increasingly supports the emergence paper's **strict** definition of emergence more than the older "benchmark jump" literature did, but it does so by moving away from broad claims of "emergent intelligence" and toward **small causal subspaces, function vectors, world-state vectors, circuit-development trajectories, and progress measures**.

In other words, the strongest papers are not saying "LLMs suddenly become intelligent." They are saying:

- a compact vector/subspace can carry a task, concept, relation, board state, spatial state, or skill variable;
- interventions on that compact object can change behavior;
- apparent phase transitions often decompose into continuous circuit formation or separate developmental transitions;
- "world model" evidence is real in controlled domains, but not yet broad, human-like, or uncontested.

That is extremely close to the emergence paper's desired standard: internal coarse-graining plus a reduced predictive or functional description.

## Aggregate Verdict

Across the 18 Level 1 papers:

- **0 / 18** establish broad emergent intelligence.
- **0 / 18** should be called fully strong without caveats.
- **6 / 18** are near-top evidence for paper-defined emergent capability or direct counter/control evidence.
- **8 / 18** are solid provisional mechanistic candidates.
- **4 / 18** should be treated as partial, theoretical, or calibration evidence rather than top positive evidence.

Best surprise candidates to read first:

1. **Which Attention Heads Matter for In-Context Learning?** - surprising because it shifts the ICL mechanism away from induction heads and toward function-vector heads.
2. **When Do Attention Circuits Form?** - surprising because it separates induction and attention-sink emergence into different developmental transitions.
3. **Mechanistic Data Attribution** - surprising because it links training data to circuit emergence through targeted data interventions.
4. **MetaOthello** - surprising because multiple world models partly share a latent basis rather than becoming isolated sub-models.
5. **Progress Measures for Grokking** - surprising because the apparent jump is explainable as gradual mechanistic amplification and cleanup.

## Current Source/Version Notes

Several rows in the old final table were incomplete or stale:

- `MetaOthello` has an arXiv source: <https://arxiv.org/abs/2602.23164>.
- `Multimodal Function Vectors` has a newer v2 from 2026-05-29: <https://arxiv.org/abs/2510.02528>.
- `Unifying Attention Heads and Task Vectors` has v2 and a NeurIPS 2025 version: <https://arxiv.org/abs/2505.18752>.
- `Which Attention Heads Matter` has an ICML 2025 PMLR version: <https://proceedings.mlr.press/v267/yin25e.html>.
- `What One Cannot, Two Can` has a NeurIPS 2025/OpenReview trail: <https://arxiv.org/abs/2508.07208>.
- `Function Vectors` has an ICLR 2024 version: <https://openreview.net/forum?id=AwyxtyMwaG>.
- `Progress Measures for Grokking` is ICLR 2023 notable/top 25 percent: <https://openreview.net/forum?id=9XFSbDPmdW>.
- `Emergent Linear Representations` has an ACL BlackboxNLP 2023 version: <https://aclanthology.org/2023.blackboxnlp-1.2/>.

## Per-Paper Audit

Legend:

Important correction: the per-paper **Full / Prov / Part** counts below are **core-check strength counts**, not the final emergence-selection criteria. They summarize how cleanly the paper passed the precursor audit checks: source, claim match, effect, method, mechanism, reduced description, and controls.

The final emergence-selection criteria are the route/evidence criteria from the emergence framing:

1. **Scaling** - does scale in data, compute, parameters, training time, or number of components reveal a new capability or internal organization?
2. **Criticality / phase-like transition** - is there a rapid qualitative reorganization, threshold, phase-change-like shift, or order-parameter-like change rather than a merely smooth score increase?
3. **Compression / coarse-graining** - does the system form a compressed higher-level description that ignores lower-level microscopic detail while retaining predictive power?
4. **Novel bases / manifolds** - does the model discover new representational bases, subspaces, manifolds, or internal alphabets that make the task more efficient?
5. **Generalization / transfer** - does the emergent structure support new tasks, analogy, OOD transfer, rapid adaptation, or reuse beyond the exact training setup?
6. **Knowledge-in mechanism** - for LLMs/neural systems, does the paper connect the global property to an internal/local mechanism rather than only reporting behavior?
7. **Capability vs intelligence boundary** - does the evidence support a narrow emergent capability only, or does it actually justify a broader emergent-intelligence claim?

So a paper should ultimately be selected because it satisfies some combination of these final criteria, especially compression/coarse-graining plus functional predictive use. The core checks below only explain why the paper is credible enough to be considered.

## Final-Selection Criteria Matrix

Counting rule:

- **Full** = criterion is satisfied cleanly through the core checks.
- **Prov** = criterion is satisfied provisionally; count it, but keep caveats.
- **Part** = partial evidence only; do not count it as satisfied.
- **No** = criterion is not meaningfully satisfied.

The **Satisfied** column counts **Full + Prov** out of the seven final-selection criteria.
The **Core support** column preserves the precursor audit strength: source, claim match, effect, method, mechanism, reduced description, and controls.

| # | Paper | DOI | Scaling | Criticality | Compression | Novel bases | Generalization | Knowledge-in mechanism | Capability vs intelligence | Satisfied | Core support |
|---:|---|---|---|---|---|---|---|---|---|---:|---|
| 1 | Emergent Structured Representations | [10.48550/arXiv.2602.07794](https://doi.org/10.48550/arXiv.2602.07794) | Part | No | Full | Full | Prov | Full | Full | **5 / 7** | 4 Full / 1 Prov / 2 Part |
| 2 | Mechanistic Data Attribution | [10.48550/arXiv.2601.21996](https://doi.org/10.48550/arXiv.2601.21996) | Prov | Part | Part | No | Prov | Full | Full | **4 / 7** | 5 Full / 0 Prov / 2 Part |
| 3 | MetaOthello | [10.48550/arXiv.2602.23164](https://doi.org/10.48550/arXiv.2602.23164) | Part | No | Full | Full | Full | Full | Full | **5 / 7** | 5 Full / 0 Prov / 2 Part |
| 4 | Relational KD with Fine-tuned FVs | [10.48550/arXiv.2601.08169](https://doi.org/10.48550/arXiv.2601.08169) | No | No | Full | Prov | Full | Full | Full | **5 / 7** | 4 Full / 1 Prov / 2 Part |
| 5 | Deductive Circuits | [10.48550/arXiv.2605.27824](https://doi.org/10.48550/arXiv.2605.27824) | Part | No | Prov | Part | Part | Full | Full | **3 / 7** | 4 Full / 0 Prov / 3 Part |
| 6 | Attention Circuits Form | [10.48550/arXiv.2606.02378](https://doi.org/10.48550/arXiv.2606.02378) | Full | Full | Part | Part | Prov | Full | Full | **5 / 7** | 4 Full / 1 Prov / 2 Part |
| 7 | Analogical Reasoning / Concept Vectors | [10.48550/arXiv.2503.03666](https://doi.org/10.48550/arXiv.2503.03666) | No | No | Prov | Prov | Part | Prov | Full | **4 / 7** | 4 Full / 0 Prov / 3 Part |
| 8 | Linear Spatial World Models | [10.48550/arXiv.2506.02996](https://doi.org/10.48550/arXiv.2506.02996) | No | No | Full | Full | Part | Full | Full | **4 / 7** | 4 Full / 1 Prov / 2 Part |
| 9 | Multimodal Function Vectors | [10.48550/arXiv.2510.02528](https://doi.org/10.48550/arXiv.2510.02528) | No | No | Full | Prov | Full | Full | Full | **5 / 7** | 4 Full / 1 Prov / 2 Part |
| 10 | Hidden-State Geometry for ICL | [10.48550/arXiv.2505.18752](https://doi.org/10.48550/arXiv.2505.18752) | Part | Prov | Full | Full | Prov | Full | Full | **6 / 7** | 5 Full / 0 Prov / 2 Part |
| 11 | Two-Layer Transformers / Induction Heads | [10.48550/arXiv.2508.07208](https://doi.org/10.48550/arXiv.2508.07208) | Full | No | Prov | Part | Full | Prov | Full | **5 / 7** | 4 Full / 0 Prov / 3 Part |
| 12 | Which Attention Heads Matter? | [10.48550/arXiv.2502.14010](https://doi.org/10.48550/arXiv.2502.14010) | Full | Prov | Full | Prov | Full | Full | Full | **7 / 7** | 5 Full / 1 Prov / 1 Part |
| 13 | Chess World Models | [10.48550/arXiv.2403.15498](https://doi.org/10.48550/arXiv.2403.15498) | Part | No | Full | Prov | Prov | Full | Full | **5 / 7** | 5 Full / 1 Prov / 1 Part |
| 14 | What Needs To Go Right For An Induction Head? | [10.48550/arXiv.2404.07129](https://doi.org/10.48550/arXiv.2404.07129) | Full | Full | Prov | Part | Prov | Full | Full | **6 / 7** | 5 Full / 1 Prov / 1 Part |
| 15 | Emergent Linear Representations / Othello | [10.18653/v1/2023.blackboxnlp-1.2](https://doi.org/10.18653/v1/2023.blackboxnlp-1.2) | Part | No | Full | Full | Part | Full | Prov | **4 / 7** | 4 Full / 1 Prov / 2 Part |
| 16 | Function Vectors in LLMs | [10.48550/arXiv.2310.15213](https://doi.org/10.48550/arXiv.2310.15213) | Part | No | Full | Full | Full | Full | Full | **5 / 7** | 5 Full / 1 Prov / 1 Part |
| 17 | Linear Latent World Models / Othello-GPT | [10.48550/arXiv.2310.07582](https://doi.org/10.48550/arXiv.2310.07582) | Prov | No | Full | Full | Part | Full | Full | **5 / 7** | 4 Full / 1 Prov / 2 Part |
| 18 | Progress Measures for Grokking | [10.48550/arXiv.2301.05217](https://doi.org/10.48550/arXiv.2301.05217) | Full | Full | Full | Full | Prov | Full | Full | **7 / 7** | 6 Full / 0 Prov / 1 Part |

Summary by satisfied final-selection criteria:

- **7 / 7:** 2 papers - `Which Attention Heads Matter?`, `Progress Measures for Grokking`.
- **6 / 7:** 2 papers - `Hidden-State Geometry for ICL`, `What Needs To Go Right For An Induction Head?`.
- **5 / 7:** 9 papers - structured representations, MetaOthello, relational KD/FVs, attention circuits, multimodal FVs, two-layer induction-head theory, chess world models, function vectors, linear latent Othello.
- **4 / 7:** 4 papers - mechanistic data attribution, concept vectors/analogy, linear spatial world models, Othello linear representations.
- **3 / 7:** 1 paper - deductive circuits, mainly because it is narrower and synthetic.

Interpretation:

- Every Level 1 paper satisfies **at least 3 / 7** final-selection criteria.
- **13 / 18** satisfy **5 or more** final-selection criteria.
- The most common satisfied criteria are **compression**, **knowledge-in mechanism**, and **capability-vs-intelligence boundary**.
- The weakest criteria across the corpus are **criticality** and broad **generalization**.
- The highest-confidence positive route remains compact internal structure: function vectors, task vectors, world-state vectors, spatial vectors, and circuit/progress variables.

## Why Each Final Criterion Was Marked

This section grounds each matrix row in the paper content. "Counted" means the criterion was marked **Full** or **Prov** in the matrix. "Not counted" means it was marked **Part** or **No**.

### 1. Emergent Structured Representations Support Flexible In-Context Inference

Counted:

- **Compression / coarse-graining:** counted because the paper identifies a low-dimensional/shared conceptual subspace rather than treating the full activation state as the explanatory object.
- **Novel bases / manifolds:** counted because the central object is a structured representational subspace whose geometry supports in-context inference.
- **Generalization / transfer:** counted provisionally because the subspace is tested across inference contexts/tasks, but the evidence is still limited to the paper's task family.
- **Knowledge-in mechanism:** counted because the paper uses causal mediation and attention-head analysis to connect internal representations to model behavior.
- **Capability vs intelligence boundary:** counted because it supports a narrow emergent capability, flexible in-context inference, not broad emergent intelligence.

Not counted:

- **Scaling:** only partial because the paper studies representational emergence in model activations but is not primarily a scaling-law or model-size sweep paper.
- **Criticality:** not counted because it does not show a sharp phase-transition-like threshold or order parameter.

### 2. Mechanistic Data Attribution

Counted:

- **Scaling:** counted provisionally because the paper studies circuit/unit formation during training and how data interventions affect the emergence/convergence of interpretable units.
- **Generalization / transfer:** counted provisionally because high-influence data augmentation/removal changes later capability and circuit formation, but the result is not broad cross-task transfer.
- **Knowledge-in mechanism:** counted because it explicitly links training examples to mechanistic units such as induction heads through attribution and interventions.
- **Capability vs intelligence boundary:** counted because the paper explains specific learned mechanisms, not broad intelligence.

Not counted:

- **Criticality:** only partial because circuit emergence is temporal/developmental but not demonstrated as a sharp critical transition.
- **Compression / coarse-graining:** only partial because interpretable units are localized, but the paper is more about data attribution than a compressed effective model.
- **Novel bases / manifolds:** not counted because the main contribution is causal attribution to data, not discovery of a new representational basis.

### 3. MetaOthello

Counted:

- **Compression / coarse-graining:** counted because multiple Othello variants share a compact board-state representation rather than separate full submodels.
- **Novel bases / manifolds:** counted because isomorphic variants are represented up to an orthogonal rotation, showing a shared latent basis/geometry.
- **Generalization / transfer:** counted because probes/interventions trained on one variant transfer causally to others.
- **Knowledge-in mechanism:** counted because it links mixed-game behavior to internal board-state representations and causal interventions.
- **Capability vs intelligence boundary:** counted because it is controlled-domain world-model evidence, not a broad intelligence claim.

Not counted:

- **Scaling:** only partial because the paper studies mixed-environment training and model organization, but not a scale threshold.
- **Criticality:** not counted because it does not establish a phase-like transition.

### 4. Relational Knowledge Distillation Using Fine-Tuned Function Vectors

Counted:

- **Compression / coarse-graining:** counted because relation/task behavior is compressed into function vectors.
- **Novel bases / manifolds:** counted provisionally because fine-tuned function vectors define usable directions/subspaces, though they are partly engineered after training.
- **Generalization / transfer:** counted because composite function vectors support analogy tasks beyond the extraction examples.
- **Knowledge-in mechanism:** counted because the method intervenes on internal activations with relation/function vectors.
- **Capability vs intelligence boundary:** counted because it supports controllable relational capability, not broad intelligence.

Not counted:

- **Scaling:** not counted because the claim is not driven by scale.
- **Criticality:** not counted because no phase transition or sharp representational threshold is shown.

### 5. Revealing Algorithmic Deductive Circuits for Logical Reasoning

Counted:

- **Compression / coarse-graining:** counted provisionally because the paper decomposes reasoning into a small set of attention heads/circuits rather than using the full model as the explanation.
- **Knowledge-in mechanism:** counted because activation/path patching links internal circuits to deductive behavior.
- **Capability vs intelligence boundary:** counted because the paper is about a narrow logical-reasoning mechanism, not broad intelligence.

Not counted:

- **Scaling:** only partial because there is some layer/circuit organization but not a scale-emergence study.
- **Criticality:** not counted because there is no phase-transition-like claim.
- **Novel bases / manifolds:** only partial because the paper finds circuits, not a new basis/manifold.
- **Generalization / transfer:** only partial because experiments are mainly synthetic and structured.

### 6. When Do Attention Circuits Form?

Counted:

- **Scaling:** counted because the paper tracks circuit formation across training revisions/tokens and architectures.
- **Criticality / phase-like transition:** counted because it identifies distinct formation timing for induction, previous-token, and BOS/attention-sink heads, including sharp or separated developmental transitions.
- **Generalization / transfer:** counted provisionally because it compares multiple 1B-class architecture/corpus settings, though not broad task transfer.
- **Knowledge-in mechanism:** counted because the work directly studies internal attention-head formation.
- **Capability vs intelligence boundary:** counted because it is about circuit emergence and capability classes, not intelligence.

Not counted:

- **Compression / coarse-graining:** only partial because it tracks heads/circuits, but does not reduce behavior to a compact predictive effective model.
- **Novel bases / manifolds:** only partial because the finding is developmental/circuit-level rather than a new representational basis.

### 7. Analogical Reasoning Inside LLMs: Concept Vectors and Limits of Abstraction

Counted:

- **Compression / coarse-graining:** counted provisionally because the paper investigates compact concept vectors as candidate abstractions.
- **Novel bases / manifolds:** counted provisionally because it studies concept-vector directions and representational geometry.
- **Knowledge-in mechanism:** counted provisionally because activation patching/function-vector-style analyses connect internal vectors to outputs, but the conclusions are mixed.
- **Capability vs intelligence boundary:** counted because the paper explicitly limits broad abstraction claims and shows fragility.

Not counted:

- **Scaling:** not counted because scale is not the core evidence.
- **Criticality:** not counted because there is no phase-transition claim.
- **Generalization / transfer:** only partial because the paper finds limits: verbal concepts work better than abstract previous/next style concepts and transformations are fragile.

### 8. Linear Spatial World Models

Counted:

- **Compression / coarse-graining:** counted because spatial configurations are decoded as linear/internal state variables rather than full-token surface patterns.
- **Novel bases / manifolds:** counted because the paper claims linear spatial world-model representations/geometric structure in embeddings.
- **Knowledge-in mechanism:** counted because it uses probes plus causal interventions to test functional use.
- **Capability vs intelligence boundary:** counted because the result is a static spatial-world-model subcase, not broad intelligence.

Not counted:

- **Scaling:** not counted because the claim is not about a scale threshold.
- **Criticality:** not counted because no phase-like transition is shown.
- **Generalization / transfer:** only partial because the paper itself says it does not cover temporal dynamics, object permanence, or broad relation diversity.

### 9. Multimodal Function Vectors for Visual Relations

Counted:

- **Compression / coarse-graining:** counted because visual relation behavior is represented through extracted function vectors.
- **Novel bases / manifolds:** counted provisionally because the vectors define relation directions/subspaces, but the geometry is not as fully established as in some text-only FV work.
- **Generalization / transfer:** counted because vectors transfer to zero-shot relation tasks and composite vectors support one-shot analogy.
- **Knowledge-in mechanism:** counted because selected attention heads and function-vector interventions connect internals to visual relation behavior.
- **Capability vs intelligence boundary:** counted because it supports multimodal relation capability, not broad intelligence.

Not counted:

- **Scaling:** not counted because the evidence is mechanism/intervention, not scaling.
- **Criticality:** not counted because no sharp transition is shown.

### 10. Hidden-State Geometry for In-Context Learning

Counted:

- **Criticality / phase-like transition:** counted provisionally because the paper describes a two-stage transition in hidden-state geometry: early separability and later alignment.
- **Compression / coarse-graining:** counted because it explains ICL through two geometric variables, separability and alignment, rather than the whole activation state.
- **Novel bases / manifolds:** counted because it analyzes hidden-state geometry and task-vector/head geometry.
- **Generalization / transfer:** counted provisionally because it mainly covers ICL classification and says generation-task analysis is preliminary.
- **Knowledge-in mechanism:** counted because it connects previous-token heads, induction heads, task vectors, and hidden-state dynamics.
- **Capability vs intelligence boundary:** counted because it explains ICL mechanism, not intelligence.

Not counted:

- **Scaling:** only partial because training-time emergence and model scaling are not the main established evidence.

### 11. Two-Layer Transformers / Induction Heads

Counted:

- **Scaling:** counted because the theory addresses how depth/model structure changes what can be represented efficiently.
- **Compression / coarse-graining:** counted provisionally because conditional k-gram/Markov structure is a reduced description of sequence statistics.
- **Generalization / transfer:** counted because the construction handles any-order Markov processes in the theoretical setting.
- **Knowledge-in mechanism:** counted provisionally because it is a mechanistic construction of induction-head capability, but more theoretical than empirical.
- **Capability vs intelligence boundary:** counted because it supports a narrow ICL/Markov capability, not intelligence.

Not counted:

- **Criticality:** not counted because it is not about a phase transition.
- **Novel bases / manifolds:** only partial because the contribution is circuit/construction capacity, not a new basis/manifold.

### 12. Which Attention Heads Matter For In-Context Learning?

Counted:

- **Scaling:** counted because the paper compares 12 models and finds that FV heads matter especially in larger models.
- **Criticality / phase-like transition:** counted provisionally because it tracks head evolution during training and finds many FV heads start as induction heads before transitioning to the FV mechanism.
- **Compression / coarse-graining:** counted because ICL task execution is explained through a small set of FV heads.
- **Novel bases / manifolds:** counted provisionally because FVs define compact task directions, though the paper is more head-mechanism focused than manifold-focused.
- **Generalization / transfer:** counted because it compares mechanisms across tasks/models and ICL settings.
- **Knowledge-in mechanism:** counted because it uses detailed ablations to compare induction heads and FV heads.
- **Capability vs intelligence boundary:** counted because it explains ICL capability, not broad intelligence.

Not counted:

- None under the Full/Prov counting rule, though the criticality and novel-basis marks remain provisional rather than full.

### 13. Chess World Models

Counted:

- **Compression / coarse-graining:** counted because board state and player skill are represented as compact latent variables.
- **Novel bases / manifolds:** counted provisionally because linear probes/vectors define editable directions, but the geometry is not the whole focus.
- **Generalization / transfer:** counted provisionally because the skill vector improves play in random-board settings, but this stays inside chess.
- **Knowledge-in mechanism:** counted because vector interventions edit internal board state/skill and change legal move behavior.
- **Capability vs intelligence boundary:** counted because it is formal-game world-model evidence, not broad natural-language intelligence.

Not counted:

- **Scaling:** only partial because it studies model depth/architecture and capability, but not a clean scale threshold.
- **Criticality:** not counted because no phase-transition-like transition is established.

### 14. What Needs To Go Right For An Induction Head?

Counted:

- **Scaling:** counted because it studies training dynamics and when induction heads emerge.
- **Criticality / phase-like transition:** counted because it directly studies the phase change associated with induction-head emergence.
- **Compression / coarse-graining:** counted provisionally because it decomposes a phase change into three subcircuits, a reduced mechanistic description.
- **Generalization / transfer:** counted provisionally because it explains data-dependent timing shifts, but the setup remains synthetic/controlled.
- **Knowledge-in mechanism:** counted because activation clamping and subcircuit analysis causally test formation mechanisms.
- **Capability vs intelligence boundary:** counted because it is about a narrow ICL circuit, not intelligence.

Not counted:

- **Novel bases / manifolds:** only partial because the paper identifies subcircuits and training dynamics rather than a new representational basis.

### 15. Emergent Linear Representations / Othello

Counted:

- **Compression / coarse-graining:** counted because the Othello board is represented as compact linear mine/yours/empty features.
- **Novel bases / manifolds:** counted because linear directions enable interpretation and vector arithmetic interventions.
- **Knowledge-in mechanism:** counted because interventions on the linear directions affect legal move predictions.
- **Capability vs intelligence boundary:** counted provisionally because the result is narrow and contested by bag-of-heuristics concerns.

Not counted:

- **Scaling:** only partial because model/training emergence is discussed but not established as a scale criterion.
- **Criticality:** not counted because no phase transition is shown.
- **Generalization / transfer:** only partial because it stays within Othello and related board-state concepts.

### 16. Function Vectors in LLMs

Counted:

- **Compression / coarse-graining:** counted because an input-output function is represented as a compact vector.
- **Novel bases / manifolds:** counted because FVs are directions/subspaces in residual-stream activation space that can trigger task behavior.
- **Generalization / transfer:** counted because FVs trigger task execution outside the original ICL contexts and show portability across tasks/models/layers.
- **Knowledge-in mechanism:** counted because causal mediation identifies heads transporting the function vector, and interventions test causal effect.
- **Capability vs intelligence boundary:** counted because the paper supports compact task abstractions, not broad intelligence.

Not counted:

- **Scaling:** only partial because effects are compared across models/layers but not framed as a scale-induced emergence threshold.
- **Criticality:** not counted because no phase-transition-like change is shown.

### 17. Linear Latent World Models / Othello-GPT

Counted:

- **Scaling:** counted provisionally because model complexity/layer depth affect the emergence and causal role of the latent representation.
- **Compression / coarse-graining:** counted because the model's decision process is explained through a linear latent world representation.
- **Novel bases / manifolds:** counted because the representation is a linear basis for opposing pieces/world state.
- **Knowledge-in mechanism:** counted because causal interventions show the representation steers decisions.
- **Capability vs intelligence boundary:** counted because it is narrow Othello evidence, not broad intelligence.

Not counted:

- **Criticality:** not counted because no sharp transition is established.
- **Generalization / transfer:** only partial because the evidence stays inside the Othello task family.

### 18. Progress Measures For Grokking

Counted:

- **Scaling:** counted because the phenomenon depends on training steps/data/regularization and the transition from memorization to generalization.
- **Criticality / phase-like transition:** counted because grokking is the apparent sudden behavioral transition being analyzed.
- **Compression / coarse-graining:** counted because the learned algorithm is reverse engineered into Fourier/trigonometric progress measures rather than described by all weights.
- **Novel bases / manifolds:** counted because the model's algorithm uses Fourier-space structure and rotations.
- **Generalization / transfer:** counted provisionally because the mechanism explains generalization on modular arithmetic and is checked across variants, but it is not broad task transfer.
- **Knowledge-in mechanism:** counted because activations, weights, and Fourier-space ablations support the mechanistic account.
- **Capability vs intelligence boundary:** counted because it is a narrow modular-addition/grokking mechanism, not intelligence.

Not counted:

- None under the Full/Prov counting rule, though generalization is provisional because the task family is narrow.

### 1. Emergent Structured Representations Support Flexible In-Context Inference in Large Language Models

Source: <https://arxiv.org/abs/2602.07794>  
Current version: arXiv v3, updated 2026-04-20. Also appears in ICLR 2026 Re-Align workshop search results.

Core-check strength count: **4 Full / 1 Prov / 2 Part**  
Support level: **PROVISIONAL_PAPER_DEFINED_EMERGENCE**

What it supports:

- conceptual subspace in middle-to-late layers;
- structure persists across contexts;
- causal mediation analysis argues the subspace is functionally central to predictions;
- early/middle attention heads integrate context and later layers use the subspace.

Surprise relative to emergence paper:

This is exactly the kind of missing evidence the emergence paper asks for: not just a capability, but an internal representation plus causal mediation. It is still new and not independently replicated, but it is more directly on-rubric than the older benchmark-emergence papers.

Action: **keep Level 1, provisional.**

### 2. Mechanistic Data Attribution: Tracing the Training Origins of Interpretable LLM Units

Source: <https://arxiv.org/abs/2601.21996>  
Current version: arXiv v2, updated 2026-06-07.

Core-check strength count: **5 Full / 0 Prov / 2 Part**  
Support level: **PROVISIONAL_PAPER_DEFINED_EMERGENCE**, near-top evidence if methods hold.

What it supports:

- influence-function framework traces interpretable units back to training samples;
- targeted removal or augmentation of high-influence samples modulates emergence of heads;
- repetitive structural data such as LaTeX/XML acts as a catalyst;
- induction-head interventions change ICL capability;
- data augmentation can accelerate circuit convergence.

Surprise relative to emergence paper:

This is a direct "knowledge-in" answer. The emergence paper warns that training data may program behavior rather than allow emergence; this paper suggests a middle path: specific data distributions catalyze identifiable internal circuits, and those circuits can be steered by data edits.

Action: **keep Level 1; mark as one of the most surprising papers.**

### 3. MetaOthello: A Controlled Study of Multiple World Models in Transformers

Source: <https://arxiv.org/abs/2602.23164>  
Current version: arXiv v1, 2026-02-26. Code/data surfaced via project/GitHub/Hugging Face search results.

Core-check strength count: **5 Full / 0 Prov / 2 Part**  
Support level: **PROVISIONAL_PAPER_DEFINED_EMERGENCE**

What it supports:

- controlled variants of Othello with shared syntax but different rules/tokenizations;
- mixed-game transformers use a mostly shared board-state representation;
- linear probes transfer causally across variants;
- isomorphic game representations are related by an orthogonal rotation;
- later layers specialize only after early/mid shared states.

Surprise relative to emergence paper:

The Othello story is not simply "coherent world model" versus "bag of heuristics." Multiple world models may be organized as a shared latent basis plus rotations/specialization. That is more nuanced and more coarse-grained than the original debate.

Action: **keep Level 1, but classify as controlled-domain evidence.**

### 4. Relational Knowledge Distillation Using Fine-tuned Function Vectors

Source: <https://arxiv.org/abs/2601.08169>  
Current version: arXiv v1, 2026-01-13. OpenReview PDF found in search.

Core-check strength count: **4 Full / 1 Prov / 2 Part**  
Support level: **PROVISIONAL / PARTIAL_PAPER_DEFINED_EMERGENCE**

What it supports:

- small sets of examples fine-tune function vectors for relation tasks;
- composite function vectors can support analogy tasks;
- inserting vectors into activations improves performance on cognitive-science and SAT-style analogies.

Surprise relative to emergence paper:

This is a very "less is more" result: a tiny tuned vector can distill relational knowledge. But because the vector is fine-tuned/engineered, it is better evidence for controllable compact mechanisms than for naturally emergent intelligence.

Action: **keep Level 1 as mechanism evidence; do not overclaim natural emergence.**

### 5. Revealing Algorithmic Deductive Circuits for Logical Reasoning

Source: <https://arxiv.org/abs/2605.27824>  
Current version: arXiv v1, 2026-05-27.

Core-check strength count: **4 Full / 0 Prov / 3 Part**  
Support level: **PARTIAL_PAPER_DEFINED_EMERGENCE**

What it supports:

- attention heads responsible for sub-reasoning patterns;
- roughly 3 percent of heads specialize for factual/rule-based substeps;
- higher layers integrate information into graph-traversal-like global reasoning strategies;
- activation/path patching is used for circuit discovery.

Main caveat from the paper:

The analysis is mostly on synthetic datasets with explicit logical structures, focuses on attention rather than MLPs, and may not generalize to free-form reasoning.

Surprise relative to emergence paper:

Reasoning can be decomposed into small algorithmic circuits, but current evidence is much narrower than "LLMs reason" as a broad claim.

Action: **keep as partial Level 1; lower confidence than the vector/world-model papers.**

### 6. When Do Attention Circuits Form? Developmental Trajectories of Capability and Attention-Sink Emergence Across Three 1B-Class Architectures

Source: <https://arxiv.org/abs/2606.02378>  
Current version: arXiv v2, 2026-06-09. Code/data/repro scripts linked in arXiv HTML.

Core-check strength count: **4 Full / 1 Prov / 2 Part**  
Support level: **PROVISIONAL_PAPER_DEFINED_EMERGENCE / strong developmental-control evidence**

What it supports:

- 30 mechanistic runs across Pythia 1B, OLMo 1B, OLMoE 1B;
- induction, previous-token, and BOS-attractor heads are tracked over log-spaced checkpoints;
- induction formation and attention-sink formation are separated by 10-20x in tokens for DCLM models;
- attention-sink emergence can be gradual or sharp depending on architecture/corpus;
- circuit identification can happen very early in training.

Surprise relative to emergence paper:

This directly complicates phase-transition language. "The" transition is not one transition: capability-circuit emergence and attention-sink emergence can separate by an order of magnitude.

Action: **keep Level 1; this is one of the most important surprises.**

### 7. Analogical Reasoning Inside Large Language Models: Concept Vectors and the Limits of Abstraction

Source: <https://arxiv.org/abs/2503.03666>  
Current version: arXiv v1, 2025-03-05. Code found at <https://github.com/gucioopielka/concept_vectors>.

Core-check strength count: **4 Full / 0 Prov / 3 Part**  
Support level: **PARTIAL_PAPER_DEFINED_EMERGENCE with strong negative evidence for broad abstraction**

What it supports:

- function vectors are not invariant to simple input-format changes;
- invariant concept vectors exist for some verbal concepts;
- a model may form a correct internal representation while producing a wrong output;
- for abstract concepts like previous/next, invariant linear representations are not observed.

Surprise relative to emergence paper:

This is a high-value negative/limiting paper. It supports compact concept vectors in some settings but undercuts broad emergent intelligence: abstract concept invariance is fragile.

Action: **keep Level 1, but label as mixed positive/counterclaim.**

### 8. Linear Spatial World Models Emerge in Large Language Models

Source: <https://arxiv.org/abs/2506.02996>  
Current version: arXiv v1, 2025-06-03. PDF had to be extracted directly because arXiv HTML returned 404.

Core-check strength count: **4 Full / 1 Prov / 2 Part**  
Support level: **PROVISIONAL_PAPER_DEFINED_EMERGENCE**

What it supports:

- linear spatial representations in contextual embeddings;
- synthetic object-position dataset;
- probes decode object positions;
- geometric consistency is tested;
- causal interventions test functional use.

Main caveat:

The paper explicitly does not cover temporal dynamics, object permanence, or broad spatial relation diversity.

Surprise relative to emergence paper:

There is a concrete world-model-like spatial subcase in LLMs, but it is much narrower than "world model" in the full cognitive sense.

Action: **keep Level 1, but scoped to static spatial relations.**

### 9. Multimodal Function Vectors for Visual Relations

Source: <https://arxiv.org/abs/2510.02528>  
Current version: arXiv v2, updated 2026-05-29.

Core-check strength count: **4 Full / 1 Prov / 2 Part**  
Support level: **PROVISIONAL_PAPER_DEFINED_EMERGENCE**

What it supports:

- small subset of attention heads transmits visual-relation representations;
- function vectors can be extracted and transferred to zero-shot relation tasks;
- composite function vectors support one-shot analogy in multimodal settings;
- v2 adds broader experiments/appendices relative to initial version.

Surprise relative to emergence paper:

Function-vector evidence is no longer only text-only. The compact vector mechanism appears to extend into visual relations, which is stronger for the "abstraction reuse" route.

Action: **keep Level 1; update version status to v2.**

### 10. Unifying Attention Heads and Task Vectors via Hidden State Geometry in In-Context Learning

Source: <https://arxiv.org/abs/2505.18752>  
Current version: arXiv v2, updated 2025-10-18; NeurIPS 2025 version found in OpenReview/search.

Core-check strength count: **5 Full / 0 Prov / 2 Part**  
Support level: **PROVISIONAL_PAPER_DEFINED_EMERGENCE**

What it supports:

- ICL can be explained through separability and alignment of query hidden states;
- separability emerges early, alignment develops later;
- previous-token heads drive separability;
- induction heads and task vectors enhance alignment.

Main caveat:

The paper says generation-task analysis is preliminary and training-time emergence is future work.

Surprise relative to emergence paper:

Some "emergence" may be better described as hidden-state geometry becoming separable and aligned, not as a mysterious new ability.

Action: **keep Level 1; strong mechanistic unifier but not final emergence proof.**

### 11. What One Cannot, Two Can: Two-Layer Transformers Provably Represent Induction Heads on Any-Order Markov Chains

Source: <https://arxiv.org/abs/2508.07208>  
Current version: arXiv v2, updated 2025-11-14; NeurIPS 2025/OpenReview trail found.

Core-check strength count: **4 Full / 0 Prov / 3 Part**  
Support level: **PARTIAL_PAPER_DEFINED_EMERGENCE / theoretical mechanism**

What it supports:

- two-layer single-head transformer can represent any conditional k-gram / kth-order Markov process;
- depth/Markov-order relation is characterized more tightly than prior work;
- simplified learning dynamics illustrate how ICL-like representations can emerge.

Surprise relative to emergence paper:

Strong ICL-related structure does not always require massive scale. A very shallow construction can implement a family of induction-head mechanisms. This weakens scale-only emergence stories.

Action: **keep, but maybe move from direct empirical Level 1 to theoretical/mechanism-calibration tier.**

### 12. Which Attention Heads Matter for In-Context Learning?

Source: <https://arxiv.org/abs/2502.14010>; final PMLR/ICML page: <https://proceedings.mlr.press/v267/yin25e.html>  
Current version: ICML 2025.

Core-check strength count: **5 Full / 1 Prov / 1 Part**  
Support level: **PROVISIONAL_PAPER_DEFINED_EMERGENCE / strong ICL mechanism evidence**

What it supports:

- compares induction heads and function-vector heads in 12 language models;
- few-shot ICL performance depends primarily on FV heads, especially in larger models;
- FV and induction heads are developmentally connected;
- many FV heads start as induction heads before transitioning to FV mechanism.

Surprise relative to emergence paper:

This is probably the biggest ICL surprise. The popular "induction heads implement ICL" story is too simple; induction may be a developmental precursor to a more abstract FV mechanism.

Action: **keep Level 1; read before induction-head-only papers.**

### 13. Emergent World Models and Latent Variable Estimation in Chess-Playing Language Models

Source: <https://arxiv.org/abs/2403.15498>; COLM/OpenReview trail found.  
Current version: arXiv v2, updated 2024-07-14.

Core-check strength count: **5 Full / 1 Prov / 1 Part**  
Support level: **PROVISIONAL_PAPER_DEFINED_EMERGENCE**

What it supports:

- chess GPT trained only on next-character prediction learns internal board-state representations;
- probes decode board state and player skill;
- activation/vector interventions edit board state and skill;
- adding a skill vector improves win rate up to 2.6x in random-board settings.

Main caveat:

Chess is constrained and rule-based; interventions have side effects; this is not natural-language world modeling.

Surprise relative to emergence paper:

The Othello world-model route generalizes to chess and latent skill estimation, but still inside a formal game domain.

Action: **keep Level 1; strong controlled-domain world-model evidence.**

### 14. What Needs To Go Right For An Induction Head?

Source: <https://arxiv.org/abs/2404.07129>; ICML 2024 trail found.  
Current version: arXiv v1, ICML 2024.

Core-check strength count: **5 Full / 1 Prov / 1 Part**  
Support level: **PROVISIONAL_PAPER_DEFINED_EMERGENCE / strong circuit-formation evidence**

What it supports:

- controlled synthetic training setup for induction-head emergence;
- optogenetics-inspired activation clamping through training;
- induction heads are diverse and additive;
- three subcircuits interact to drive formation and phase change;
- subcircuits explain data-dependent timing shifts.

Surprise relative to emergence paper:

The "phase change" becomes mechanically decomposable. This supports the emergence paper's demand for internal mechanisms, while weakening the idea that a sudden metric change is explanatory.

Action: **keep Level 1.**

### 15. Emergent Linear Representations in World Models of Self-Supervised Sequence Models

Source: <https://arxiv.org/abs/2309.00941>; ACL BlackboxNLP version: <https://aclanthology.org/2023.blackboxnlp-1.2/>  
Current version: arXiv v2, ACL workshop 2023.

Core-check strength count: **4 Full / 1 Prov / 2 Part**  
Support level: **PROVISIONAL_PAPER_DEFINED_EMERGENCE, but contested**

What it supports:

- Othello board state is linearly encoded as mine/yours/empty;
- simple vector arithmetic can causally intervene on model behavior;
- additional linear concepts such as flipped tiles appear.

Counterpressure:

- The "bag of heuristics" critique remains relevant.
- Probe interpretation and world-model semantics are still contested.

Surprise relative to emergence paper:

The world model may be linearly accessible, but linear accessibility does not automatically imply a unified, human-like world model.

Action: **keep Level 1 with explicit counterclaim link.**

### 16. Function Vectors in Large Language Models

Source: <https://arxiv.org/abs/2310.15213>; ICLR 2024 version: <https://openreview.net/forum?id=AwyxtyMwaG>; project: <https://functions.baulab.info/>  
Current version: arXiv v2, ICLR 2024.

Core-check strength count: **5 Full / 1 Prov / 1 Part**  
Support level: **PROVISIONAL_PAPER_DEFINED_EMERGENCE, near-top positive evidence**

What it supports:

- small number of attention heads transport compact task/function representations;
- function vectors causally affect behavior across tasks, models, and layers;
- FVs trigger task execution outside the original ICL context;
- some vector composition is possible;
- FVs contain more than output-vocabulary information.

Surprise relative to emergence paper:

This is one of the cleanest examples of "less is more": a compact internal vector can encode and trigger a function. It is closer to the emergence paper's desired evidence than most benchmark-scaling work.

Action: **keep Level 1; use as central positive route B/C evidence.**

### 17. Linear Latent World Models in Simple Transformers: A Case Study on Othello-GPT

Source: <https://arxiv.org/abs/2310.07582>  
Current version: arXiv v2, 2023-10-12; OpenReview/NeurIPS workshop trail found.

Core-check strength count: **4 Full / 1 Prov / 2 Part**  
Support level: **PROVISIONAL_PAPER_DEFINED_EMERGENCE, contested**

What it supports:

- Othello-GPT has linear representation of opposing pieces;
- representation causally steers decisions;
- layer depth and model complexity matter.

Surprise relative to emergence paper:

This reinforces the linear-world-model route, but it is mostly an extension/calibration of the Othello evidence rather than a separate broad LLM claim.

Action: **keep but merge conceptually with the Othello cluster.**

### 18. Progress Measures For Grokking Via Mechanistic Interpretability

Source: <https://arxiv.org/abs/2301.05217>; ICLR 2023: <https://openreview.net/forum?id=9XFSbDPmdW>  
Current version: arXiv v3, ICLR 2023 notable/top 25 percent.

Core-check strength count: **6 Full / 0 Prov / 1 Part**  
Support level: **STRONG_CONTROL / PROVISIONAL_PAPER_DEFINED_EMERGENCE for the narrow modular-addition setting**

What it supports:

- grokking's apparent sudden jump decomposes into continuous progress measures;
- a transformer learns a Fourier/trigonometric modular-addition algorithm;
- activations and weights support the reverse engineering;
- Fourier-space ablations validate the mechanism;
- training has phases: memorization, circuit formation, cleanup.

Surprise relative to emergence paper:

This is both positive and deflationary. It gives a real reduced mechanism, but it also shows that apparent emergence can be an artifact of observing only the final behavioral curve.

Action: **keep Level 1 as one of the best control papers.**

## Cluster-Level Findings

### A. Function vectors are the most coherent LLM-positive route

Papers 4, 9, 12, and 16 converge on compact vector/subspace mechanisms for ICL, relation knowledge, and multimodal relations. This is the strongest positive pattern for the emergence paper's compression/coarse-graining criterion.

Surprise: the function-vector route is now stronger than the induction-head-only route.

### B. Induction heads are developmental, not the whole ICL story

Papers 6, 10, 12, and 14 all refine the old induction-head story. The emerging view is:

- earlier circuits may enable separability or primitive matching;
- later heads/vectors align or transport task abstractions;
- induction and attention-sink transitions can be temporally distinct;
- induction heads may become or seed function-vector heads.

Surprise: the emergence paper should not treat "induction heads" as a single mechanism or single transition.

### C. World models are real in controlled games, but "world model" is not monolithic

Papers 3, 8, 13, 15, and 17 support internal state representations and causal interventions. But the evidence is mostly controlled games or synthetic spatial settings.

Surprise: the strongest world-model story is not "one coherent world model." It is shared latent bases, linear variables, rotations, and intervention-sensitive subspaces.

### D. Apparent emergence often becomes continuous after mechanistic inspection

Papers 6, 14, and 18 show that "phase transitions" or jumps can decompose into measurable internal progress. This strongly supports the emergence paper's skepticism about benchmark jumps, while also giving the paper's preferred mechanistic alternative.

### E. Broad emergent intelligence remains unsupported

Even the strongest Level 1 papers are domain-limited:

- controlled ICL tasks,
- synthetic logic,
- Othello/chess,
- modular addition,
- spatial relation datasets,
- constrained multimodal relation tasks.

They support **paper-defined emergent capabilities**, not broad emergent intelligence.

## Re-Segregation Recommendation

If we revise Level 1 after this audit, I would split it as follows.

### Level 1A - Highest Priority Positive Mechanistic Evidence

1. Function Vectors in Large Language Models
2. Which Attention Heads Matter for In-Context Learning?
3. Mechanistic Data Attribution
4. MetaOthello
5. Emergent World Models and Latent Variable Estimation in Chess-Playing Language Models
6. What Needs To Go Right For An Induction Head?

### Level 1B - Strong Provisional / Scoped Evidence

1. Emergent Structured Representations Support Flexible In-Context Inference
2. Multimodal Function Vectors for Visual Relations
3. Unifying Attention Heads and Task Vectors
4. When Do Attention Circuits Form?
5. Linear Spatial World Models
6. Emergent Linear Representations in World Models
7. Linear Latent World Models in Simple Transformers

### Level 1C - Important Controls / Limits / Calibration

1. Progress Measures for Grokking
2. Analogical Reasoning Inside LLMs
3. What One Cannot, Two Can
4. Revealing Algorithmic Deductive Circuits

## Bottom Line

The surprising result is not that all 18 are "verified." They are not.

The surprising result is that a subset of the Level 1 papers now forms a fairly coherent answer to the emergence paper:

> The credible version of LLM emergence is not sudden benchmark behavior or broad intelligence. It is the appearance and functional use of compact internal variables: function vectors, task vectors, concept vectors, board/spatial states, skill vectors, and circuit-development progress measures.

That means our final framing should become:

> **Some LLM and transformer systems show paper-defined emergent capabilities through compact causal internal structure. The evidence remains controlled-domain and mechanism-specific, and it does not establish broad emergent intelligence.**
