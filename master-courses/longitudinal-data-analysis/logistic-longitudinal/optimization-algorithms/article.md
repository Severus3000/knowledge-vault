---
title: "Optimization Algorithms for Logistic Regression: Gradient Descent and Newton-Raphson"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, logistic-regression, optimization, newton-raphson, gradient-descent, IRLS]
category: "master-courses/longitudinal-data-analysis/logistic-longitudinal"
compiled: true
---

## Overview

This lecture covers two fundamental optimization algorithms -- Gradient Descent and Newton-Raphson -- and applies Newton-Raphson to compute the MLE in logistic regression. The Newton-Raphson method applied to logistic regression yields the Iteratively Reweighted Least Squares (IRLS) algorithm, which is the standard algorithm used by statistical software.

## The Optimization Problem

In statistics and machine learning, we often face:

$$\hat{\theta} = \underset{\theta \in \Theta \subset \mathbb{R}^p}{\text{argmin}} \; h(\theta)$$

When $h(\theta)$ is smooth, we want to solve $h'(\theta) = 0$ using **iterative methods**: find a sequence of $\theta^{(i)}$ values until convergence to $\hat{\theta}$, where $h'(\hat{\theta}) = 0$.

## Two Optimization Algorithms

### 1. Gradient Descent

Widely used in machine learning:

$$\theta_{\text{new}} = \theta_{\text{old}} - \lambda \, h'(\theta_{\text{old}})$$

where $\lambda$ is the **learning rate**.

### 2. Newton-Raphson Method

Very popular in statistics:

$$\theta_{\text{new}} = \theta_{\text{old}} - [h''(\theta_{\text{old}})]^{-1} h'(\theta_{\text{old}})$$

### Derivation via Taylor Expansion

Starting at $\theta_{\text{old}}$, we want to update to $\theta_{\text{new}} = \theta_{\text{old}} + \epsilon$ such that $h'(\theta_{\text{new}}) = 0$.

By **Taylor series expansion** (one-dimensional case):

$$h'(\theta_{\text{old}} + \epsilon) \approx h'(\theta_{\text{old}}) + \epsilon \, h''(\theta_{\text{old}})$$

Setting to 0:

$$\epsilon \approx -\frac{h'(\theta_{\text{old}})}{h''(\theta_{\text{old}})}$$

For high-dimensional $\theta$, this generalizes to:

$$\boldsymbol{\theta}_{\text{new}} = \boldsymbol{\theta}_{\text{old}} - [h''(\boldsymbol{\theta}_{\text{old}})]^{-1} h'(\boldsymbol{\theta}_{\text{old}})$$

### Why Newton-Raphson is Popular in Statistics

At convergence, Newton-Raphson provides two values:

- The estimate $\hat{\theta}$
- The variance estimate $\hat{V} = -[h''(\hat{\theta})]^{-1}$

When $h(\theta)$ is the log-likelihood function, by asymptotic theory:

$$\frac{\hat{\theta} - \theta}{\sqrt{\hat{V}}} \sim N(0, 1)$$

yielding the 95% confidence interval: $\hat{\theta} \pm 1.96 \sqrt{\hat{V}}$.

## Application to Logistic Regression

### Log-likelihood and Derivatives

The log-likelihood (in vector notation):

$$\log L(\beta) = \sum_{i=1}^{n} [y_i \beta^\top x_i - \log(1 + e^{\beta^\top x_i})]$$

**First-order derivatives (score/gradient)**:

$$\frac{\partial \log L(\beta)}{\partial \beta} = \sum_{i=1}^{n} (y_i - \pi_i) x_i$$

**Second-order derivatives (Hessian)**:

$$\frac{\partial^2 \log L(\beta)}{\partial \beta \partial \beta^\top} = -\sum_{i=1}^{n} x_i \pi_i (1 - \pi_i) x_i^\top$$

### Newton-Raphson for Logistic Regression (IRLS)

Let $\pi = (\pi_1, \ldots, \pi_n)^\top$ and $W = \text{diag}(\pi_i(1-\pi_i))$, both depending on $\beta_{\text{old}}$.

Then $h'(\beta) = X^\top(Y - \pi)$ and $h''(\beta) = -X^\top W X$.

Applying Newton-Raphson:

$$\boldsymbol{\beta}_{\text{new}} = \boldsymbol{\beta}_{\text{old}} + (X^\top W X)^{-1} X^\top (Y - \pi) = (X^\top W X)^{-1} X^\top W Z$$

where $Z = X \boldsymbol{\beta}_{\text{old}} + W^{-1}(Y - \pi)$ is the **adjusted response**. This is **weighted least squares** -- hence the name IRLS.

### Complete Algorithm

1. Initialize $\beta_{\text{init}} = 0$
2. Given $\beta_{\text{old}}$, compute three variables:
   - $\hat{\pi}_i = \frac{e^{\beta_{\text{old}}^\top x_i}}{1 + e^{\beta_{\text{old}}^\top x_i}}$
   - $w_i = \hat{\pi}_i(1 - \hat{\pi}_i)$
   - $Z_i = \beta_{\text{old}}^\top x_i + \frac{Y_i - \hat{\pi}_i}{\hat{\pi}_i(1 - \hat{\pi}_i)}$
3. Conduct weighted least squares: $\beta_{\text{new}} \leftarrow \underset{\beta}{\text{argmin}} [(Z - X\beta)^\top W (Z - X\beta)]$
4. Repeat step 2-3 until convergence

> **Remark**: The algorithm fails only when $\hat{\pi}_i = 0$ or $1$, i.e., with perfect fits.

## Key Takeaways

- Gradient Descent uses only first derivatives; Newton-Raphson uses both first and second derivatives
- Newton-Raphson converges faster (quadratically) and naturally provides variance estimates
- Applied to logistic regression, Newton-Raphson becomes the IRLS algorithm -- iteratively solving weighted least squares problems
- The algorithm is the standard method used by `glm()` in R

## Original Slides

![[assets/9.2_Optimizations_in_Logistic_Regression.pdf]]
