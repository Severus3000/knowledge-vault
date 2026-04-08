---
title: "Local Smoothing Methods for Longitudinal Data"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, local-smoothing, loess, kernel-smoothing, spline-smoothing, nonparametric-regression]
category: "master-courses/longitudinal-data-analysis/foundations"
compiled: true
---

# Local Smoothing Methods for Longitudinal Data

## Overview and Motivation

When exploring longitudinal data, we often want to estimate the underlying trend $f(x)$ without imposing a strict parametric form. Local smoothing methods provide a flexible, nonparametric approach to estimating the relationship between a response $Y$ and a predictor $x$. This lecture covers the distinction between interpolation and smoothing, then presents three popular local smoothers: LOESS, kernel smoothing, and spline smoothing.

## Regression in General

Given data $(Y_i, X_{i1}, \ldots, X_{ip})$ for $i = 1, 2, \ldots, n$:

- The ordinary linear regression model assumes:

$$Y = \beta_0 + \beta_1 X_1 + \cdots + \beta_p X_p + \epsilon$$

but this may be too restrictive.

- A more general model allows:

$$Y = f(X_1, X_2, \ldots, X_p) + \epsilon$$

for a broad class of "smooth" functions $f$.

### Special Case: $p = 1$

- **Data**: $(Y_i, x_i)$, $i = 1, 2, \ldots, n$
- **Objective**: Predict $Y$ at a given $X = x$
- **Model**: $Y_i = f(x_i) + \epsilon_i$ for some nonlinear function $f(\cdot)$
- **Question**: How to estimate $f$?

## Method of Least Squares

We want to find a function $f$ to minimize the residual sum of squares:

$$RSS = \sum_{i=1}^{n} \epsilon_i^2 = \sum_{i=1}^{n} (Y_i - f(x_i))^2$$

If we seek $f$ that passes through all points (i.e., $RSS = 0$), we get **interpolation**.

## Interpolation

Three popular interpolation methods:

1. **Piecewise constant** -- Discontinuous; uses only one data point per interval
2. **Piecewise linear interpolation** -- Connects adjacent points with straight lines
3. **Polynomial interpolation** -- Very smooth; uses a single high-degree polynomial through all points

### Weakness of Interpolation

- Easy to understand and provides a good picture, but generally inadequate for prediction or estimation
- Difficult to control model complexity
- **Local vs. Global tradeoff**:
  - Piecewise constant/linear is too local (uses only 1-2 data points)
  - Polynomial interpolation uses all data points but performs poorly when $n$ is large (Runge's phenomenon)

## Transition to Local Smoothers

- **Interpolation** assumes all error terms $\epsilon_i \equiv 0$
- **Local Smoothers** allow non-zero (ideally small) error terms and assume $f(\cdot)$ is locally smooth

### Problem Formulation

- **Data**: $(Y_i, x_i)$ for $i = 1, 2, \ldots, n$
- **Model**: $Y_i = f(x_i) + \epsilon_i$ where $\epsilon_i$ are i.i.d. with mean 0
- **Question**: Estimate $f(x)$ at a given $x$

## 1. LOESS/LOWESS Algorithm

**LOcally Estimated/Weighted Scatterplot Smoothing**, developed by Cleveland (1979).

### High-Level Idea

Combines two concepts:
- **k-nearest neighbor**: For a given $x$, find the $k$ training data points closest to $x$
- **Weighted linear regression**: Fit a low-degree polynomial (degree 1-3) using locally weighted least squares, where closer points receive more weight

The predicted value $\hat{Y} = \hat{f}(x)$ comes from this local polynomial at $x$.

### Algorithm Details

**Step 1**: Define the tri-cube weight function at a given $x$:

$$w_i = \begin{cases} \left(1 - \left|\frac{x_i - x}{d_k}\right|^3\right)^3 & \text{if } |x_i - x| \leq d_k \\ 0 & \text{otherwise} \end{cases}$$

where $d_k$ = the $k$-th smallest distance from any $x_i$ to $x$.

**Step 2**: Fit the weighted least squares:

$$\hat{\beta} = \arg\min \sum_{i=1}^{n} w_i \left(Y_i - (\beta_0 + \beta_1 x_i + \beta_2 x_i^2 + \beta_3 x_i^3)\right)^2$$

**Step 3**: Predict at the given $x$:

$$\hat{f}(x) = \hat{\beta}_0 + \hat{\beta}_1 x + \hat{\beta}_2 x^2 + \hat{\beta}_3 x^3$$

### Advantages

- Nonparametric -- does not fit a closed-form function
- Works best on large, densely sampled, low-dimensional data

### Weaknesses

- Computationally expensive; needs a lot of data for good fit
- No convenient closed-form function, making results hard to communicate
- Not intended for high-dimensional data

## 2. Kernel Smoothing

### High-Level Idea

Kernel smoothing is **linear** in the sense that the estimate is a weighted average of the observed $Y_i$ values:

$$\hat{f}(x) = \sum_{i=1}^{n} w(x_i, x) Y_i$$

where the weights $w(x_i, x)$ are constructed from a kernel function $K_h(u)$ that describes the "distance" between $x_i$ and $x$.

- The **shape** of the weights comes from the kernel $K(u)$
- The **size** of the weights is determined by the **bandwidth** $h$

### Nadaraya-Watson Estimator

The Nadaraya-Watson (NW) kernel estimate of $f(x)$ is:

$$\hat{f}(x) = \sum_{i=1}^{n} w(x_i, x) Y_i = \frac{\sum_{i=1}^{n} K_h(x - x_i) Y_i}{\sum_{i=1}^{n} K_h(x - x_i)}$$

### Kernel Properties

A kernel $K(u)$ is a bounded, continuous function on $(-\infty, \infty)$ satisfying:

1. $K(u) \geq 0$
2. $\int_{-\infty}^{+\infty} K(u) \, du = 1$

The scaled kernel: $K_h(u) = \frac{1}{h} K\left(\frac{u}{h}\right)$

**Example** (Gaussian kernel):

$$K(u) = \frac{1}{\sqrt{2\pi}} \exp\left(-\frac{u^2}{2}\right) = \text{pdf of } N(0,1)$$

and $K_h = \text{pdf of } N(0, h^2)$.

### Bandwidth Selection

The bandwidth $h$ controls the bias-variance tradeoff:
- **Small $h$**: Low bias, high variance (wiggly fit)
- **Large $h$**: High bias, low variance (over-smoothed fit)

## 3. Spline Smoothing: Cubic Splines

### Setup

- **Data**: $(Y_i, x_i)$, $i = 1, 2, \ldots, n$, where $a = x_1 < x_2 < \cdots < x_n = b$
- **Model**: $Y_i = f(x_i) + \epsilon_i$
- **Question**: Estimate $f(x)$ at a given $x \in [a, b]$

### Cubic Splines: Piecewise Polynomials of Degree 3

Two approaches:

1. **Interpolating**: $Y_i = f(X_i)$ for all $i$ (passes through every point)
2. **Smoothing**: Solution of the **penalized optimization problem**:

$$\hat{f} = \arg\min_{f \in H^2[a,b]} \left[\frac{1}{n} \sum_{i=1}^{n} (Y_i - f(X_i))^2 + \lambda \int_a^b (f''(t))^2 \, dt \right]$$

The first term measures **goodness of fit** (RSS). The second term is a **roughness penalty** controlled by $\lambda$:
- $\lambda \to 0$: Interpolation (passes through all points)
- $\lambda \to \infty$: Straight line (maximum smoothness)

### Optimization via B-spline Basis

**Idea**: Use the B-spline basis decomposition:

$$\hat{f}(x) = \sum_{i=1}^{n-d} \beta_i B_{i,d}(x)$$

Restate the optimization as a **ridge regression** problem:

$$\hat{\beta} = \arg\min_{\beta} \left[|Y - X\beta|^2 + \lambda^* \beta^T V \beta\right] \quad \text{with } \lambda^* = n\lambda$$

Taking the derivative w.r.t. $\beta$ and setting to 0:

$$-2 U^T(Y - U\beta) + 2\lambda^* V\beta = 0$$

The optimal solution:

$$\hat{\beta} = (U^T U + \lambda^* V)^{-1} U^T Y$$

This has the same form as ridge regression, making computation efficient.

## Comparison of Methods

All three local smoothers produce similar results in practice. Key differences:

| Method | Approach | Key Parameter | Strengths |
|--------|----------|---------------|-----------|
| LOESS | k-NN + local polynomial | $k$ (neighbors) | Nonparametric, intuitive |
| Kernel | Weighted average via kernel | $h$ (bandwidth) | Theoretically elegant, closed-form weights |
| Spline | Penalized piecewise polynomial | $\lambda$ (smoothing) | Efficient computation, global optimization |

## Key Takeaways

1. **Interpolation** (passing through all points) is generally inadequate for prediction -- it overfits noise
2. **Local smoothers** allow non-zero errors and assume local smoothness of $f$
3. **LOESS** combines k-nearest neighbors with weighted polynomial regression; nonparametric but computationally expensive
4. **Kernel smoothing** estimates $f(x)$ as a weighted average of $Y_i$ values using kernel-derived weights; bandwidth $h$ controls the bias-variance tradeoff
5. **Spline smoothing** solves a penalized optimization balancing fit and roughness; connects to ridge regression via B-spline basis
6. All three methods require choosing a **tuning parameter** that controls the smoothness of the estimate

## Original Slides

![[assets/lecture3_local_smooth.pdf]]
