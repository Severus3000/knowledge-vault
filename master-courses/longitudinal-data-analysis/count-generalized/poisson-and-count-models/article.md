---
title: "Poisson Regression and Count Data Models for Longitudinal Data"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, poisson-regression, count-data, generalized-models]
category: "master-courses/longitudinal-data-analysis/count-generalized"
compiled: true
---

# Poisson Regression and Count Data Models for Longitudinal Data

## Overview

This lecture covers Generalized Linear Models (GLMs) for count data, with a focus on Poisson regression and its extensions for longitudinal settings. When the outcome variable is a non-negative integer count, standard linear regression is inappropriate -- Poisson regression provides a natural framework. The lecture also addresses model violations (overdispersion, excess zeros) and introduces alternative distributions: Negative Binomial and Zero-Inflated Poisson (ZIP).

## 1. Generalized Linear Model (GLM) Framework

A GLM consists of two specification steps:

1. **Distribution** for the response $Y_i$ (with mean $\mu_i$)
2. **Link function** connecting $\mu_i$ to predictors:

$$g(\mu_i) = \beta_0 + \beta_1 X_{1i} + \cdots + \beta_p X_{pi}$$

### Three Special Cases

| Outcome type | Model | Distribution | Link function |
|---|---|---|---|
| Continuous | Linear regression | $Y_i \sim N(\mu_i, \sigma^2)$ | $g(\mu_i) = \mu_i$ (identity) |
| Binary/Binomial | Logistic regression | $Y_i \sim \text{Bernoulli}(n_i, \pi_i)$ | $g(\pi_i) = \log\frac{\pi_i}{1-\pi_i}$ (logit) |
| Count | Poisson regression | $Y_i \sim \text{Poisson}(\mu_i)$ | $g(\mu_i) = \log \mu_i$ (log) |

## 2. Poisson Distribution Review

If $Y \sim \text{Poisson}(\lambda)$, the probability mass function is:

$$P(Y = k) = \frac{\lambda^k e^{-\lambda}}{k!}, \quad k = 0, 1, 2, \ldots$$

Key properties:

- **Mean equals variance**: $E(Y) = \text{Var}(Y) = \lambda$
- **Law of Small Numbers**: If $Y \sim \text{Binomial}(n, p = \lambda/n)$ for large $n$, then $Y \approx \text{Poisson}(\lambda)$
- **Additivity**: If $Y_i \sim \text{Poisson}(\lambda_i)$ are independent, then $Y_1 + \cdots + Y_m \sim \text{Poisson}(\lambda_1 + \cdots + \lambda_m)$

### Connection to Normal Distribution

For large $\lambda$:

- **CLT**: $Z = \frac{Y - \lambda}{\sqrt{\lambda}} \approx N(0, 1)$
- **Square root transformation**: $Z = 2\sqrt{Y} \approx N(2\sqrt{\lambda}, 1)$
- **Anscombe transformation**: $2\sqrt{Y + 3/8}$ (variance-stabilizing)

### Poisson as Exponential Family

The Poisson distribution belongs to the one-parameter exponential family:

$$f_\theta(y) = f_0(y) \exp(\theta y - b(\theta))$$

where $\theta = \log \lambda$, $b(\theta) = e^\theta = \lambda$, so:

- Mean: $b'(\theta) = e^\theta = \lambda$
- Variance: $b''(\theta) = e^\theta = \lambda$

## 3. Poisson Regression Model

### Model Specification

For observed data $(Y_i, x_{i1}, x_{i2}, \ldots, x_{i,p-1})$ with count responses $Y_i \in \{0, 1, 2, 3, \ldots\}$:

- **Distribution**: $Y_i \sim \text{Poisson}(\mu_i)$, i.e., $P(Y_i = y_i) = \frac{\mu_i^{y_i} e^{-\mu_i}}{y_i!}$
- **Link function**: $\log(\mu_i) = \beta_0 + \beta_1 x_{i1} + \beta_2 x_{i2} + \cdots + \beta_{p-1} x_{i,p-1} = \mathbf{x}_i^T \boldsymbol{\beta}$

Thus $\mu_i = \exp(\mathbf{x}_i^T \boldsymbol{\beta})$, which ensures the mean is always non-negative.

### Maximum Likelihood Estimation

The log-likelihood function is:

$$\log L(\boldsymbol{\beta}) = \sum_{i=1}^{n} \left( y_i \log(\mu_i) - \mu_i - \log(y_i!) \right) = \sum_{i=1}^{n} \left( y_i \mathbf{x}_i^T \boldsymbol{\beta} - \exp(\mathbf{x}_i^T \boldsymbol{\beta}) - \log(y_i!) \right)$$

Differentiating with respect to $\beta_j$ gives the score equations:

$$\sum_{i=1}^{n} (y_i - \exp(\mathbf{x}_i^T \hat{\boldsymbol{\beta}})) x_{ij} = 0, \quad \text{for all } j = 0, 1, \ldots, p-1$$

Or equivalently: $\mathbf{X}^T \mathbf{Y} = \mathbf{X}^T \hat{\boldsymbol{\mu}}$ (analogous to OLS normal equations).

### R Code

```r
# Standard Poisson regression (independent data)
pois.glm_model <- glm(Y ~ X1 + ... + Xp, family = poisson, data = your_data)
summary(pois.glm_model)

# Poisson mixed-effects model (longitudinal data)
pois.lme_model <- glmer(Y ~ X1 + ... + Xp + (1 | ID),
                        data = your_data, family = poisson(link = "log"),
                        offset = log(size))
summary(pois.lme_model)
```

## 4. Worked Example: 2x2 Table (Vaccine and Shingles)

| | Vaccine No | Vaccine Yes | Total |
|---|---|---|---|
| **Shingles No** | 14 | 320 | 334 |
| **Shingles Yes** | 36 | 80 | 116 |
| **Total** | 50 | 400 | 450 |

### Sampling Scheme #a: Poisson Regression on Cell Counts

With indicator variables $X_1$ (vaccine) and $X_2$ (shingles), there are $n = 4$ observations. The Poisson model $\log(\mu_i) = \beta_0 + \beta_1 x_{i1} + \beta_2 x_{i2}$ yields MLE:

$$\hat{\beta}_0 = 3.6139, \quad \hat{\beta}_1 = 2.0794, \quad \hat{\beta}_2 = -1.0576$$

Fitted values follow the rule: **fitted value = row sum x col sum / total**, which is exactly Pearson's expected count under independence.

**Pearson's Chi-square** from the Poisson regression: $\sum \frac{(O - E)^2}{E} = 62.8123$.

### Comparison: Linear Regression on the Same Data

Linear regression gives $\hat{\beta}_0 = 79.5$, $\hat{\beta}_1 = 175.0$, $\hat{\beta}_2 = -109.0$ with fitted value of $-29.5$ for (Shingles Yes, Vaccine No) -- a negative count, which is nonsensical.

### Sampling Scheme #b: Logistic Regression on Individual-Level Data

With $n = 450$ individual observations and binary outcome (shingles yes/no), logistic regression gives:

$$\hat{\beta}_0 = \log\left(\frac{36}{14}\right) = 0.9445, \quad \hat{\beta}_1 = \log\left(\frac{80 \times 14}{320 \times 36}\right) = -2.3308$$

The log-odds ratio $\hat{\beta}_1$ is the same quantity testable by Fisher's exact test, two-sample proportion test, or Pearson's chi-square ($T^2 = 62.81 = \chi^2$).

## 5. Deviance and Model Evaluation

### Deviance for GLM

The **deviance** for a model $M_0$ is:

$$\text{Dev}(M_0) = -2 \log L(Y; M_0) + 2 \log L(Y; M_{\text{saturated}})$$

### Deviance for Poisson Regression

$$\text{Dev}(M_0) = -2 \sum_i \left( Y_i \log\left(\frac{\hat{\mu}_i}{Y_i}\right) - \hat{\mu}_i + Y_i \right)$$

With an intercept term, $\sum \hat{\mu}_i = \sum Y_i$, and the deviance becomes the **G-statistic**:

$$\text{Dev}(M_0) = 2 \sum_i O_i \log\left(\frac{O_i}{E_i}\right)$$

By Taylor approximation, this is approximately **Pearson's chi-squared**:

$$\sum_i \frac{(O_i - E_i)^2}{E_i}$$

The **Pearson residuals** are defined as: $e_i^{\text{pear}} = \frac{Y_i - \hat{\mu}_i}{\sqrt{\hat{\mu}_i}}$

## 6. Dispersion Parameter and Quasi-Poisson

Since the Poisson distribution requires $E(Y) = \text{Var}(Y)$, but real data often violates this (overdispersion: $\text{Var}(Y) > E(Y)$), we introduce a **dispersion parameter** $\phi$:

$$\text{Var}(Y) = \phi \cdot E(Y)$$

The dispersion parameter is estimated by:

$$\hat{\phi} = \frac{\sum_{i=1}^{n} (Y_i - \hat{\mu}_i)^2 / \hat{\mu}_i}{n - p}$$

Key points:

- $\phi$ only affects $\text{Var}(\hat{\boldsymbol{\beta}})$, not the point estimates $\hat{\boldsymbol{\beta}}$ or $\hat{\mu}_i$
- In R, **quasi-Poisson regression** uses $\hat{\phi}$ for confidence intervals and F-tests
- If $\hat{\phi} \gg 1$, the Poisson model underestimates standard errors

## 7. Poisson Regression for Longitudinal Count Data

### Random-Intercept Model

For longitudinal data $(Y_{ij}, x_{1ij}, x_{2ij}, \ldots, x_{pij})$ with $i = 1, \ldots, m$ subjects and $j = 1, \ldots, n_i$ observations:

- **Distribution**: $Y_{ij} \sim \text{Poisson}(\mu_{ij})$
- **Link function**: $\log(\mu_{ij}) = \beta_0 + \beta_1 x_{1ij} + \cdots + \beta_p x_{pij} + b_i$

where $b_i \sim N(0, \sigma_b^2)$ is a subject-specific random intercept.

### Loglinear Specification for Panel Data

$$\log(\lambda_{it}) = \mu_t + \beta x_{it} + \gamma z_i$$

where $x_{it}$ are time-varying predictors and $z_i$ are time-invariant predictors. The log-link ensures $\lambda > 0$.

## 8. Key Assumptions and Violations

### Assumption 1: Mean = Variance (Equidispersion)

- **Overdispersion** ($\text{Var} > \text{Mean}$): The most common violation. Detectable by comparing sample mean and variance (e.g., mean = 1.81, variance = 20.38 indicates severe overdispersion)
- **Underdispersion** ($\text{Mean} > \text{Var}$): Rarely observed in practice

### Assumption 2: Independent Observations

Events making up a Poisson count should be independent. Often violated when an event occurring increases/decreases the likelihood of the event recurring.

## 9. Alternative Models for Count Data

### Negative Binomial (NB) Distribution

$$P(Y = y) = \binom{y + r - 1}{y} (1-p)^y p^r$$

Often used to handle **overdispersion** in count data. The NB distribution has an extra parameter allowing variance to exceed the mean.

### Zero-Inflated Poisson (ZIP)

For data with excess zeros beyond what a Poisson distribution predicts, the ZIP model assumes two groups:

1. **Structural zero group**: Always produces zero (modeled with a logit component)
2. **Count group**: Produces counts from a Poisson (or NB) process

$$P(Y = 0) = \pi + (1-\pi) e^{-\lambda}$$

$$P(Y = y) = (1-\pi) \frac{\lambda^y e^{-\lambda}}{y!}, \quad y = 1, 2, 3, \ldots$$

R package: **glmmTMB** (Generalized Linear Mixed Models using Template Model Builder)

### Other Approaches to Overdispersion

- **Mixture of Poisson distributions**: $P(Y = y) = \sum_i \pi_i \frac{\lambda_i^y}{y_i!} e^{-\lambda_i}$ where $\sum_i \pi_i = 1$
- **Box-Cox transformation**: $Y^* = \frac{Y^\lambda - 1}{\lambda}$ if $\lambda \neq 0$; $\log(Y)$ if $\lambda = 0$

## 10. Applied Example: German Health Care Reform

### Data Description

Study of the effect of a 1997 German health care reform on doctor visits, with variables:

- **numvisit**: Number of doctor visits in 3 months (count outcome)
- **reform**: Post-reform indicator (1997 vs 1999)
- **Covariates**: age, education, married, bad health (badh), log income (loginc), summer

### Population-Average Poisson (GEE)

Using robust standard errors clustered by individual:

| Variable | IRR | z | p-value |
|---|---|---|---|
| reform | 0.869 | -2.53 | 0.011 |
| badh | 3.105 | 13.31 | 0.000 |
| age | 1.004 | 1.32 | 0.186 |
| loginc | 1.161 | 1.89 | 0.059 |

**Interpretation**: There was a 13% reduction in doctor visits between 1996-1998 (IRR = 0.869), controlling for other covariates, suggesting the health reform was effective.

Model diagnostics show overdispersion: $(1/\text{df}) \times \text{Deviance} = 3.34$, $(1/\text{df}) \times \text{Pearson} = 4.37$ (both should be near 1 under a well-fitting Poisson model).

### Random-Effects Poisson (Mixed Model)

Random intercept model (`xtpoisson` in Stata):

| Variable | IRR | z | p-value |
|---|---|---|---|
| reform | 0.955 | -1.42 | 0.155 |
| badh | 2.467 | 14.66 | 0.000 |
| age | 1.006 | 2.13 | 0.033 |

$\hat{\sigma}_u = 0.904$ (substantial between-subject variation). LR test vs. standard Poisson: $\chi^2(1) = 2598.82$, $p < 0.0001$ -- the random-effects model is strongly preferred.

### Random-Coefficients Poisson

Adding a random slope for reform:

| Variable | IRR | z | p-value |
|---|---|---|---|
| reform | 0.902 | -1.92 | 0.055 |
| badh | 3.028 | 14.44 | 0.000 |

Random effects: $\text{sd}(\text{reform}) = 0.930$, $\text{sd}(\text{cons}) = 0.954$, $\text{corr} = -0.491$.

LR test (random intercept vs. random coefficients): $\chi^2(2) = 259.10$, $p < 0.0001$ -- **the random coefficients model is preferred**.

## 11. Group-Based Trajectory Models (GBTM) Application

### Zero-Inflated GBTM for Substance Use

Study: P18 Cohort (N=597), 6-year cohort of young sexual minority men (ages 18-24), 14 waves of data.

**Alcohol use trajectories** (best-fitting ZIP model, 5 groups):
1. Low gradual increase drinkers (28%)
2. Consistently low drinkers (30%)
3. Moderate drinkers who waver and decrease (21%)
4. Moderate drinkers who become heavy drinkers (5%)
5. Consistently moderate drinkers (16%)

**Marijuana use trajectories** (ZIP, 5 groups):
1. Abstainers (45%)
2. Moderate users who gradually increase (12%)
3. Low users who drastically increase (11%)
4. Moderate users who decrease (13%)
5. Frequent users who increase to heavy use (20%)

**Key finding**: Square root transformation was insufficient for zero-inflated count data. The ZIP specification better captured the data-generating process and revealed distinct trajectory subgroups.

## 12. Course Summary: Longitudinal Models

| Approach | Key Feature |
|---|---|
| Random effects (intercept/coefficient) | Subject-specific inference |
| GEE (population average) | Population-level inference, robust SE |
| Fixed effects | Causal inference for time-varying predictors (needs 3+ time points) |
| Hybrid models | Combines time-varying and time-invariant effects |

## Key Takeaways

- **Poisson regression** is the natural GLM for count outcomes: log link ensures non-negative predictions
- The **mean-variance equality** assumption ($E(Y) = \text{Var}(Y)$) is frequently violated in practice; check dispersion diagnostics
- **Overdispersion** is addressed by quasi-Poisson, Negative Binomial, or mixture models
- **Zero-inflated models** (ZIP/ZINB) handle excess structural zeros via a two-component mixture
- For **longitudinal count data**, add random effects (intercept and/or slopes) to the Poisson GLM using `glmer` (R) or `xtpoisson`/`xtmepoisson` (Stata)
- **Incidence Rate Ratios (IRR)** = $e^{\beta}$ provide interpretable effect sizes: IRR < 1 means reduction, IRR > 1 means increase
- Model comparison uses **LR tests**, **AIC/BIC**, and **deviance** diagnostics

## Original Slides

![[assets/Lecture 11 - Poisson and Other Models.pdf]]
