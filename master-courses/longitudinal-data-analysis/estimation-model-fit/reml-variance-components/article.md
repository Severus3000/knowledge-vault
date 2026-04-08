---
title: "REML Estimation of Variance Components in Linear Mixed Models"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, estimation, REML, MLE, variance-components, linear-mixed-models, error-contrasts, ANOVA]
category: "master-courses/longitudinal-data-analysis/estimation-model-fit"
compiled: true
---

# REML Estimation of Variance Components in Linear Mixed Models

Lecture 16 (Spring 2017) provides a formal mathematical treatment of variance component estimation in linear mixed models, covering ANOVA methods, Maximum Likelihood (ML), and Restricted Maximum Likelihood (REML). It derives the REML estimator from first principles using error contrasts and projection matrices.

## Overview

This lecture focuses on the theoretical foundations of three variance component estimation methods: ANOVA (method of moments), ML, and REML. It explains why ML underestimates variance components and how REML corrects this bias through error contrasts -- linear combinations of the response that are free of the fixed-effect parameters $\beta$.

## The Linear Mixed Model

The general form:

$$Y = X\beta + Zu + \varepsilon$$

where:
- $Y$ is an $n \times 1$ response vector
- $X$ is an $n \times p$ design matrix (fixed effects)
- $\beta$ is a $p \times 1$ vector of fixed unknown parameters
- $Z$ is an $n \times q$ model matrix of known constants (random effects design)
- $u$ is a $q \times 1$ random vector
- $\varepsilon$ is an $n \times 1$ random error

### Distributional Assumptions

Assume $(\varepsilon, u)$ are jointly normal:

$$E(\varepsilon) = 0, \quad \text{Var}(\varepsilon) = R, \quad E(u) = 0, \quad \text{Var}(u) = G$$

Therefore:

$$\text{Var}(Y) = \Sigma = ZGZ^T + R$$

## Three Variance Component Estimation Methods

| Method | Key Properties |
|--------|---------------|
| **ANOVA** | Easy to compute (balanced case), unbiased, no distributional assumptions required, but may produce negative estimates |
| **ML** | Good large-sample properties (efficiency), computationally difficult, underestimates variance components |
| **REML** | Same as ANOVA in simple balanced case, typically less biased than ML, unbiased for some special cases |

## Maximum Likelihood Method

Assume $\Sigma$ is a function of $\gamma$ (vector of all variance components). The likelihood function for $\beta, \gamma$ is:

$$L(\beta, \gamma) = (2\pi)^{-n/2} |\Sigma(\gamma)|^{-1/2} \exp\left\{-\frac{1}{2}(Y - X\beta)^T \Sigma(\gamma)^{-1}(Y - X\beta)\right\}$$

For a fixed $\gamma$, the MLE of $\beta$ is (if $X$ is full rank):

$$\hat{\beta}(\gamma) = (X^T \Sigma^{-1}(\gamma) X)^{-1} X^T \Sigma^{-1}(\gamma) Y$$

### Profile Likelihood

Plugging $\hat{\beta}(\gamma)$ back into the likelihood:

$$L^*(\gamma) = (2\pi)^{-n/2} |\Sigma(\gamma)|^{-1/2} \exp\left[-\frac{1}{2}\{Y - X\hat{\beta}(\gamma)\}^T \Sigma(\gamma)^{-1}\{Y - X\hat{\beta}(\gamma)\}\right]$$

Then the MLE for $\gamma$ is:

$$\hat{\gamma}^2 = \arg\max_\gamma L^*(\gamma)$$

### MLE Bias

The consistency and asymptotic normality of MLEs are supported by large-sample theory. But in small samples, MLE for variance components tends to **underestimate** due to failure to account for degrees of freedom lost estimating fixed effects.

**Example**: For the simple case $\Sigma = \sigma^2 I_n$ and $\gamma = \sigma^2$:

$$\hat{\sigma}^2 = \frac{1}{n}(Y - X\hat{\beta})^T(Y - X\hat{\beta})$$

which has expectation $\frac{n - \text{rank}(X)}{n} \sigma^2 < \sigma^2$.

The MLE is criticized for "failing to account for the loss of degrees of freedom needed to estimate $\beta$."

## Restricted Maximum Likelihood (REML)

### The Core Idea

REML constructs a likelihood for a set of **error contrasts** whose distributions are unrelated to the fixed parameters $\beta$. It produces unbiased estimators for some special cases and less biased estimates than ML in general.

### Error Contrasts

If vector $a$ is orthogonal to all columns of $X$ (i.e., $a^T X = 0$), then $a^T Y$ is an **error contrast**.

We can find at most $N - k$ such linearly independent vectors $b_1, \ldots, b_{N-k}$ (where $k = \text{rank}(X)$) such that $b_i^T X = 0$ for all $i$.

### Construction via Projection Matrix

Let $S = I_N - X(X^T X)^{-} X^T$ (the residual projection). Then $SX = 0$, and:

$$(I - P_X)Y = Y - P_X Y = Y - \hat{Y}$$

The elements of $(I - P_X)Y$ are error contrasts. Because $\text{rank}(I - P_X) = n - p$, there exists a set of $n - p$ linearly independent rows of $I - P_X$ that can be used to find error contrasts.

This is the reason the procedure is also called **residual maximum likelihood estimator** -- the error contrasts are a subset of the residual vector $Y - \hat{Y}$.

### The Error Contrast Vector

Define $A = I_n - P_X$ and $B$ (an $n \times (n-p)$ matrix) such that:

$$BB^T = A \quad \text{and} \quad B^T B = I_{n-p}$$

The error contrasts are $w = B^T Y$. It can be shown that $B^T Y$ and $\hat{\beta} = (X^T \Sigma^{-1} X)^{-1} X^T \Sigma^{-1} Y$ are **independent**.

### The REML Log-Likelihood

The REML is defined as the maximizer of:

$$\ell^*(\gamma) = -\frac{1}{2}\log(|\Sigma|) - \frac{1}{2}\log(|X^T \Sigma^{-1} X|) - \frac{1}{2}(Y - X\hat{\beta})^T \Sigma^{-1}(Y - X\hat{\beta})$$

That is:

$$\hat{\gamma} = \arg\max_\gamma \ell^*(\gamma)$$

Note the extra term $-\frac{1}{2}\log(|X^T \Sigma^{-1} X|)$ compared to the ML log-likelihood. This term accounts for the degrees of freedom used to estimate $\beta$.

### Simple Example

For $Y_1, \ldots, Y_n$ iid $N(\mu, \sigma^2)$:

- **MLE**: $\hat{\sigma}^2 = \frac{1}{n}\sum_{i=1}^{n}(Y_i - \bar{Y})^2$ (biased)
- **REML**: $\hat{\sigma}^2 = \frac{1}{n-1}\sum_{i=1}^{n}(Y_i - \bar{Y})^2$ (unbiased)

## Application to Linear Mixed-Effects Model

For subject $i$ with $N_i$ serial measurements:

$$y_i = X_i \beta + Z_i b_i + \epsilon_i$$

where:
- $b_i \sim N(0, D)$ (random effects covariance)
- $\epsilon_i \sim N(0, \sigma^2 I_{N_i})$ (residual)
- All $\epsilon_i, b_1, \ldots, b_M$ independent

The subject-specific covariance is:

$$H_i(\theta) = Z_i D Z_i^T + \sigma^2 I_{N_i}$$

### Stacked Data

$$\mathbf{y} = \mathbf{X}\beta + \mathbf{Z}\mathbf{b} + \epsilon$$

where the block-diagonal covariance matrix $\mathbf{H}(\theta) = \text{diag}(H_1(\theta), \ldots, H_M(\theta))$.

### REML Log-Likelihood for LME

$$\mathcal{L}_w(\theta | A^T y) = -\frac{1}{2}\sum_{i=1}^{M}\log\det H_i - \frac{1}{2}\sum_{i=1}^{M}\log\det X_i^T H_i^{-1} X_i - \frac{1}{2}\sum_{i=1}^{M}(y_i - X_i\hat{\beta})^T H_i^{-1}(y_i - X_i\hat{\beta})$$

where:

$$\hat{\beta} = (\mathbf{X}^T \mathbf{H}^{-1} \mathbf{X})^{-1} \mathbf{X}^T \mathbf{H}^{-1} \mathbf{y} = \left(\sum_{i=1}^{M} X_i^T H_i^{-1} X_i\right)^{-1} \sum_{i=1}^{M} X_i^T H_i^{-1} y_i$$

Maximize $\mathcal{L}_w$ w.r.t. $\beta$, $\sigma^2$, and $D$. Computational details use Newton-Raphson iteration (Lindstrom and Bates, 1988).

## Key Takeaways

1. REML addresses the fundamental bias in ML estimation of variance components by working with error contrasts that are free of $\beta$
2. The extra log-determinant term $-\frac{1}{2}\log|X^T \Sigma^{-1} X|$ in the REML likelihood accounts for degrees of freedom lost estimating fixed effects
3. In the simplest case (iid normal), REML gives the familiar $n-1$ denominator instead of $n$
4. Error contrasts are the residuals $Y - \hat{Y}$, hence the name "residual maximum likelihood"
5. For LME models, the block-diagonal structure of the covariance matrix enables efficient computation
6. REML matches ANOVA in simple balanced cases but extends to unbalanced and more complex designs

## Original Slides

![[assets/Lecture_16_Spring_2017.pdf]]
