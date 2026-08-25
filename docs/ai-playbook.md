# Personal AI Coding Playbook

## 1. When I reach for AI first

- [ ] Task type: writing complex backend code like in module 2 when we created the backend using Copilot Chat in VS Code.
- [ ] Desired first-pass output: commented code explained in details
- [ ] Project context I can safely provide: source code and previous code

## 2. When I do not reach for AI

- [ ] Situation: what needs refactoring like in module 3.4
- [ ] Information involved: creative original ideas
- [ ] Preferred alternative: ask ai for a plan and review it 

## 3. My non-negotiables

- [ ] Boundary I will not cross: pasting ai answers without verifying them. For example in the frontend implementation, ai wasn't grasping the full artistic vibe I wanted to create. So I had to repeat the process multiple times and try to communicate my idea.
- [ ] Verification I require before use: review and test
- [ ] Record I will keep: documentations about ai's work and my own changes

## 4. My review rules

- [ ] Review step for code changes: read the diff and verify it meets the stated requirement. Creating tables to compare different prompts and outputs was very helpful. For instance, having 3 different architectures compared in module 5.
- [ ] Evidence I require for factual claims: documentation and clear easy explanation
- [ ] Condition for rejecting an output: it cannot be explained, verified, or safely scoped

## 5. What I am still figuring out

- [ ] Workflow decision to test: when AI assistance saves time without weakening understanding or inventing weird non-optimal solutions
- [ ] Signal that this is working: fewer avoidable mistakes and faster, confident reviews

AI-Assisted Coding - Module 5 Prompt Library
- For a new feature I reach for: planning, scaffolding, and test ideas using the chatbot in VS code
- For a code review I reach for: Claude
- For debugging I reach for: hypothesis generation and targeted diagnostic steps also using Claude
- For infrastructure I reach for: Codex
- I will never paste API keys for ai 
- My one rule is: use ai as a tool not a replacement for me.

I will re-read this document in 30 days.

## Decision Card

| Situation | My first move |
|---|---|
| New feature | Ask AI for a small plan, edge cases, and test ideas; I decide the product scope before code is written. |
| Code review | Ask for file-specific findings, then inspect the diff and label each finding useful, noise, or wrong. |
| Debugging | Use AI for hypotheses and focused diagnostic commands, then reproduce the issue before changing code. |
| Infrastructure | Use AI to explain CI/Docker options, then run the exact commands and inspect the resulting configuration. |
| Never paste | Credentials, API keys, `.env` values, private user data, or production logs. |

**One rule:** If I cannot explain a change and verify it with repository evidence, I do not submit it.
