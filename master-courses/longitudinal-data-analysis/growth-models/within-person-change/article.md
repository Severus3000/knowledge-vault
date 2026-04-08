---
title: "Within-Person Change: Level-1 Individual Growth Models"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, growth-models, within-person-change, level-1-model, OLS, MLE, individual-growth-model]
category: "master-courses/longitudinal-data-analysis/growth-models"
compiled: true
---

## Overview

This lecture introduces the Level-1 individual growth model for longitudinal data, which describes **within-person change** over time. It bridges from basic statistical models (without and with covariates) to the multilevel framework needed for repeated-measures data, where observations are nested within individuals.

The central motivation: standard regression assumes independent observations, but longitudinal data violates this because repeated measures on the same person are correlated. The Level-1 model addresses this by fitting an individual trajectory for each subject.

## Review of Basic Models

### Models Without Covariates

- **Data:** Observe $Y_i$ for $i = 1, \ldots, n$
- **Model:** $Y_1, Y_2, \ldots, Y_n$ are i.i.d. with pdf $f_\theta(\cdot)$, e.g., $N(\mu, \sigma^2)$ or $\text{Bernoulli}(p)$
- **Statistical inference** on $\theta$:
  - **Point estimation** via Method of Moments or Maximum Likelihood
  - **Hypothesis testing:** $H_0: \theta = \theta_0$ vs $H_1: \theta \neq \theta_0$
  - **Confidence intervals:** $\theta \in [\hat{\theta}_L, \hat{\theta}_U]$

### Cross-Sectional vs. Longitudinal: Two-Sample Tests

A key distinction is between **independent samples** (cross-sectional) and **paired samples** (longitudinal):

- **Independent two-sample t-test:** pooled variance $s_p^2 = \frac{(m-1)s_1^2 + (n-1)s_2^2}{m+n-2}$, test statistic $T_{obs} = \frac{\bar{Y}_2 - \bar{Y}_1}{s_p\sqrt{\frac{1}{m}+\frac{1}{n}}}$
- **Paired two-sample t-test:** uses differences $d_i = Y_{2i} - Y_{1i}$, test statistic $T'_{obs} = \frac{\bar{d}}{s_d / \sqrt{n}}$

**Drug relief example:** The same data yields p = 0.2961 (independent test, not significant) vs p = 0.0484 (paired test, significant). Same data, different conclusions -- because the paired test accounts for within-subject correlation.

### Models With Covariates

- **Data:** Observe $(Y_i, x_{i1}, \ldots, x_{ip})$ for $i = 1, \ldots, n$
- **Linear regression:** $Y_i = \beta_0 + \beta_1 x_{i1} + \cdots + \beta_p x_{ip} + \epsilon_i$
- **Logistic regression** for binary outcomes: $\log\frac{p_i}{1-p_i} = \beta_0 + \beta_1 x_{i1} + \cdots + \beta_p x_{ip}$

### MLE in Simple Linear Regression

For $Y_i = \beta_0 + \beta_1 x_i + \epsilon_i$ where $\epsilon_i \sim N(0, \sigma^2)$:

$$\hat{\beta}_1 = \frac{S_{xy}}{S_{xx}}, \quad \hat{\beta}_0 = \bar{Y} - \hat{\beta}_1 \bar{x}$$

where $S_{xy} = \sum x_i Y_i - n\bar{x}\bar{Y}$ and $S_{xx} = \sum x_i^2 - n(\bar{x})^2$.

Maximizing the likelihood is equivalent to minimizing the Residual Sum of Squares:

$$RSS(\beta_0, \beta_1) = \sum_{i=1}^{n}(Y_i - \beta_0 - \beta_1 x_i)^2$$

### Optimization Algorithms for MLE

- **Gradient descent** (first-order, used in ML): $\theta_{new} = \theta_{old} - \lambda L'(\theta)\big|_{\theta_{old}}$
- **Newton's algorithm** (second-order, used in statistics): $\theta_{new} = \theta_{old} - [L''(\theta)]^{-1} L'(\theta)\big|_{\theta_{old}}$

## Data in Longitudinal Studies

### Notation

- **Wide format:** (ID, outcome.1, ..., outcome.m, X1, X2, ..., Xp)
- **Long format:** (ID, Outcome, Time, X1, X2, ..., Xp)
- **Mathematical notation:** Observe $(i, Y_{ij}, t_{ij}, x_{ij1}, \ldots, x_{ijp})$ for subject $i = 1, \ldots, m$ and occasion $j = 1, \ldots, n_i$

### Special Cases

1. When $n_i \equiv 1$: reduces to standard regression
2. When $n_i \equiv 2$ with pre/post measurements: reduces to paired samples

## Naive Approaches to Longitudinal Data

Three possible strategies:

1. **One population model** ignoring repeated measures: $Y_{ij} = h_\theta(t_{ij}, x_{ij1}, \ldots, x_{ijp}) + \epsilon_{ij}$ -- violates independence assumption
2. **Summary statistics** per subject, then regress on those -- loses information
3. **Individual models** with different $\theta_i$ per subject: $Y_{ij} = h_{\theta_i}(t_{ij}, x_{ij1}, \ldots, x_{ijp}) + \epsilon_{ij}$ -- this is the Level-1 model, and modeling the relationship among $\theta_i$ gives the Level-2 model

## Key Takeaways from Descriptive Analyses

Before fitting models, examine (Singer & Willet pp. 35-37):

1. **Sample means** of estimated intercepts and slopes -- unbiased estimates of the average observed change trajectory
2. **Sample variances** (standard deviations) of estimated intercepts and slopes -- estimate interindividual heterogeneity in change
3. **Correlation** between estimated intercepts and slopes -- whether initial status and rate of change are related

**Tolerance example:** Mean intercept = 1.36, mean slope = 0.13, SD intercept = 0.30, SD slope = 0.17, correlation = -0.45 (adolescents with high initial tolerance become more tolerant less rapidly).

### Time-Invariant Predictors

Plotting trajectories by groups (e.g., male vs. female, low vs. high exposure) reveals whether predictors affect initial status and/or rate of change.

## The Level-1 Model (Singer & Willet pp. 49-55)

### Motivation

We always model two levels of change:
- **Level-1:** within-person change (individual change over time)
- **Level-2:** between-person differences in change (how changes vary across individuals)

### Formal Specification

For each individual $i$, the Level-1 model is:

$$Y_{ij} = [\pi_{0i} + \pi_{1i}(AGE_{ij} - 1)] + [\epsilon_{ij}]$$

where:
- $Y_{ij}$: outcome for person $i$ at time $j$
- $\pi_{0i}$: person $i$'s true initial status (intercept)
- $\pi_{1i}$: person $i$'s true rate of change (slope)
- $\epsilon_{ij}$: random measurement error for person $i$ at time $j$

### Structural and Stochastic Components

- **Structural part:** $\pi_{0i} + \pi_{1i}(AGE_{ij} - 1)$ -- specifies the shape of the true trajectory (linear)
- **Stochastic part:** $\epsilon_{ij}$ -- the residual (measurement error)

### Assumptions on Residuals

$$\epsilon_{ij} \sim N(0, \sigma_\epsilon^2)$$

Key assumptions:
1. Residuals are independently and identically distributed
2. Homoscedastic variances across time and individuals
3. Normally distributed

**Common violations in longitudinal data:**
- Autocorrelation (occasion 1 is related to occasion 2)
- Systematic differences between IV and DV at different time points

### Generalization

For each subject $i$, use its own $n_i$ observations to build an individual model with parameter vector $\theta_i$:

$$Y_{ij} = h_{\theta_i}(t_{ij}, x_{ij1}, \ldots, x_{ijp}) + \epsilon_{ij}$$

Some components of $\theta_i$ might be the same across subjects (**fixed effects**), while others might be i.i.d. (**random effects**).

## Examples

### Example 1: Early Intervention and Cognitive Performance

- **Data:** 103 African American infants from low-income families (Burchinal et al., 1997)
- Randomized to intensive early intervention (n=58) or control (n=45)
- Cognitive scores measured at ages 12, 18, and 24 months
- Trajectories generally declining, mostly linear
- Level-1 model: $Y_{ij} = \pi_{0i} + \pi_{1i}(AGE_{ij} - 1) + \epsilon_{ij}$

### Example 2: Trajectories of Depression

- **Data:** National Longitudinal Study of Adolescent to Adult Health (Add Health), N ~ 6,500
- **Research question:** Are there biological sex differences in depression trajectories?
- Level-1: $\text{Depression}_{ij} = \pi_{0i} + \pi_{1i} \cdot Time_{ij} + \epsilon_{ij}$
- Average estimated intercept = 0.91, average estimated slope = -0.12
- Correlation between intercept and slope = -0.42 (those starting with high depression decrease less rapidly)

### Example 3: HIV Viral Dynamics

- Two-phase linear model for determining viral set point:

$$Y_{ij} = \begin{cases} \beta_{0i} - \beta_{1i} t_{ij} + \epsilon_{ij} & \text{if } t_{ij} < v_i \\ u_i + \epsilon_{ij} & \text{if } t_{ij} \geq v_i \end{cases}$$

- Continuity constraint: $\beta_{0i} - \beta_{1i} v_i = u_i$
- Compact form: $Y_{ij} = u_i - \beta_{1i}\min(t_{ij} - v_i, 0) + \epsilon_{ij}$

## Key Takeaways

- The Level-1 model captures **within-person change** as an individual-specific trajectory over time
- Each person gets their own intercept ($\pi_{0i}$) and slope ($\pi_{1i}$)
- The structural part specifies the functional form (usually linear as a starting point)
- The stochastic part ($\epsilon_{ij}$) captures measurement error, assumed i.i.d. $N(0, \sigma_\epsilon^2)$
- Longitudinal data requires paired (not independent) analysis -- the same data can yield different conclusions depending on the test used
- Descriptive analysis (means, variances, correlations of OLS-estimated intercepts and slopes) should always precede formal modeling
- The Level-1 model sets up the foundation for the Level-2 model, which explains **why** individuals differ in their growth parameters

## Original Slides

![[assets/Updated Lecture 3 - Within person change.pdf]]
