---
title: "Fixed Effects Models for Longitudinal Data"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, fixed-effects, panel-data, within-estimator, dummy-variables]
category: "master-courses/longitudinal-data-analysis/logistic-longitudinal"
compiled: true
---

## Overview

This lecture introduces fixed-effects models as an alternative to random-effects models for longitudinal data. Fixed-effects models allow each subject to have their own intercept (treated as fixed, unknown parameters) while constraining a common slope. This approach controls for all time-invariant unobserved confounders without distributional assumptions on the subject effects.

## Recall: Random-Effects Model

**Data**: $(Y_{ij}, X_{1ij}, X_{2i}, \ldots, X_{pi})$ for $i = 1, \ldots, m$ and $j = 1, \ldots, n_i$.

**Random-Effects Model** (two-level):

- **Level 1**: $Y_{ij} = \beta_{0i} + \beta_{1i} X_{1ij} + \epsilon_{ij}$
- **Level 2** (many scenarios):
  - Random intercepts only: $\beta_{0i} = \beta_0 + b_{0i}$, $\beta_{1i} \equiv \beta_1$
  - Random intercepts with level-2 predictors: $\beta_{0i} = \beta_0 + \beta_{02}X_{2i} + \cdots + \beta_{0p}X_{pi} + b_{0i}$, $\beta_{1i} \equiv \beta_1$
  - Random slopes: $\beta_{0i} \equiv \beta_0$, $\beta_{1i} = \beta_1 + \beta_{12}X_{2i} + \cdots + \beta_{1p}X_{pi} + b_{1i}$
  - Both random intercepts and slopes (correlated or uncorrelated)

where $b_{0i} \sim N(0, \sigma_{0b}^2)$ and $b_{1i} \sim N(0, \sigma_{1b}^2)$.

## Fixed-Effects Model

$$Y_{ij} = \beta_{0i} + \beta_1 X_{1ij} + \epsilon_{ij}$$

**Key properties**:

- All individuals share the **same slope** $\beta_1$
- Each individual has a **different intercept** $\beta_{0i}$ (treated as a fixed parameter, not random)
- Controls for a long list of **unobserved variables** $(X_{2i}, \ldots, X_{pi})$ that are fixed over time
- Similar ideas appear in Cox's proportional hazards model in survival analysis

**Advantage**: No distributional assumptions on $\beta_{0i}$ -- unlike random-effects models which assume $b_{0i} \sim N(0, \sigma^2)$.

## Parameter Estimation

Two equivalent methods to estimate $\beta_1$ (and $\beta_{0i}$):

### Method 1: Absorbing the Fixed Effects (Within Estimator)

**Key idea**: Subtract subject means to eliminate $\beta_{0i}$.

$$Y_{ij} = \beta_{0i} + \beta_1 X_{1ij} + \epsilon_{ij}$$

$$\bar{Y}_i = \beta_{0i} + \beta_1 \bar{X}_{1i} + \bar{\epsilon}_i$$

Subtracting:

$$Y_{ij} - \bar{Y}_i = \beta_1 (X_{1ij} - \bar{X}_{1i}) + (\epsilon_{ij} - \bar{\epsilon}_i)$$

**Implementation**: Create a new dataset with centered variables:

$$Y_{ij}^* = Y_{ij} - \bar{Y}_i, \quad X_{ij}^* = X_{1ij} - \bar{X}_{1i}$$

Then run a simple linear regression **without intercept**:

$$Y^* = \beta_1 X^* + \epsilon^*$$

```r
lm(Ystar ~ Xstar - 1, newdata1)
```

### Method 2: Adding Binary Indicator Variables

**Key idea**: Rewrite the model using subject dummy variables.

$$Y_{ij} = \beta_{0i} + \beta_1 X_{1ij} + \epsilon_{ij} = \beta_{01} + (\beta_{0i} - \beta_{01}) + \beta_1 X_{1ij} + \epsilon_{ij}$$

**Implementation**: Set the ID variable as a factor and include it in the regression:

$$Y_{ij} = \beta_0' + \beta_2' \cdot ID_i + \beta_1' X_{1ij} + \epsilon_{ij}'$$

```r
lm(Y ~ factor(ID) + X, data0)
```

Both methods yield **identical estimates** of $\beta_1$.

## Key Takeaways

- Fixed-effects models treat subject-specific intercepts as fixed parameters, not random variables
- The within estimator (method 1) removes all time-invariant confounders by demeaning
- The dummy variable approach (method 2) is equivalent but includes $m-1$ indicator variables
- Fixed effects cannot estimate coefficients for time-invariant predictors (they are absorbed)
- No distributional assumption on $\beta_{0i}$ is required -- more robust than random effects in this regard
- Choice between fixed and random effects depends on whether the subject effects are correlated with covariates (Hausman test)

## Original Slides

![[assets/9.6.fixed effects models.pdf]]
