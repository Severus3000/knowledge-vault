---
title: "Time-Varying Covariates in Multilevel Growth Models"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Dr. Stephanie H. Cook"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, advanced-modeling, time-varying-covariates, multilevel-models, growth-models, model-fit]
category: "master-courses/longitudinal-data-analysis/advanced-continuous"
compiled: true
---

# Time-Varying Covariates in Multilevel Growth Models

## Overview

This lecture covers two major topics: (1) model fit review (ICC, ANOVA, deviance, AIC/BIC), and (2) the incorporation of time-varying covariates (TVCs) into multilevel growth models. Time-varying predictors change over time and can influence outcomes at any measurement occasion, unlike time-invariant predictors which remain constant across occasions for each individual. The lecture follows Singer and Willett (ALDA, Chapters 5-6).

## Part 1: Model Fit Review

### Intraclass Correlation (ICC)

The ICC measures how strongly units within the same group resemble each other. In an intercept-random-effects model:

$$Y_{ij} = \beta_0 + \beta_1 x_{1ij} + \cdots + \beta_p x_{pij} + b_{0i} + \epsilon_{ij}$$

The variance and covariance are:

$$Var(Y_{ij}) = \sigma_b^2 + \sigma^2$$

$$Cov(Y_{ij}, Y_{ij'}) = \sigma_b^2$$

Thus:

$$ICC = corr(Y_{ij}, Y_{ij'}) = \frac{\sigma_b^2}{\sigma_b^2 + \sigma^2}$$

**Interpretation:**
- ICC = ratio of between-cluster variance to total variance
- ICC = proportion of total variance in $Y$ accounted for by clustering/grouping
- If ICC = 0, a simpler analysis technique (e.g., standard linear regression) suffices

**Trait vs. State distinction:**
- **Trait**: varies among people but not within a person across occasions (high ICC)
- **State**: varies little among people but varies a lot across occasions (low ICC)

### ANOVA for Model Comparison

For testing $H_0: M_0$ (sub-model) vs. $H_1: M_1$ (larger model) with $p_0 < p_1$ parameters:

**F-test:**

$$F_{obs} = \frac{|\hat{Y}_1 - \hat{Y}_0|^2 / (p_1 - p_0)}{|Y - \hat{Y}_1|^2 / (n - p_1)}$$

Reject $M_0$ if $F_{obs} > F_{p_1 - p_0, n - p_1, \alpha}$.

**Chi-square (deviance) test:**

$$\chi^2_{obs} = D(M_0) - D(M_1)$$

Reject $H_0$ if $\chi^2_{obs} \geq \chi^2_{p_1 - p_0, \alpha}$.

### Deviance

Deviance is a goodness-of-fit statistic (smaller is better):

$$D(M) = -2\log(Y|M) - [-2\log(Y|M_s)] = 2[\log(Y|M_s) - \log(Y|M)]$$

where $M_s$ is the saturated model. In practice: $\text{Deviance} = -2LL_{\text{current model}}$.

**Requirements for deviance-based model comparison:**
1. Models must be nested
2. Same data must be used
3. Same number of cases in both models
4. Use FML when comparing entire models
5. Use REML only when comparing random effects

### AIC/BIC

- **AIC** controls for the increase in model parameters
- **BIC** controls for both number of parameters and sample size
- Models do **not** need to be nested (unlike deviance tests)
- Smaller AIC/BIC = better model
- Under MLE: can use both fixed and random effect parameters
- Under REML: only random effects

## Part 2: Time-Varying Covariates

### Definition

Time-varying predictors (TVCs) change over time and may influence the outcome at any given measurement occasion. Unlike time-invariant predictors (e.g., sex, race), TVCs take different values at each wave.

**Examples:**
- How do changes in parental support influence depression trajectories?
- How does unemployment status affect depression symptomatology over time?

### Running Example: Unemployment and Depression (Ginexi et al., 2000)

- **Sample:** 254 people identified at unemployment offices
- **Design:** 3 waves (1, 5, and 11 months post-job-loss)
- **Outcome:** CES-D depression scale (0-80)
- **Time-varying predictor:** Unemployment status (UNEMP = 1, employed = 0)
- **Time variable:** Months since job loss

### Model Building Taxonomy (Table 5.7)

#### Model A: Unconditional Growth Model

$$Y_{ij} = [\gamma_{00} + \gamma_{10}TIME_{ij}] + [\zeta_{0i} + \zeta_{1i}TIME_{ij} + \varepsilon_{ij}]$$

Results: Average initial depression = 17.67, declining at -0.42 per month. All variance components significant.

#### Model B: Main Effect of TVC

$$Y_{ij} = [\gamma_{00} + \gamma_{10}TIME_{ij} + \gamma_{20}UNEMP_{ij}] + [\zeta_{0i} + \zeta_{1i}TIME_{ij} + \varepsilon_{ij}]$$

Key findings:
- $\gamma_{10} = -0.20$: monthly rate of decline is halved after controlling for UNEMP
- $\gamma_{20} = 5.11$: depression scores are 5.11 points higher when unemployed
- Deviance improved: $\Delta D = 25.5$, 1 df, $p < .001$
- UNEMP explains 9.4% of within-person variance in CES-D

**Important:** The effect is constrained to shift only the trajectory's level (intercept), not its slope.

#### Model C: Interaction with TIME

$$Y_{ij} = \gamma_{00} + \gamma_{10}TIME_{ij} + \gamma_{20}UNEMP_{ij} + \gamma_{30}UNEMP_{ij} \times TIME_{ij} + [\zeta_{0i} + \zeta_{1i}TIME_{ij} + \varepsilon_{ij}]$$

Key findings:
- Main effect of TIME becomes positive and non-significant ($\gamma_{10} = 0.16$, ns)
- UNEMP x TIME interaction is significant ($\gamma_{30} = -0.47$, $p < .05$)
- Model B is a poorer fit ($\Delta D = 4.6$, 1 df, $p < .05$)

Interpretation: the effect of unemployment on depression changes over time -- depression declines only for the unemployed.

#### Model D: Constraining the Reemployed Trajectory

$$Y_{ij} = \gamma_{00} + \gamma_{20}UNEMP_{ij} + \gamma_{30}UNEMP_{ij} \times TIME_{ij} + [\zeta_{0i} + \zeta_{2i}UNEMP_{ij} + \zeta_{3i}UNEMP_{ij} \times TIME_{ij} + \varepsilon_{ij}]$$

Key findings:
- Upon layoff, initial CES-D = 18.15 (= 11.27 + 6.88)
- Unemployed CES-D declines at -0.33/month ($p < .01$)
- Employed trajectory is flat at 11.27
- Best fitting model (lowest AIC = 5113.6, BIC = 5148.9)
- Includes random effects for UNEMP ($\sigma^2_2 = 40.45$) and UNEMP x TIME ($\sigma^2_3 = 0.71$)

### Variance Components with TVCs

**Critical distinction from time-invariant predictors:**

| Predictor Type | $\sigma^2_\varepsilon$ (Level-1) | $\sigma^2_0, \sigma^2_1$ (Level-2) |
|---|---|---|
| Time-invariant | Stays stable | Declines if predictor explains between-person variance |
| Time-varying | Can decrease (interpretable) | Can change in either direction (not directly interpretable) |

With TVCs, all three variance components can change because TVCs vary both between and within persons. You can interpret decreases in the within-person variance component, but **cannot reliably interpret** changes in Level-2 variance components. Instead, focus on Level-1 residuals and goodness-of-fit statistics.

## Part 3: Variably Spaced Measurement Occasions

### Balanced vs. Unbalanced Data
- **Balanced:** Everyone has the same number of timepoints
- **Time-structured:** Timepoints are consistent for all individuals
- Irregularities arise from data collection realities, missing data, or by design (accelerated cohort studies)

### Selecting a Time Variable

Time can be operationalized in multiple ways: wave, target age (AGEGRP), or actual age (AGE). The choice matters:

**CNLSY Reading Example (n = 89):**

| Parameter | AGEGRP - 6.5 | AGE - 6.5 |
|---|---|---|
| Intercept ($\gamma_{00}$) | 21.16*** | 21.06*** |
| Rate of change ($\gamma_{10}$) | 5.03*** | 4.54*** |
| AIC | 1831.9 | 1815.9 |
| BIC | 1846.9 | 1830.8 |

AGE provides better fit (lower AIC/BIC). Treating unstructured data as time-structured introduces error.

### Varying Number of Timepoints

Multilevel models handle unbalanced data (unlike repeated measures ANOVA). The NLSY wages example (n = 888) demonstrates individuals with 1 to 13 timepoints and unequally spaced measurements.

## Part 4: Discontinuous Individual Change

### Conceptualizing Discontinuity

Discontinuity requires knowing **why** and **when** the change occurs. Two types:
1. Immediate shift in **slope only** (Model C)
2. Immediate shift in both **elevation and slope** (Model D)

### GED and Wage Trajectories (Murnane et al., 1999)

Four possible discontinuous trajectories upon GED receipt:
- **A:** No effect (linear trajectory continues)
- **B:** Elevation shift only: $Y_{ij} = \pi_{0i} + \pi_{1i}EXPER_{ij} + \pi_{2i}GED_{ij} + \varepsilon_{ij}$
- **C:** Slope shift only: $Y_{ij} = \pi_{0i} + \pi_{1i}EXPER_{ij} + \pi_{3i}POSTEXP_{ij} + \varepsilon_{ij}$
- **D:** Both elevation and slope shift: $Y_{ij} = \pi_{0i} + \pi_{1i}EXPER_{ij} + \pi_{2i}GED_{ij} + \pi_{3i}POSTEXP_{ij} + \varepsilon_{ij}$

where POSTEXP = work experience accumulated after GED receipt (0 before GED).

### Model Selection (Table 6.2)

Model F (both GED and POSTEXP, with random effects for intercept, EXPER, and POSTEXP) provides the best fit with Deviance = 4789.4. The model comparison approach uses deviance differences tested against chi-square distributions.

### Other Extensions

- Effects can depend on **timing** of GED receipt
- Non-linear changes before/after the transition point
- Effects may be **instantaneous** but not enduring
- Effects may be **delayed**
- Multiple transition points possible

## Practical Considerations

- **Boundary constraints:** Negative variance estimates or "Hessian is not negative semidefinite" errors -- simplify the model
- **Nonconvergence:** Model too complex, poorly specified, or insufficient data -- increase iterations or simplify
- **Missing data:** MCAR (preferred), MAR (can model under conditions), MNAR (need different technique)

## Key Takeaways

1. TVCs enter the model at Level 1 and shift the trajectory's level; interactions with TIME allow TVCs to also affect the slope
2. Variance component interpretation changes fundamentally with TVCs -- focus on Level-1 residuals and fit statistics, not Level-2 variance components
3. Selecting the right time variable is critical for variably spaced data -- use AIC/BIC to compare non-nested time representations
4. Multilevel models naturally handle unbalanced data, but severe imbalance can cause convergence issues
5. Discontinuous change models use time-varying indicators (GED, POSTEXP) to capture shifts in elevation and/or slope at known transition points
6. Model building is sequential: start unconditional, add main effects, test interactions, compare with deviance/AIC/BIC

## Original Slides

![[assets/Lecture 8a - Time-varying covariates.pdf]]
