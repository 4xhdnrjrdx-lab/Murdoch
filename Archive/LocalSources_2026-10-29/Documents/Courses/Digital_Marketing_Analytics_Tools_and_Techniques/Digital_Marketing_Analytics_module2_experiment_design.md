# Digital Marketing Analytics: Tools and Techniques — Online Testing: Experiment Design

> **Source / origin note.** External course material — *not* Murdoch. From the edX course **"Digital Marketing Analytics: Tools and Techniques"** (University of Maryland — Robert H. Smith School of Business). **Module 2.** Reading + video transcript + drag-and-drop exercise reproduced verbatim for study reference; player line numbers omitted as non-content.

---

Now we will explore deeper into online testing, talk about Experiment Design, and discuss the differences between A/B and Multivariate Testing.

## Definitions

- **Response** (or Dependent Variable, Outcome, Performance metric) — a quantitative measure of the experiment's objective.
- **Factor** (or Variable) — a controllable variable that is thought to influence response.
  - Factors are assigned **Values** (or Levels, Versions).
- **Treatment** (or Variant, Version) — a user experience being tested by assigning levels to the factors.

---

## Video transcript — Online Testing: Experiment Design

*(5-minute video.)*

Hello and welcome. In this video, we will talk about experiment design and discuss the differences between A/B and multivariate testing.

Let's begin with terminology, using two copies of display ads the Smith School uses to promote its Executive MBA Program. In display advertising, advertisers want their ads to bring prospects to their websites, so a key performance metric is the **click-through rate** — in online-experiment terminology, the **Response (or Dependent Variable / Outcome)**.

When developing ads, firms can have completely different creatives or just manipulate particular design aspects. In the example, two ads look similar and differ only in title and subtitle. The design aspect being manipulated across versions is a **Factor (or Variable)**. Each factor can be manipulated on two or multiple **Levels (Versions/Values)**. Here the factor "header" is manipulated on two levels: "Successful leaders see the whole board" and "Problem-solvers know which move to take." Any combination served to a user is a **Treatment (or Variant/Version)**, composed of selected levels of the corresponding factors.

Note: if only two versions of the ad (two treatments) are used, and both factors change at the same time, we **won't be able to differentiate the effects of the two factors individually.** This leads to multivariate testing.

### A/B vs multivariate testing

In contrast to **A/B testing** (goal: establish the best-performing design), **multivariate testing** involves understanding the impact of individual factors *and their interactions* — i.e., how each factor contributes to performance, and whether the effect is moderated by levels of other factors. In the MBA-ad example, the advertiser uses four treatments combining two factors on two dimensions each; this setup lets you establish the individual effects of the header and the image on click-through rate, and whether a certain header–image combination has a **synergistic** effect. (The data-collection procedure is the same idea: ad impressions are split across treatments while performance statistics are collected.)

**Comparison:**
- **A/B testing** — relatively easy to set up and interpret; plenty of free tools; cheap and easy to get started; **lower traffic requirements**. Downside: an "all-or-nothing" approach — establishes the best option but gives little insight into the role of each individual design element (unless specially designed), so results are harder to generalize.
- **Multivariate testing** — generates insights on individual design elements and their interactions; a more general version of A/B testing. Downside: requires a **large amount of traffic** to collect sufficient statistics; may not be feasible for smaller websites.

How to choose? It depends on your experiment goals and resources (number of observations you can collect). Typically, **A/B testing is the more common starting point.**

### The statistics behind hypothesis testing

We start with a default assumption that the proposed change does **not** result in better performance — the **null hypothesis**. We also set an **alternative hypothesis** suggesting the new version is an improvement. Hypothesis testing comes down to establishing whether the null hypothesis should be rejected (meaning the new version performs better and should be adopted). The math looks at how big the difference is between the two versions' performance; if it's big enough, we reject the null hypothesis. (What counts as "big enough" is a topic of statistics beyond this video.)

---

## Exercise — Experiment Design Terminology Identification (ungraded, 4 points)

**Problem:** Match the terms — **Factor, Response, Level, Treatment** — to the appropriate part(s) of the Smith Part-Time MBA "I Am Fearless" display ads. *(Feedback note: the two ads on the left can be defined with one term — you can drag the term to either box.)*

Mapping (per the course definitions):
- **Response** → Click-through Rate (the outcome metric).
- **Treatment** → a complete ad version/variant (the fully outlined ad).
- **Factor** → the header/quote text element being manipulated.
- **Level** → the specific header wordings ("EVEN IF MY SCHEDULE ISN'T." vs "OR OPPORTUNITIES TO WASTE.") — the two left boxes share this one term.
