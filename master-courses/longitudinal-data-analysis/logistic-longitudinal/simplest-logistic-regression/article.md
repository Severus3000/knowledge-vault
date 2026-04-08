---
title: "Simplest Logistic Regression: Closed-Form MLE for Binary Predictors"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, logistic-regression, MLE, odds-ratio, 2x2-table, confidence-interval, fisher-information]
category: "master-courses/longitudinal-data-analysis/logistic-longitudinal"
compiled: true
---

## Overview

This lecture derives the explicit (closed-form) MLE for the simplest logistic regression model -- when $p = 2$ and the single predictor $x_{i1} \in \{0, 1\}$. This special case connects logistic regression to the classic 2x2 contingency table analysis common in biostatistics, and provides intuition for the general theory.

## The Simplest Model

When $p = 2$ and $x_i \in \{0, 1\}$:

$$P(Y_i = 1) = \pi_i, \quad P(Y_i = 0) = 1 - \pi_i$$

$$\log \frac{\pi_i}{1 - \pi_i} = \beta_0 + \beta_1 x_i$$

### Data as a 2x2 Table

The data $(Y_i, x_i)$ can be summarized as a 2x2 contingency table:

|  | $Y = 1$ | $Y = 0$ | Sum |
|---|---------|---------|-----|
| $X = 1$ | $a$ | $b$ | $a + b$ |
| $X = 0$ | $c$ | $d$ | $c + d$ |

where $n = a + b + c + d$.

In biostatistics, $X$ typically refers to **exposure** (e.g., does the subject smoke?) and $Y$ to **disease** (e.g., lung cancer).

## Deriving the MLE

### Likelihood Function

$$L(\boldsymbol{\beta}) = \prod_{i=1}^{n} \frac{e^{Y_i(\beta_0 + \beta_1 x_i)}}{1 + e^{\beta_0 + \beta_1 x_i}} = \frac{e^{\beta_0(a+c) + \beta_1 a}}{(1 + e^{\beta_0 + \beta_1})^{a+b} (1 + e^{\beta_0})^{c+d}}$$

### Log-Likelihood and Score Equations

$$\log L = (a + c)\beta_0 + a\beta_1 - (c + d)\log(1 + e^{\beta_0}) - (a + b)\log(1 + e^{\beta_0 + \beta_1})$$

Setting partial derivatives to zero:

$$\frac{\partial \log L}{\partial \beta_0} = (a + c) - (c + d)\frac{e^{\beta_0}}{1 + e^{\beta_0}} - (a + b)\frac{e^{\beta_0 + \beta_1}}{1 + e^{\beta_0 + \beta_1}} = 0$$

$$\frac{\partial \log L}{\partial \beta_1} = a - (a + b)\frac{e^{\beta_0 + \beta_1}}{1 + e^{\beta_0 + \beta_1}} = 0$$

### Closed-Form Solutions

$$\hat{\beta}_0 = \log\left(\frac{c}{d}\right) \qquad \text{and} \qquad \hat{\beta}_1 = \log\left(\frac{ad}{bc}\right)$$

Note that $\hat{\beta}_1$ is the **log odds ratio**, a fundamental measure of association in epidemiology.

## Fisher Information and Variance

### Fisher Information Matrix

For $\theta = (\beta_0, \beta_1)^\top$:

$$I(\hat{\theta}) = -\frac{\partial^2 \log L(\theta)}{\partial \theta \partial \theta^\top}\bigg|_{\hat{\theta}} = \begin{pmatrix} \frac{ab}{a+b} + \frac{cd}{c+d} & \frac{ab}{a+b} \\ \frac{ab}{a+b} & \frac{ab}{a+b} \end{pmatrix}$$

### Covariance Matrix of MLE

$$\text{Cov}(\hat{\theta}) = I(\hat{\theta})^{-1} = \begin{pmatrix} \frac{1}{c} + \frac{1}{d} & -\left(\frac{1}{c} + \frac{1}{d}\right) \\ -\left(\frac{1}{c} + \frac{1}{d}\right) & \frac{1}{a} + \frac{1}{b} + \frac{1}{c} + \frac{1}{d} \end{pmatrix}$$

### Variance of $\hat{\beta}_1$

$$\widehat{\text{Var}}(\hat{\beta}_1) = \frac{1}{a} + \frac{1}{b} + \frac{1}{c} + \frac{1}{d}$$

## Testing Association

**Hypothesis**: $H_0: \beta_1 = 0$ vs. $H_1: \beta_1 \neq 0$

**95% Confidence Interval** for $\beta_1$:

$$\log\left(\frac{ad}{bc}\right) \pm 1.96 \sqrt{\frac{1}{a} + \frac{1}{b} + \frac{1}{c} + \frac{1}{d}}$$

$X$ is associated with $Y$ **if and only if 0 is outside this CI**.

## Key Takeaways

- When both $X$ and $Y$ are binary, the MLE has a closed-form solution
- $\hat{\beta}_1 = \log(\text{odds ratio})$ -- directly interpretable as the log of the cross-product ratio
- The variance $\text{Var}(\hat{\beta}_1) = 1/a + 1/b + 1/c + 1/d$ -- the classic formula for variance of the log odds ratio
- Testing $\beta_1 = 0$ is equivalent to testing independence in the 2x2 table
- This special case builds intuition for the general logistic regression framework

## Original Slides

![[assets/9.3_Simplest_Logistic_Regression.pdf]]
