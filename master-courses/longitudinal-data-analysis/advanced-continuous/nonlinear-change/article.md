---
title: "Nonlinear Change in Longitudinal Growth Models"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Dr. Stephanie H. Cook"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, advanced-modeling, nonlinear-change, variably-spaced-data, discontinuous-change, multilevel-models]
category: "master-courses/longitudinal-data-analysis/advanced-continuous"
compiled: true
---

# Nonlinear Change in Longitudinal Growth Models

## Overview

This lecture addresses treating time more flexibly in longitudinal multilevel models. It covers three major topics: (1) variably spaced measurement occasions and selecting an appropriate time variable, (2) handling varying numbers of measurement occasions across individuals, and (3) modeling discontinuous individual change. The material follows Singer and Willett (ALDA, Chapters 5-6, pp. 138-208).

## Learning Objectives

- Handle variably spaced measurement occasions by selecting the right time variable
- Model data with varying numbers of measurement occasions per person
- Address boundary constraints, nonconvergence, and missing data
- Specify and compare discontinuous level-1 models for change

## 1. Variably Spaced Measurement Occasions

### The Problem of Time

Two key features of longitudinal data:

- **Balanced:** Everyone in the sample has the same number of timepoints (unbalanced otherwise)
- **Time-structured:** Timepoints are consistent for all individuals in the sample

Irregularities arise from:
- Realities of data collection (e.g., Ginexi et al.'s unemployment study)
- Missing data
- Funding delays/gaps (e.g., Flint Adolescent Study)
- By design: accelerated cohort studies where individuals start at different ages

### Selecting a Time Variable

Time can be operationalized in multiple ways, and the choice has real consequences. Three options for the CNLSY reading study:

| Variable | Description | Type |
|---|---|---|
| **WAVE** | Design variable (1, 2, 3) | Not very informative on its own |
| **AGEGRP** | Expected age at data collection (6.5, 8.5, 10.5) | Time-structured |
| **AGE** | Actual age on the day data was collected | Time-unstructured (varies by person) |

The cadence of data does not matter -- what matters is the functional form.

### Variable Selection Process

1. Ask: what is our research question?
2. Fit unconditional growth model using both time variables
3. Assess model fit (AIC/BIC -- can compare across non-nested models; Deviance cannot)

### CNLSY Reading Example (n = 89)

The growth model:

$$Y_{ij} = \pi_{0i} + \pi_{1i}TIME_{ij} + \varepsilon_{ij}$$

$$\pi_{0i} = \gamma_{00} + \zeta_{0i}, \quad \pi_{1i} = \gamma_{10} + \zeta_{1i}$$

**Results (Table 5.2):**

| Parameter | AGEGRP - 6.5 | AGE - 6.5 |
|---|---|---|
| Initial status $\gamma_{00}$ | 21.1629*** | 21.0608*** |
| Rate of change $\gamma_{10}$ | 5.0309*** | 4.5400*** |
| $\sigma^2_\varepsilon$ (within-person) | 27.04*** | 27.45*** |
| $\sigma^2_0$ (initial status) | 11.05* | 5.11 |
| $\sigma^2_1$ (rate of change) | 4.40*** | 3.30*** |
| Deviance | 1819.8 | 1803.9 |
| AIC | 1831.9 | 1815.9 |
| BIC | 1846.9 | 1830.8 |

**Key findings:**
- Very little difference in intercept between models
- Rate of change is half a point larger for AGEGRP (steeper slope due to regular, shorter intervals)
- AGEGRP has larger Level-2 residuals because it fits less well
- **AIC/BIC clearly favor the AGE model** -- treating unstructured data as time-structured introduces error

## 2. Varying Number of Timepoints

### Why It Matters

Individuals can have different numbers of measurement occasions (e.g., 1 to 13 timepoints). Multilevel modeling, unlike repeated measures ANOVA, can handle both issues:
- Varying spacing between occasions
- Varying number of occasions per person

### NLSY Wages Example (n = 888)

Labor market experiences of male high school dropouts:

- **LWN:** Natural logarithm of wages
- **EXPER:** Years of labor force experience (time since first day of work)
- **HGC-9:** Highest grade completed, centered at 9th grade
- **BLACK:** Race/ethnicity indicator (Black vs. White/Latino)

Complications: starting ages 14-17, gaps of 1-2 years between waves, data collection at different times of year, multiple simultaneous jobs, different labor force entry/exit times.

### Model Results (Table 5.4)

| Parameter | Model A | Model B | Model C |
|---|---|---|---|
| $\gamma_{00}$ (Intercept) | 1.7156*** | 1.7171*** | 1.7215*** |
| $\gamma_{01}$ (HGC - 9) | -- | 0.0349*** | 0.0384*** |
| $\gamma_{02}$ (BLACK) | -- | 0.0154 (ns) | -- |
| $\gamma_{10}$ (Rate of change) | 0.0457*** | 0.0493*** | 0.0489*** |
| $\gamma_{11}$ (HGC - 9 on slope) | -- | 0.0013 (ns) | -- |
| $\gamma_{12}$ (BLACK on slope) | -- | -0.0182** | -0.0161*** |
| Deviance | 4921.4 | 4873.8 | 4874.7 |

**Interpretation:**
- $(e^{0.0457} - 1) = 4.7\%$ annual wage increase for average male dropout
- Highest grade completed affects intercept (higher grade = higher initial wages) but not slope
- BLACK is significant for slope but not intercept: wages of Black males increase less rapidly ($e^{0.0328} - 1 = 3.3\%$) compared to White/Latino males ($e^{0.0489} - 1 = 5.0\%$)
- After about 7 years in the labor market, the education effect disappears and race dominates

## 3. Practical Issues

### Boundary Constraints
- Covariance matrix calculates negative values
- "Hessian is not negative semidefinite" error in Stata
- **Fix:** Simplify the model

### Nonconvergence
- Model too complex for the data (highly unbalanced)
- Poorly specified or insufficient data
- **Fix:** Increase iterations or simplify the model
- Problems manifest via variance components, not fixed effects

### Missing Data
- **MCAR** (Missing Completely at Random): Preferred -- no bias
- **MAR** (Missing at Random): Can continue modeling under certain conditions
- **MNAR** (Missing Not at Random): Need a different technique entirely

## 4. Discontinuous Individual Change

### Concept

Discontinuous change occurs when a known event creates a shift in the trajectory. You must know **why** and **when** the change occurs. Examples: relationship status changes affecting depression, GED attainment affecting wages.

Two types of discontinuity:
1. **Slope shift only** -- no immediate jump in level
2. **Elevation and slope shift** -- immediate jump plus change in rate

### GED and Wage Trajectories (Murnane, Boudett & Willett, 1999)

Same 888 male high school dropouts; 34.6% (n = 307) earned a GED during the study. Research question: Does earning a GED affect wage trajectory elevation, slope, or both?

### Four Discontinuous Trajectory Types

**A -- No effect (linear):**

$$Y_{ij} = \pi_{0i} + \pi_{1i}EXPER_{ij} + \varepsilon_{ij}$$

**B -- Elevation shift only:**

$$Y_{ij} = \pi_{0i} + \pi_{1i}EXPER_{ij} + \pi_{2i}GED_{ij} + \varepsilon_{ij}$$

$GED_{ij} = 0$ before obtaining GED, $GED_{ij} = 1$ after. The parameter $\pi_{2i}$ captures the immediate wage jump upon GED receipt.

**C -- Slope shift only:**

$$Y_{ij} = \pi_{0i} + \pi_{1i}EXPER_{ij} + \pi_{3i}POSTEXP_{ij} + \varepsilon_{ij}$$

$POSTEXP_{ij}$ = accumulated work experience after GED (0 before GED). The parameter $\pi_{3i}$ captures the change in rate of wage growth.

**D -- Both elevation and slope shift:**

$$Y_{ij} = \pi_{0i} + \pi_{1i}EXPER_{ij} + \pi_{2i}GED_{ij} + \pi_{3i}POSTEXP_{ij} + \varepsilon_{ij}$$

Alternative formulation using interaction: $Y_{ij} = \pi_{0i} + \pi_{1i}EXPER_{ij} + \pi_{2i}GED_{ij} + \pi_{3i}(GED_{ij} \times EXPER_{ij}) + \varepsilon_{ij}$

Note: In the interaction formulation, the elevation differential depends on when GED was received ($\pi_{2i} + \pi_{3i} \times EXPER$).

### Model Selection (Table 6.2, n = 888)

| Model | Fixed Effects | Variance Components | Deviance | Comparison |
|---|---|---|---|---|
| A | Intercept, EXPER, HGC-9, BLACK x EXPER, URATE-7 | Intercept, EXPER | 4830.5 | -- |
| B | Model A + GED | Intercept, EXPER, GED | 4805.5 | A: 25.0*** (4 df) |
| C | Model B w/o GED | Model B w/o GED | 4818.3 | B: 12.8** (3 df) |
| D | Model A + POSTEXP | Intercept, EXPER, POSTEXP | 4817.4 | A: 13.1** (4 df) |
| **F** | **Model A + GED and POSTEXP** | **Intercept, EXPER, GED, POSTEXP** | **4789.4** | B: 16.2** (5 df); D: 28.1*** (5 df) |
| I | Model A + GED and GED x EXPER | Intercept, EXPER, GED, GED x EXPER | 4787.0 | B: 18.5*** (5 df) |

Model F (with both GED and POSTEXP) provides excellent fit. Model I (interaction formulation) performs similarly.

### Extensions and Considerations

- Effects may depend on **timing** of GED receipt
- Non-linear changes possible before or after the transition
- GED effect might be **instantaneous but not enduring**
- Effect might be **delayed**
- **Multiple transition points** possible (e.g., GED then college entry)
- More limited by data and theory than by ability to specify the model

## Key Takeaways

1. **Choose the right time variable** based on theory and model fit (AIC/BIC). Using time-structured representations for unstructured data introduces error
2. **Multilevel models handle unbalanced data** with varying numbers of timepoints, but severe imbalance can cause convergence problems
3. **Discontinuous change models** use time-varying indicators ($GED$, $POSTEXP$) to capture abrupt shifts at known transition points
4. **Always conceptualize the discontinuity first** -- sketch it out, consult the literature, then specify the statistical model accordingly
5. **Model comparison is iterative**: fit competing models, compare deviance (nested) or AIC/BIC (non-nested), then reconcile with theory
6. **Practical warnings**: boundary constraints, nonconvergence, and missing data patterns (MCAR/MAR/MNAR) require careful attention

## Original Slides

![[assets/Lecture 8b - Nonlinear change.pdf]]
