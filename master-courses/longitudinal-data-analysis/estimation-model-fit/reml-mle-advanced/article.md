---
title: "REML and MLE Advanced Topics: Warning Messages and Convergence Issues"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, estimation, REML, MLE, convergence, warning-messages, variance-components, linear-mixed-effects]
category: "master-courses/longitudinal-data-analysis/estimation-model-fit"
compiled: true
---

# REML and MLE Advanced Topics: Warning Messages and Convergence Issues

Lecture 7a (March 6, 2025) extends the MLE/REML framework with a focus on practical computing issues: when and why the optimization algorithms fail to converge, how to interpret warning messages, and the critical distinction between $\theta \to 0$ and $\theta \to \infty$ scenarios.

## Overview

Building on the ball weight problem from Lecture 6, this lecture demonstrates that both REML and MLE can produce warning messages when the optimization diverges. The key parameter $\theta = \sigma/\sigma_b$ can drift toward 0 or infinity, each with distinct consequences for the estimated model.

## Review: MLE vs REML Algorithm

For the LME model $Y_{ij} = \beta_1 x_{ij1} + \cdots + \beta_p x_{ijp} + b_i + \epsilon_{ij}$:

**MLE**: Find $(\beta_1, \ldots, \beta_p, \sigma_b, \sigma)$ maximizing:

$$L(\beta_1, \ldots, \beta_p, \sigma_b, \sigma) = \prod_{i=1}^{m} f(Y_{i1}, \ldots, Y_{i,n_i})$$

**REML** (two-step):
1. Find $(\sigma_b, \sigma)$ maximizing the restricted likelihood $L_{RE}(\sigma_b, \sigma) = \iiint L(\beta_1, \ldots, \beta_p, \sigma_b, \sigma) d\beta_1 \cdots d\beta_p$
2. With estimated $(\hat{\sigma}_b, \hat{\sigma})$, find $(\beta_1, \ldots, \beta_p)$ maximizing $L(\beta_1, \ldots, \beta_p, \hat{\sigma}_b, \hat{\sigma})$

## Computing Issues

Both REML and MLE might not converge and produce warning messages:

1. **Non-unique optimal solution**: When minimizing $RSS(\theta)$, the standard linear regression $Y \sim X_1 + \cdots + X_p$ may have infinite solutions due to collinearity
2. **Divergent $\theta$**: When minimizing the likelihood function, the optimization algorithm for estimating $\theta$ might diverge, e.g., $\theta \to 0$ or $\theta \to \infty$

## Ball Weight Problem Revisited (Jack/Kathy)

### REML Output (works well)

```r
lme1 <- lmer(Y ~ X1 + X2 - 1 + (1 | ID), data=data1)
```

- $\hat{\theta} = 0.2236/0.5000 = 0.4472$
- Fixed effects: X1 = 1.80, X2 = 3.65
- Random effects: $\hat{b}_1 = 0.25$, $\hat{b}_2 = -0.50$
- Variance: ID (Intercept) = 0.25, Residual = 0.05

### MLE Output (fails!)

```r
lme2 <- lmer(Y ~ X1 + X2 - 1 + (1 | ID), REML=F, data=data1)
```

**Warning messages**:
1. `NLOPT_ROUNDOFF_LIMITED`: Roundoff errors broke the optimization algorithm
2. `unable to evaluate scaled gradient`
3. `Model failed to converge: degenerate Hessian with 1 negative eigenvalue`

**MLE results** (problematic):
- Fixed effects: X1 = 2.000, X2 = 4.000
- Random effects: $\hat{b}_1 \approx 0$, $\hat{b}_2 = -1.000$
- Variance: ID (Intercept) = 0.25, **Residual = 1.672e-17** (essentially zero!)

The MLE has $\hat{\theta} \to 0$, meaning $\hat{\sigma} \to 0$ while $\hat{\sigma}_b$ stays finite.

## Potential Issue: $\theta \to 0$

When $\hat{\theta} \to 0$ (i.e., $\sigma \to 0$), the penalty on random effects vanishes:

$$RSS(\theta) = \sum_{i=1}^{m} \left( \sum_{j=1}^{n_i} (Y_{ij} - (\beta_1 x_{ij1} + \cdots + \beta_p x_{ijp} + b_i))^2 + \theta^2 b_i^2 \right)$$

With $\theta = 0$, the augmented data becomes:

| Y | X1 | X2 | b1 | b2 |
|---|----|----|----|----|
| 2 | 1  | 0  | 1  | 0  |
| 4 | 0  | 1  | 1  | 0  |
| 0 | 0  | 0  | 0  | 0  |
| 3 | 0  | 1  | 0  | 1  |
| 5 | 1  | 1  | 0  | 1  |
| 0 | 0  | 0  | 0  | 0  |

**Perfect fit**: $\hat{A} = 2, \hat{B} = 4, \hat{b}_1 = 0, \hat{b}_2 = -1, RSS = 0$!

The MLE of $\hat{\theta} = 0$ means the likelihood is maximized at the boundary.

## Potential Issue: $\theta \to \infty$

### Example 2: David/Emily/Frank

Three students each take 3 measurements of different ball combinations. REML gives $\hat{\theta} = 7570.023$ (diverging to infinity), while MLE gives $\hat{\theta} = \infty$.

When $\hat{\theta} \to \infty$, we have $\hat{\sigma}_b = \hat{\sigma}/\hat{\theta} = 0$:
- $b_1 = \cdots = b_m = 0$ (no random effects needed)
- The model reduces to standard linear regression
- No need for mixed-effects framework at all

**MLE output** (`boundary (singular) fit`):
- Random effects variance: ID (Intercept) = 0.0000
- All random effects: David = 0, Emily = 0, Frank = 0

## Comparing the Likelihood Functions

### When $\theta \to 0$ (Jack/Kathy MLE)

The log-likelihood is monotonically decreasing toward $\theta = 0$, with no interior maximum. The MLE pushes $\theta$ to the boundary.

### When $\theta \to \infty$ (David/Emily/Frank MLE)

The log-likelihood is monotonically increasing toward $\theta = \infty$. The MLE pushes $\theta$ to infinity, eliminating the random effects.

## The Optional REML vs MLE Likelihood

For the ball weight problem, the explicit forms are:

**MLE likelihood**:
$$Lik(\theta) = \frac{16 \theta^2}{(\sqrt{2\pi})^4 (\theta^2 + 2)[RSS(\theta)]^2} \exp(-2)$$

**REML likelihood**:
$$L_{RE}(\theta) = \frac{\theta^2}{\pi \sqrt{5\theta^4 + 10\theta^2 + 1} \cdot RSS(\theta)} \exp(-1)$$

The REML likelihood has a proper interior maximum at $\hat{\theta}_{REML} = 0.4472$, while the MLE likelihood does not for this particular dataset.

## What If There Is a Warning Message?

When running REML or MLE and encountering a warning:

1. **It is likely that $\hat{\theta} \to 0$ or $\infty$**
2. **The variance estimates of $\sigma$ and $\sigma_b$ can be problematic** (e.g., one is 0). More generally, the covariance structure estimate can be problematic
3. **Check insights** by examining $RSS(\theta)$ and the profile likelihood function as functions of $\theta$
4. **The fixed-effect point estimates $(\hat{\beta}_1, \ldots, \hat{\beta}_p)$ might still be meaningful**, but hypothesis testing and confidence intervals will likely be problematic

## Summary

| Point | Detail |
|-------|--------|
| REML vs MLE agreement | Often similar results, esp. when $p$ is small |
| Warning messages | Algorithm for variance component estimation likely did not converge ($\theta \to 0$ or $\infty$) |
| REML advantage | Better for parameter inference; often yields unbiased estimators |
| MLE advantage | Better for model selection/comparison via AIC/BIC/log-likelihood |
| REML limitation | Cannot be used for AIC/BIC criterion |

## Key Takeaways

1. Warning messages in `lmer()` typically indicate $\theta$ diverging to 0 or infinity
2. $\theta \to 0$ means zero residual variance (overfitting with random effects absorbing all error)
3. $\theta \to \infty$ means zero random-effect variance (no between-subject variability -- model reduces to standard regression)
4. REML is more robust than MLE in small-sample scenarios -- it can find a proper interior maximum when MLE cannot
5. Always inspect the profile likelihood function to understand convergence behavior
6. Fixed-effect estimates may still be usable even when variance estimation fails

## Original Slides

![[assets/Lecture 7a - REMl.MLE.warning messages.pdf]]
