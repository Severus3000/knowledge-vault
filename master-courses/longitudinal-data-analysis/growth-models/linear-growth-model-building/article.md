---
title: "Linear Growth Model Building: From Unconditional to Final Model"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Dr. Cook"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, growth-models, model-building, unconditional-mean-model, unconditional-growth-model, ICC, variance-components, alcohol-use-example]
category: "master-courses/longitudinal-data-analysis/growth-models"
compiled: true
---

## Overview

This lecture by Dr. Cook provides a practical, step-by-step guide to **building linear growth models**. It walks through the complete model-building sequence: starting with unconditional models to understand baseline variation, then progressively adding substantive predictors to reach a "final model." The running example uses adolescent alcohol use data from Singer and Willett's ALDA textbook.

## Prerequisite Knowledge

Before fitting models (Singer & Willet Chapter 3):
1. Examine empirical growth plots and fitted OLS trajectories
2. Verify person-period data set is correct
3. **Do not** jump directly to models with substantive predictors -- first understand the data behavior through unconditional models

## Step 1: Fitting the Unconditional Models (Singer & Willet pp. 92-104)

Two unconditional models serve as baselines:

| Model | Description | Purpose |
|-------|-------------|---------|
| **Unconditional means model** | No predictors at either level | Partition total outcome variation (within vs. between persons) |
| **Unconditional growth model** | TIME as only Level-1 predictor, no Level-2 predictors | Evaluate baseline amount of change |

### Key Questions Answered

1. Is there systematic variation in the outcome worth exploring?
2. If so, where does the variation lie (within, between, or both)?
3. Provides a **baseline for comparison** for subsequent models

## Unconditional Means Model (Model A)

### Specification

$$Y_{ij} = \pi_{0i} + \epsilon_{ij} \quad \text{OR equivalently} \quad Y_{ij} = \gamma_{00} + \zeta_{0i} + \epsilon_{ij}$$

- $\gamma_{00}$: grand mean (fixed effect) -- the population average across all time points and individuals
- $\zeta_{0i}$: the amount person $i$'s mean deviates from the population mean (**between-person**)
- $\epsilon_{ij}$: the amount the response on occasion $j$ deviates from person $i$'s mean (**within-person**)

Distributional assumptions:
- $\epsilon_{ij} \sim N(0, \sigma_\epsilon^2)$
- $\zeta_{0i} \sim N(0, \sigma_0^2)$

### Alcohol Use Results (Model A)

```
xtmixed alcuse || id: , variance mle
```

| Parameter | Estimate | SE |
|-----------|----------|-----|
| $\gamma_{00}$ (grand mean) | 0.922*** | 0.096 |
| $\sigma_0^2$ (between-person variance) | 0.564*** | 0.119 |
| $\sigma_\epsilon^2$ (within-person variance) | 0.562*** | 0.062 |

**Interpretation:**
- Average alcohol use for adolescents aged 14-16 is 0.92 (0.85 when squared)
- Both between-person and within-person variances are significantly different from zero
- Adolescents differ from each other AND vary over time

### Intraclass Correlation Coefficient (ICC)

$$\rho = \frac{\sigma_0^2}{\sigma_0^2 + \sigma_\epsilon^2} = \frac{0.564}{0.564 + 0.562} = 0.50$$

**Interpretation:**
- **50% of total variation** in alcohol use is attributable to differences **between** adolescents
- The ICC also measures autocorrelation in the model -- there is a large amount
- Since both variance components are significant, there is reason to proceed with modeling

## Unconditional Growth Model (Model B)

### Specification

Level-1: $Y_{ij} = \pi_{0i} + \pi_{1i} \cdot TIME_{ij} + \epsilon_{ij}$

Level-2: $\pi_{0i} = \gamma_{00} + \zeta_{0i}$, $\pi_{1i} = \gamma_{10} + \zeta_{1i}$

Composite: $Y_{ij} = \gamma_{00} + \gamma_{10} \cdot TIME_{ij} + [\zeta_{0i} + \zeta_{1i} \cdot TIME_{ij} + \epsilon_{ij}]$

Parameters:
- $\gamma_{00}$: average intercept (fixed effect) -- average true initial status
- $\gamma_{10}$: average slope (fixed effect) -- average true rate of change
- $\zeta_{0i}$: person $i$'s deviation from population intercept
- $\zeta_{1i}$: person $i$'s deviation from population slope
- $\sigma_\epsilon^2$: scatter around each person's own linear trajectory
- $\sigma_0^2$: between-person variability in intercepts
- $\sigma_1^2$: between-person variability in slopes
- $\sigma_{01}$: covariance between $\zeta_{0i}$ and $\zeta_{1i}$

### Alcohol Use Results (Model B)

```
xtmixed alcuse age_14 || id: age_14, cov(un) variance mle
```

**Fixed Effects:**

| Parameter | Estimate | SE | z | p |
|-----------|----------|-----|------|------|
| $\gamma_{00}$ (intercept) | 0.651*** | 0.105 | 6.20 | 0.000 |
| $\gamma_{10}$ (slope, age_14) | 0.271*** | 0.062 | 4.33 | 0.000 |

**Random Effects:**

| Parameter | Estimate | SE |
|-----------|----------|-----|
| $\sigma_1^2$ (var of slope) | 0.151 | 0.056 |
| $\sigma_0^2$ (var of intercept) | 0.624 | 0.148 |
| $\sigma_{01}$ (covariance) | -0.068 | 0.070 |
| $\sigma_\epsilon^2$ (residual) | 0.337 | 0.053 |

**Fitted equation:** $\widehat{ALCUSE} = 0.651 + 0.271(AGE - 14)$

### Key Findings from Model B

- The residual variance declined from 0.562 (Model A) to 0.337 (Model B), suggesting **40% of within-person variation** in alcohol use is associated with linear change in time
- There is significant between-person **residual variance in initial status** ($\sigma_0^2 = 0.624$***)
- There is between-person **residual variance in rate of change** ($\sigma_1^2 = 0.151$**) -- suggests adding Level-2 predictors
- Estimated residual covariance between initial status and change ($\sigma_{01} = -0.068$) is not significant
- Correlation between intercept and slope: -0.22 (weak, negative)

### Standard Deviations

```
xtmixed, stddeviations
```

| Parameter | SD | SE |
|-----------|-----|-----|
| sd(age_14) | 0.389 | 0.073 |
| sd(_cons) | 0.790 | 0.094 |
| corr(age_14, _cons) | -0.223 | 0.188 |
| sd(Residual) | 0.581 | 0.045 |

## Step 2: Model Building to the Final Model (Singer & Willet pp. 104-113)

### Philosophy

- Model building is a **mixture of art and science**
- Guide choices by theory, research, and concepts
- Typical model sequence:
  1. Unconditional mean model
  2. Unconditional growth model
  3. Conditional model with main predictor (question variable)
  4. Conditional model with main predictor + control variables
  5. Simplified "final" model

### Model C: Main IV Growth Model (COA only)

```
xtmixed alcuse i.coa age_14 i.coa#c.age_14 || id: age_14, cov(un) variance mle
```

| Parameter | Model B | Model C |
|-----------|---------|---------|
| $\gamma_{00}$ (intercept) | 0.651*** | 0.316*** |
| $\gamma_{01}$ (COA) | -- | 0.743*** |
| $\gamma_{10}$ (slope) | 0.271*** | 0.293*** |
| $\gamma_{11}$ (COA x slope) | -- | -0.049 (n.s.) |
| $\sigma_\epsilon^2$ | 0.337*** | 0.337*** |
| $\sigma_0^2$ | 0.624*** | 0.488** |
| $\sigma_1^2$ | 0.151** | 0.151* |
| $\sigma_{01}$ | -0.068 | -0.059 |

**Interpretation:**
- Initial ALCUSE for non-COAs is 0.316 (p<.001)
- COAs start 0.743 points higher (p<.001)
- Annual rate of change for non-COAs is 0.293 (p<.001)
- No significant differential in rate of change between COAs and non-COAs (-0.049, n.s.)
- COA "explains" 22% of variation in initial status ($\sigma_0^2$ declined from 0.624 to 0.488)
- Rate of change variance unchanged -- COA explains no variation in change

### Model D: Adding PEER as Control

| Parameter | Model C | Model D |
|-----------|---------|---------|
| $\gamma_{00}$ | 0.316*** | -0.317*** |
| $\gamma_{01}$ (COA) | 0.743*** | 0.579*** |
| $\gamma_{02}$ (PEER) | -- | 0.694*** |
| $\gamma_{10}$ (slope) | 0.293*** | 0.429*** |
| $\gamma_{11}$ (COA x slope) | -0.049 | -0.014 |
| $\gamma_{12}$ (PEER x slope) | -- | -0.150~ |
| $\sigma_0^2$ | 0.488** | 0.241** |
| $\sigma_1^2$ | 0.151* | 0.139* |

**Interpretation:**
- Controlling for PEER, COA effect on initial ALCUSE is 0.579 (p<.001) -- remains significant but attenuated
- PEER: teens whose peers drink more at age 14 also drink more initially (0.694, p<.001)
- Modest negative effect of PEER on rate of change (-0.150, p<.10)
- Together, PEER and COA explain **61.4% of variation in initial status** and **7.9% of variation in rates of change**

### Model E: Removing Non-Significant COA Effect on Change

| Parameter | Model D | Model E |
|-----------|---------|---------|
| $\gamma_{00}$ | -0.317*** | -0.314*** |
| $\gamma_{01}$ (COA) | 0.579*** | 0.571*** |
| $\gamma_{02}$ (PEER) | 0.694*** | 0.695*** |
| $\gamma_{10}$ (slope) | 0.429*** | 0.425*** |
| $\gamma_{12}$ (PEER x slope) | -0.150~ | -0.151~ |
| All VCs | unchanged | unchanged |
| AIC | 608.7 | 606.7 |
| BIC | 632.8 | 628.4 |

**Model E is the tentative "final model":**
- Controlling for PEER, the estimated differential in ALCUSE between COAs and non-COAs is **0.571** (p<.001)
- Controlling for COA, for each 1-point difference in PEER: initial ALCUSE is **0.695 higher** (p<.001) but rate of change is **0.151 lower** (p<.10)
- Variance components are unchanged from Model D -- little is lost by removing the non-significant COA effect on rate of change
- After controlling for PEER and COA, initial status and rate of change are unrelated ($\sigma_{01} \approx 0$)

## Summary of Findings

- Adolescent alcohol usage differs depending on **parental history of alcoholism** (COA) and **peer alcohol consumption** (PEER)
- At each level of peer drinking, children of non-alcoholics had less alcohol use than children of alcoholics
- Regardless of parental drinking status, if peers drank at age 14, adolescent alcohol use increased

## Key Takeaways

- **Always start with unconditional models** before adding substantive predictors -- they establish baseline variation and whether modeling is worthwhile
- The **ICC** from the unconditional means model tells you how much variation lies between vs. within persons
- Moving from unconditional means to unconditional growth model quantifies how much within-person variation is explained by **linear time**
- **Variance component changes** across models reveal what each predictor explains
- Model building is iterative: add predictors guided by theory, examine significance and variance reduction, simplify non-significant terms
- The "final model" should be **parsimonious** while addressing research questions

## Original Slides

![[assets/Lecture 5 - Linear Growth Models by Dr. Cook.pdf]]
