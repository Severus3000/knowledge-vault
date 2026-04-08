---
title: "Selecting an Estimator: MLE vs REML in Linear Mixed-Effects Models"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, estimation, MLE, REML, linear-mixed-effects, model-fitting, random-effects, variance-components]
category: "master-courses/longitudinal-data-analysis/estimation-model-fit"
compiled: true
---

# Selecting an Estimator: MLE vs REML in Linear Mixed-Effects Models

Lecture 6 (Feb 27, 2025) covers the foundational estimation procedures for linear mixed-effects (LME) models, introducing both Maximum Likelihood Estimation (MLE) and Restricted Maximum Likelihood (REML), with a worked "ball weight" example that builds intuition for how these estimators operate computationally.

## Overview

The lecture bridges from the previous session's introduction of LME model fitting to a deeper understanding of how MLE and REML work mathematically and computationally. It then introduces the model-building workflow: unconditional models first, then building toward a final model.

## The Linear Mixed-Effects Model

The simple LME model for data $(Y_{ij}, x_{ij1}, \ldots, x_{ijp})$ with $i = 1, \ldots, m$ subjects and $j = 1, \ldots, n_i$ observations:

$$Y_{ij} = \beta_1 x_{ij1} + \cdots + \beta_p x_{ijp} + b_i + \epsilon_{ij}$$

where:
- $b_i \sim N(0, \sigma_b^2)$ are random effects (between-subject)
- $\epsilon_{ij} \sim N(0, \sigma^2)$ are measurement errors (within-subject)
- $b_i$ and $\epsilon_{ij}$ are independent

## MLE: Mathematical Formulation

**MLE** finds $(\beta_1, \ldots, \beta_p, \sigma_b, \sigma)$ that maximizes the likelihood function:

$$L(\beta_1, \ldots, \beta_p, \sigma_b, \sigma) = \prod_{i=1}^{m} f(Y_{i1}, \ldots, Y_{i,n_i})$$

## REML: Mathematical Formulation

**REML** finds $(\sigma_b, \sigma)$ that maximizes the restricted likelihood:

$$L_{RE}(\sigma_b, \sigma) = \iiint L(\beta_1, \ldots, \beta_p, \sigma_b, \sigma) \, d\beta_1 \cdots d\beta_p$$

Then, with estimated $(\hat{\sigma}_b, \hat{\sigma})$, find $(\beta_1, \ldots, \beta_p)$ that maximizes $L(\beta_1, \ldots, \beta_p, \hat{\sigma}_b, \hat{\sigma})$.

## Computational Algorithm (MLE/REML)

The key parameter is $\theta = \sigma / \sigma_b$.

1. Given $\theta$, find $(\beta_1, \ldots, \beta_p)$ and $(b_1, \ldots, b_m)$ that minimize the penalized RSS:

$$RSS(\theta) = \sum_{i=1}^{m} \left( \sum_{j=1}^{n_i} (Y_{ij} - (\beta_1 x_{ij1} + \cdots + \beta_p x_{ijp} + b_i))^2 + \theta^2 b_i^2 \right)$$

2. Estimate $\hat{\sigma}^2$:
   - **REML**: $\hat{\sigma}_\theta^2 = \frac{RSS(\theta)}{N - p}$
   - **MLE**: $\hat{\sigma}_\theta^2 = \frac{RSS(\theta)}{N}$

3. Find $\theta$ that maximizes $L_{RE}(\theta)$ (REML) or $L(\hat{\beta}(\theta), \hat{\sigma}_\theta / \theta, \hat{\sigma}_\theta)$ (MLE).

This is equivalent to running standard linear regression on an augmented dataset with $n_1 + \cdots + n_m + m$ data points, including pseudo-observations $(0, 0, \ldots, 0, \ldots, \theta, \ldots)$ for each subject.

## Ball Weight Example

Two students (Jack and Kathy) measure two balls (A, B):
- Jack: measures A (2 lbs) and B (4 lbs)
- Kathy: measures B (3 lbs) and A+B (5 lbs)

**Model**: Observed Data = True Value + Subject Random Effect + Measurement Error

$$2 = Y_{11} = A + b_1 + \epsilon_{11}$$
$$4 = Y_{12} = B + b_1 + \epsilon_{12}$$
$$3 = Y_{21} = B + b_2 + \epsilon_{21}$$
$$5 = Y_{22} = A + B + b_2 + \epsilon_{22}$$

### R Code

```r
data1 <- rbind(c(1,2,1,0), c(1,4,0,1), c(2,3,0,1), c(2,5,1,1))
colnames(data1) <- c("ID", "Y", "X1", "X2")
data1 = data.frame(data1)
data1lme1 <- lmer(Y ~ X1 + X2 - 1 + (1 | ID), data=data1)
summary(lme1)
```

### REML Results
- **Fixed effects**: $\hat{A} = 1.80$, $\hat{B} = 3.65$
- **Random effects**: $\hat{b}_1 = 0.25$, $\hat{b}_2 = -0.50$
- **Variance**: ID (Intercept) = 0.25, Residual = 0.05
- $\hat{\theta} = 0.2236 / 0.5000 = 0.4472$

### Verification via Linear Regression

Using the augmented data approach with $\theta = \sqrt{0.05/0.25} = \sqrt{1/5}$:

```r
theta = sqrt(0.05/0.25)
data2 <- rbind(c(2,1,0,1,0), c(4,0,1,1,0), c(0,0,0,theta,0),
               c(3,0,1,0,1), c(5,1,1,0,1), c(0,0,0,0,theta))
lm(Y ~ . -1, data=data2)
# Coefficients: A=1.80, B=3.65, b1=0.25, b2=-0.50
```

The RSS = 0.1, and $\hat{\sigma}^2 = RSS/(n-p) = 0.1/(4-2) = 0.05$ (matching REML output).

## Comparison of MLE and REML

| Aspect | REML | MLE |
|--------|------|-----|
| Variance estimation | Less biased (divides by $N-p$) | Biased downward (divides by $N$) |
| Best use | Parameter inference | Model selection (AIC/BIC) |
| When they differ | Large $p$ relative to $N$ | Large $p$ relative to $N$ |
| Information criteria | Cannot use for model comparison | Can use AIC/BIC/log-likelihood |

**Key rule**: REML is better for inference on parameters; MLE is better for model selection.

## Model Building Workflow

### Step 1: Unconditional Models

**Unconditional Mean Model**: $Y_{ij} = \gamma_{00} + \zeta_{0i} + \epsilon_{ij}$
- $\gamma_{00}$ = grand mean (fixed effect)
- $\zeta_{0i} \sim N(0, \sigma_0^2)$ = between-person deviation
- $\epsilon_{ij} \sim N(0, \sigma_\epsilon^2)$ = within-person deviation

**Unconditional Growth Model**: $Y_{ij} = \gamma_{00} + \gamma_{10} \cdot time_{ij} + \zeta_{0i} + \zeta_{1i} \cdot time_{ij} + \epsilon_{ij}$
- $\gamma_{00}$ = average intercept, $\gamma_{10}$ = average slope
- $\zeta_{0i}$ = person-specific intercept deviation
- $\zeta_{1i}$ = person-specific slope deviation
- Covariance between $\zeta_{0i}$ and $\zeta_{1i}$: $\rho \sigma_0 \sigma_1$

### Step 2: Build to Final Model
- Predictor-only model
- Predictor with control variable model
- "Final" model

## Exploratory Data Analysis

The lecture emphasizes using person-period ("long") data format and examining:
1. **Empirical growth plots** (scatter of individual trajectories)
2. **Non-parametric smoothing** (LOWESS) to let data speak
3. **Parametric OLS trajectories** superimposed on individual plots
4. **Overall mean trajectory line** across all participants

These visualizations help determine: Is there growth? What functional form? Who is increasing/decreasing?

## Key Takeaways

1. REML produces less biased variance estimates than MLE, especially when $p/N$ is not negligible
2. MLE enables model comparison via AIC/BIC/log-likelihood -- REML cannot
3. The computational algorithm reduces LME estimation to a sequence of linear regressions on augmented data
4. Always start with unconditional models before adding predictors
5. The ratio $\theta = \sigma/\sigma_b$ is the key parameter controlling the penalty on random effects

## Original Slides

![[assets/Lecture 6 - Spring2025.Selecting an Estimator, Model Fit, and Testing Assumptions.pdf]]
