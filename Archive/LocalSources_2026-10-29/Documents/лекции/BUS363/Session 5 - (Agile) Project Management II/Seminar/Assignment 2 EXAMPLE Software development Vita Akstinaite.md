# Assignment 2 EXAMPLE — Software Development Project (Dr. Vita Akstinaite) — Content Dump

Source: BUS363 Moodle resource — "Assignment 2 EXAMPLE: Software development project", slide deck by Dr. Vita Akstinaite (delivered as `Assignment_2_EXAMPLE_Software_development_Vita_Akstinaite.pdf`, uploaded from Moodle). 17 slides. This is the worked example/template the lecturer provides to show what an A2 Individual Project Plan can look like — most slides contain placeholder prompts (what _you_ should write) plus a few filled-in example artefacts.

> Note: "VA:" markers in the deck are the lecturer's own annotations/instructions to students. They are kept verbatim below because they tell you how she expects the section to be used.

---

## Slide 1 — Title (decorative)

"Software development project — EXAMPLE — Dr. Vita Akstinaite". Cover slide with a dashboard/analytics screenshot. No substantive content.

---

## Slide 2 — Background & Assumptions

Placeholder prompts for the student to complete:

- Describe your Project Background here.
- List your project Assumptions.

---

## Slide 3 — Overall Project Approach

Lecturer annotation (verbatim):

> (VA: in the next few slides please explain your project approach; the one in the example does not necessarily means that it works for your project!)

So the following approach slides are illustrative only — you are expected to adapt or replace the approach to fit your own project.

---

## Slide 4 — Example of a Project Approach (phase diagram)

A left-to-right linear phase/stage diagram showing six sequential stages (chevron/arrow style banner):

1. **INITIATION**
2. **ANALYSIS & DESIGN**
3. **LAUNCH / RELEASE**
4. **DELIVERY**
5. **SUPPORT**
6. **CLOSE**

This is the high-level lifecycle that structures the rest of the deck (each later slide drills into one of these stages).

---

## Slide 5 — INITIATION (project organisation chart)

This slide presents the **project governance / team structure** as an organisation chart. The "INITIATION" stage is highlighted in the phase banner at the top; the remaining phases are shown greyed/dashed (not yet active).

The org chart boxes and their members (TBC = "to be confirmed"):

**Oversight**

- Vita Akstinaite (Delivery)
- TBC (Technical)

**Project Board** (top of hierarchy)

- Simon Peters (Director)
- TBC (Company/Client)

**Project Management** (reports up to the Board; Oversight feeds in)

- TBC (client)
- TBC (service provider)

Reporting/feeding **into** Project Management, three branches sit below it:

**Additional resource**

- BA (Business Analyst)
- Architect
- Designer
- Infrastructure
- Testing Lead
- Support

**Technical**

- Technical Lead
- Lead/Senior Developer(s)
- Developer(s)
- Consultant(s)
- Tester(s)/QA(s)

**Adoption and change**

- BA (Business Analyst)

Structure in words: a **Project Board** (sponsor/director level) sits at the top; **Oversight** provides delivery + technical assurance to the side; **Project Management** sits beneath the Board and coordinates three delivery groups — _Additional resource_, _Technical_, and _Adoption and change_.

---

## Slide 6 — ANALYSIS & DESIGN

Placeholder prompts. Explain your requirements here:

- **Functional requirements** (i.e., hardware, software).
- **Non-functional requirements** (i.e., user experience).
- **Visual design** (i.e., how the app is going to look like?).

---

## Slide 7 — Deliverables (Example)

A three-column table: **Stage/Schedule | Deliverable | Acceptance criteria**. One worked example row is filled in:

| Stage/Schedule                           | Deliverable        | Acceptance criteria                                                                                                                                                                                                                                                                                                                                                                                                 |
| ---------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Test, Deploy & Extended Support Services | **Systems Manual** | The systems manual is a comprehensive document that describes in detail the information and activities required to ensure the system can be supported and managed on an ongoing basis. The systems manual must include: (1) inventory of system components; (2) installation instructions; (3) configuration documentation; (4) interface and batch jobs; (5) release notes; (6) backup and disaster recovery plan. |

Student prompt on the slide (verbatim intent): _Summarise here what are you going to deliver? The app itself, probably some support for the app too? What about Help Desk? Additional services?_

---

## Slide 8 — DELIVERY (iterative cycle)

Stated focus areas for the Delivery stage:

- Iterations
- Product backlog
- Reviews
- Testing

Accompanying **iterative development cycle diagram** (circular/looping process). The labelled steps around the cycle:

- Requirements
- Planning
- Analysis
- Design
- Implementation
- Testing
- Deployment

This represents repeating Agile iterations rather than a single linear pass — each iteration runs requirements → planning → analysis → design → implementation → testing → deployment, then loops.

---

## Slide 9 — Proposed timeline (Gantt chart)

Lecturer annotation (verbatim): _Example of how your plan could look like — change to what works for your plan and list all your activities._

A **Gantt-style schedule**. Columns are months **May'19 → Nov'19** (May, Jun, Jul, Aug, Sep, Oct, Nov). Rows are workstreams, with labelled activity bars placed in the month cells:

| Workstream                | Scheduled activity (and rough month placement)                         |
| ------------------------- | ---------------------------------------------------------------------- |
| **Initiation**            | (start of project, May)                                                |
| **Analysis and Design**   | "Discover" — May/Jun                                                   |
| **Iterative development** | "Deliver: Development Iteration Cycles" — long bar spanning ~Jun → Oct |
| **UAT**                   | "Test" — ~Sep                                                          |
| **Infrastructure**        | "Set Up" (~Sep/Oct) → "Deploy" (~Oct/Nov)                              |
| **Migration**             | "Strategy" (~Jul) → "Prepare" (~Jul–Oct) → "Migrate" (~Oct/Nov)        |
| **Training**              | "Basic" (~Oct) → "Advanced" (~Oct/Nov)                                 |
| **Support (TBA)**         | (to be advised)                                                        |

**Milestones** (pink dots along the bottom timeline):

- **Kick-off** (early, ~May/Jun)
- **Reviews** — a series of review milestones bracketed across the middle of the project (~Jun → Oct)
- **Go live sign-off** (end, ~Nov)

---

## Slide 10 — Billing

Student prompt (verbatim intent): _Explain here how you are going to charge your client, when and what sums._

Two tables.

**Table 1 — Activity vs Cost / Billing milestone:**

| Activity               | Cost / Billing milestone                                     |
| ---------------------- | ------------------------------------------------------------ |
| Initiation             | **$300,000 (to be split accordingly)** across all activities |
| Discovery and Design   | (part of the $300,000)                                       |
| Development iterations | (part of the $300,000)                                       |
| Testing (UAT)          | (part of the $300,000)                                       |
| Training               | (part of the $300,000)                                       |
| Support                | (part of the $300,000)                                       |
| Enhancements           | (part of the $300,000)                                       |

**Table 2 — Payment schedule (% of total):**

| Activity                           | Cost / Billing milestone |
| ---------------------------------- | ------------------------ |
| Project kick off (payment upfront) | **25 %**                 |
| Deploying to UAT/Production        | **50 %**                 |
| Project Closure                    | **25 %**                 |

---

## Slide 11 — Monitor: Project Status

Student prompt (verbatim intent): _Explain how you are monitoring the progress visually!_

A **weekly status-tracking board** (RAG-style). Columns are calendar weeks across **Jun, July, Aug, Sep** (week-ending dates: Jun 12/19/26; Jul 02/09/16/23; Aug 02/09/16/23/30; Sep 06/13/20/27). Each row is an activity with a status colour, an owner (Responsibility), and milestone dates.

**Legend / status keys used:** Ready to go / In progress · At Risk · On hold · plus markers for **Kick-off**, **Weekly meetings**, **Milestones**, **Achieved**, and stage markers **UAT**, **Deploy**, **Go live**.

**Activities and owners (Responsibility column):**

- Finalise documentation — _Laura_
- Acute flags (LTC) – confirm/customise
- Testing
- Build GP data load process for EMIS — (key events / go-live, kick-off noted)
- Receive pseudonymised EMIS data
- Hammersmith data
- Develop LTC/QoF process (SystemOne) — _Matt_ (26.01 / 04.02)
- EMIS/System One integration — TBC
- Build referrals data
- Build A&E data feed
- Build Social Care data feed
- Costing for Primary Care & Social Care — _Matt_
- Amending costing algorithms for MH, CIDS, SUS data feeds — _Matt_
- Reporting tables — TBC
- Adding security layers for Tableau views — TBC
- Environments set up (TBC) — TBC
- Deploy + Data load at SECSU — _Laura_ (30.03 / 20.03)
- Population segmentation — _Matt_ (20.02)
- Load received System One data — (04.02 / 19.02)
- Build incremental load process for SystmOne — TBC
- Showing Dr Tahir's data — TBC (24.02)
- Reporting / sign-off owners — _Simon_ (several rows TBC)

(The exact cell-by-cell colour coding isn't fully recoverable from the export; the point of the slide is the _format_ — a colour-coded weekly grid mapping activities × weeks, with owners and milestone dates, and stage bands for UAT / Deploy / Go live.)

---

## Slide 12 — Commercial control (financial tracking)

Student prompt (verbatim intent): _Explain how you are tracking your costs._

A **financials tracking table** grouped under three headings — **Budget | Actuals To Date | Forecasts**:

| Field                     | Value           |
| ------------------------- | --------------- |
| Commercial Basis          | **Fixed price** |
| Budget at Complete ($k)   | 300.00          |
| Actual Cost ($k)          | 20.0            |
| Percent Complete          | 7%              |
| Estimate To Complete ($k) | 280.00          |
| Estimate At Complete ($k) | 300.00          |
| Budget Variance ($k)      | 0.00            |
| Forecast Finish Date      | 15/11/19        |

In words: a fixed-price engagement budgeted at $300k; $20k spent to date (7% complete); $280k estimated still to spend; estimate at completion still $300k, so zero budget variance; forecast finish 15 Nov 2019.

---

## Slide 13 — LAUNCH / RELEASE

Placeholder prompt:

- Explain how you are going to Launch your app? Will you provide any training or post-launch support?

---

## Slide 14 — SUPPORT

Placeholder prompts:

- Do you support go-live and post go-live issues?
- Hosting environments?
- Support — 1st, 2nd, 3rd line?
- Operational improvements.
- Additions to the app.

---

## Slide 15 — CLOSE

Prompt: _What will be the process of closing your project?_

- Client sign off.
- Handover to support (if agreed).
- Final reports, closure in systems.
- Final invoicing / Finance team.

---

## Slide 16 — Ensuring project success

Prompt: _List here your project success factors. What will make this project work?_ Example factors given:

- Ensuring involvement and alignment from all stakeholders.
- Timely feedback.
- Relevant workshops / meetings / reviews.
- Monitoring risks.
- Process for dealing with change.

---

## Slide 17 — Anything else you want to add about your project

- ☺ (placeholder / open slot for any additional content).

---

## Key terms & references

**Lifecycle / stages (this deck's approach):** Initiation → Analysis & Design → Launch / Release → Delivery → Support → Close.

**Governance roles:** Project Board (Director, Company/Client), Oversight (Delivery + Technical assurance), Project Management (client-side + service-provider PM), Technical team (Technical Lead, Lead/Senior Developers, Developers, Consultants, Testers/QA), Additional resource (BA, Architect, Designer, Infrastructure, Testing Lead, Support), Adoption and change (BA).

**Agile / delivery concepts:** Iterations, Product backlog, Reviews, Testing; iterative cycle = Requirements → Planning → Analysis → Design → Implementation → Testing → Deployment (looped). UAT (User Acceptance Testing). Go live / Go-live sign-off.

**Planning & control artefacts modelled in the deck:**

- Project organisation chart (Slide 5).
- Requirements split: functional / non-functional / visual design (Slide 6).
- Deliverables table with acceptance criteria (Slide 7), e.g. Systems Manual.
- Gantt-style timeline with workstreams + milestones (Slide 9).
- Billing model: total fee + milestone-based payment schedule (25% kick-off / 50% deploy / 25% closure) (Slide 10).
- Visual status board (RAG, weekly, owner-assigned) for progress monitoring (Slide 11).
- Commercial control table: Budget / Actuals / Forecast, with Percent Complete, ETC, EAC and Budget Variance (Slide 12).

**Systems Manual must include (acceptance criteria, Slide 7):** inventory of system components; installation instructions; configuration documentation; interface and batch jobs; release notes; backup and disaster recovery plan.

**Support tiers referenced:** 1st / 2nd / 3rd line support; hosting environments; operational improvements (Slide 14).

**Closure checklist (Slide 15):** client sign-off; handover to support; final reports + system closure; final invoicing.

**Success factors (Slide 16):** stakeholder alignment; timely feedback; workshops/reviews; risk monitoring; change-management process.

**Named example data sources (Slide 11, from the worked NHS-style example):** EMIS, SystmOne / System One, Tableau, SECSU, plus data feeds for referrals, A&E, Social Care, SUS, MH, CIDS — included only as realistic placeholders in the example.

---

## Relevance to BUS363

This is **the most directly A2-relevant artefact in the whole course** — it is the lecturer's own worked example of an **Individual Project Plan (A2, 35%)**, so it effectively previews the structure she rewards.

- **Project Plan Design (15%):** The deck is a ready-made section map for your plan — Background & Assumptions, Approach/lifecycle, Governance/org chart, Requirements (functional/non-functional/visual), Deliverables + acceptance criteria, Timeline (Gantt), Billing, Status monitoring, Commercial control, Launch, Support, Close, Success factors. Mirroring these sections is a safe scaffold; the placeholder prompts on each slide are essentially the marking checklist of _what to include_.
- **Integration of PM Concepts (20%):** The example shows where to plug in PMBOK/Agile concepts — governance & roles (PMBOK stakeholder/resource management), iterative delivery & product backlog (Agile Practice Guide), milestone-based billing and EAC/ETC/variance tracking (cost management & EVM-style control), RAG status monitoring (performance domains/measurement in PMBOK 7th), and explicit risk/change processes. Naming these frameworks against each slide is exactly the "integration" the rubric asks for.
- **Caveat the lecturer flags herself:** the approach shown is _one_ example (her "VA:" notes stress it may not fit your project). For your own A2, you're expected to adapt the lifecycle and tailor each section to your chosen software/app project, not copy this NHS-style delivery example.
- Lower relevance to A1/A3/A4, though the governance, success-factors and risk/change-process material is reusable supporting context anywhere a plan or scaling argument needs structure.
