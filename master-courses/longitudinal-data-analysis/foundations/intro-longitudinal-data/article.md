---
title: "Introduction to Longitudinal Data Analysis"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, repeated-measures, panel-data, study-design, time-series]
category: "master-courses/longitudinal-data-analysis/foundations"
compiled: true
---

# Introduction to Longitudinal Data Analysis

## Overview and Motivation

Longitudinal data analysis is concerned with understanding how phenomena change over time. The defining feature is that **the same individuals are measured repeatedly through time**, allowing direct study of change. This stands in contrast to cross-sectional data, which captures a snapshot at a single point.

The primary objective is to **characterize the change in response over time and the factors that influence change**. With repeated measures on individuals, we can capture within-individual variations that cross-sectional designs cannot reveal.

### Why Longitudinal Data?

- We want to understand how something changes over time
- We need metrics (months, semesters, days, years) to operationalize time
- We are interested in knowing the **functional form** of a phenomenon
- Repeated measures allow capturing **within-individual change**

## Key Concepts and Definitions

### Terminology

- **Individuals/Subjects**: Participants in a longitudinal study
- **Occasions**: Time points at which individuals are measured repeatedly
- **Balanced design**: When the number and timing of repeated measurements are the same for all individuals
- **Incompleteness**: Even balanced designs may have missing data in practice

### Types of Longitudinal Studies

1. **Panel Studies** -- Follow individuals over time who start at the same time with data collected at uniform intervals (e.g., Panel Study of Income Dynamics)
2. **Retrospective Studies** -- Look back to understand what exposure led to the outcome; used when the outcome is rare (e.g., developmental causes of rare cancers)
3. **Cohort (Clustered) Studies** -- Collect data from a group with a shared characteristic; usually interested in establishing causal associations

## Features of Longitudinal Data

### Correlation Structure

Repeated measures on the same individual are usually **positively correlated**. This violates the fundamental assumption of independence that underpins many standard statistical techniques. Failing to account for this correlation leads to incorrect standard errors and potentially invalid inferences.

### Heteroscedasticity

The variability of the outcome often differs across measurement occasions -- typically, variability at the end of a study is discernibly different from variability at the start. This violates the **homoscedasticity assumption** of standard linear regression.

**Two key difficulties** of longitudinal data:
1. Repeated measures on the same individual are usually positively correlated
2. Variability is often heterogeneous across measurement occasions

## Key Features of Studying Change

(Singer and Willet, pages 9-15)

### Requirements

- **Three or more time points** -- Serial cross-sectional data introduces bias due to history, cohort effects, etc.
- **A meaningful metric for time** -- Choose based on theory and conceptual sense (age, calendar time, time since event, etc.)
- **An outcome that changes systematically over time** -- Must be valid at each time point and measure the same construct consistently

### Outcome Variable Types

- **Continuous** (e.g., viral load, blood lead levels)
- **Binary** (e.g., substance use / no substance use)
- **Count** (e.g., number of seizures in the last 30 days)

### Attrition

Participants or units can have missing data, which is a common challenge in longitudinal studies.

## Motivating Examples

### Example 1: Treatment of Lead-Exposed Children Trial

- Randomized trial of Succimer (oral) vs. placebo for children with high blood lead levels
- 100 children randomized; measured at baseline, week 1, week 4, and week 6
- Succimer group showed dramatic initial drop (26.5 to 13.5 $\mu$g/dL at week 1) followed by rebound
- Placebo group showed gradual, slight decline (26.3 to 23.2 $\mu$g/dL)

### Example 2: Six Cities Study of Air Pollution and Health

- Longitudinal study of lung function growth (FEV$_1$) in children and adolescents
- 300 female participants in Topeka, Kansas; enrolled ages 6-7, measured annually through high school graduation
- Response: log(FEV$_1$/height) vs. age shows increasing trend with individual variation

### Example 3: Anti-Epileptic Drug Progabide Trial

- Randomized, placebo-controlled study of epileptic seizures
- 28 on placebo, 31 on progabide; measured at baseline and four 2-week intervals
- Count outcome (number of seizures)

### Additional Applications

- **Interrupted Time Series / Difference-in-Differences (DID)**: Formally discussed by Card and Krueger (1994); distinguishes level change from trend change after an intervention
- **Epidemiological trends**: Prevalence of hypertension, diabetes, smoking, obesity stratified by income (1994-2005)
- **Midlife well-being nadir**: U-shaped relationship between age and life satisfaction across four datasets

## Applications Across Disciplines

Longitudinal methods are increasingly popular:
- **Economics**: DID, regression discontinuity, event studies, bunching (Currie et al., 2020)
- **Political Science**: Fixed effects + panel data, DID, synthetic control (Xu, Stanford, 2024)
- **Public Health**: Disease prevalence trends, substance use trajectories
- **Biology**: Gene expression over time (RNA-seq time-course data)

## Key Takeaways

1. Longitudinal data = repeated measures on the **same individuals** over time
2. The two main statistical complications are **within-person correlation** and **heteroscedasticity**
3. Proper longitudinal analysis requires at least three time points, a sensible time metric, and a systematically changing outcome
4. Standard regression methods (OLS) are inadequate because they assume independence and constant variance
5. Longitudinal designs enable studying **within-individual change**, not just between-group differences

## Original Slides

![[assets/Lecture1.pdf]]
