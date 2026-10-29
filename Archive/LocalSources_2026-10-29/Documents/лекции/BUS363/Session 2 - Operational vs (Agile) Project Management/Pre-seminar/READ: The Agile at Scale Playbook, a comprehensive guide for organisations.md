READ: The Agile at Scale Playbook, a comprehensive guide for organisations File
This playbook aims to guide organizations in successfully implementing agile methodologies at scale. By taking a deep dive into the principles, frameworks, roles and responsibilities of agile, to provide a roadmap for scaling agile within an organization.

Agile at Scale is the application of agile methodologies across an organization or on large projects involving multiple teams. It is an approach that promotes flexibility, customer collaboration, rapid delivery, and continuous improvement, applied at a larger scale than base agile implementations like Scrum and Kanban.

---

# The Agile at Scale Playbook (Tempo) — Content Dump

**Source:** _The Agile at Scale Playbook — A comprehensive guide for large organizations_, published by Tempo (Tempo.io). PDF, 74 pages, 11 chapters. Vendor-authored guide (Tempo makes Timesheets, Structure, Roadmunk, Planner, Cost Tracker, Custom Charts; partners with LiquidPlanner).

> Note: this is a copyrighted commercial PDF, so the content below is paraphrased in my own words. All frameworks, roles, models, tables, figures, and factual claims from the source are retained. Decorative chapter-cover pages are skipped.

---

## I. Introduction

**Definition — Agile at Scale:** applying agile methodologies across an entire organization or on large projects involving multiple teams. It extends agile's core ideas — flexibility, customer collaboration, rapid delivery, continuous improvement — to a level beyond base single-team implementations like Scrum and Kanban.

### Benefits of Agile at Scale

- **Efficiency** — applying proven agile methods at portfolio level produces faster development/deployment cycles and quicker time-to-market.
- **Collaboration** — forces cross-functional collaboration across teams/departments; diverse perspectives improve innovation and problem-solving.
- **Responsiveness to change** — makes large orgs more adaptable; iterative approaches at the strategic level allow adjustments to shifts in customer preferences, market dynamics, and competition.
- **Quality and customer satisfaction** — maximizes customer focus; connecting strategy to agile customer-centricity improves product quality and satisfaction.
- **Visibility and predictability** — supplies reporting/visibility at all org levels to drive action and maximize value throughput; transparency improves predictability and decision-making.

### Challenges of Agile at Scale

- **Maintaining consistency** — scaling across many teams can create inconsistencies without a robust framework and clear communication.
- **Coordinating multiple teams** — managing dependencies and coordinating work across teams is complex; early visibility into dependency impact plus layered coordination strategies help avoid bottlenecks/misalignments.
- **Culture and adoption** — moving to Agile at Scale is a significant cultural change; rigid "shock" transformations breed resistance. (Tempo positions itself as starting "where your teams are.")
- **Providing flexibility and control** — orgs must manage at the strategic level without diminishing team-level agility; agile reporting systems need more team-level adaptability than traditional top-down systems.
- **Skills and training** — requires both understanding agile principles and the skills to apply them at scale; pulls in leadership and non-engineering areas unfamiliar with agile, creating high demand for executive-level coaching and resources beyond engineering (agile's traditional domain).

**Closing claim:** with strong leadership, the right tools, and commitment to agile principles at all levels, Agile at Scale can improve an org's ability to deliver value and attract top talent while reducing costs.

---

## II. Agile principles and practices

### Key agile principles (the four Agile Manifesto values)

1. **Individuals and interactions over processes and tools** — communication, collaboration, and team dynamics are essential for success.
2. **Working software over comprehensive documentation** — deliver a working product; documentation matters but shouldn't impede development.
3. **Customer collaboration over contract negotiation** — keep the customer engaged throughout; welcome input and adapt to feedback rather than relying only on up-front contract terms.
4. **Responding to change over following a plan** — changes are inevitable; agile teams respond even late in development to adapt to evolving business realities and customer needs.

### Additional Manifesto principles (the Manifesto also has 12 principles; examples cited)

- Deliver valuable software frequently, preferring shorter timescales.
- Welcome changing requirements, even late in development (change as competitive advantage).
- Work at a sustainable pace that developers, sponsors, and users can maintain indefinitely.
- Reflect at regular intervals on how to be more effective and adjust behavior.

### Agile frameworks (single-team / base frameworks)

1. **Scrum** — for managing complex software/product development using fixed-length iterations (sprints, usually 2–4 weeks). Key elements:
   - _Product backlog_ — ordered list of features/enhancements/fixes, maintained by the Product Owner.
   - _Sprint planning_ — start-of-sprint meeting where the team selects backlog items.
   - _Daily Scrum / standup_ — brief daily sync on progress and blockers.
   - _Sprint review_ — end-of-sprint demo of completed work.
   - _Sprint retrospective_ — post-review reflection to identify improvements.
   - Roles: **Product Owner** (represents customer, prioritizes), **Scrum Master** (facilitates process, helps team improve), **Development Team** (does the work).
2. **Kanban** — lean method emphasizing visualizing workflow, limiting work-in-progress (WiP), and optimizing flow. Uses a Kanban board with work-item cards moving left-to-right through stages. Limiting WiP focuses teams on finishing before starting. Unlike Scrum, prescribes no roles or iterations; can be standalone or combined with other frameworks.
3. **Extreme Programming (XP)** — software-focused, emphasizing collaboration and customer satisfaction. Key practices:
   - _Pair programming_ — two programmers at one workstation (one codes, one reviews).
   - _Test-driven development (TDD)_ — tests written before code.
   - _Continuous integration_ — frequent integration/testing to catch issues early.
   - _Refactoring_ — regular code cleanup for quality/simplicity.
   - _On-site customer_ — an end-user representative embedded in the team for rapid feedback.
4. **Lean Software Development** — based on lean manufacturing. Principles: eliminate waste, amplify learning, decide as late as possible, deliver as fast as possible, empower the team, build quality in, optimize the whole.
5. **Dynamic Systems Development Method (DSDM)** — prioritizes scope and functionality across the lifecycle. Principles: focus on the business need, deliver on time, collaborate, never compromise quality, build incrementally, communicate continuously and clearly.

> The right framework depends on context: nature of the work, the team's skills/preferences, and organizational culture.

### Agile roles and responsibilities (within a Scrum team)

- **Product Owner (PO)** — maximizes product value and the team's work; represents business/users; defines and prioritizes the product backlog. Responsibilities: clearly express backlog items; order items to best achieve goals; keep backlog visible/transparent/clear and show what's next; ensure the dev team understands items to the level needed.
- **Scrum Master** — servant-leader for the team; helps everyone understand Scrum theory/practices/rules/values; facilitates events; removes impediments; coaches toward maturity. Responsibilities: guide team/org on agile/Scrum use; facilitate discussion, decision-making, conflict resolution; assist internal/external communication and transparency; support/educate the PO (backlog grooming/maintenance).
- **Development Team** — self-organizing, cross-functional professionals delivering a potentially releasable increment each sprint. Responsibilities: deliver the increment; determine technical means/methods; manage own work and report at daily standup; collaborate with the PO to clarify/refine backlog items.

> These roles are Scrum-context definitions; other agile methodologies may name/assign them differently, but all distinguish the role that represents the business (like PO), the role that facilitates the process (like Scrum Master), and the role that does the work (Development Team).

---

## III. Scaling agile principles (Agile-at-Scale frameworks)

### Overview of the main Agile-at-Scale frameworks

1. **Scaled Agile Framework (SAFe)** — knowledge base of integrated lean/agile/DevOps practices at scale; promotes alignment, collaboration, delivery across many teams. **Four levels: Team, Program, Large Solution, Portfolio.**
2. **Large-Scale Scrum (LeSS)** — scales Scrum to multiple teams on the same product, building directly on Scrum while keeping its simplicity/flexibility. Two variants: **Basic LeSS (up to 8 teams)** and **LeSS Huge (8+ teams)**.
3. **Nexus** — developed by **Ken Schwaber** (co-creator of Scrum); scales Scrum so multiple Scrum teams work together to deliver working software every sprint. Uses the same Scrum roles/events/artifacts plus new ones to manage cross-team dependencies/interactions.
4. **Scrum at Scale (Scrum@Scale)** — created by **Jeff Sutherland** (a Scrum co-creator); scales across the whole organization (not just dev teams). Lightweight; extends fundamental Scrum to coordinate multiple teams across divisions/departments.
5. **Disciplined Agile Delivery (DAD)** — process-decision framework for simplified decisions around incremental/iterative delivery; builds on Scrum, agile modeling, XP, and others; offers context-sensitive guidance to streamline processes.

> Choice depends on org size/structure, nature of the work, and culture/goals.

### Comparison of Agile-at-Scale frameworks (page-17 table, reconstructed)

Legend: **●** = Defined and prescribed · **◐** = Defined with recommendations · **○** = Not clearly defined. Where a cell names a construct instead of a status, the name is shown.

| Process / aspect                     | SAFe                      | LeSS (Large Scale Scrum & LeSS Huge) | Spotify | Scrum@Scale     | DAD (Disciplined Agile Delivery) |
| ------------------------------------ | ------------------------- | ------------------------------------ | ------- | --------------- | -------------------------------- |
| Long-term planning & strategy        | ●                         | ●                                    | ●       | ●               | ◐                                |
| Multi agile teams                    | ●                         | ●                                    | ●       | ●               | ◐                                |
| Team of Teams                        | Agile Release Train (ART) | Area                                 | Tribes  | Scrum of Scrums | ◐                                |
| PM / PO                              | ●                         | ●                                    | ●       | ●               | ●                                |
| Scrum Master / Agile Coach           | ●                         | ●                                    | ●       | ●               | ●                                |
| Release Engineer / Group Manager     | ●                         | ●                                    | ●       | ●               | ◐                                |
| Agile practice (Scrum, Kanban, etc.) | ●                         | ●                                    | ●       | ●               | ●                                |
| Demo                                 | ●                         | ●                                    | ●       | ●               | ●                                |
| Retros                               | ●                         | ●                                    | ●       | ●               | ◐                                |
| Customer driven / value focused      | ●                         | ●                                    | ●       | ●               | ◐                                |
| Dependency management                | ●                         | ◐                                    | ●       | ●               | ◐                                |
| Strategy transparency                | ●                         | ●                                    | ●       | ●               | ◐                                |
| Portfolio management                 | ●                         | ◐                                    | ●       | ●               | ◐                                |
| Release on demand                    | ●                         | ●                                    | ●       | ○               | ◐                                |
| Risk management                      | ●                         | ○                                    | ◐       | ◐               | ◐                                |
| DevOps                               | ●                         | ●                                    | ◐       | ●               | ●                                |

> Note: "Spotify" appears as a comparison column here (the "Spotify Model"), though it is described later (Ch. X) as a case-study approach rather than a formal off-the-shelf framework.

### Framework breakdowns — principles / structure / applicability

- **SAFe** — _Principles:_ Lean + agile; alignment, collaboration, delivery across many teams. _Structure:_ highly structured, four levels (Team, Program, Large Solution, Portfolio), each with defined roles, artifacts, ceremonies. _Applicability:_ large enterprises with many teams needing coordination; especially helpful when transitioning from waterfall to agile.
- **LeSS** — _Principles:_ builds directly on Scrum; simplicity, flexibility, customer-centric development. _Structure:_ less prescriptive than SAFe; fewer added roles/artifacts; two levels (Basic LeSS ≤8 teams; LeSS Huge 8+). _Applicability:_ orgs already doing team-level Scrum that want to scale without adding complexity.
- **Nexus** — _Principles:_ extends Scrum, keeping focus on a "Done," integrated increment every sprint. _Structure:_ same Scrum roles/events/artifacts plus new ones for dependencies/interactions; accommodates **3–9 Scrum teams**. _Applicability:_ orgs already succeeding with Scrum that want to apply it to larger projects/programs.
- **Scrum@Scale** — _Principles:_ extends fundamental Scrum to coordinate multiple teams across divisions/departments. _Structure:_ a "scale-free" architecture — the same basic unit (a Scrum team) builds orgs of any size. _Applicability:_ across industries/departments; easy for those already familiar with Scrum.
- **DAD** — _Principles:_ process-decision framework for simplified decisions around incremental/iterative delivery. _Structure:_ hybrid model extending Scrum, Agile Modeling, XP, and other techniques; more comprehensive. _Applicability:_ orgs wanting to improve existing agile practices with more discipline while keeping implementation flexibility.

### Selecting the right framework — decision criteria

- **Current agile maturity level** — SAFe/DAD suit orgs transitioning from waterfall; LeSS/Nexus suit those already familiar with basic Scrum.
- **Organization size and structure** — LeSS, Nexus, or Scrum@Scale for small-to-medium orgs; SAFe or DAD for larger, more complex orgs.
- **Nature of work** — many small independent projects → less-structured (LeSS/Nexus); large complex initiatives with many interdependencies → more-structured (SAFe/DAD).
- **Culture and change readiness** — ready for a big lean-agile shift → SAFe/DAD; prefer gradual change → start with Scrum then move to a less prescriptive framework (LeSS/Nexus).
- **Available resources** — time/money/personnel matter; SAFe and DAD typically need more extensive training and change-management investment.
- **Desired speed of transformation** — quick transition → LeSS/Nexus; gradual transition or many intertwined projects → SAFe/DAD.
- **Seek outside advice** — talk to other orgs, consult agile coaches/consultants, use online resources. The best framework is the one that fits the org's needs/context — not the most popular or newest.

---

## IV. Organizational structure and culture

### Organizational structure for Agile at Scale

- **Cross-functional teams** — include all roles needed to design, develop, test, and deliver value without heavy reliance on other teams (e.g., Software Developers, Testers, UX/UI Designers, Business Analysts).
- **Agile Release Trains (ARTs)** — in SAFe, the primary value-delivery construct; a long-lived "team of agile teams" that incrementally develops/delivers/validates a solution in a value stream. **Typically 5–12 agile teams (≈50–125 individuals)**, aligned to a common mission.
- **Communities of Practice (CoPs)** — groups sharing a concern/topic who deepen expertise through ongoing interaction; facilitate knowledge sharing/standardization across teams. Can be organized by role (Scrum Masters, POs), technology (Java, Python), or practice (TDD, CI/CD).
- **Alignment with value streams** — align teams/ARTs to the org's flow of value (the sequence of activities to fulfill a customer request) so teams always work on highest-value activities.
- **Scaling the roles** — scale PO, Scrum Master, and team-member roles; may introduce new roles like a **Chief Product Owner** (coordinating multiple POs) or a **Release Train Engineer** in SAFe (servant-leader/coach for an ART).
- **Organizational design principles** — minimize inter-team dependencies; keep team sizes manageable (the "two-pizza rule" — no bigger than two pizzas can feed); ensure clear communication/reporting lines.
- **Flattening hierarchies** — agile favors flat structures with decentralized decision-making; flatten as much as possible to foster autonomy and empowerment.
- **Embrace change** — the org must evolve; regularly inspect and adapt the structure to changing customer/business needs. No one-size-fits-all structure exists.

### Fostering an agile mindset and culture — seven ways

1. **Promote transparency** — create a safe environment to speak without fear; agile relies on standups, reviews, retrospectives where people share misgivings. Both teams and leadership must share openly; agile starts from respect for all parts of the business.
2. **Make it personal** — change must be embraced, not just accepted; show how new tools/practices improve people's lives, not just company finances. Pitch individual benefits, not only company-wide angles.
3. **Encourage continual learning and improvement** — learning orgs invest in growth; provide individual/team training budgets; encourage reflection (what went wrong/right, how to improve) and act on feedback.
4. **A new kind of leader (servant leadership)** — leadership embedded within the team, not above it; focuses on keeping everyone organized/on-task and filling weak points; ensures the team comes first and feels in control. Creates accountability — a core tenet of agile workplaces.
5. **Get the right tools for the job** — agile was enabled by technology; not using it is "swimming up a waterfall." Tools let teams see others' progress, provide actionable data, enable cross-team collaboration; invest in tools that visualize workflows, allocate resources, and enable communication.
6. **Foster a sense of ownership and accountability** — self-organizing teams have autonomy but keep responsibility; failure is a learning opportunity (not punished), small successes are celebrated; tie work to the whole so people see their part and feel responsible for overall success.
7. **Over-communicate** — make goals/plans/documents big and visible; keep everyone in the loop via daily meet-ups, on-demand progress tools, and empowered conversation about pain points. Without deliberate constant communication, teams silo and lose track of objectives.

> Cultural transformation is a journey requiring commitment at all levels — persistence and consistency in living agile values.

### How to be an Agile at Scale leader

- Leaders remain essential even in self-organizing teams; Agile at Scale paradoxically requires building hierarchies on top of non-hierarchical team structures.
- Leaders must embody agile values and take on an embedded, supportive role rather than dictating direction.

### The roles of leadership in Agile at Scale

- **Team servant** — "servant leadership": get everyone organized/on-task, keep communication flowing via standups/sprints; encourage transparency from above and around; prevail through respect for all points of the process.
- **Providing clear strategic direction** — teams decide _how_ they work, but leaders set the vision, align around strategic goals, and ensure teams understand how their work contributes; teams must also know where their work ends (protected from overload).
- **Removing obstacles** — watch for silos; push for daily communication between individuals/teams (not just management). The leader can become the biggest obstacle by reverting to control; without trust/respect, agile fails.
- **Continual improvement** — foster a culture of reflection/improvement; invest in agile training, education, and tools; stay current on practices/trends.
- **Measure and reward agility** — collect feedback and data on efficiency/effectiveness (time to market, customer retention, defect rate, etc.); celebrate when metrics are on track and reward the team. Important when work is purely iterative with no fixed end-state.

> Being an agile leader is not zero-sum (success vs. failure); it iterates and develops like agile itself. The goal: better outcomes, less wasted time, a happier and better-functioning team.

---

## V. Agile at Scale roles and responsibilities

New roles often introduced to manage complexity/coordination in large-scale projects (many single-team roles also remain):

- **Product Manager** — strategic role; understands market, customer needs, business goals; prioritizes the high-level backlog; ensures strategic vision aligns with team work.
- **Release Train Engineer (RTE)** — in SAFe, a servant-leader facilitating execution of ARTs; manages risks/dependencies, drives program-level continuous improvement, escalates/tracks impediments.
- **Solution Architect/Engineer** — works with system/enterprise architects to provide technical leadership for an ART or a **solution train** (a larger construct coordinating multiple ARTs); defines/communicates technical vision and architectural direction; ensures alignment.
- **Business Owners** — key stakeholders with primary business/technical responsibility for governance, compliance, and ROI of a solution developed by an ART; engaged in defining the backlog and preparing for ART events.
- **System Team** — builds/maintains the agile development environment; handles integration, end-to-end testing, and other technical tasks supporting ARTs.
- **Shared services** — specialized capabilities needed but not present in every ART (e.g., Security Specialists, Database Administrators, UX Designers); called on as needed.
- **Epic Owner** — defines and coordinates realization of **epics** in SAFe; works with stakeholders on the epic and its business case; follows it through its lifecycle.
- **Customer** — expanded role including internal/external stakeholders who ultimately consume the solution; provides feedback and guides product direction.
- **Supplier** — external organizations providing components/services; integrated into the process; may join planning, demos, and **Inspect & Adapt (I&A)** workshops.

> Not all roles are needed in every implementation — it depends on the chosen framework, org size/complexity, and nature of the work.

---

## VI. Agile practices at scale

### Multi-team coordination and planning

- **Program Increment (PI) planning** — in SAFe; a **two-day event** where all ART members align on a shared mission/vision and agree objectives for the next increment (**typically 8–12 weeks**); surfaces dependencies and risks.
- **Scrum of Scrums (SoS)** — coordination meeting of representatives (usually Scrum Masters) from each team; synchronizes work, discusses dependencies/conflicts, identifies risks/impediments needing escalation.
- **Cross-team planning** — coordinate planning across teams so each has insight into others' work; may use joint planning sessions or a shared planning tool.
- **Dependency management** — teams must be aware of and plan for dependencies; may use a dependency map or visualization tool.
- **Integration points** — regular points (integration testing, continuous integration, or set combine-and-test points) to ensure everything comes together.
- **Inspect and Adapt (I&A) workshops** — in SAFe, held at the end of every PI; teams reflect on performance, identify improvements, solve problems, and produce action items.
- **Product management and shared backlog** — a shared backlog plus active product management keeps teams on highest-priority, goal-aligned items, focused on customer value.

> Practices must be adapted to the org's context; keep open communication and ensure transparency/alignment across teams.

### Scaling daily stand-ups, reviews, and retrospectives

- **Daily stand-ups** — still happen at team level; for cross-team coordination: _Scrum of Scrums_ (standup for Scrum Masters/representatives, daily or a few times/week) and _Scaling online_ (digital tools for distributed teams, mindful of time zones).
- **Reviews / sprint reviews** — each team demos its increment; at scale: _Joint reviews_ (when teams share a product) and _System demo_ (in SAFe, at the end of every iteration the integrated solution from all ART teams is demoed to stakeholders).
- **Retrospectives** — _Team-level retrospectives_ (as in single-team agile); _RTE-facilitated retrospectives_ (overall retro at end of PI, facilitated by the RTE, to gather program-level improvements); _Large-scale retrospectives_ (techniques for big groups such as **appreciative inquiry, speedboat, open space**).

### Scaling backlog management and prioritization

- **Hierarchical backlogs:**
  - _Team backlog_ — each team's user stories for upcoming iterations/sprints.
  - _Program backlog_ — features for multiple teams on an ART; managed by a Product/Program Manager; feeds the team backlogs.
  - _Portfolio backlog_ — strategic-level **Epics**/large initiatives spanning multiple ARTs; managed by portfolio management; broken down into features for the program backlog.
- **Backlog grooming at scale** — beyond individual team grooming, larger refinement sessions (multiple teams or representatives) ensure alignment, handle dependencies, and build shared understanding.
- **Prioritization at scale (techniques):**
  - _Weighted Shortest Job First (WSJF)_ — used in SAFe; prioritizes features by **cost of delay** and **job size**.
  - _Business value points_ or _MoSCoW_ (**Must have, Should have, Could have, Won't have**) — rank by relative value/necessity.
  - _Dependency analysis_ — prioritize tasks based on their dependencies.
- **Tools for scaling backlog management** — agile PM tools that manage hierarchical backlogs and provide visibility/transparency at all levels.
- **Consistent communication** — between all levels (often via PI planning and synchronization meetings) to understand priorities.

> Goal: a clear path forward for each team while aligning with broader org goals.

### Coordinating cross-team dependencies

- **Identification of dependencies** — done during backlog grooming, planning sessions, or PI planning (SAFe); actively identify and document inter-team dependencies.
- **Visualizing dependencies** — dependency maps, **Dependency Structure Matrix (DSM)**, or agile-software tools; in SAFe, the **program board** is used during PI planning.
- **Managing and prioritizing dependencies** — once identified/visualized, teams agree who does what by when; high-impact dependencies get priority; involves collaboration, negotiation, sometimes escalation.
- **Regular communication and re-assessment** — via Scrum of Scrums or the **ART sync** (SAFe) to track dependencies and emerging issues; reassess frequently as priorities change.
- **Risk management** — include dependency-related risks in the overall risk process (delays in one team affect others).
- **Fostering a collaborative culture** — teams working together to solve problems, negotiate, and make collective decisions about dependencies.

> Ultimate goal: maintain a smooth, efficient flow of value through the organization; effective dependency management improves productivity and delivery speed.

### Use of tools — Tempo product mapping (vendor section)

- **Roadmunk** — portfolio vision; capture customer feedback, build strategic themes, communicate strategy across the org.
- **Structure** — visualize multiple Jira projects, programs, and portfolios in one place to align execution with strategy.
- **Planner** — centralize/fast-track capacity planning; insights into workforce operations/requirements; right resources in the right place to deliver the roadmap.
- **Timesheets** — track billable time for invoicing; measure/report on **CAPEX and OPEX**; build custom reports.
- **Cost Tracker** — translate Timesheets data into true project costs; monitor financial health at every org level.
- **Custom Charts** — report on multiple teams/sprints/projects directly on Jira dashboards; plan/monitor/reflect day-to-day and at project/sprint boundaries.

---

## VII. Implementing Agile at Scale

### Main transition considerations

- **Understand the need for scaling agile** — clarify _why_ (existing challenges or strategic goals like faster market delivery, better quality, improved satisfaction).
- **Choose the right scaling framework** — among SAFe, LeSS, DAD, Nexus; align with org needs/culture/context (see Ch. III).
- **Assess organizational readiness** — evaluate current culture, leadership support, existing practices, resource availability.
- **Training and coaching** — agile basics, the specific framework, and role-specific training; consider experienced agile coaches.
- **Pilot projects** — run pilots before full rollout to test, learn, and adjust.
- **Leadership engagement and support** — leaders understand their role, provide resources, remove roadblocks.
- **Change management** — effective communication, managing resistance, ensuring changes are effective and sustainable.
- **Aligning with business strategy** — correlate team objectives with strategic goals; ensure value delivery at all levels.
- **Measurement and continuous improvement** — establish metrics; inspect and adapt regularly.

> Transition is not only about processes/tools — it's equally about cultivating an agile mindset/culture; challenging but rewarding.

### Training and coaching needs

- **Training needs assessment** — gauge current agile maturity and skills gaps (surveys, interviews, assessment tools).
- **Agile basics training** — fundamental agile principles/practices, including the specific base framework (Scrum, Kanban).
- **Specific Agile at Scale framework training** — detailed training on the chosen framework's principles, practices, roles, artifacts (e.g., SAFe, LeSS).
- **Role-specific training** — tailored to roles (Product Owners, Scrum Masters, RTEs, etc.); content depends on the framework.
- **Leadership training** — for executives/managers/leaders on leading in an Agile-at-Scale environment: agile mindset, team empowerment, removing impediments.
- **Technical practices training** — depending on maturity: **TDD, CI/CD, automated testing, refactoring**, etc.
- **Coaching** — coaches give real-time guidance applying new knowledge and ensure practices are properly adopted.
- **Ongoing learning and improvement** — regular retrospectives, sharing sessions, continuous-education opportunities.

> Success of the transformation hinges heavily on training and coaching to build skills and a shared understanding.

### Overcoming resistance and other challenges

- Resistance ranges from individuals clinging to old ways to systemic issues (processes/structures that don't support agile).
- **Create a compelling vision for change** — communicate benefits (faster response to market, better quality, higher satisfaction); build buy-in and a sense of urgency; involve all stakeholders for ownership/engagement.
- **Address individual resistance** via training/coaching — show how Agile at Scale affects day-to-day work; teach practices _and_ foster the mindset; encourage feedback and adjust.
- **Overcome systemic resistance** by aligning structure/processes with agile principles — redefine roles, break down silos, change decision-making; consider an experienced agile coach/consultant.
- **Be patient and persistent** — change takes time with setbacks; keep focus on long-term benefits; over time resistance fades and the new way becomes the norm.

---

## VIII. Agile at Scale Metrics and KPIs

### Identifying suitable metrics — guiding principles

- **Alignment with business objectives** — e.g., to accelerate time to market, measure **lead time** (time for work to flow through the system).
- **Balance process and outcome metrics** — _process metrics_ measure efficiency (velocity, cycle time); _outcome metrics_ assess results (quality, customer satisfaction, business value delivered). Both needed for a balanced view.
- **Actionability** — choose metrics that point toward solutions; e.g., **escaped defects** (defects found by customers) signal a testing gap.
- **Simplicity** — keep metrics few; too many dilute focus.
- **Value over volume** — don't measure activity for its own sake; high story-point counts mean little if they don't deliver customer value.
- **Teams over individuals** — focus on team-level metrics to foster collaboration and avoid unhealthy competition.

> Metrics drive behavior, so choose wisely; review and adapt as the implementation matures and objectives evolve.

### Tracking and visualizing metrics — key considerations

- **Use appropriate tools** — from dedicated agile PM tools (Jira, Custom Charts) to general data-viz platforms (Tableau); choice depends on needs/infrastructure.
- **Transparency** — make metrics easily accessible to stakeholders, e.g., a centralized real-time dashboard.
- **Different levels of detail** — team members need detailed WiP views; executives need high-level delivery/quality views.
- **Trends over absolute numbers** — a single sprint's velocity has limited use; the **velocity trend over several sprints** is informative; visualization helps spot trends.
- **Regular reviews** — review metrics for anomalies/unexpected trends as part of reviews/retrospectives.
- **Avoid vanity metrics** — metrics that look good but provide no real value give false security and distract.

> Goal of tracking/visualizing: not just to measure performance but to drive continuous improvement.

### Using metrics for continuous improvement

- Treat metrics as a means for continuous improvement — providing feedback, identifying improvement areas, and guiding decision-making.

---

## IX. Continuous improvement and adaptation

### Feedback and inspection — best practices

- **Regular feedback loops** — within teams, between teams, and from stakeholders.
- **Retrospectives** — reflect on performance/processes; identify strengths, improvement areas, and action steps.
- **Agile metrics** — velocity, cycle time, customer satisfaction, defect rates to assess performance and inform improvement.
- **Customer and user feedback** — surveys, interviews, usability testing, direct observation; integrate into iterative development.
- **Continuous monitoring and evaluation** — monitor progress, evaluate effectiveness, make timely adjustments based on metrics/objective evaluation.
- **Experimentation and iteration** — culture of experimentation/learning; embrace "inspect and adapt."
- **Documentation and knowledge sharing** — document lessons learned, best practices, improvements to foster organizational learning.

### Adapting processes and practices — considerations

- **Embrace an agile mindset** — value adaptability/continuous improvement; stay open to change.
- **Continuously assess and evaluate** — use retrospectives/reviews/feedback loops to find adaptation areas.
- **Tailor processes to fit the context** — adapt to size, complexity, industry, specific needs.
- **Experiment and iterate** — try new approaches; implement small changes and assess before scaling.
- **Foster a culture of learning** — cross-team collaboration, communities of practice, professional development.
- **Empower teams** — give autonomy/ownership to self-organize and find effective ways of working.
- **Provide support and resources** — coaching, mentoring, guidance, training.
- **Regularly review and adjust** — use feedback/metrics/evaluations to identify further improvements.

### Maintaining and nurturing an agile mindset — best practices

- **Leadership modeling** — leaders demonstrate agile values/behaviors (openness to change, collaboration, empowerment, customer-value focus).
- **Continuous education and training** — workshops, seminars, certifications at all levels.
- **Cross-functional collaboration** — break down silos; share knowledge/experiences across teams/departments.
- **Celebrate successes and learn from failures** — celebrate agile-aligned achievements; treat failures as learning; emphasize experimentation/adaptation.
- **Continuous improvement rituals** — integrate regular retrospectives, reviews, feedback sessions.
- **Supportive environment** — psychological safety, trust, open communication; voice ideas/concerns without fear.
- **Agile coaching and mentoring** — access to coaches/mentors.
- **Regular communication and reinforcement** — communicate the importance of the mindset, share success stories, reinforce values via internal channels.

> Sustaining the mindset sustains a culture of agility, collaboration, and continuous improvement; keep nurturing it as the org grows (learning, improvement, collaboration, customer value).

---

## X. Case studies and best practices

### Case studies (companies cited as Agile-at-Scale examples)

- **Spotify** — the "Spotify Model": cross-functional teams, decentralized decision-making, autonomy + alignment; shared via articles, blog posts, presentations.
- **ING** (global banking/financial services) — transformed its entire org into **squads, tribes, and chapters**, enabling faster delivery and better collaboration; shared in publications/case studies.
- **Salesforce** (cloud software) — applied agile across multiple teams for faster cycles and iterative improvement; shared via conferences, webinars, blog posts.
- **Ericsson** (telecommunications) — adopted **SAFe** to improve product development; shared in case studies, presentations, industry events.
- **Scania** (commercial vehicles manufacturer) — used Scrum and Kanban in product development/engineering to boost collaboration, efficiency, customer value; shared via presentations, interviews, publications.

### Common pitfalls and how to avoid them

- **Lack of leadership support and engagement** — leaders must advocate agile, provide resources, actively participate.
- **Insufficient training and education** — ensure teams/individuals get adequate training to understand/embrace agile.
- **Scaling too quickly** — don't roll out org-wide without planning/piloting; start with pilots, learn, then scale gradually.
- **Lack of alignment with business objectives** — ensure efforts deliver value and support strategic goals.
- **Overemphasis on tools and processes** — (Tempo notes it sells tools but) too much focus on tools can overshadow the mindset; agile is people/interactions over tools/processes.
- **Failure to address cultural resistance** — foster transparency, collaboration, continuous improvement to handle resistance.
- **Inadequate collaboration and communication** — foster open communication/collaboration.
- **Neglecting continuous improvement** — keep reviewing/adapting; encourage learning, experimentation, continuous improvement.

> Awareness of these pitfalls lets orgs mitigate risk and improve chances of success; embrace continuous learning, adaptability, collaboration.

---

## XI. Implementing Agile at Scale with Tempo (vendor section)

- Premise: every org leverages agile differently; legacy monolithic enterprise software is too rigid for Agile at Scale, so Tempo's approach differs.
- Claim: Tempo's **Jira-native** solutions support **a third of Fortune 500 companies**; described as **modular** (start with the greatest need, build on success), **flexible** (use tools to fit outcomes regardless of methodology), and **Jira native** (simple to implement, easy to adopt, cost-effective).

### Tool overview (mapped to four needs)

- **Roadmapping and communicating strategy → Roadmunk** — portfolio vision, customer feedback, strategic themes, roadmaps.
- **Project and program management across teams → Structure** — "where the work happens"; keep the ART on track, supercharge PI work; paired with Roadmunk it consumes high-level portfolio objectives, organizes by theme, and extends down the hierarchy (capabilities → features → stories) as normal Jira issue management.
- **Team capacity and financial management → Planner, Cost Tracker, LiquidPlanner** — Planner centralizes/fast-tracks capacity planning; ensures the right resources in the right place to deliver the roadmap.
- **Time management and reporting → Timesheets & Cost Tracker, Custom Charts** — Timesheets tracks billable time, reports CAPEX/OPEX, builds custom reports; Cost Tracker derives true project costs; Custom Charts reports across teams/sprints/projects on Jira dashboards (sprint progress, retrospectives, programs, customer satisfaction, workloads, age of issues, cumulative spend, etc.).
- CTA: learn more / book a demo at Tempo.io.

---

## Key terms & references

**Base agile frameworks:** Scrum (sprints, product backlog, sprint planning, daily Scrum/standup, sprint review, sprint retrospective), Kanban (WiP limits, Kanban board, flow), Extreme Programming/XP (pair programming, TDD, continuous integration, refactoring, on-site customer), Lean Software Development, Dynamic Systems Development Method (DSDM).

**Agile-at-Scale frameworks:** SAFe (Team / Program / Large Solution / Portfolio levels), LeSS (Basic LeSS ≤8 teams; LeSS Huge 8+), Nexus (Ken Schwaber; 3–9 teams), Scrum@Scale (Jeff Sutherland; scale-free architecture), Disciplined Agile Delivery/DAD, "Spotify Model" (squads/tribes/chapters/guilds).

**Core roles:** Product Owner (PO), Scrum Master, Development Team, Product Manager, Release Train Engineer (RTE), Solution Architect/Engineer, Business Owners, System Team, Shared Services, Epic Owner, Customer, Supplier, Chief Product Owner.

**Constructs:** Agile Release Train (ART, 5–12 teams / ~50–125 people), Solution Train, Value Stream, Communities of Practice (CoPs), Epic, hierarchical backlogs (team / program / portfolio).

**Practices/events:** Program Increment (PI) planning (2-day; 8–12-week increment), Scrum of Scrums (SoS), ART sync, System Demo, Inspect & Adapt (I&A) workshop, joint reviews, large-scale retrospective techniques (appreciative inquiry, speedboat, open space).

**Prioritization techniques:** Weighted Shortest Job First (WSJF — cost of delay + job size), MoSCoW (Must/Should/Could/Won't have), Business value points, Dependency analysis, Dependency Structure Matrix (DSM), program board.

**Metrics:** velocity, cycle time, lead time, customer satisfaction, defect rate, escaped defects; process vs. outcome metrics; trends over absolutes; vanity-metric avoidance.

**Technical practices:** TDD, CI/CD, automated testing, refactoring, continuous integration.

**Concepts:** servant leadership, two-pizza rule, flattening hierarchies, self-organizing/cross-functional teams, inspect-and-adapt, VUCA-adjacent responsiveness to change, CAPEX/OPEX reporting.

**Org examples:** Spotify, ING, Salesforce, Ericsson (SAFe), Scania (Scrum + Kanban).

**Vendor tools (Tempo):** Roadmunk, Structure, Planner, Timesheets, Cost Tracker, Custom Charts, LiquidPlanner — Jira-native. Reference: Tempo.io.

---

## Relevance to BUS363

- **A1 (Project Scope Canvas + Video, due Session 4):** Ch. III's framework-selection criteria (maturity, size, nature of work, culture, resources, speed) and Ch. VII's "understand the need for scaling agile" directly support justifying scope and the chosen scaling approach in a video pitch.
- **A2 (Project Plan + Integration of PM Concepts, due Session 8):** richest source here. Maps cleanly to PMBOK→Agile Practice Guide integration: roles/structures (Ch. IV–V), multi-team coordination, hierarchical backlogs, dependency management (Ch. VI), metrics/KPIs (Ch. VIII), and continuous improvement (Ch. IX). Use the comparison table (Ch. III) and WSJF/MoSCoW for prioritization sections; use ART/PI planning for the scheduling/coordination narrative.
- **A3 (Team Presentation — scaling a business globally, due Session 12):** Ch. VII (implementation/change management), Ch. X case studies (ING, Spotify, Ericsson, Salesforce, Scania) give concrete global-scaling exemplars; Ch. IV culture + Ch. III framework fit support the internationalisation angle.
- **A4 (Participation, weekly):** supplies vocabulary and discussion hooks (servant leadership, VUCA-style responsiveness, inspect-and-adapt, vanity metrics) for weekly engagement.
- **Caveat for academic use:** this is a vendor (Tempo) playbook — treat product-promo sections (Ch. VI tools, Ch. XI) as illustrative, not neutral evidence, and cite primary framework sources (Scaled Agile Inc. for SAFe, less.works for LeSS, Scrum.org for Nexus, etc.) in formal submissions.
