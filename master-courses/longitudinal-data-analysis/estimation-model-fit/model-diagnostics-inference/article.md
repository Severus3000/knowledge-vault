---
title: "Model Fit Diagnostics, Inference, and Testing Assumptions in LME Models"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, model-fit, diagnostics, AIC, BIC, deviance, inference, hypothesis-testing, assumptions, homoscedasticity, normality]
category: "master-courses/longitudinal-data-analysis/estimation-model-fit"
compiled: true
---

# Model Fit Diagnostics, Inference, and Testing Assumptions in LME Models

Lecture 7b (March 6, 2025) covers the full model-fitting pipeline for longitudinal data analysis: formulation, estimation, inference, diagnostics, and model selection. It provides practical guidance on assessing model fit using deviance, AIC/BIC, and testing model assumptions.

## Overview

This lecture presents a comprehensive five-stage framework for confirmatory data analysis in the LME context:
1. Formulation
2. Estimation
3. Inference
4. Diagnostics
5. Model Selection

## 1. Formulation of a Model

Model formulation is a continuation of exploratory/empirical data analysis.

### Preliminary Checks
- Address **identification and/or outlier** issues
- Check if $Y \sim X_1 + \cdots + X_p$ has collinearity problems
- Look for unusual large or small values

### Two Structural Components

**Mean Structure (Level-1 model / fixed effects)**:
- Use time-plots of observed averages for well-replicated models
- Non-parametric local smoothing (e.g., LOESS) when few measurements per time
- Examples of mean structure $Y_{ij} = h_{\theta_i}(X_{ij}) + \epsilon_{ij}$:
  - **Simple linear**: $h(x) = \beta_0 + \beta_1 x$
  - **Two-phase linear**: $h(x) = u - \beta \max(0, v - x)$
  - **Broken stick**: piecewise linear models
  - **Logistic (S-shape)**: $h(x) = \phi_1 + \frac{\phi_2 - \phi_1}{1 + \exp(-(x - \phi_3)/\phi_4)}$
  - **First-order compartment**: $h(x) = \frac{D \phi_1 \phi_2}{\phi_3(\phi_2 - \phi_1)}[e^{-\phi_1 x} - e^{-\phi_2 x}]$

**Covariance Structure (Level-2 / random effects)**:
- Start with intercept random effects, then add more
- Or start with all components as random effects with general correlation structure
- If algorithm doesn't converge, simplify by reducing random effects or adding uncorrelation structure
- Use AIC/BIC for model selection among covariance structures

### Two Equivalent Approaches for Model Specification

For data $(ID_i, Y_{ij}, t_{ij}, X_i)$ with composite model $Y_{ij} = \beta_0 + \beta_1 t_{ij} + \beta_2 X_i + \beta_3 X_i t_{ij} + b_{0i} + b_{1i} t_{ij} + \epsilon_{ij}$:

**Approach #1** (separate levels):
- Level-1: $Y_{ij} = \beta_{0i} + \beta_{1i} t_{ij} + \epsilon_{ij}$
- Level-2: $\beta_{0i} = \beta_0 + \beta_2 X_i + b_{0i}$ and $\beta_{1i} = \beta_1 + \beta_3 X_i + b_{1i}$

**Approach #2** (all in Level-1):
- Level-1: $Y_{ij} = \beta_{0i} + \beta_{1i} t_{ij} + \beta_{2i} X_i + \beta_{3i} X_i t_{ij} + \epsilon_{ij}$
- Level-2: $\beta_{0i} = \beta_0 + b_{0i}$, $\beta_{1i} = \beta_1 + b_{1i}$, $\beta_{2i} \equiv \beta_2$, $\beta_{3i} \equiv \beta_3$

## 2. Estimation

Two estimators for model parameters (including variance parameters):
- **Maximum Likelihood Estimator (MLE)**
- **Restricted Maximum Likelihood (REML) estimator**

**Key distinctions**:
- REML reduces bias of variance estimates, yielding more accurate statistical inference -- especially important when $\dim(\beta)$ is large relative to $N$
- MLE can produce **log-likelihood, deviance, AIC/BIC** for comparing different models, but REML cannot

## 3. Inference

### Asymptotic Distribution

In the LME model, asymptotically:

$$\hat{\beta} \sim MVN(\beta, \hat{V}) \quad \text{where} \quad \hat{V} = \left[-\frac{\partial \log L(\beta)}{\partial \beta \partial \beta^T}\right]^{-1}$$

### R Implementation

```r
fixef(lme1)          # beta_hat = (beta_1, ..., beta_p)
vcov(lme1)           # V_hat = p x p covariance matrix
sqrt(diag(vcov(lme1)))  # standard errors (sigma_1, ..., sigma_p)
```

### 3(i) Hypothesis Test / CI on Individual $\beta_j$

**95% CI**: $\left[\hat{\beta}_j - 1.96\hat{\sigma}_j, \quad \hat{\beta}_j + 1.96\hat{\sigma}_j\right]$

**Test** $H_0: \beta_j = 0$ vs $H_1: \beta_j \neq 0$:

$$Z_{obs} = \frac{\hat{\beta}_j - 0}{\hat{\sigma}_j}$$

Reject $H_0$ if $|Z_{obs}| \geq 1.96$ at $\alpha = 5\%$.

### 3(ii) CI on Linear Combination of $\beta$

For $\psi = c_1 \beta_1 + \cdots + c_p \beta_p$:

$$\hat{\psi} = c_1 \hat{\beta}_1 + \cdots + c_p \hat{\beta}_p \sim N\left(\psi, \hat{\sigma}_\psi^2\right)$$

where $\hat{\sigma}_\psi^2 = (c_1, \ldots, c_p) \hat{V} (c_1, \ldots, c_p)^T$

```r
cnew = as.matrix(c(c1,..,cp))
psi.hat = as.numeric(t(cnew) %*% as.matrix(fixef(lme1)))
psi.sigma = as.numeric(sqrt(t(cnew) %*% vcov(lme1) %*% cnew))
psi.hat + c(-1,1) * 1.96 * psi.sigma
```

### 3(iii) Confidence Region of $\beta$

For joint confidence region of $r$ linear combinations $\psi_{r \times 1} = C_{r \times p} \beta_{p \times 1}$:

$$S(\psi) = (\hat{\psi} - \psi)^T [C\hat{V}C^T]^{-1} (\hat{\psi} - \psi) \sim \chi_r^2$$

A $100(1-\alpha)\%$ confidence region: $\{\psi : S(\psi) \leq c_r(q)\}$ where $c_r(q)$ is the $q$-critical value of $\chi_r^2$.

## 4. Diagnostics

The aim is to compare data with the fitted model to highlight systematic discrepancies.

LME models are models for **mean and covariance structures**, so effective checks include:
- Compare fitted mean vs time-plot observed averages
- **QQ-normal plots** for level-1 residuals
- **Constant variance checks** for level-2 random effects

## 5. Model Selection

### For Nested Models: Hypothesis Testing

- **Fixed effects**: Test whether a coefficient is significantly different from 0 via Z-statistics $\geq 1.96$ (from REML or MLE)
- **Random effects**: Test whether variance of some random effects is zero via **ANOVA from MLE**

### For Non-nested Models: Information Criteria

Use **log-likelihood, deviance, and AIC/BIC** from MLE (smaller AIC/BIC = better).

### Full vs Restricted Estimation

| Feature | Full (ML) | Restricted (REML/GLS) |
|---------|-----------|----------------------|
| Estimation | Simultaneous fixed + variance | Sequential: fixed then variance |
| Default in | MLwiN, HLM | SAS Proc Mixed, Stata xtmixed |
| Goodness of fit | Applies to entire model | Applies to random effects only |
| Model comparison | Can compare entire models | Can only compare random effects (same fixed effects required) |

## Assessing Model Fit

### Log-likelihood
- Want the overall LL value to increase (if negative, get closer to 0) from mean-only model to final model
- LL always increases when additional variables are added -- this is why we examine multiple fit indicators together

### Deviance Statistic

$$\text{Deviance} = -2[LL_{\text{current model}} - LL_{\text{saturated model}}] = -2 LL_{\text{current model}}$$

- Compares current model to the saturated model (best possible fit)
- Small deviance = close to saturated model = good fit
- Large deviance = poor fit

**Requirements for comparison**:
- One model must be nested in the other
- Same data, same number of cases
- If FML: comparing entire models
- If REML: only comparing random effects

### Deviance Example (Alcohol Use Data)

- Mean model only: $-2LL = -335.08 \Rightarrow$ Deviance = 670.16
- Growth model: $-2LL = -318.83 \Rightarrow$ Deviance = 636.61
- Difference: $670.16 - 636.61 = 33.5$
- $33.5 > 16.27$ (the .001 critical value for $\chi^2$)
- **Conclusion**: The unconditional growth model provides a better fit than the mean-only model

### AIC/BIC (Singer and Willett, pgs. 120-122)

- AIC controls for the increase in model parameters
- BIC controls for the number of parameters **and** sample size
- Models do not need to be nested (as long as same data is used)
- **The smaller the AIC/BIC, the better the model**
- Under MLE: can use both fixed and random effect parameters
- Under REML: only random effects
- Should always be used together; conceptual model is important

## Testing Model Assumptions (Singer and Willett, pgs. 127-137)

Three key assumptions to check:

### Checking Functional Form
- **Level-1**: Examine empirical growth plots with OLS-estimated trajectories superimposed -- confirm suitability of hypothesized shape
- **Level-2**: Plot OLS estimates of individual growth parameters against each level-2 predictor -- confirm level-2 relationships

### Checking Normality
- QQ-normal plots for residuals at both level-1 and level-2
- Plot standardized residuals vs ID for unusual data points
- Normality is key to many assumptions for random effects and MLE

### Checking Homoscedasticity
- Equal variances of level-1 and level-2 residuals at each level of every predictor
- Plot residuals vs predictors (e.g., residuals vs AGE, vs COA, vs PEER)

## Key Takeaways

1. Model formulation requires specifying both mean structure (fixed effects) and covariance structure (random effects)
2. Use REML for parameter inference, MLE for model selection via AIC/BIC
3. The deviance test ($\chi^2$) can compare nested models; AIC/BIC work for non-nested models
4. Model fit statistics should be taken together -- when all trend in the same direction, confidence in model fit increases
5. Always check three assumptions: functional form, normality, and homoscedasticity at both levels
6. In Stata, use `estat ic` to get model fit statistics

## Original Slides

![[assets/Lecture 7b - Model Fit, and Testing Assumptions.pdf]]
