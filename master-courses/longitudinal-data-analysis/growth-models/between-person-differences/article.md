---
title: "Between-Person Differences: Level-2 Model and Mixed-Effects Framework"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, growth-models, between-person-differences, level-2-model, mixed-effects, random-effects, fixed-effects, LME]
category: "master-courses/longitudinal-data-analysis/growth-models"
compiled: true
---

## Overview

This lecture introduces the Level-2 model for **interindividual differences in change trajectories** and builds toward the full **Linear Mixed-Effects (LME) model**. Where [[master-courses/longitudinal-data-analysis/growth-models/within-person-change/article.md]] focused on modeling each person's trajectory (Level-1), this lecture asks: why do people's trajectories differ, and how do we model that variation?

The key conceptual advance is combining the Level-1 and Level-2 models into a **composite (mixed-effects) model** that simultaneously handles within-person change and between-person differences.

## Overview of Level-1 and Level-2 Models

### Three Modeling Approaches for Longitudinal Data

Given data $(i, Y_{ij}, t_{ij}, x_{ij1}, \ldots, x_{ijp})$ for subject $i = 1, \ldots, m$ and $j = 1, \ldots, n_i$:

1. **Population model:** One model ignoring repeated measures -- use LOESS or other smoothers to brainstorm parametric forms
2. **Summary statistics:** Compute per-subject statistics (e.g., $\theta_i$ components), then regress on those
3. **Individual models (Level-1):** $Y_{ij} = h_{\theta_i}(t_{ij}, x_{ij1}, \ldots, x_{ijp}) + \epsilon_{ij}$ with subject-specific $\theta_i$ -- the relationship among $\theta_i$ is the **Level-2 model**

### Linear Mixed-Effect Model

For longitudinal data $(Y_{ij}, x_{ij1}, \ldots, x_{ijp})$:

- **Population model:** $Y_{ij} = \beta_0 + \beta_1 x_{ij1} + \cdots + \beta_p x_{ijp} + \epsilon_{ij}$
- **Individual model (Level-1):** $Y_{ij} = \beta_{i0} + \beta_{i1} x_{ij1} + \cdots + \beta_{ip} x_{ijp} + \epsilon_{ij}$

The subject-specific parameters $(\beta_{i0}, \beta_{i1}, \ldots, \beta_{ip})$ are decomposed into:
- **Fixed effects:** Components constant over different $i$
- **Random effects:** Components modeled as independent deviations from population averages $(\beta_0, \beta_1, \ldots, \beta_p)$

## Four LME Models (p=1 Case: Simple Linear Regression)

With Level-1 model $Y_{ij} = \beta_{i0} + \beta_{i1} x_{ij} + \epsilon_{ij}$ where $\epsilon_{ij} \sim N(0, \sigma^2)$:

### Model 1: Random Intercept Only

$$Y_{ij} = \beta_0 + \beta_1 x_{ij} + b_{0i} + \epsilon_{ij}$$

where $b_{0i} \sim N(0, \sigma_{b0}^2)$

### Model 2: Random Slope Only

$$Y_{ij} = \beta_0 + \beta_1 x_{ij} + x_{ij} b_{1i} + \epsilon_{ij}$$

where $b_{1i} \sim N(0, \sigma_{b1}^2)$

### Model 3: Random Intercept + Random Slope (Uncorrelated)

$$Y_{ij} = \beta_0 + \beta_1 x_{ij} + b_{0i} + x_{ij} b_{1i} + \epsilon_{ij}$$

where $b_{0i} \sim N(0, \sigma_{b0}^2)$, $b_{1i} \sim N(0, \sigma_{b1}^2)$, and $b_{0i} \perp b_{1i}$ ($\rho = 0$)

### Model 4: Random Intercept + Random Slope (Correlated)

$$Y_{ij} = \beta_0 + \beta_1 x_{ij} + b_{0i} + x_{ij} b_{1i} + \epsilon_{ij}$$

where $(b_{0i}, b_{1i})$ follow a bivariate normal with mean $(0,0)$ and covariance:

$$\Omega = \begin{pmatrix} \sigma_{b0}^2 & \rho\sigma_{b0}\sigma_{b1} \\ \rho\sigma_{b0}\sigma_{b1} & \sigma_{b1}^2 \end{pmatrix}$$

### Choosing Among Models

There is **no unique answer** -- use:
- Empirical plots for $b_{0i}$ and $b_{1i}$
- Domain knowledge
- Model selection criteria (AIC/BIC)
- Trial and error (start with the most complex; simplify if it does not converge)

## Special Case: p=2 with Time-Invariant Covariate

When $x_{2ij} \equiv x_{2i}$ is constant over $j$ (e.g., gender):

**Approach 1 (useful for practice):**
- Level-1: $Y_{ij} = \beta_{i0} + \beta_{i1} x_{1ij} + \epsilon_{ij}$
- Level-2: $\beta_{i0} = \beta_0 + \beta_2 x_{2i} + b_{0i}$ and $\beta_{i1} = \beta_1 + \beta_3 x_{2i} + b_{1i}$
- Composite: $Y_{ij} = \beta_0 + \beta_1 x_{1ij} + \beta_2 x_{2i} + \beta_3 x_{1ij} x_{2i} + b_{0i} + b_{1i} x_{1ij} + \epsilon_{ij}$

**Approach 2 (useful for theory):** Define interaction $x_{3ij} = x_{1ij} x_{2ij}$, then model directly -- yields the same composite model.

## General Notation for LME

$$Y_{ij} = \beta_1 x_{ij1} + \cdots + \beta_p x_{ijp} + b_{1i} z_{ij1} + \cdots + b_{qi} z_{ijq} + \epsilon_{ij}$$

where:
- $\{z_{ij1}, \ldots, z_{ijq}\}$ is a **subset** of $\{x_{ij1}, \ldots, x_{ijp}\}$
- $\boldsymbol{\beta} = (\beta_1, \ldots, \beta_p)^T$ are **fixed effects**
- $\mathbf{b}_i = (b_{1i}, \ldots, b_{qi})^T$ are **random effects**, i.i.d. multivariate normal with mean $\mathbf{0}$ and covariance $\Omega$
- $\epsilon_{ij} \sim N(0, \sigma^2)$, independent of random effects

### Additive Noise Model

The key statistical idea:

$$\text{Observed Data} = \text{True Value} + \text{Noise}$$

where **Noise = Subject-Random-Effects + Measurement Error**

## Ball Weight Example

Three NYU students (Alice, Bob, Charlie) measure weights of balls A and B with random errors. Each student measures A, B, and A+B, giving the model:

$$\text{Observed} = \text{True Value} + b_i + \epsilon_{ij}$$

where $b_i$ is the subject random effect. In long format with indicators $X_1$ (for A) and $X_2$ (for B):

$$Y_{ij} = A \cdot X_1 + B \cdot X_2 + b_i + \epsilon_{ij}$$

R code: `lmer(Y ~ X1 + X2 - 1 + (1 | ID1), data = data0)` yields $\hat{A} = 1.6264$, $\hat{B} = 2.6264$.

A second scenario (David/Emily/Frank each measure a single quantity multiple times) demonstrates that the grouping structure matters -- sorting by ID1 vs ID2 gives different but equivalent long-format representations.

## Selecting Random Effects

### Using 95% Confidence Intervals

For each component of $\theta_i$ across individuals:
- When 95% CIs **overlap**: treat as the same (**fixed effects**)
- When 95% CIs are **very different**: treat as i.i.d. random variables (**random effects**)

### Practical Strategies

- Empirical plots (95% CIs for individual model parameters)
- Domain knowledge
- Model selection criteria (AIC/BIC)
- Trial and error: if the most complicated model does not converge, try a simpler model

## Orthodont Example: 4 LME Models with R Code

Data: Potthoff and Roy (1964) -- distance from pituitary gland to pterygomaxillary fissure measured every 2 years from age 8 to 14 in 27 children (16 males, 11 females).

### Model 1: Random Intercept Only

$$Y_{ij} = \beta_0 + \beta_1(Age_{ij} - 11) + \beta_2 \cdot Female + \beta_3 \cdot Female \cdot (Age_{ij} - 11) + b_{0i} + \epsilon_{ij}$$

```r
# nlme
lme.A01 <- lme(distance ~ Sex*I(age-11), data=Orthodont, random=~1)
# lme4
lme.B01 <- lmer(distance ~ Sex*I(age-11) + (1|Subject), data=Orthodont)
```

### Model 2: Random Slope Only

```r
# nlme
lme.A02 <- lme(distance ~ Sex*I(age-11), data=Orthodont, random=~I(age-11)-1)
# lme4
lme.B02 <- lmer(distance ~ Sex*I(age-11) + (0+I(age-11)|Subject), data=Orthodont)
```

### Model 3: Both Random, Uncorrelated

```r
# nlme
lme.A03 <- lme(distance ~ Sex*I(age-11), data=Orthodont, random=pdDiag(~I(age-11)))
# lme4
lme.B03 <- lmer(distance ~ Sex*I(age-11) + (1|Subject) + (0+I(age-11)|Subject), data=Orthodont)
```

### Model 4: Both Random, Correlated

```r
# nlme
lme.A04 <- lme(distance ~ Sex*I(age-11), data=Orthodont, random=~I(age-11))
# lme4
lme.B04 <- lmer(distance ~ Sex*I(age-11) + (I(age-11)|Subject), data=Orthodont)
```

## Level-2 Individual Model of Change (Singer & Willet pp. 57-58)

### Purpose

The Level-2 model examines the association between individual growth parameters and **time-invariant covariates** (e.g., how does program participation influence initial cognitive scores and rate of change?).

### Four Important Features

1. We are modeling the **population distribution** of Level-1 growth parameters
2. Growth parameters ($\pi_{0i}$ and $\pi_{1i}$) become the **outcomes** for Level-2 equations
3. Each equation specifies an association between growth parameters and time-invariant covariates
4. Each Level-2 model must allow individuals to **vary** in their growth trajectories

### Formal Specification (Early Intervention Example)

$$\pi_{0i} = \gamma_{00} + \gamma_{01} \cdot PROGRAM_i + \zeta_{0i}$$
$$\pi_{1i} = \gamma_{10} + \gamma_{11} \cdot PROGRAM_i + \zeta_{1i}$$

- $\gamma_{00}$: population average true initial status for nonparticipants
- $\gamma_{01}$: difference in initial status between participants and nonparticipants
- $\gamma_{10}$: population average annual rate of change for nonparticipants
- $\gamma_{11}$: difference in rate of change between participants and nonparticipants
- $\zeta_{0i}, \zeta_{1i}$: Level-2 residuals (individual deviations from group averages)

### Subscript Convention for $\gamma$

- **First subscript:** role in Level-1 model (0 = intercept, 1 = slope)
- **Second subscript:** role in Level-2 model (0 = intercept, 1 = slope)

### Stochastic Component

$$\begin{pmatrix} \zeta_{0i} \\ \zeta_{1i} \end{pmatrix} \sim N\left(\begin{pmatrix} 0 \\ 0 \end{pmatrix}, \begin{pmatrix} \sigma_0^2 & \sigma_{01} \\ \sigma_{10} & \sigma_1^2 \end{pmatrix}\right)$$

- $\sigma_0^2$: Level-2 residual variance in true intercept (population residual variance of initial status, controlling for predictors)
- $\sigma_1^2$: Level-2 residual variance in true slope (population residual variance of rate of change)
- $\sigma_{01}$: Level-2 residual covariance between true intercept and true slope

## Estimating Fixed Effects (Singer & Willet p. 69)

### Early Intervention Results (Table 3.3)

| Parameter | Estimate | SE | z |
|-----------|----------|-----|------|
| $\gamma_{00}$ (initial status, nonparticipant) | 107.84*** | 2.04 | 52.97 |
| $\gamma_{01}$ (PROGRAM effect on initial status) | 6.85* | 2.71 | 2.53 |
| $\gamma_{10}$ (rate of change, nonparticipant) | -21.13*** | 1.89 | -11.18 |
| $\gamma_{11}$ (PROGRAM effect on rate of change) | 5.27* | 2.52 | 2.09 |

**Interpretation:**
- When PROGRAM = 0: $\hat{\pi}_{0i} = 107.84$, $\hat{\pi}_{1i} = -21.13$
- When PROGRAM = 1: $\hat{\pi}_{0i} = 107.84 + 6.85 = 114.69$, $\hat{\pi}_{1i} = -21.13 + 5.27 = -15.86$
- Program participants start 6.85 points higher and decline 5.27 points less per year

### Variance Components

| Component | Estimate |
|-----------|----------|
| Level-1 within-person $\sigma_\epsilon^2$ | 74.24*** |
| Level-2 initial status $\sigma_0^2$ | 124.64*** |
| Level-2 rate of change $\sigma_1^2$ | 12.29 (n.s.) |
| Covariance $\sigma_{01}$ | -36.41 (n.s.) |

- Significant within-person residual variability remains
- Significant between-person variance in initial status persists after controlling for PROGRAM
- No significant residual variance in rates of change (nor residual covariance)

## Composite Model: Alcohol Use Example (Singer & Willet pp. 76-81)

### Setup

- **Outcome:** ALCUSE (alcohol use, 8-point scale)
- **Time-invariant predictors:** COA (child of alcoholic, binary), PEER (proportion of peers who use alcohol)
- **Time variable:** Age (13-17)

### Level-1 and Level-2

- Level-1: $Y_{ij} = \pi_{0i} + \pi_{1i} \cdot TIME_{ij} + \epsilon_{ij}$
- Level-2: $\pi_{0i} = \gamma_{00} + \gamma_{01} \cdot COA_i + \zeta_{0i}$ and $\pi_{1i} = \gamma_{10} + \gamma_{11} \cdot COA_i + \zeta_{1i}$

### Composite Model

$$Y_{ij} = [\gamma_{00} + \gamma_{10} TIME_{ij} + \gamma_{01} COA_i + \gamma_{11}(COA_i \times TIME_{ij})] + [\zeta_{0i} + \zeta_{1i} TIME_{ij} + \epsilon_{ij}]$$

The composite specification:
- Shows how outcome depends simultaneously on Level-1 predictor (TIME) and Level-2 predictor (COA)
- Identifies the **cross-level interaction** ($COA \times TIME$)
- Is mathematically identical to the multilevel specification
- Maps most easily onto person-period data and software packages

## Key Takeaways

- The Level-2 model explains **why** individuals differ in their Level-1 growth parameters using time-invariant covariates
- The four LME model variants (random intercept only, random slope only, both uncorrelated, both correlated) offer increasingly flexible random-effects structures
- Fixed effects assess interindividual differences in trajectories by values of predictors; variance components quantify residual variation at each level
- The composite model = Level-1 + Level-2 = fixed effects + random effects -- it is the specification used by most software
- Model selection for random effects uses empirical plots, domain knowledge, AIC/BIC, and trial-and-error

## Original Slides

![[assets/Updated Lecture 4 - Between Person.pdf]]
