---
title: "Randomized Controlled Trials: Design, Analysis, and Causal Identification"
source: "master-2026-spring-intermediate-epidemiology"
platform: "lecture"
author: "Farzana Kapadia"
date: 2026-03-09
ingested: 2026-04-05T00:00:00Z
tags: [epidemiology, study-design, rct, randomization, blinding, causal-inference, intent-to-treat, quasi-experimental]
category: "master-courses/epidemiology/study-designs"
compiled: true
---

# Randomized Controlled Trials: Design, Analysis, and Causal Identification

## Overview

Randomized controlled trials (RCTs) are the **gold standard** for evaluating the efficacy and side effects of new treatments or interventions. They sit on the **experimental** branch of analytic epidemiologic studies, where exposure is **assigned** by the investigator rather than self-selected.

RCTs begin with a defined population that is **randomized** to receive either the current treatment (standard of care / placebo) or the new treatment. Participants are followed over time and monitored for primary and secondary outcomes.

### When to Use RCTs

- Required by regulatory bodies as the basis for approval decisions for new treatments
- Researchers have a specific, targeted study question about a potential treatment
- Conditions exist for appropriate recruitment, enrollment, randomization, and follow-up
- Data can be gathered, cleaned, analyzed, and reported accurately

### Taxonomy of Epidemiologic Studies

```
EPI Studies
├── Descriptive
│   └── Cross-sectional (Survey)
└── Analytic
    ├── Experimental (exposure assigned)
    │   ├── RCTs
    │   │   ├── Individual-level
    │   │   ├── Group-level (cluster)
    │   │   ├── Cross-over designs
    │   │   └── Multi-arm / Factorial designs
    │   └── Quasi-Experimental Designs
    └── Observational (exposure not assigned)
        ├── Cohort study
        ├── Cross-sectional (Analytic)
        └── Case-control study
```

## Key Characteristics of Controlled Trials

### 1. Eligibility

Strict **inclusion/exclusion criteria** define who can participate. This affects both internal validity and external generalizability.

### 2. Randomization

- **Minimizes confounding** by known and unknown factors (when sample size is large)
- Ensures **comparability** of the randomized sample across treatment arms
- Achieves **exchangeability of treatment assignment in expectation** -- on average, risk factors for the outcome are balanced between arms, even for unmeasured confounders

### 3. Blinding/Masking

- Ensures **comparability** of collected exposure and disease information
- **Minimizes differential misclassification** of exposure and outcome data

### 4. Control

- Placebo or standard of care serves as the comparison group
- Ensures **comparability of trial circumstances/conditions** across arms
- Minimizes **misspecification of the effect measure**

### 5. Endpoints

- **Primary endpoint**: the main outcome the trial is powered to detect
- **Secondary endpoints**: additional outcomes of interest

### 6. Adverse Events and Stopping Rules

Trials must monitor safety and have pre-specified rules for early termination.

## Causal Identification in RCTs

RCTs are a gold standard for causal inference when they can demonstrate **four arguments**:

### Temporality

The treatment must precede the outcome. In an RCT, this is ensured by design -- randomization and treatment assignment occur before follow-up begins.

### Consistency of Treatment Assignment

In a placebo-controlled RCT, participants are assigned to treatment or placebo in the same way. There is **no variation in treatment assignment** mechanism.

### Positivity of Treatment Assignment

All RCT participants have a **nonzero probability** of being assigned to each treatment arm AND getting that treatment.

### Exchangeability in Treatment Assignment

For every participant with characteristic $X$ randomized to treatment, a participant with characteristic $X$ is randomized to the placebo arm. We refer to this as **"exchangeability of treatment assignment in expectation"** when sample sizes are sufficiently large.

> **Key insight**: These arguments hold under **perfect compliance**. They apply to the causal effect *of treatment assignment*, not necessarily of treatment itself. Only with perfect compliance do they extend to the causal effect of actual treatment.

## Example: Women's Health Initiative (WHI) Estrogen Trial (JAMA 2004)

- **Context**: Role of estrogen alone in preventing chronic diseases in postmenopausal women was uncertain
- **Design**: Randomized, double-blind, placebo-controlled disease prevention trial
- **Population**: 10,739 postmenopausal women aged 50-79 with prior hysterectomy, 23% minority race/ethnicity
- **Setting**: 40 US clinical centers, beginning 1993
- **Intervention**: 0.625 mg/d conjugated equine estrogen (CEE) vs. placebo
- **Primary outcome**: Coronary heart disease (CHD) incidence
- **Primary safety outcome**: Invasive breast cancer incidence

Assessing exchangeability involved comparing baseline characteristics (age, race/ethnicity, BMI, smoking, hormone use history, medical history) between CEE ($n = 5310$) and placebo ($n = 5429$) arms -- a "Table 1" comparison.

## Analytic Approaches

### Intent to Treat (ITT) Analysis

Comparisons are made between the complete groups assigned to different treatment regimens, **irrespective of departure from protocol**:

- Analyzes by **assignment**, exploring the effect of assignment, not actual receipt
- Preserves the randomization-based exchangeability
- Minimizes non-comparability between groups

**ITT numerical example** (new drug A vs. standard treatment B, $n = 1000$, 500 per arm, 1-year follow-up):

|  | Dx | No Dx | LTFU | Total N | $\text{PT}_{-\text{LTFU}}$ | $\text{PT}_{\text{LTFU}}$ | $\text{PT}_{\text{Total}}$ |
|---|---|---|---|---|---|---|---|
| Treatment | 15 | 30 | 5 | 50 | 30 | 20 | 50 |
| Placebo | 20 | 20 | 10 | 50 | 25 | 25 | 50 |

- **ITT-based findings**: $\text{CIR} = 0.75$, $\text{IDR} = 0.75$
- **Not employing ITT**: $\text{CIR} = 0.67$, $\text{IDR} = 0.63$

### Compliance-Corrected (As-Treated) Analysis

Comparisons are made based on **actual compliance with intervention** -- analyzing people by what they actually did, not what they were assigned:

- Also called "as-treated" or "adherence-corrected"
- Explores the effect of **actual receipt** of the drug, not assignment
- **Randomization is broken** in this approach: factors like smoking, age, and comorbidities can affect who complies, and these factors are not randomized between compliers vs. non-compliers

### Per-Protocol Analysis

Includes only participants who **strictly adhered to the study protocol**, excluding non-compliant subjects:

- Affected by **selection bias** since the per-protocol population is a non-random subset
- Cannot claim exchangeability

### Comparison of the Three Approaches

| | ITT | Per-protocol | Compliance-corrected |
|---|---|---|---|
| **Inclusion** | By randomization status | Excludes non-compliers | Reclassifies by actual compliance |
| **Bias risk** | Minimizes bias via comparability | Increased bias (non-compliers dropped, comparability reduced) | Biased if compliance associated with outcome risk |
| **Purpose** | Evaluate efficacy, broadly speaking | Efficacy under ideal conditions | Efficacy under ideal conditions |

## Confounding in RCTs

In an ITT analysis, analyzing by treatment **assignment** reduces confounding because randomization ensures assignment is unconfounded.

However, when the exposure is no longer treatment assignment but **actual treatment** (compliance-corrected analysis), confounding can occur.

**DAG example** (aspirin trial):

```
Random ──────→ Daily Aspirin ──→ Death
                      ↑              ↑
                Healthy Habits ──────┘
```

The effect of randomization to Daily Aspirin vs. placebo is **not confounded** by Healthy Habits. But the effect of *actually taking* daily Aspirin **is confounded** by Healthy Habits.

### Non-Compliance and Measurement Error

- **Non-compliance as non-differential misclassification**: If non-compliance is independent of outcome risk, it is a form of non-differential misclassification that generally **biases toward the null** in two-category comparisons
- **ITT with non-compliance**: Some people assigned to treatment are actually untreated (and vice versa), making groups more similar and effect estimates **closer to the null**
- If the goal is to estimate the effect of **actual treatment**, compliance-corrected analysis is needed, but must then account for confounding as in an observational study

## Problems and Limitations

### Non-Compliance

- Participants may not accept or adhere to their assigned intervention
- ITT asks only about **treatment assignment**, so non-compliance is absorbed into the total effect
- If treatment assignment is used as a **proxy** for actual treatment effect, non-compliance weakens this proxy

### Loss to Follow-Up (LTFU)

- Participants drop out during the trial, creating **missing outcome data**
- LTFU causes **selection bias** when it is related to the outcome (e.g., sicker people are more likely to be lost)
- LTFU **reduces study power**
- **Right-censoring**: At end of follow-up, some participants have not experienced the event; administrative right-censoring is usually uninformative, but LTFU-related right-censoring may not be

**Handling non-compliance and LTFU**:
- Careful inclusion/exclusion criteria at screening
- Collect extensive baseline data
- Actively prevent LTFU and assess reasons for dropout
- Monitor compliance continuously (surveys, biosamples, MEMSCap systems)

### Biases in RCTs

- Missing data
- Confounding (especially in compliance-corrected analyses)
- Selection bias (from LTFU or per-protocol analysis)
- Measurement error
- Non-differential misclassification

## Types of RCT Designs

### Parallel Design

The standard RCT design: two or more groups receive different interventions simultaneously. Participants are assigned to one arm at baseline and remain in that arm throughout.

### Superiority vs. Non-Inferiority/Equivalence

- **Superiority**: Traditional RCT designed to show that a new treatment is **more efficacious** than the control
- **Equivalence/Non-inferiority**: Designed to show that a new treatment (easier, cheaper) is **not worse** than the standard by more than a pre-established margin
  - Cannot statistically prove equivalency -- only show that the difference is less than some threshold
  - Issues: small sample size can lead to non-significant results that do not imply equivalence; treatment margin can be arbitrary

### Cluster Randomized Trials

Units of assignment are **groups** (schools, clinics, communities) rather than individuals. Units of observation remain individuals within those groups.

**Advantages**:
- Logistically more feasible
- Avoids contamination between arms
- Allows mass intervention ("public health trial")

**Disadvantages**:
- Effective sample size is less than number of subjects (due to intra-cluster correlation)
- Many units needed to overcome unit-to-unit variation
- Requires cluster sampling methods for analysis

Can use *a priori* matching, stratification, or constrained randomization to balance confounders across clusters.

### Crossover Designs

Each participant receives **all treatments sequentially**, serving as their own control.

**Advantages**:
- Reduced error variance (within-subject comparison)
- Smaller sample size needed due to increased power from paired analysis
- Each participant receives treatment at some point
- Blinding can be maintained

**Disadvantages**:
- Assumes underlying disease state is **static**
- Assumes no carry-over effect from initial treatment
- May require lengthy washout periods between treatments
- Cannot be used for one-time treatments (e.g., surgery) or treatments with permanent effects

### Factorial Designs

Test **two or more interventions simultaneously**. The most common is a $2 \times 2$ design where patients receive Treatment A, Treatment B, both, or neither.

### Multi-Arm Trials

Compare effects of Treatment A, Treatment B, Treatment C, etc., to a single placebo/control group simultaneously. Efficient when several treatment options exist.

## Efficacy vs. Effectiveness

| | Efficacy Study | Effectiveness Study |
|---|---|---|
| **Question** | Does it work under ideal conditions? | Does it work in real-world practice? |
| **Setting** | Resource-intensive, ideal setting | Real-world everyday clinical setting |
| **Population** | Highly selected, homogeneous, several exclusion criteria | Heterogeneous, few exclusion criteria |
| **Providers** | Highly experienced and trained | Representative usual providers |
| **Intervention** | Strictly enforced and standardized, no concurrent interventions | Applied with flexibility, concurrent interventions permitted |

## Additional Important Terms

### Run-in / Washout Period

A pre-defined period before the trial begins where no intervention is given, used to:
- Screen out ineligible or non-compliant participants
- Ensure that measured effects are from the study drug, not prior medications
- Assess drug metabolism, side effects, and measurable effects
- **Disadvantage**: May deter enrollment

### Contamination

When the experimental group influences the control group or vice versa:
- Social interactions between participants in different arms
- Health professionals delivering both intervention and standard care
- Cluster randomization is one strategy to reduce contamination

### Sample Size Considerations

Sample size requires knowledge of:
- Expected number of events
- Expected timing of events over follow-up
- Potential non-compliance and dropout rates
- Must be large enough to achieve stated goals with reasonable **power**
- Need to be **conservative but realistic**

## Quasi-Experimental Studies

When classic RCT design is not feasible or ethical, quasi-experimental designs provide alternatives:

### Non-Equivalent Control Group Designs

- **Posttest-only**: Treatment and control groups measured only after intervention
- **One-group pretest-posttest**: Single group measured before and after intervention (no control)
- **Pretest-posttest with control**: Both treatment and control measured before and after

### Regression Discontinuity Design (RDD)

A pretest-posttest design using a **cutoff threshold** for treatment assignment:
- Compares observations lying close to either side of the threshold
- Key assumption: treatment assignment is "as good as random" at the threshold
- Example: Scholarship eligibility at GPA 3.5 -- comparing outcomes for students just above vs. just below

### Difference in Differences (DiD)

Uses longitudinal data from treatment and control groups to estimate causal effects:
- Compares **changes in outcomes over time** between groups
- Key assumptions:
  - Intervention unrelated to outcome at baseline
  - **SUTVA** (Stable-Unit-Treatment-Value-Assumption)
  - **Parallel Trends**: In the absence of treatment, the difference between groups would remain constant over time

## Key Takeaways

1. RCTs are the gold standard for causal inference because randomization achieves exchangeability, temporality, consistency, and positivity **of treatment assignment**
2. The four causal arguments apply to treatment assignment, not actual treatment receipt -- **perfect compliance** is needed to extend them to treatment effects
3. **ITT** preserves randomization and minimizes bias; **per-protocol** and **compliance-corrected** analyses break randomization and introduce potential confounding and selection bias
4. Non-compliance acts as **non-differential misclassification**, generally biasing ITT results toward the null
5. **LTFU** causes selection bias when related to the outcome and reduces statistical power
6. Multiple trial designs exist beyond parallel RCTs: cluster, crossover, factorial, multi-arm, and quasi-experimental approaches -- each with distinct advantages and trade-offs
7. DAGs are essential tools for understanding when confounding arises in trial analysis, particularly when moving from ITT to compliance-corrected approaches

## Original Slides

![[assets/Lecture 5 and 6_RCTs - Copy.pdf]]
