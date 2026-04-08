---
title: "Causal Inference Frameworks and Directed Acyclic Graphs"
source: "master-2026-spring-intermediate-epidemiology"
platform: "lecture"
author: "Farzana Kapadia, PhD MPH"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [epidemiology, causal-inference, dags, counterfactual, bradford-hill, rothman-causal-pies, confounding, mediation, effect-modification, exchangeability]
category: "master-courses/epidemiology/causal-inference"
compiled: true
---

# Causal Inference Frameworks and Directed Acyclic Graphs

## Overview

Causal inference is the central intellectual challenge of epidemiology: moving from observed statistical associations to defensible claims about cause and effect. This lecture covers the major causal frameworks -- Bradford-Hill criteria, Rothman's sufficient-component cause model (causal pies), directed acyclic graphs (DAGs), the counterfactual framework, and the potential outcomes model -- and shows how they connect to core epidemiologic concepts like confounding, mediation, effect measure modification, and exchangeability.

## How Do We Study "Causes"?

The process of studying causation follows five steps:

1. **Theory of causation** -- formulate a research question: does exposure to certain risk factors cause disease?
2. **Formulate a testable hypothesis** -- exposure to variable X will be related to disease Y
3. **Design and conduct a study** -- randomized trials, cohort studies, case-control studies, ecological studies; goal is to minimize bias, minimize random error, collect data on confounding variables
4. **Analyze the data**
5. **Interpret the results**

Bradford-Hill criteria enter at multiple stages: **temporality** and **biological plausibility** guide theory formation, while **strength of association**, **dose-response**, **consideration of alternate explanations**, **cessation of exposure**, **coherence with established facts**, **specificity of association**, and **replication of findings** guide interpretation.

---

## Causal Paradigms

### Why Single Causes Are Insufficient

Very rarely is one factor a sufficient cause of disease. Genetic diseases can be exceptions (e.g., defect in BOTH Hex-A genes causes Tay-Sachs), but most diseases result from a complex system of many related factors (multiple causes). We need formal frameworks to understand these connections.

### Rothman's Sufficient-Component Cause Model (Causal Pies)

**Key definitions:**

- **Sufficient cause**: the minimum set of conditions that, when all present, inevitably produce the outcome
- **Component cause**: an individual factor that is part of a sufficient cause
- **Necessary cause**: a component cause that appears in every sufficient cause for a given disease (e.g., B in the diagram below appears in all causal pies)
- **U (unknown causes)**: the component that is often largest -- we don't fully understand all mechanisms

There may be multiple sufficient causes for the same disease, each represented as a "pie" with different component slices. If we could specify all mechanisms perfectly, we could predict all disease -- but there are likely infinite combinations of causal pies.

> In risk factor epidemiology, we focus on one component cause and often ignore its complements within a sufficient cause.

**What happens if you remove a component cause?**
- Removing a non-necessary component (e.g., A) prevents only the sufficient causes that contain A
- Removing the necessary cause (e.g., B) prevents ALL sufficient causes

### Component Causes as "Exposures"

When studying component causes as exposures, precision matters. For example, asking "does smoking cause lung cancer?" is too imprecise -- we need to specify:

- **Dose** -- how much?
- **Duration** -- how long?
- **Induction period** -- time between exposure and disease (NOT latency)

Ignoring these attributes (e.g., treating someone who smoked 1 lifetime cigarette the same as a 10 pack/day smoker) biases results.

#### Measuring Dose Attributes

| Type | Example |
|------|---------|
| Time-weighted average dose | Grams of fat per day |
| Maximum dose | Highest adult body weight |
| Body weight/surface area scaled | Grams of alcohol per kg body weight |
| Cumulative dose | Pack-years of cigarettes |

#### Duration Attributes

- Total time of exposure (years employed)
- Biologically relevant time of exposure (smoking before first pregnancy)
- Time of exposure beyond a minimum (years of driving after age 25)
- Time of exposure after gathering another component cause (HIV infection after HPV infection)

#### Induction Period

The **induction period** is the time between completion of a component cause (exposure of interest) and completion of the sufficient cause (disease occurrence).

Key points:
- Characterizes the **component cause-disease pair**, not the disease alone
- Every disease has a component cause with zero induction time (the last component to act)
- Failure to exclude induction time from person-time **biases toward the null**

### Strength Is Determined by Complements

The strength of a risk factor (typically on the relative scale) is determined by the relative prevalence in the population of the causal complements, and also affected by competing risks of other sufficient causes for the same disease.

---

## Directed Acyclic Graphs (DAGs)

### Definition and Properties

**Directed acyclic graphs (DAGs)** represent causal concepts visually:

- **Graph**: nodes (variables) connected by lines (edges)
- **Directed**: edges have a single arrowhead indicating causal direction
- **Acyclic**: no loops (though real-world feedback loops can exist, they are modeled as separate time-indexed nodes)

### Key Rules for Constructing DAGs

- Build DAGs **before** analysis and **before** data collection, based on subject-matter knowledge
- All antecedents of both exposure and outcome must be on the DAG (even variables not collected)
- DAGs are **non-parametric** -- the same DAG applies to risk differences, risk ratios, rate ratios, etc.
- Arrows represent hypothetical causal effects: $E \rightarrow D$ means "if E changes, D's risk will change"
- Arrows are **non-determinative**: $E \rightarrow D$ does not mean that if E goes from 0 to 1, D deterministically changes

### Example: Statins and Heart Attack

Two possible DAG structures:

**DAG 1** (direct + multiple paths):
$$\text{Statins} \rightarrow \text{Heart Attack}$$
$$\text{Statins} \rightarrow \text{LDL Cholesterol} \rightarrow \text{Heart Attack}$$
$$\text{Age} \rightarrow \text{Statins}, \quad \text{Age} \rightarrow \text{Heart Attack}, \quad \text{Age} \rightarrow \text{LDL Cholesterol}$$

**DAG 2** (fully mediated):
$$\text{Statins} \rightarrow \text{LDL Cholesterol} \rightarrow \text{Heart Attack}$$
$$\text{Age} \rightarrow \text{LDL Cholesterol}, \quad \text{Age} \rightarrow \text{Heart Attack}$$

The choice between DAGs depends on prior knowledge, not on data.

---

## Connecting DAGs and Causal Pies

### I. Independent Risk Factors

When E (exposure) and T (another risk factor) are in **separate** sufficient causes with no shared components (except U), they are independent risk factors. In a DAG: both T and E point to D with no arrow between T and E.

$$T \longrightarrow D \longleftarrow E$$

### II. Confounding

**T is a confounder** of the E-D relationship when T appears as a component in a sufficient cause for D AND T is causally linked to E. In a DAG:

$$T \rightarrow E$$
$$T \rightarrow D$$
$$E \rightarrow D$$

T is a common cause of both E and D, creating a "backdoor path" that must be blocked to isolate the causal effect of E on D.

### III. Mediation

**T is a mediator** when T lies on the causal pathway from E to D. In causal pies, E produces T, and T (along with other complements) produces D.

$$E \rightarrow T \rightarrow D$$

E may also have a direct effect on D that does not go through T.

### IV. Effect Measure Modification

**T modifies the effect** of E on D when T and E appear together within the same sufficient cause -- they are "synergistic" component causes. In a DAG, this is sometimes shown as T and E jointly pointing to D, with no separate arrow from T to E.

### Worked Example: Sedentary Behavior and BMI

| Scenario | DAG Structure |
|----------|--------------|
| **1. Independent risk factors** | Physical Activity $\rightarrow$ BMI; Sedentary Behavior $\rightarrow$ BMI (no arrow between them) |
| **2. Confounding** | Physical Activity $\rightarrow$ BMI; Physical Activity $\rightarrow$ Sedentary Behavior; Sedentary Behavior $\rightarrow$ BMI |
| **3. Mediation** | Sedentary Behavior $\rightarrow$ Sugar Sweetened Beverage Consumption $\rightarrow$ BMI |
| **4. Effect Modification** | Family History and Sedentary Behavior jointly $\rightarrow$ BMI |

---

## Counterfactual Framework

### The Core Idea

In practice, we compare a group of **exposed** subjects with a group of **unexposed** subjects. The validity of this comparison depends on the assumption that the risk of disease in the unexposed group equals the risk that **would have occurred** in the exposed group **in the absence of exposure**.

When this assumption fails, the observed comparison may not reflect the true causal difference -- likely due to **uncontrolled confounding**.

### Counterfactual Reasoning

A counterfactual asks: "what would have happened to this individual under the alternative exposure?"

- **Observed**: cyclist rides in storm $\rightarrow$ accident
- **Counterfactual**: if the same cyclist at the same time had sunny weather $\rightarrow$ would they still have had an accident?

The causal effect depends on comparing the actual outcome with the counterfactual outcome for the **same individual at the same time**.

### The Fundamental Problem of Causal Inference

In the real world, a population splits into exposed (E) and unexposed (No E) groups, each experiencing disease (D) or not (No D). The key question: are these two groups **exchangeable**?

> Epidemiology is centrally concerned with ensuring **exchangeability or comparability** of the exposed and unexposed groups.

---

## Potential Outcomes Framework

### Notation

For a binary treatment $X$ and binary outcome $Y$:

- $Y^0$ = potential outcome if the individual does **not** receive treatment
- $Y^1$ = potential outcome if the individual **does** receive treatment

**Only one of these is ever observed** for any individual:
- If $X = 0$: we observe $Y^0$, and $Y^1$ is counterfactual
- If $X = 1$: we observe $Y^1$, and $Y^0$ is counterfactual

### Individual-Level Causal Effect

The individual causal effect is defined as:

$$\text{ICE}_i = Y_i^1 - Y_i^0$$

For each person, this yields one of:
- **No effect**: $Y^1 = Y^0$
- **Harmful**: $Y^1 > Y^0$ (exposure causes disease)
- **Protective**: $Y^1 < Y^0$ (exposure prevents disease)

### The Fundamental Problem

We **never** observe both $Y^0$ and $Y^1$ for the same individual. It is therefore over-ambitious to infer individual-level causal effects.

### Population-Level (Average) Causal Effect

A more achievable goal is the **average causal effect (ACE)**:

$$\text{ACE} = E_{\text{avg}}(Y^1) - E_{\text{avg}}(Y^0)$$

For binary outcomes:

$$\text{ACE} = P(Y^1 = 1) - P(Y^0 = 1)$$

### Example: Headache Medicine (12 Subjects)

With "ideal" (omniscient) data showing both potential outcomes:
- $P(Y^0 = 1) = 4/12$ (4 of 12 would have headache relief without medicine)
- $P(Y^1 = 1) = 4/12$ (4 of 12 would have headache relief with medicine)
- $\text{ACE} = 4/12 - 4/12 = 0$ -- **no causal effect** at the population level

Yet at the individual level, some people had harmful effects (person 2, 9) and some had protective effects (person 3, 12).

### Causal Types Model

Each individual falls into one of four types:

| Causal Type | Exposed | Unexposed | Interpretation |
|-------------|---------|-----------|----------------|
| 1) Doomed | Disease | Disease | Gets disease regardless |
| 2) Causative | Disease | No Disease | Exposure causes disease |
| 3) Preventive | No Disease | Disease | Exposure prevents disease |
| 4) Immune | No Disease | No Disease | No disease regardless |

### Causal Measures (Single Cohort)

For Cohort 1 (exposed), with proportions $p_1, p_2, p_3, p_4$:

$$\text{Causal RD} = (p_1 + p_2) - (p_1 + p_3) = p_2 - p_3$$

$$\text{Causal RR} = \frac{p_1 + p_2}{p_1 + p_3}$$

$$\text{Causal OR} = \frac{(p_1 + p_2)/(p_3 + p_4)}{(p_1 + p_3)/(p_2 + p_4)}$$

> If $p_2 - p_3 = 0$, the causal risk ratio = 1 and causal odds ratio = 1, meaning there is balance between causative and preventive effects.

### Two-Cohort Problem and Exchangeability

When comparing exposed (Cohort 1) with unexposed (Cohort 0), the causal risk difference becomes:

$$\text{CRD} = (p_1 + p_2) - (q_1 + q_3)$$

If $q_1 + q_3 \neq p_1 + p_3$, then the unexposed group **cannot** be substituted for the counterfactual of the exposed group. The resulting association measure is **confounded** by the discrepancy between these two quantities.

### Risk Conceptualized via Causal Types

- **Risk in exposed** = proportion of doomed + causative types among the exposed:

$$R_{\text{exposed}} = \frac{\text{Doomed} + \text{Causative}}{\text{Doomed} + \text{Causative} + \text{Immune} + \text{Preventive}}$$

- **Risk in exposed had they NOT been exposed** = proportion of doomed + preventive types among the same individuals:

$$R_{\text{counterfactual}} = \frac{\text{Doomed} + \text{Preventive}}{\text{Doomed} + \text{Causative} + \text{Immune} + \text{Preventive}}$$

### Causal Contrast vs. Association Measure

**Causal contrast** (what we want):

$$\text{Causal RR} = \frac{R_{\text{exposed}}}{R_{\text{exposed, had they not been exposed}}} = \frac{p_1 + p_2}{p_1 + p_3}$$

This compares proportions **among the same individuals** under different exposure conditions.

**Association measure** (what we get):

$$\text{Observed RR} = \frac{R_{\text{exposed}}}{R_{\text{unexposed}}} = \frac{p_1 + p_2}{q_1 + q_3}$$

This compares proportions **in different groups of people**. The association equals the causal contrast only when the exposed and unexposed are **exchangeable**.

---

## Descriptive/Predictive vs. Causal Inference

| Type | Focus | Example |
|------|-------|---------|
| **Descriptive/Predictive** | Describing or classifying observations | "Is this group at high risk of side effects from this medication?" |
| **Causal** | Involves an intervention that can be modified | "Which type of anesthetic should these patients receive to minimize complications?" |

Causal inference explicitly or implicitly involves an **intervention** that can, at least in principle, be modified.

---

## Goal of Epidemiologic Methods

The overall workflow for causal reasoning in epidemiology:

1. **Posit causal theory** -- identify causes, develop causal explanations
2. **Gather data to test theory** -- RCT, cohort, case-control, cross-sectional studies
3. **Compare theory with data collected** -- stratification and modeling
4. **Acknowledge uncertainty**

### The Big Questions in Analytic Epidemiology

1. Is there a **statistical association** between an exposure and a disease?
2. Is it likely due to **random chance or study bias**?
3. Is the strength of association large enough to be **clinically important**?
4. Is it **consistent** with other studies?

---

## Key Takeaways

1. **Bradford-Hill criteria** provide a checklist for evaluating causality but are neither necessary nor sufficient -- they are guidelines for judgment
2. **Rothman's causal pies** formalize multi-causality: diseases arise from combinations of component causes forming sufficient causes
3. **DAGs** are the modern standard for representing causal assumptions; they must be built before data analysis based on prior knowledge
4. **Confounding, mediation, and effect modification** have distinct representations in both causal pie and DAG frameworks
5. **The counterfactual framework** defines causation as the difference between what happened and what would have happened under alternative exposure
6. **The fundamental problem of causal inference** is that we never observe both potential outcomes for the same individual
7. **Exchangeability** (comparability of exposed and unexposed groups) is the core assumption that allows observed associations to approximate causal effects
8. The gap between **causal contrast** (same people, different exposures) and **association measure** (different people, different exposures) is the source of confounding bias

## Original Slides

![[assets/Lecture 4_Causal Inference.pdf]]
