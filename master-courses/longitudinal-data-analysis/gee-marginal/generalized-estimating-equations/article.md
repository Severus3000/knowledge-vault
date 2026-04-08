---
title: "Generalized Estimating Equations (GEE) Models and Methods"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, gee, marginal-models, glm, correlation-structures, semi-parametric, geepack]
category: "master-courses/longitudinal-data-analysis/gee-marginal"
compiled: true
---

## Overview

Generalized Estimating Equations (GEE) extend the Generalized Linear Model (GLM) framework to handle **dependent/correlated data**, such as longitudinal or clustered observations. First proposed by **Liang and Zeger (Biometrika, 1986)** -- one of the most cited statistical papers (22,255 citations as of April 2025) -- GEE is a **semi-parametric** approach whose primary goal is estimating population-averaged regression coefficients $(\beta_0, \ldots, \beta_p)$ without requiring full specification of the joint distribution.

## Background: From GLM to GEE

### Recall: Generalized Linear Model (GLM)

For independent data $(Y_i, X_{1i}, \ldots, X_{pi})$, $i = 1, \ldots, m$, the GLM specifies:

1. A **distribution** for the response $Y_i$ (with mean $\mu_i$)
2. A **link function** connecting $\mu_i$ to predictors:

$$g(\mu_i) = \beta_0 + \beta_1 X_{1i} + \cdots + \beta_p X_{pi}$$

Three special cases:

| Response type | Distribution | Link function $g(\mu_i)$ |
|---|---|---|
| Continuous | $Y_i \sim N(\mu_i, \sigma^2)$ | $g(\mu_i) = \mu_i$ (identity) |
| Binary/Binomial | $Y_i \sim \text{Bernoulli}(n_i, \pi_i)$ | $g(\pi_i) = \log\frac{\pi_i}{1 - \pi_i}$ (logit) |
| Count | $Y_i \sim \text{Poisson}(\mu_i)$ | $g(\mu_i) = \log \mu_i$ (log) |

### The Standard GLM and Exponential Family

The standard GLM assumes $Y_i$'s are **independent** with density from a one-parameter exponential family:

$$f_\theta(y) = f_0(y) \exp(\theta y - b(\theta))$$

where $E_\theta(Y) = b'(\theta)$ and $Var_\theta(Y) = b''(\theta)$. Estimation uses **maximum likelihood (MLE)**.

### The Problem: Dependent Data

Standard GLM assumes independence, but longitudinal data has repeated measures within subjects:

- **Data:** $(ID, Y_{ij}, X_{1ij}, \ldots, X_{pij})$ for $i = 1, \ldots, m$ subjects and $j = 1, \ldots, n_i$ observations per subject

## GEE Model Specification

### Key Assumptions

GEE requires specifying only:

1. **Mean structure** (same as GLM):
   - Linear: $E(Y_i) = \mu_i = \beta_0 + \beta_1 X_{1i} + \cdots + \beta_p X_{pi}$
   - Logistic: $\log\frac{\mu_i}{1-\mu_i} = \beta_0 + \beta_1 X_{1i} + \cdots + \beta_p X_{pi}$
   - General: $g(\mu_i) = \beta_0 + \beta_1 X_{1i} + \cdots + \beta_p X_{pi}$

2. **Mean-variance relationship** $V(\mu)$:
   - e.g., for logistic GEE: $Var(Y) = \phi\mu(1 - \mu)$

3. **Working correlation matrix** $W_i$ for the response vector $Y_i = (Y_{i1}, \ldots, Y_{i,n_i})^T$

The key insight: the working correlation can be **different from the true** $\text{corr}(Y_i)$ -- it is acceptable to mis-specify the covariance-variance matrix.

### Variance/Correlation Structure

For the response vector, we specify $Var(Y_i) = \Omega_i$ as an $n_i \times n_i$ matrix.

For example, with a random-intercept linear mixed-effects model $Y_{ij} = \beta_0 + \beta_1 X_{1i} + \cdots + \beta_p X_{pi} + b_i + \epsilon_{ij}$:

$$\Omega_i = \begin{pmatrix} \sigma_b^2 + \sigma_\epsilon^2 & \cdots & \sigma_b^2 \\ \vdots & \ddots & \vdots \\ \sigma_b^2 & \cdots & \sigma_b^2 + \sigma_\epsilon^2 \end{pmatrix} = \sigma_\epsilon^2 \begin{pmatrix} 1/\theta^2 + 1 & \cdots & 1/\theta^2 \\ \vdots & \ddots & \vdots \\ 1/\theta^2 & \cdots & 1/\theta^2 + 1 \end{pmatrix}$$

## Parameter Estimation

### When $\Omega_i$ is Known

For linear regression, minimize the weighted sum of squares:

$$WSS = \sum_{i=1}^{m} (Y_i - \mu_i)^T \Omega_i^{-1} (Y_i - \mu_i)$$

Taking derivatives with respect to $\beta_h$ yields:

$$\sum_{i=1}^{m} \frac{\partial \mu_i}{\partial \beta_h} \Omega_i^{-1} (Y_i - \mu_i) = 0$$

### When $\Omega_i$ is Unknown: The GEE Solution

Replace the unknown $\Omega_i$ with a **working matrix** $\sigma^2 W_i$.

### Score-like Equations

For MLE in GLM, the score equation for each parameter $h$:

$$\sum_{i=1}^{m} \frac{\partial \mu_i}{\partial \beta_h} [Var(Y_i)]^{-1} [Y_i - \mu_i] = 0$$

The GEE form is analogous -- replace $Var(Y_i)$ with the working covariance matrix $W_i$:

$$\sum_{i=1}^{m} \frac{\partial \mu_i}{\partial \beta_h} [W_i]^{-1} [Y_i - \mu_i] = 0$$

## Working Correlation Structures

The most common choices for $W_i$:

| Structure | Description | Parameters |
|---|---|---|
| **Independence** | No correlation between time points | 0 |
| **Exchangeable** | Same correlation $\rho$ for all time pairs | 1 ($\rho$) |
| **Autoregressive (AR)** | Correlation declines exponentially with time lag: $\rho^{|t_j - t_k|}$ | 1 ($\rho$) |
| **Unstructured** | Different correlation for each pair | $n(n-1)/2$ |

### How to Choose a Correlation Structure

- **Start with exchangeable** -- if patterns emerge, try a different structure
- Use domain knowledge (e.g., prior work, statistical theory) to guide the choice
- AR assumes constant time intervals between occasions

## Effects of Mis-specifying the Correlation Structure

- Generally **not too striking** for point estimates
- **Standard error estimates** are more often affected than parameter estimates
- Can have effects on both standard errors and parameter estimates in some cases
- The sandwich (robust) variance estimator provides protection against mis-specification

## Interpretation of GEE Models

When using GEE for logistic regression with correlated dichotomous responses, interpretation is similar to standard logistic regression:

**Similarities with standard GLM:**
- Point estimates
- Odds ratio (OR) estimates
- Confidence intervals
- Wald test statistics

**Differences:**
- Underlying assumptions (allows correlated data)
- Method of parameter estimation (quasi-likelihood rather than full MLE)
- Coefficients have a **population-averaged (marginal)** interpretation

## R Packages Comparison

| Package | Purpose | Syntax |
|---|---|---|
| **lme4** | Linear mixed effects (multilevel/hierarchical models with fixed + random effects) | `lmer(Y ~ X1 + X2 + (1|id), data)` |
| **plm** | Economic panel data (observations over time for same units) | `plm(Y ~ X1 + X2, index=c("id","time"), data)` |
| **geepack** | GEE models | `geeglm(...)` |

## Key Takeaways

1. GEE is a **semi-parametric, marginal (population-averaged)** approach -- it does not model individual-level random effects
2. Only requires correct specification of the **mean structure** -- the working correlation matrix does not need to be correct for consistent $\hat{\beta}$
3. Robust (sandwich) standard errors protect against correlation mis-specification
4. Four common working correlation structures: independence, exchangeable, AR, unstructured
5. Coefficients are interpreted the same way as in standard GLM (OR, CI, Wald tests) but represent **population-averaged** effects
6. Implemented in R via `geeglm()` in the **geepack** library

## Original Slides

![[assets/Lecture 10a - GEE.pdf]]
