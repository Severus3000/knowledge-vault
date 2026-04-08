---
title: "CHD Applied Example: Logistic Regression in Practice with R"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, logistic-regression, CHD, R-programming, applied-example, hypothesis-testing]
category: "master-courses/longitudinal-data-analysis/logistic-longitudinal"
compiled: true
---

## Overview

This lecture applies logistic regression to a real-world coronary heart disease (CHD) dataset using R. It demonstrates both continuous-predictor logistic regression (Age as continuous) and the simplest logistic regression (Age dichotomized at 50), including hand calculations that verify the R output.

## The CHD Dataset

- **Response** $Y$ (CHD): 0 = No disease, 1 = Disease
- **Predictor** $X$: Age (continuous, range 20--69)
- **Sample size**: $n = 100$ (43 with disease, 57 without)
- **Research questions**: Is Age associated with CHD? How to predict CHD from Age?

### Exploratory Data Analysis

```r
data0 <- read.table("chdage.csv", head=T, sep=",")
summary(data0)
```

| Statistic | Age | CHD |
|-----------|------|------|
| Min | 20.00 | 0.00 |
| 1st Qu. | 34.75 | 0.00 |
| Median | 44.00 | 0.00 |
| Mean | 44.38 | 0.43 |
| 3rd Qu. | 55.00 | 1.00 |
| Max | 69.00 | 1.00 |

## Logistic Regression with Continuous Predictor

### Fitting the Model in R

```r
glm1 <- glm(CHD ~ Age, family=binomial(link="logit"), data=data0)
summary(glm1)
```

| | Estimate | Std. Error | z value | Pr(>\|z\|) |
|---|----------|-----------|---------|-----------|
| (Intercept) | -5.30945 | 1.13365 | -4.683 | 2.82e-06 |
| Age | 0.11092 | 0.02406 | 4.610 | 4.02e-06 |

**Fitted model**:

$$\log\left(\frac{P(Y=1)}{1 - P(Y=1)}\right) = -5.3095 + 0.1109 \cdot \text{Age}$$

**Interpretation**: For each one-year increase in age, the log-odds of CHD increases by 0.1109 (equivalently, the odds are multiplied by $e^{0.1109} \approx 1.117$).

### Confidence Intervals

```r
confint(glm1, level=0.95)
```

| | 2.5% | 97.5% |
|---|------|-------|
| (Intercept) | -7.7259 | -3.2462 |
| Age | 0.0669 | 0.1620 |

Since the 95% CI for Age does not contain 0, Age is significantly associated with CHD.

## Simplest Logistic Regression: Dichotomized Age

### Setup

Define $\text{Flag} = I(\text{Age} \geq 50)$ -- a binary indicator for age 50 or older.

**Model**: $\log \frac{\pi_i}{1 - \pi_i} = \beta_0 + \beta_1 \cdot \text{Flag}_i$

**Question**: Is $\text{Age} \geq 50$ a risk factor of CHD?

### R Analysis

```r
flag <- I(Age >= 50)
glm2 <- glm(CHD ~ flag, family=binomial(link="logit"), data=data0)
summary(glm2)
```

| | Estimate | Std. Error | z value | Pr(>\|z\|) |
|---|----------|-----------|---------|-----------|
| (Intercept) | -1.0380 | 0.2822 | -3.678 | 0.000235 |
| flagTRUE | 2.0989 | 0.4788 | 4.384 | 1.17e-05 |

**Fitted model**:

$$\log\left(\frac{P(Y=1)}{1 - P(Y=1)}\right) = -1.0380 + 2.0989 \cdot I(\text{Age} \geq 50)$$

### Verification by Hand

The 2x2 table:

| | CHD+ ($Y=1$) | CHD- ($Y=0$) | Sum |
|---|---|---|---|
| Age $\geq$ 50 ($X=1$) | $a = 26$ | $b = 9$ | 35 |
| Age $< 50$ ($X=0$) | $c = 17$ | $d = 48$ | 65 |

**Hand calculations**:

$$\hat{\beta}_0 = \log\left(\frac{c}{d}\right) = \log\left(\frac{17}{48}\right) = -1.0380$$

$$\hat{\beta}_1 = \log\left(\frac{ad}{bc}\right) = \log\left(\frac{26 \times 48}{9 \times 17}\right) = 2.0989$$

**Standard errors**:

$$\text{se}(\hat{\beta}_0) = \sqrt{\frac{1}{17} + \frac{1}{48}} = 0.2822$$

$$\text{se}(\hat{\beta}_1) = \sqrt{\frac{1}{26} + \frac{1}{9} + \frac{1}{17} + \frac{1}{48}} = 0.4788$$

These match the R output exactly.

### Hypothesis Test

Testing $H_0: \beta_1 = 0$ against $H_1: \beta_1 \neq 0$:

$$Z_{\text{obs}} = \frac{\hat{\beta}_1 - 0}{\text{se}(\hat{\beta}_1)} = \frac{2.0989}{0.4788} = 4.3837$$

$$p\text{-value} = 2P(N(0,1) > 4.3837) = 1.167 \times 10^{-5}$$

**Conclusion**: Age $\geq 50$ is a statistically significant risk factor of CHD.

## Key Takeaways

- R's `glm()` with `family=binomial(link="logit")` fits logistic regression models
- For continuous predictors, interpretation is per-unit change in log-odds
- For binary predictors, the coefficient equals the log odds ratio from the 2x2 table
- Hand calculations using the closed-form MLE formulas match software output exactly
- Always verify model results with exploratory plots (`plot(Age, CHD)` + fitted curve)

## Original Slides

![[assets/9.4_CHD_Example.pdf]]
