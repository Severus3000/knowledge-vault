---
title: "Guide: Longitudinal Data Analysis"
type: guide
category: "master-courses/longitudinal-data-analysis"
created: 2026-04-05
updated: 2026-04-05
articles:
  - "[[master-courses/longitudinal-data-analysis/foundations/intro-longitudinal-data/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/foundations/descriptive-statistics/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/foundations/local-smoothing-methods/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/growth-models/within-person-change/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/growth-models/between-person-differences/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/growth-models/linear-growth-model-building/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/estimation-model-fit/mle-reml-estimation/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/estimation-model-fit/reml-mle-advanced/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/estimation-model-fit/model-diagnostics-inference/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/estimation-model-fit/reml-variance-components/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/estimation-model-fit/reml-tutorial/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/advanced-continuous/time-varying-covariates/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/advanced-continuous/nonlinear-change/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/logistic-longitudinal/logistic-regression-estimation/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/logistic-longitudinal/optimization-algorithms/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/logistic-longitudinal/simplest-logistic-regression/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/logistic-longitudinal/chd-applied-example/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/logistic-longitudinal/random-effects-logistic/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/logistic-longitudinal/fixed-effects-models/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/gee-marginal/generalized-estimating-equations/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/gee-marginal/hybrid-models/article.md]]"
  - "[[master-courses/longitudinal-data-analysis/count-generalized/poisson-and-count-models/article.md]]"
tags: [longitudinal-data, mixed-effects, growth-models, estimation, logistic-regression, gee, master-course]
---

# Longitudinal Data Analysis

A comprehensive course covering the theory and application of statistical methods for analyzing repeated-measures and panel data. Progresses from foundational concepts through multilevel growth models, estimation theory, and generalized outcomes.

---

## 1. Foundations of Longitudinal Data

Core concepts, data structures, and exploratory techniques before any modeling.

- [[master-courses/longitudinal-data-analysis/foundations/intro-longitudinal-data/article.md|Introduction to Longitudinal Data]] — What longitudinal data is, why it matters, study types (panel, cohort, retrospective), key statistical challenges
- [[master-courses/longitudinal-data-analysis/foundations/descriptive-statistics/article.md|Descriptive Statistics for Longitudinal Data]] — Wide vs. long formats, profile plots, empirical growth plots, standardization methods
- [[master-courses/longitudinal-data-analysis/foundations/local-smoothing-methods/article.md|Local Smoothing Methods]] — LOESS/LOWESS, kernel smoothing, cubic spline smoothing for trajectory exploration

---

## 2. Multilevel Growth Models

The core modeling framework: within-person change (Level 1) and between-person differences (Level 2).

- [[master-courses/longitudinal-data-analysis/growth-models/within-person-change/article.md|Within-Person Change (Level-1 Model)]] — Individual growth models, structural and stochastic components, Level-1 specification
- [[master-courses/longitudinal-data-analysis/growth-models/between-person-differences/article.md|Between-Person Differences (Level-2 Model)]] — Inter-individual variation, mixed-effects framework, four LME model variants, random effects selection
- [[master-courses/longitudinal-data-analysis/growth-models/linear-growth-model-building/article.md|Linear Growth Model Building Strategy]] — Practical workflow from unconditional means → unconditional growth → final model with predictors

---

## 3. Estimation & Model Fitting

How to fit, compare, and diagnose multilevel models.

- [[master-courses/longitudinal-data-analysis/estimation-model-fit/mle-reml-estimation/article.md|MLE vs. REML Estimation]] — Maximum likelihood and restricted maximum likelihood fundamentals, ball weight example
- [[master-courses/longitudinal-data-analysis/estimation-model-fit/reml-mle-advanced/article.md|REML/MLE Advanced Topics]] — Convergence issues, warning messages, boundary constraints, profile likelihood
- [[master-courses/longitudinal-data-analysis/estimation-model-fit/model-diagnostics-inference/article.md|Model Diagnostics & Inference]] — Five-stage fitting pipeline, deviance tests, AIC/BIC, assumption checking
- [[master-courses/longitudinal-data-analysis/estimation-model-fit/reml-variance-components/article.md|REML Variance Components (Mathematical)]] — Formal derivation via error contrasts and projection matrices
- [[master-courses/longitudinal-data-analysis/estimation-model-fit/reml-tutorial/article.md|REML Tutorial (Zhang 2015)]] — Complete derivation from linear regression bias through REML log-likelihood

---

## 4. Advanced Continuous Outcomes

Extensions for continuous outcomes beyond basic linear growth.

- [[master-courses/longitudinal-data-analysis/advanced-continuous/time-varying-covariates/article.md|Time-Varying Covariates]] — TVCs in growth models, model taxonomy, ICC, model comparison
- [[master-courses/longitudinal-data-analysis/advanced-continuous/nonlinear-change/article.md|Nonlinear Change & Practical Issues]] — Unbalanced data, boundary constraints, missing data, discontinuous change models

---

## 5. Logistic Regression for Longitudinal Data

Transitioning from continuous to binary outcomes in the longitudinal framework.

- [[master-courses/longitudinal-data-analysis/logistic-longitudinal/logistic-regression-estimation/article.md|Logistic Regression Estimation]] — Probability, odds, odds ratios, binary logistic model, MLE
- [[master-courses/longitudinal-data-analysis/logistic-longitudinal/optimization-algorithms/article.md|Optimization Algorithms]] — Gradient descent, Newton-Raphson, IRLS for logistic regression
- [[master-courses/longitudinal-data-analysis/logistic-longitudinal/simplest-logistic-regression/article.md|Simplest Logistic Regression (2×2 Table)]] — Closed-form MLE for binary predictor, Fisher information
- [[master-courses/longitudinal-data-analysis/logistic-longitudinal/chd-applied-example/article.md|CHD Applied Example]] — Coronary heart disease analysis with R `glm()`
- [[master-courses/longitudinal-data-analysis/logistic-longitudinal/random-effects-logistic/article.md|Random Effects Logistic Models]] — Marginal vs. subject-specific, random intercepts, Laplace approximation
- [[master-courses/longitudinal-data-analysis/logistic-longitudinal/fixed-effects-models/article.md|Fixed Effects Models]] — Within estimator, dummy variables, comparison with random effects

---

## 6. GEE & Marginal Models

Population-averaged approaches for correlated non-normal data.

- [[master-courses/longitudinal-data-analysis/gee-marginal/generalized-estimating-equations/article.md|Generalized Estimating Equations (GEE)]] — GLM framework, working correlation, marginal interpretation
- [[master-courses/longitudinal-data-analysis/gee-marginal/hybrid-models/article.md|Hybrid Models]] — Combining random and fixed effects strengths, within/between decomposition

---

## 7. Count Data & Generalized Models

Extending to count outcomes and other GLM families.

- [[master-courses/longitudinal-data-analysis/count-generalized/poisson-and-count-models/article.md|Poisson & Count Data Models]] — Poisson regression, negative binomial, zero-inflated models, mixed-effects extensions
