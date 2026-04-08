---
title: "A Tutorial on Restricted Maximum Likelihood Estimation in Linear Regression and LME Models"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Xiuming Zhang"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, estimation, REML, MLE, variance-components, linear-regression, linear-mixed-effects, bias-correction, error-contrasts, tutorial]
category: "master-courses/longitudinal-data-analysis/estimation-model-fit"
compiled: true
---

# A Tutorial on Restricted Maximum Likelihood Estimation in Linear Regression and LME Models

This tutorial by Xiuming Zhang (A*STAR-NUS Clinical Imaging Research Center, October 2015) derives the REML estimation procedure in full mathematical detail. It starts from bias in simple linear regression, derives the REML log-likelihood through error contrasts, and applies it to the linear mixed-effects (LME) model for longitudinal analysis.

## Overview

The tutorial covers three main topics:
1. **Linear Regression**: Introduces variance component estimation bias in ML
2. **Restricted Maximum Likelihood**: Derives REML from error contrasts with full proofs
3. **Linear Mixed-Effects Model**: Applies REML to longitudinal data with inter-subject variability

Key references: Patterson and Thompson (1971), Harville (1974), Bernal-Rusiel et al. (2013).

## 1. Linear Regression

### 1.1 The Model

Simple linear regression: $y = \beta_0 + \beta_1 x + \epsilon$, where $\epsilon \sim N(0, \sigma^2)$.

In matrix form (multiple regression):

$$y = X\beta + \epsilon, \quad \epsilon \sim N(0, \sigma^2 I_N)$$

Therefore $y \sim N(X\beta, \sigma^2 I_N)$.

This mandates: (i) residuals are independent, (ii) residuals have the same variance $\sigma^2$. This model cannot handle intercorrelated responses (e.g., longitudinal measurements), motivating LME.

### 1.2 Parameter Estimation

Maximize the log-likelihood w.r.t. $\beta$ and $\sigma^2$:

$$\mathcal{L}(\beta, \sigma^2 | y, X) = -\frac{N}{2}\log 2\pi - \frac{N}{2}\log \sigma^2 - \frac{1}{2\sigma^2}(y - X\beta)^T(y - X\beta)$$

Solutions:

$$\hat{\beta} = (X^T X)^{-1} X^T y$$
$$\hat{\sigma}^2 = \frac{1}{N}(y - X\hat{\beta})^T(y - X\hat{\beta})$$

The $\hat{\beta}$ is simply the OLS estimator. However, $\hat{\sigma}^2$ is **biased downwards**.

### 1.3 Estimation Bias in Variance Component

Define $A = X(X^T X)^{-1} X^T$ (the **orthogonal projection** / hat matrix), which is **idempotent** ($A^2 = A$) and **Hermitian** ($A^* = A$).

**Theorem 1.1**: If $y \sim N(0, I_N)$ and $A$ is an orthogonal projection, then $y^T A y \sim \chi^2(k)$ with $k = \text{rank}(A)$.

*Proof*: Since $A$ is idempotent and Hermitian, its eigendecomposition gives $A = Q\Lambda Q^{-1}$ where $\Lambda$ is diagonal with entries 0 or 1. Then $y^T A y = W_k^T W_k$ where $W_k \sim N(0, I_k)$, which is $\chi^2(k)$ by definition.

Using this theorem:

$$E\{y^T y\} = N\sigma^2 + (X\beta)^T(X\beta)$$
$$E\{y^T A y\} = k\sigma^2 + (X\beta)^T(X\beta)$$

where $k = \text{rank}(A) = \text{rank}(X)$. Therefore:

$$E\{\hat{\sigma}^2\} = \frac{N - k}{N}\sigma^2 < \sigma^2$$

The bias factor is $\frac{N-k}{N}$. The corrected unbiased estimator:

$$\hat{\sigma}^2_{\text{unbiased}} = \frac{1}{N - k}(y - X\hat{\beta})^T(y - X\hat{\beta})$$

## 2. Restricted Maximum Likelihood

### 2.1 The Theory

For the general linear regression model $y = X\beta + \epsilon$ with $\epsilon \sim N(0, H(\theta))$ where $H(\theta)$ is a general covariance matrix parameterized by $\theta$ ("variance components"):

**The core intuition**: If we estimated variance components with true mean values, the estimation would be unbiased. REML maximizes a modified likelihood that is **free of mean components**.

#### Error Contrasts

If $a^T X = 0$, then $a^T y$ is an **error contrast**:

$$w = A^T y = A^T(X\beta + \epsilon) = A^T \epsilon \sim N(0, A^T H A)$$

which is free of $\beta$. Patterson and Thompson (1971) proved that in the absence of information on $\beta$, no information about $\theta$ is lost when inference is based on $w$ rather than $y$.

#### Generalized Least Squares (GLS)

Once $H(\theta)$ is known, the GLS solution for $\beta$ is:

$$\hat{\beta} = (X^T H^{-1} X)^{-1} X^T H^{-1} y$$

### 2.1 Deriving the REML Log-Likelihood

Starting from the restricted log-likelihood $\mathcal{L}_w(\theta | A^T y)$:

$$\mathcal{L}_w(\theta | A^T y) = \log f_w(A^T y | \theta) \int f_{\hat{\beta}}(G^T y | \beta, \theta) d\beta$$

Through a series of algebraic manipulations involving:

**Interlude 2.1**: $|\det[A \quad G]| = (\det X^T X)^{-1/2}$

**Interlude 2.2**: Decomposition of $(y - X\beta)^T H^{-1}(y - X\beta)$ into:

$$(y - X\hat{\beta})^T H^{-1}(y - X\hat{\beta}) + (\beta - \hat{\beta})^T(X^T H^{-1} X)(\beta - \hat{\beta})$$

The final REML log-likelihood:

$$\mathcal{L}_w(\theta | A^T y) = -\frac{1}{2}(N - k)\log(2\pi) + \frac{1}{2}\log\det X^T X - \frac{1}{2}\log\det H - \frac{1}{2}\log\det X^T H^{-1} X - \frac{1}{2}(y - X\hat{\beta})^T H^{-1}(y - X\hat{\beta})$$

where $\hat{\beta} = (X^T H^{-1} X)^{-1} X^T H^{-1} y$.

### 2.2 Verification: Simple Linear Regression

For $H = \sigma^2 I_N$, set $\frac{d}{d\sigma^2}\mathcal{L}_w = 0$:

$$\frac{d}{d\sigma^2}\left[-\frac{1}{2}(N-k)\log\sigma^2 - \frac{1}{2\sigma^2}(y - X\hat{\beta})^T(y - X\hat{\beta})\right] = 0$$

This yields exactly the unbiased estimator $\hat{\sigma}^2 = \frac{1}{N-k}(y - X\hat{\beta})^T(y - X\hat{\beta})$, matching the post-hoc correction.

**Important note**: In simple linear regression, $\hat{\beta}$ is independent of $\theta$ (Equation 3), so ML and ReML give the same $\hat{\beta}$. This is **not true** for more complex models like LME, where the ReML estimate of $\theta$ affects the estimate of $\beta$.

## 3. Linear Mixed-Effects Model

### 3.1 The Model

For subject $i$ with $N_i$ serial measurements:

$$y_i = X_i \beta + Z_i b_i + \epsilon_i$$

where:
- $X_i$: $n_i \times p$ design matrix for fixed effects (e.g., gender, education, clinical group)
- $\beta$: $p \times 1$ fixed effects regression coefficients
- $Z_i$: $N_i \times q$ design matrix for random effects (columns are a subset of $X_i$)
- $b_i$: $q \times 1$ random effects vector
- $\epsilon_i$: $N_i \times 1$ residual vector

Distributional assumptions:

$$b_i \sim N(0, D), \quad \epsilon_i \sim N(0, \sigma^2 I_{N_i}), \quad \epsilon_1, \ldots, \epsilon_M, b_1, \ldots, b_M \text{ independent}$$

### Conditional vs Marginal

- **Conditional (subject-specific) mean**: $E\{y_i | b_i\} = X_i \beta + Z_i b_i$
- **Marginal (population-average) mean**: $E\{y_i\} = X_i \beta$
- **Conditional covariance**: $\text{Cov}\{y_i | b_i\} = \sigma^2 I_{N_i}$ (diagonal)
- **Marginal covariance**: $\text{Cov}\{y_i\} = Z_i D Z_i^T + \sigma^2 I_{N_i}$ (structured, **not** diagonal)

The random effects $Z_i$ and $D$ add **structure** to the originally diagonal covariance matrix, allowing the model to capture **intra-subject measurement correlations**.

### 3.2 Estimation by Restricted Maximum Likelihood

Stack all subjects: $\mathbf{y} = \mathbf{X}\beta + \mathbf{Z}\mathbf{b} + \epsilon$ where $\mathbf{H}(\theta)$ is block-diagonal:

$$\mathbf{H}(\theta) = \text{diag}(H_1(\theta), \ldots, H_M(\theta))$$

with $H_i(\theta) = Z_i D Z_i^T + \sigma^2 I_{N_i}$.

The REML log-likelihood decomposes into per-subject terms:

$$\mathcal{L}_w(\theta | A^T y) = -\frac{1}{2}\sum_{i=1}^{M}\log\det H_i - \frac{1}{2}\sum_{i=1}^{M}\log\det X_i^T H_i^{-1} X_i - \frac{1}{2}\sum_{i=1}^{M}(y_i - X_i\hat{\beta})^T H_i^{-1}(y_i - X_i\hat{\beta})$$

where:

$$\hat{\beta} = \left(\sum_{i=1}^{M} X_i^T H_i^{-1} X_i\right)^{-1} \sum_{i=1}^{M} X_i^T H_i^{-1} y_i$$

Maximize w.r.t. $\beta$, $\sigma^2$, and $D$ using Newton-Raphson (Lindstrom and Bates, 1988).

## References

- Patterson, H. D. and Thompson, R. (1971). Recovery of inter-block information when block sizes are unequal. *Biometrika*, 58(3):545-554.
- Harville, D. A. (1974). Bayesian inference for variance components using only error contrasts. *Biometrika*, 61(2):383-385.
- Laird, N. M. and Ware, J. H. (1982). Random-effects models for longitudinal data. *Biometrics*, pages 963-974.
- Lindstrom, M. J. and Bates, D. M. (1988). Newton-Raphson and EM algorithms for linear mixed-effects models for repeated-measures data. *JASA*, 83(404):1014-1022.
- Bernal-Rusiel, J. L. et al. (2013). Statistical analysis of longitudinal neuroimage data with linear mixed effects models. *NeuroImage*, 66:249-260.
- Verbeke, G. and Molenberghs, G. (2009). *Linear mixed models for longitudinal data*. Springer.

## Key Takeaways

1. ML variance estimation is biased downward by a factor of $(N-k)/N$ due to ignoring degrees of freedom for estimating $\beta$
2. REML eliminates this bias by maximizing a likelihood based on error contrasts -- linear combinations of $Y$ that are orthogonal to the fixed-effect design matrix $X$
3. Error contrasts are equivalent to residuals $Y - \hat{Y}$, hence "residual maximum likelihood"
4. The key mathematical insight: the REML likelihood includes the extra penalty term $-\frac{1}{2}\log|X^T H^{-1} X|$ that accounts for fixed-effect estimation
5. In simple linear regression, REML and ML give the same $\hat{\beta}$; in LME models, they generally differ because $\hat{\beta}$ depends on the variance components
6. The LME model adds structure ($Z_i D Z_i^T$) to the covariance matrix, capturing intra-subject correlations that standard regression cannot model

## Original Slides

![[assets/reml.pdf]]
