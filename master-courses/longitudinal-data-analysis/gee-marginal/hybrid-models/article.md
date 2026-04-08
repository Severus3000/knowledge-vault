---
title: "Hybrid Models: Combining Fixed and Random Effects in Longitudinal Analysis"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Dr. Cook"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, hybrid-models, fixed-effects, random-effects, within-between, hausman-test, xthybrid]
category: "master-courses/longitudinal-data-analysis/gee-marginal"
compiled: true
---

## Overview

Hybrid models combine the strengths of **fixed effects** and **random effects** models in longitudinal/panel data analysis. They allow simultaneous estimation of **within-person** (time-varying) and **between-person** (time-invariant) effects while producing unbiased within-person estimates that are not contaminated by level-2 heterogeneity. This approach is incredibly useful but under-utilized in practice.

## Motivation: The RE vs. FE Trade-off

### Random Effects Models

- **Key assumption:** the level-2 error $u_i$ is **not correlated** with the covariates
- If this assumption is violated, coefficients are **biased** (omitted variable bias)
- Can estimate effects of both time-varying and time-invariant predictors

### Fixed Effects Models

- Do **not** require the assumption that level-2 errors are uncorrelated with covariates
- Provide **unbiased** estimates of level-1 (time-varying) variables
- **Cannot** estimate effects of level-2 (time-invariant) variables (e.g., race, sex) -- they are absorbed by the individual fixed effects

### The Hybrid Solution

Hybrid models combine both benefits:
- Model **level-1 covariates** that are not biased by level-2 heterogeneity (like FE)
- Model **level-2 time-invariant covariates** (like RE)
- Can be used with both **linear** and **logit** link functions

## The Hybrid Model Formula

$$g(\mu_{ij}) = \beta_W (x_{ij} - \bar{x}_i) + \beta_B \bar{x}_i + \gamma c_i + u_i$$

Where:
- $\beta_W$ = **within-group** (within-person) coefficient -- captures time-varying effects
- $\beta_B$ = **between-group** (between-person) coefficient -- captures cross-sectional differences
- $(x_{ij} - \bar{x}_i)$ = deviation of observation from person-specific mean
- $\bar{x}_i$ = person-specific mean of the time-varying variable
- $c_i$ = time-invariant covariates
- $\gamma$ = coefficient for time-invariant covariates
- $u_i$ = random intercept

## Construction Steps

1. **Calculate person-specific means** of each time-varying predictor $X_{ij}$ -- these represent **between-group differences** ($\bar{X}_i$)
2. **Calculate deviations** from person-specific means: $X_{ij} - \bar{X}_i$ -- these represent **within-group variability**
3. **Estimate a random effects model** that includes both the means and the deviation variables
4. **Test for differences** in between vs. within coefficients (if RE assumptions hold, $\beta_B$ should equal $\beta_W$)
5. Time-invariant predictors can also be included directly

## Example 1: Teen Poverty (Logistic)

**Dataset:** 1,151 teenaged girls interviewed annually for 5 years (1979--1984)

**Outcome:** POV (1 = household in poverty, 0 = not in poverty)

**Predictors:**
- Age (time-invariant at first interview)
- Black (time-invariant: 1 = Black, 0 = other)
- Mother (time-varying: 1 = at least 1 child)
- Spouse (time-varying: 1 = currently living with spouse)
- School (time-varying: 1 = currently enrolled)
- Hours (time-varying: hours worked per week)

### Comparing RE, FE, and Hybrid Results

**Random effects model** (`xtlogit pov ... , re`): All variables estimable, but Hausman test rejects RE assumptions ($\chi^2(8) = 168.18$, $p < 0.0001$).

**Fixed effects model** (`xtlogit pov ... , fe`): Age and Black **dropped** (time-invariant). Remaining coefficients differ from RE -- smaller magnitudes, larger SEs. School coefficient **changed sign**. Sample reduced from 5,755 to 4,135 obs (827 groups with variation).

**Hybrid model** (`xthybrid`): Separates within (W_) and between (B_) effects:

| Variable | Within (W_) | Between (B_) |
|---|---|---|
| Mother | 0.6013*** | 1.0784*** |
| Spouse | -0.8234*** | -2.1452*** |
| School | 0.2914** | -1.3586*** |
| Hours | -0.0208*** | -0.0468*** |

- W_ coefficients are similar to the fixed effects model (but not identical for logistic)
- R_ (time-invariant): Age = -0.1233*, Black = 0.5707***
- If RE assumptions hold, B_ coefficients should equal W_ coefficients -- here they differ substantially, confirming the Hausman test result

## Example 2: Hours Worked (Linear)

**Dataset:** National Longitudinal Survey (NLS) -- Young Women 14-26 years old in 1968 (28,428 obs, 4,709 groups)

**Outcome:** Hours (usual hours worked)

**Predictors:** Age (time-varying), MSP (married spouse present, time-varying), Black and Other (time-invariant race indicators)

### Hybrid Model Results

**Within-person interpretation:**
- Women work **fewer hours** in years when they are **younger and unmarried** relative to years when they are **older and married**

**Between-person interpretation:**
- A 1-unit increase in age is associated with a 0.055 increase in work hours (between persons)
- Never-married women work about **3 hours less** than always-married women

**Test of RE assumptions:** Both $\beta_B(\text{age}) \neq \beta_W(\text{age})$ ($p = 0.0004$) and $\beta_B(\text{msp}) \neq \beta_W(\text{msp})$ ($p < 0.0001$), indicating the RE model is **not preferred**.

### Adding a Random Slope

Using `randomslope(age)` with the hybrid model and comparing via likelihood-ratio test: LR $\chi^2(1) = 1861.97$, $p < 0.0001$ -- the model with random slope is preferred.

## Stata Implementation: `xthybrid`

```stata
* Basic syntax
xthybrid depvar indepvars, use(time_varying_vars) ///
    family(gaussian|binomial) link(identity|logit) ///
    clusterid(id_var) [se] [test] [star]

* Example with random slope
xthybrid hours age msp black other, ///
    clusterid(idcode) se randomslope(age)
```

### Limitations of `xthybrid`

- Factor variable notation (e.g., `i.gender`) is **not supported** -- must create dummies manually
- Temporary variables are created then deleted -- some **post-estimation commands** (e.g., `predict`) will not work
- **Marginal effects** may not be estimable correctly
- **Interaction terms** may be cumbersome to specify
- For logit/Poisson models, within-person estimates may show **slight deviations** from pure fixed effects estimates

## Key Takeaways

1. Hybrid models estimate **both within- and between-person effects** simultaneously while obtaining unbiased within-person estimates
2. The hybrid model decomposes time-varying predictors into person-mean ($\bar{x}_i$) and deviation ($x_{ij} - \bar{x}_i$) components
3. If RE assumptions hold, the between-group coefficients ($\beta_B$) should equal the within-group coefficients ($\beta_W$) -- testing this is a **built-in Hausman-like diagnostic**
4. For **linear** outcomes, within-person estimates mirror fixed effects exactly; for **logistic** models there will be slight deviations
5. Both **random-intercept** and **random-slope** specifications are supported; use `lrtest` to compare model fit
6. Implemented in Stata via `xthybrid`

## Original Slides

![[assets/Lecture 10b - Hybrid.pdf]]
