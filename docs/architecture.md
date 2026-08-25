# Architecture-document context strategy comparison

## Strategy comparison

| Strategy | What it got right | What it got wrong, missed, or invented | Best suited task shape |
|---|---|---|---|
| A — minimal context | Produces a complete architecture narrative: system purpose, data model, create flow, key files, validation, storage, error handling, and frontend behavior. It also explicitly distinguishes source-based statements from unexecuted runtime behavior and flags the timestamp-timezone ambiguity. | It is highly detailed despite minimal context, including drag-and-drop optimistic updates, a specific frontend integration test file, and several “not present” claims. Those details may be correct, but the draft does not show enough internal evidence to separate verified facts from inferred coverage. | A small, well-bounded documentation task where a concise architecture overview is needed and the model can safely work from a compact prompt. |
| B — structured context | Gives the most balanced, implementation-oriented description. It captures partial-update/null behavior, storage semantics, defaults, status transitions, and the frontend/API lifecycle without omitting the main architecture layers. | It makes several especially specific claims that need support: `POST http://localhost:8000/tasks`, CORS allowing credentials, a multi-stage Docker build, README coverage of CI, and the frontend hard-coding that URL. It also groups “not implemented” and “not exposed” together, which weakens the distinction between absence and route-level visibility. | A repository-wide architecture document that needs broad coverage across application code, frontend, operational files, and documented constraints. |
| C — targeted anchor files | Is the most disciplined about scope. It clearly labels what was not visible, gives a precise API-to-storage create flow, and avoids claiming frontend or business-rule behavior it did not inspect. | It misses useful architecture information that the other drafts provide, especially the status-transition rules, frontend request/render behavior, Docker/runtime context, tests, and dependencies. Its repeated “not visible” statements make the document less useful as a repository architecture reference. | A narrow, evidence-sensitive task focused on a few anchor files—for example, documenting an API boundary or reviewing a specific subsystem without making repository-wide claims. |

## Verdict

I chose Strategy B as the basis for the final architecture document because it has the strongest repository-wide coverage while still organizing the result around concrete components and behaviors. Before merging it, I would remove or verify its unusually specific operational claims—especially the hard-coded frontend URL, CORS credentials, Docker build structure, and CI reference—and preserve C’s habit of marking unseen behavior as unconfirmed.

## Context-engineering rule

For task shape “repository-wide architecture documentation,” I use structured context (Strategy B) because it connects the API, models, storage, frontend, runtime files, and documented constraints into one coherent description.

For task shape “a bounded subsystem or anchor-file review,” I use targeted context (Strategy C) because it keeps conclusions tied to the files actually examined and makes coverage gaps explicit.
