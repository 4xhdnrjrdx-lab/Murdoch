# BUS363 A2 — Individual Project Plan (Content Draft)
**Project:** Murdoch Student LMS App v2.0 · **Budget:** A$500,000 fixed-price · **Duration:** 6 months
**Methodology:** Hybrid (predictive governance + agile delivery) · **Target:** Distinction
**Student:** Faiaz Dzhafarov (35553299) · BUS363 Scaling Agile Projects · Assessment 2

> Format = PowerPoint, management-level. Slides = concise headings + visuals/tables; detail lives in speaker notes.
> PMBOK 7th terminology is deliberately seeded throughout (rubric: PM Concepts = 10/35).

---

## Slide 1 — Title
- **Murdoch Student LMS App v2.0 — Individual Project Plan**
- Prepared by: Faiaz Dzhafarov (35553299) · BUS363 · Assessment 2
- Visual: clean cover (app/dashboard mock)

## Slide 2 — Background & Objectives
- **Context:** IT delivery company engaged to build v2.0 of the Murdoch Student LMS App. Fixed price A$500k, 6 months, requirements signed off.
- **Vision:** a fast, mobile-first app that gives students one place for timetable, grades, unit materials, notifications and submissions.
- **Goals (SMART-style):** ship v2.0 in 6 months within A$500k; ≥99.5% crash-free sessions; SSO with myMurdoch; ≥80% active-student adoption in 3 months.
- **Key deliverables:** iOS + Android app (cross-platform), integrations (Moodle/myMurdoch, timetable, grades, SSO), systems manual, 3-month hypercare.
- **Assumptions:** requirements frozen at kickoff; Murdoch provides API access + test data; one client product owner available.

## Slide 3 — Scope
- **In scope:** cross-platform app (iOS/Android); SSO; timetable, grades, materials, push notifications, offline read; integration to existing Murdoch systems; UAT; deployment; 3-month post-go-live support.
- **Out of scope:** changes to Moodle core/back-end; new academic content; staff training beyond admin handover; hardware procurement.
- **Constraints:** fixed price A$500k (triple-constraint: cost & scope fixed → schedule/quality managed); 6-month hard deadline; university data-privacy & security policy.
- **Scope baseline:** scope statement + WBS + schedule (100% rule — all work captured, nothing extra).

## Slide 4 — Project Approach & Governance
- **Hybrid approach:** *predictive* outer shell (stage gates, fixed milestones, milestone billing) + *agile* delivery core (2-week sprints, product backlog, MoSCoW prioritisation) inside the Build phase. Justification: fixed-price/fixed-scope needs predictive control; software build benefits from iterative feedback.
- **Org chart (governance):**
  - **Project Board** (sponsor level): Murdoch IT Sponsor (Director) + Vendor Director
  - **Oversight / assurance:** Delivery assurance + Technical assurance
  - **Project Management:** Client-side PM + Vendor PM
  - **Delivery groups:** Technical (Tech Lead, Senior/Devs, QA) · Additional resource (BA, Solution Architect, UX Designer, Infrastructure, Test Lead) · Adoption & Change (BA, Training)

## Slide 5 — Project Lifecycle (phases)
Chevron banner, 6 phases:
1. **Initiation** (M1)
2. **Discovery & Design** (M1–M2)
3. **Iterative Development** — agile sprints (M2–M5)
4. **UAT** (M4–M5)
5. **Deployment & Go-live** (M5–M6)
6. **Hypercare & Close** (M6)

## Slide 6 — Requirements (Analysis & Design)
- **Functional:** SSO login; view timetable; view grades; access unit materials (offline); push notifications; submit/track assignments.
- **Non-functional:** performance (<2s screen load); availability 99.5%; security (Murdoch data-privacy, encryption); accessibility (WCAG 2.1 AA); scalability to peak enrolment.
- **Visual design:** Murdoch-branded UI kit; mobile-first; usability testing with student cohort.

## Slide 7 — Key Deliverables & Acceptance Criteria (table)
| Phase | Deliverable | Acceptance criteria |
|---|---|---|
| Initiation | Project charter & plan | Board sign-off |
| Discovery & Design | UX/UI designs + solution architecture | Product Owner sign-off; architecture review passed |
| Development | App increments (per sprint) | Definition of Done; passes automated tests; demo accepted at sprint review |
| UAT | Tested release candidate | All severity-1/2 defects closed; UAT sign-off |
| Deployment | Production release (iOS/Android stores) + Systems Manual | Go-live sign-off; Systems Manual incl. component inventory, install/config, release notes, backup & DR plan |
| Close | Handover + closure report | Client sign-off; support handover accepted |

## Slide 8 — Work Breakdown Structure (WBS)
Workstreams (level-2):
1. Project Management & Governance
2. Discovery & Design
3. Development — Frontend / Backend / Integration
4. Quality Assurance & UAT
5. Infrastructure & Deployment
6. Data & Migration
7. Training & Adoption
8. Support (Hypercare)
*(100% rule: all in-scope work mapped to a workstream; nothing outside the baseline.)*

## Slide 9 — Timeline / Gantt (6 months)
| Workstream | M1 | M2 | M3 | M4 | M5 | M6 |
|---|---|---|---|---|---|---|
| Initiation | ▓ | | | | | |
| Discovery & Design | ▓ | ▓ | | | | |
| Iterative Development (Sprints 1–6) | | ▓ | ▓ | ▓ | ▓ | |
| UAT | | | | ▓ | ▓ | |
| Infrastructure & Deployment | | | | | ▓ | ▓ |
| Data & Migration | | | ▓ | ▓ | ▓ | |
| Training & Adoption | | | | | ▓ | ▓ |
| Hypercare & Support | | | | | | ▓ |
**Milestones:** ◆ Kick-off (M1) · ◆ Design sign-off (end M2) · ◆ Sprint reviews (M2–M5) · ◆ Feature complete (M5) · ◆ UAT sign-off (M5) · ◆ Go-live (M6) · ◆ Project close (end M6)

## Slide 10 — Billing Schedule (milestone-based, A$500k fixed)
| Milestone | Trigger | Payment | Amount |
|---|---|---|---|
| 1. Kick-off | Contract signed, project initiated | 25% | A$125,000 |
| 2. Go-live | Deployed to production (stores live) | 50% | A$250,000 |
| 3. Closure | Hypercare complete + client sign-off | 25% | A$125,000 |
| **Total** | | **100%** | **A$500,000** |
*Commercial basis: fixed price. ~10% management reserve held inside the fee for contingency.*

## Slide 11 — Team & Resources
- **Core team (~9 FTE):** Vendor PM, Solution Architect, BA, UX Designer, Tech Lead, 2× Developers, QA/Test Lead, DevOps/Infra.
- **Client side:** Product Owner, IT/security liaison, student test group.
- Resource histogram: peak staffing during Development (M2–M5).

## Slide 12 — Risk & Issue Management
**Risk matrix (Likelihood × Consequence, 1–5):**
| # | Risk | L | C | Score | Response (strategy) |
|---|---|---|---|---|---|
| R1 | Legacy integration harder than expected | 4 | 5 | 20 (High) | **Mitigate** — integration spike/PoC in Discovery; dedicated integration BA |
| R2 | Scope creep despite sign-off | 3 | 4 | 12 (High) | **Mitigate** — change-control process; locked scope baseline |
| R3 | Fixed-price cost overrun | 3 | 5 | 15 (High) | **Mitigate** — EAC/ETC tracking; 10% reserve; MoSCoW de-scope of "could-haves" |
| R4 | Key resource unavailable | 3 | 3 | 9 (Med) | **Mitigate** — cross-skilling; named backups |
| R5 | UAT delays / low tester availability | 3 | 3 | 9 (Med) | **Mitigate** — book UAT windows early; student tester pool |
| R6 | App-store approval delay | 2 | 3 | 6 (Med) | **Transfer/Accept** — submit early; follow store guidelines |
- **Issue log (example):** ID · description · raised-by · severity · owner · status · resolution date.
- 5 responses available: Mitigate / Avoid / Transfer / Accept / Escalate.

## Slide 13 — Stakeholder Management
**Power–Interest grid (Mendelow):**
- **Manage closely** (high power/high interest): Project Board / Sponsor; Product Owner
- **Keep satisfied** (high power/low interest): University Executive; Finance
- **Keep informed** (low power/high interest): Students (end users); Lecturers; Help Desk; Library
- **Monitor** (low/low): other departments
**Communication plan:** weekly RAG status → PM/Board; fortnightly sprint review → stakeholders; monthly steering committee; go-live comms campaign → students.

## Slide 14 — Monitoring & Control
- **Schedule/scope:** weekly RAG status board; fortnightly sprint burndown + sprint reviews; milestone tracking.
- **Commercial control (EVM-style table):**
| Field | Value |
|---|---|
| Commercial basis | Fixed price |
| Budget at Complete (BAC) | A$500k |
| Actual cost to date | A$40k |
| Percent complete | 8% |
| Estimate to Complete (ETC) | A$460k |
| Estimate at Complete (EAC) | A$500k |
| Budget variance | A$0 |
| Forecast finish | Month 6 |
- **Change control:** all change requests logged, impact-assessed against the baseline, Board-approved.

## Slide 15 — Success Factors & Closure
- **Success factors:** stakeholder alignment & sponsor engagement; early de-risking of integration; disciplined change control; agile prioritisation (MoSCoW); continuous UAT; clear governance & reporting.
- **Closure:** client sign-off; handover to support/BAU; final reports + lessons learned; system closure; final invoice (milestone 3).

## Slide 16 — References (Chicago)
- Project Management Institute. 2021. *A Guide to the Project Management Body of Knowledge (PMBOK Guide)*. 7th ed. Newtown Square, PA: PMI.
- Project Management Institute. 2017. *Agile Practice Guide*. Newtown Square, PA: PMI.
- (+ 1–2 supporting sources if needed, e.g. Mendelow stakeholder model, MoSCoW prioritisation.)
