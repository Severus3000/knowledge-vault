---
title: "Random Effects Logistic Regression: From Marginal to Subject-Specific Models"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, logistic-regression, random-effects, marginal-model, GLMM, laplace-approximation, lme4]
category: "master-courses/longitudinal-data-analysis/logistic-longitudinal"
compiled: true
---

## Overview

This lecture extends logistic regression from the ordinary (marginal) setting to the random-effects (subject-specific) framework for longitudinal binary data. It contrasts marginal vs. random-intercepts logistic regression, derives the likelihood function for random-effects models, and introduces the Laplace approximation as the default optimization algorithm used by `glmer()` in R.

## Marginal vs. Individual Probabilities

Two fundamentally different modeling targets:

- **Marginal (ordinary) logistic regression**: models the overall (population-averaged) probabilities
- **Random effects logistic regression**: models the individual (subject-specific) probabilities

## Marginal (Ordinary) Logistic Regression

**Data**: $(Y_{ij}, x_{ij1}, \ldots, x_{ij,p-1})$ for $i = 1, \ldots, m$, $j = 1, \ldots, n_i$, where $Y_{ij} \in \{0, 1\}$.

The marginal model:

1. $P(Y_{ij} = 1) = \pi_{ij}$ and $P(Y_{ij} = 0) = 1 - \pi_{ij}$
2. Link to predictors:

$$\log \frac{\pi_{ij}}{1 - \pi_{ij}} = \beta_0 + \beta_1 x_{ij1} + \beta_2 x_{ij2} + \cdots + \beta_{p-1} x_{ij,p-1}$$

### R Code

```r
glm(Y ~ X1 + ... + Xp, data=data0, family=binomial)
```

- Generally a convex optimization problem; MLE usually exists
- Warning messages often indicate **perfect fit** -- consider removing some predictor variables

## Random Intercepts Logistic Regression

The random-intercepts model adds a subject-specific term:

$$\log \frac{\pi_{ij}}{1 - \pi_{ij}} = \beta_0 + \beta_1 x_{ij1} + \beta_2 x_{ij2} + \cdots + \beta_{p-1} x_{ij,p-1} + u_i$$

where $u_i \sim N(0, \sigma_u^2)$ are iid random effects.

### R Code

```r
library(lme4)
glmer(Y ~ X1 + ... + Xp + (1 | ID), data=data0, family=binomial)
```

If convergence fails, try:

```r
glmer(Y ~ X1 + ... + Xp + (1 | ID), data=data0, family=binomial,
      control=glmerControl(optimizer="bobyqa",
                           optCtrl=list(maxfun=100000)))
```

### Troubleshooting Non-Convergence

- **Perfect fitting?** Remove some $X$ variables
- **Optimization not converging?** Change optimizer or increase max iterations

## The Simple Case: Random-Intercepts with Binary Predictor

**Data**: $(Y_{ij}, x_{ij})$ for $i = 1, \ldots, m$ where $Y_{ij} \in \{0,1\}$, $x_{ij} \in \{0,1\}$.

The data for each subject $i$ forms a 2x2 table:

| | $Y_{ij} = 1$ | $Y_{ij} = 0$ | Sum |
|---|---|---|---|
| $x_{ij} = 1$ | $a_i$ | $b_i$ | $a_i + b_i$ |
| $x_{ij} = 0$ | $c_i$ | $d_i$ | $c_i + d_i$ |

with $n_i = a_i + b_i + c_i + d_i$.

### Model

$$P(Y_{ij} = 1) = \pi_{ij}, \quad P(Y_{ij} = 0) = 1 - \pi_{ij}$$

$$\log \frac{\pi_{ij}}{1 - \pi_{ij}} = \beta_0 + \beta_1 x_{ij} + u_i \quad \text{where } u_i \sim N(0, \sigma_u^2)$$

### Likelihood Function

The likelihood requires integrating over the random effects:

$$L(\boldsymbol{\beta}) = \prod_{i=1}^{m} \int_{-\infty}^{\infty} f(Y_{i1}, \ldots, Y_{i,n_i} \mid u_i) \, f(u_i) \, du_i$$

$$= \prod_{i=1}^{m} \int_{-\infty}^{\infty} \prod_{j=1}^{n_i} \frac{e^{Y_{ij}(\beta_0 + \beta_1 x_{ij} + u_i)}}{1 + e^{\beta_0 + \beta_1 x_{ij} + u_i}} \cdot \frac{1}{\sqrt{2\pi}\,\sigma_u} e^{-\frac{1}{2\sigma_u^2} u_i^2} \, du_i$$

### Further Simplification (Simple Case)

$$L(\boldsymbol{\beta}) = \prod_{i=1}^{m} \int_{-\infty}^{\infty} \frac{e^{(\beta_0 + u_i)(a_i + c_i) + \beta_1 a_i}}{(1 + e^{\beta_0 + \beta_1 + u_i})^{a_i + b_i}(1 + e^{\beta_0 + u_i})^{c_i + d_i}} \cdot \frac{1}{\sqrt{2\pi}\,\sigma_u} e^{-\frac{1}{2\sigma_u^2} u_i^2} \, du_i$$

There are **no explicit mathematical solutions** -- numerical optimization is required.

## Laplace Approximation

The default optimization algorithm in `glmer()` for handling the integrals.

**Key Idea**: Suppose $h(u)$ achieves a local maximum at $u_0$ (so $h'(u_0) = 0$). By Taylor expansion:

$$h(u) \approx h(u_0) + \frac{1}{2} h''(u_0)(u - u_0)^2$$

Thus:

$$\int_a^b e^{h(u)} \, du \approx (\sqrt{2\pi}\,\sigma^*) \, e^{h(u_0)} \int_a^b \frac{1}{\sqrt{2\pi}\sigma^*} e^{-\frac{1}{2\sigma^{*2}}(u - u_0)^2} \, du$$

where $\sigma^{*2} = -\frac{1}{h''(u_0)}$.

The integrand is recognized as the PDF of $N(u_0, \sigma^{*2})$, making the integral analytically tractable.

## Key Takeaways

- Marginal models estimate population-averaged effects; random-effects models estimate subject-specific effects
- Random intercepts $u_i$ capture unobserved heterogeneity between subjects
- The likelihood involves intractable integrals over random effects -- no closed-form MLE
- Laplace approximation (default in `glmer`) approximates these integrals using Taylor expansion around the mode
- Convergence issues are common -- try different optimizers or simplify the model
- The coefficients in marginal vs. random-effects models have different interpretations even for the same data

## Original Slides

![[assets/9.5.Logistic random.effects.Models.pdf]]
