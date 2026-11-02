# Academia MVP specification

## Purpose and principles

Support independent recall across multiple classes with a fully offline core. AI may help prepare drafts and, later, evaluate an already submitted attempt. It must never be the primary answer source during retrieval. Every generated question needs human review before entering the trusted bank; review includes the answer, source, wording, and hints.

## Phase 1 — Retrieval MVP (implemented)

- Course creation and listing; separate banks and histories keyed by course ID.
- Flexible topics and question kinds: recall, proof, derivation, debugging, or transfer can use the same text-based format.
- Manual authoring and JSON import with origin attribution, source references, and optional hints.
- Pending → trusted or rejected review workflow; only trusted questions are studied. New IDs preserve earlier questions and attempt snapshots.
- Course/topic selection, optional shuffle, and session size limits.
- Attempt → confidence → answer reveal → self-assessed correctness and difficulty → persisted history. Hints are explicit and counted.
- Local SQLite persistence and JSON history export. No runtime dependencies or AI calls.
- Basic descriptive accuracy, confidence calibration, and hint-use summaries.

Acceptance criteria: one class cannot receive another's questions or attempts; importing a claimed approval cannot bypass review; an answer is hidden until an attempt and confidence are entered; completed attempts survive restart; malformed imports do not partially commit; re-running the legacy migration does not duplicate cards. Automated tests cover these paths.

Current limits: single local user, one-line responses, manual grading, no question editor, no automatic PDF extraction, and no scheduling. Difficulty is recorded but does not yet change a queue. Source references are human-verifiable text, not automatically verified citations. Legacy cards also require review because their provenance does not establish correctness.

## Phase 2 — Memory scheduling

Add per-course concept identifiers, due dates, spaced repetition, review queues, and overdue concepts. Use difficulty and retrieval outcomes to update intervals; distinguish assisted success from independent success. Make the scheduling rule inspectable, test it with a controllable clock, and preserve all historical attempts. Provide explicit migrations for future database changes.

## Phase 3 — Reasoning and transfer

Add multiline proof/code/derivation responses, grading rubrics, links between source questions and new variations, and misconception tracking. Mark a transfer item as previously unseen and record its relationship to the original concept; a simple `kind=transfer` label alone does not establish measured transfer.

## Phase 4 — Intelligent assistance

Optional lecture-note/PDF ingestion produces drafts with source locations and generator provenance. Human review remains mandatory. Offer optional answer feedback and tutoring only after the learner's attempt is submitted. Preserve the original response, separate AI feedback from human assessment, obtain consent before sending course material to a provider, and retain offline functionality when no provider is configured.

## Phase 5 — Research analytics

Measure delayed unaided recall at target delays of 1, 3, 7, and 14 days. Record actual elapsed delays and anchor each probe to its study exposure; repeated practice between exposure and probe is a confound to record. Report counts and missing probes alongside accuracy.

Track confidence before feedback, calibration by confidence band, hint dependence, and performance on novel transfer items. Separate assisted from unaided outcomes and distinguish self-assessment from externally evaluated correctness.

For exploratory within-person experiments, assign comparable material to rereading, retrieval, and interleaved retrieval conditions. Counterbalance conditions and order across material sets, hold exposure time and delayed tests comparable, and log intervening study. Store experiment ID, condition, assignment order, material set, exposure, actual delay, and evaluation method. Analyze within-person differences with uncertainty and disclose small samples, material differences, grading bias, and carryover effects. Current aggregate CLI stats do not implement these experiments or establish causality.

## Delivery sequence

Stabilize Phase 1 with actual courses before implementing scheduling. Add richer reasoning workflows next, optional AI after the independent practice loop works, and experiment analytics after exposure and assessment data can support valid comparisons.
