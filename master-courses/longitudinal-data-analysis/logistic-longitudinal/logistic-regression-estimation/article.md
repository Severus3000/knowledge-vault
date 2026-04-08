---
title: "Logistic Regression Estimation: Model Building and MLE"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, logistic-regression, maximum-likelihood, estimation, classification]
category: "master-courses/longitudinal-data-analysis/logistic-longitudinal"
compiled: true
---

## Overview

This lecture provides a comprehensive review of binary logistic regression, covering the model formulation, maximum likelihood estimation (MLE), asymptotic properties of the MLE, the latent variable interpretation, and alternative link functions. It serves as the foundation for extending logistic regression to longitudinal data settings.

## Classification Methods

Given data $(Y_i, x_{i1}, \ldots, x_{i,p-1})$ for $i = 1, \ldots, n$, where $Y_i$ is the class label, there are two probability-based approaches:

1. **Model the conditional densities** $f_k = p(X | Y = k)$ at a given $k$-th class
   - Normality assumption on $X$: LDA, QDA, Naive Bayes
2. **Model the conditional probability** $P(Y = k | X)$ directly
   - Bernoulli assumption on $Y$: **logistic regression**

## Binary Logistic Regression Model

The logistic regression model has two components:

1. **Response distribution**: Model $Y$ as Bernoulli:

$$P(Y_i = 1) = \pi_i, \quad P(Y_i = 0) = 1 - \pi_i$$

2. **Link function**: Connect parameters to predictors via the logit link:

$$\log \frac{\pi_i}{1 - \pi_i} = \beta_0 + \beta_1 x_{i1} + \beta_2 x_{i2} + \cdots + \beta_{p-1} x_{i,p-1}$$

where $p$ is the number of $\beta$ coefficients.

### Basic Concepts

- **Probability**: $P(Y_i = 1) = \pi_i$
- **Odds**: $\text{Odd}_i = \frac{\pi_i}{1 - \pi_i}$
- **Odds Ratio**: $\theta = \frac{\text{Odd}_1}{\text{Odd}_2} = \frac{\pi_1 / (1 - \pi_1)}{\pi_2 / (1 - \pi_2)}$

### Conditional Probabilities

Under the logistic regression model, at a given $X = (x_1, \ldots, x_{p-1})$:

$$P(Y = 1 | X) = \pi = \frac{e^{\beta_0 + \beta_1 x_1 + \cdots + \beta_{p-1} x_{p-1}}}{1 + e^{\beta_0 + \beta_1 x_1 + \cdots + \beta_{p-1} x_{p-1}}}$$

$$P(Y = 0 | X) = 1 - \pi = \frac{1}{1 + e^{\beta_0 + \beta_1 x_1 + \cdots + \beta_{p-1} x_{p-1}}}$$

## Maximum Likelihood Estimation

### Likelihood Function

The likelihood function of the logistic regression model is:

$$L(\boldsymbol{\beta}) = \prod_{i=1}^{n} \pi_i^{y_i} (1 - \pi_i)^{1 - y_i} = \prod_{i=1}^{n} \frac{e^{y_i(\beta_0 + \beta_1 x_{i1} + \cdots + \beta_{p-1} x_{i,p-1})}}{1 + e^{\beta_0 + \beta_1 x_{i1} + \cdots + \beta_{p-1} x_{i,p-1}}}$$

The MLE $\hat{\boldsymbol{\beta}}$ is found by maximizing $L(\boldsymbol{\beta})$.

### Asymptotic Properties of MLE

The MLE has nice asymptotic properties:

$$\hat{\boldsymbol{\beta}} \sim N(\boldsymbol{\beta}, I_{p \times p}^{-1})$$

where $I_{p \times p}$ is the observed **Fisher Information Matrix**, defined by the negative of the second-order derivatives of the log-likelihood:

$$I_{p \times p} = \left( -\frac{\partial^2 \log L}{\partial \beta_i \partial \beta_j} \right) \bigg|_{\hat{\boldsymbol{\beta}}}$$

## Logistic Regression as a Latent Variable Model

An alternative formulation posits:

1. A latent continuous variable: $Y_i^* = \beta_0 + \beta_1 x_{i1} + \cdots + \beta_{p-1} x_{i,p-1} + \epsilon_i$
2. Observed dichotomous response: $Y_i = \begin{cases} 0, & \text{if } Y_i^* < 0 \\ 1, & \text{if } Y_i^* \geq 0 \end{cases}$
3. Error terms $\epsilon_i$ are iid with a **logistic distribution**:
   - PDF: $f(\epsilon) = \frac{\exp(-\epsilon)}{[1 + \exp(-\epsilon)]^2}$
   - CDF: $F(\epsilon) = \frac{1}{1 + \exp(-\epsilon)}$

## Other Link Functions (Generalized Linear Model)

The logistic regression is a special case of the GLM framework with two steps:

1. $P(Y_i = 1) = \pi_i$, $P(Y_i = 0) = 1 - \pi_i$
2. $g(\pi_i) = \beta_0 + \beta_1 x_{i1} + \cdots + \beta_{p-1} x_{i,p-1}$

where $g(\cdot): (0,1) \to (-\infty, \infty)$ is the **link function**.

Alternative link functions include:

- **Normit/Probit Link**: $g = \Phi^{-1}$, where $\Phi(t) = P(N(0,1) \leq t)$ is the CDF of the standard normal. Corresponds to error terms $\epsilon_i \sim N(0, \sigma_\epsilon^2)$.

## Key Takeaways

- Logistic regression models $P(Y=1|X)$ directly using the logit link function
- MLE is used for parameter estimation (no closed-form solution in general)
- The MLE is asymptotically normal with covariance given by the inverse Fisher Information Matrix
- The logistic model can be viewed through a latent variable lens with logistic-distributed errors
- Logistic regression is a special case of GLMs; the probit model uses normal errors instead

## Original Slides

![[assets/9.1_Logistic_Regression_Estimation.pdf]]
