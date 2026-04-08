---
title: "Descriptive Statistics for Longitudinal Data"
source: "master-2026-spring-longitudinal-analysis"
platform: "lecture"
author: "Course Instructor"
date: 2026-01-01
ingested: 2026-04-05T00:00:00Z
tags: [longitudinal-data, descriptive-statistics, wide-format, long-format, data-visualization, empirical-growth-plots]
category: "master-courses/longitudinal-data-analysis/foundations"
compiled: true
---

# Descriptive Statistics for Longitudinal Data

## Overview and Motivation

Before fitting formal models to longitudinal data, it is essential to explore the data descriptively. This lecture covers the two fundamental data formats (wide and long), their respective strengths and weaknesses, and the exploratory tools available for each. The emphasis is on understanding within-person change patterns before imposing parametric assumptions.

## Review: Why Longitudinal Data?

- We want to understand how something changes over time
- Defining feature: measurements of the **same individuals** taken repeatedly through time
- Primary goal: characterize the change in response over time and the factors that influence change
- Need a **time metric** (months, semesters, days, years)
- Interested in the **functional form** of a phenomenon
- Repeated measures capture **within-individual change**

## Key Features of Studying Change

(Singer and Willet, pages 9-15)

Three requirements for studying change:

1. **Three or more time points** -- Serial cross-sectional data introduces bias from history, cohort effects, etc.
2. **A sensible metric for time** -- Driven by theory and conceptual appropriateness
3. **An outcome that changes systematically over time** -- Must be valid and consistent across time points

### Outcome Variable Types

- Continuous (e.g., viral load)
- Binary (e.g., substance use / no substance use)
- Count (e.g., number of seizures in 30 days)

### Attrition

Participants or units can have missing data -- a common challenge that must be handled explicitly.

### Statistical Complications

- **Correlation**: Repeated measures on the same individual are usually positively correlated, violating the independence assumption
- **Heteroscedasticity**: Variability often differs across measurement occasions, violating the constant-variance assumption of standard linear regression

## Data Formats

### Person-Level ("Wide") Format

(Singer and Willet, pages 17-22)

In wide format, each person has **one row** of data with multiple columns for repeated measures.

**Example** (Tolerance data): columns `id`, `tol11`, `tol12`, `tol13`, `tol14`, `tol15`, `male`, `exposure`

**Pros:**
- Easy to examine general trends in data
- You can "eyeball" the functional form
- Great for data management

**Cons:**
- Non-informative summaries (means across columns mix different time points)
- No explicit time variable
- Inefficient if there is unequal spacing between measurements
- Cannot easily handle time-varying predictors

**Visualization**: Profile plots (using Stata's `profileplot` command) show individual trajectories across the repeated measures.

### Person-Period ("Long") Format

In long format, each person has **multiple rows** -- one for each measurement occasion.

**Example**: columns `id`, `age`, `tolerance`, `male`, `exposure`, `time`

**Pros:**
- Explicit time variable enables proper temporal modeling
- Handles unequal spacing naturally
- Accommodates time-varying predictors
- Required format for most longitudinal modeling procedures

**Cons:**
- Larger dataset (more rows)
- Harder to "eyeball" individual trajectories in raw data

### Converting Between Formats

In Stata: `reshape long` and `reshape wide` commands convert between formats. Most statistical modeling requires long format.

## Exploratory Visualization

### Empirical Growth Plots

The most informative exploratory tool for longitudinal data. Plot the outcome against time for each individual, revealing:

- Individual trajectories
- Overall trends
- Variability across individuals
- Potential functional forms (linear, quadratic, etc.)

### Profile Plots (Wide Format)

Connect the repeated measurements for each individual across the measurement columns. Useful for quick visual inspection but lack a true time axis.

### Descriptive Statistics by Time Point

Computing means and standard deviations at each time point (and by group) reveals:

- Average trajectories
- Changes in variability over time (heteroscedasticity)
- Group differences in trends

**Example** (Lead exposure trial):

| Group | Baseline | Week 1 | Week 4 | Week 6 |
|-------|----------|--------|--------|--------|
| Succimer | 26.5 (5.0) | 13.5 (7.7) | 15.5 (7.8) | 20.8 (9.2) |
| Placebo | 26.3 (5.0) | 24.7 (5.5) | 24.1 (5.7) | 23.2 (6.2) |

Note how the Succimer group shows increasing standard deviations over time -- a clear example of heteroscedasticity.

## Applications: Interrupted Time Series / DID

- **Difference-in-Differences (DID)**: Formally discussed by Card and Krueger (1994)
- Distinguishes **level change** from **trend change** after an intervention
- Compares observed trajectory to counterfactual trajectory
- Extremely popular in economics (Currie et al., 2020) and increasingly in political science (Xu, 2024)

## Basic Concepts for Modeling

### Non-parametric Standardization

Using the long-format data, compute summary statistics (means, medians, quantiles) at each time point without assuming a functional form.

### Parametric Standardization

Fit simple parametric models (e.g., linear, quadratic) to individual trajectories as a preliminary step before formal multilevel modeling.

## Key Takeaways

1. **Wide format** (one row per person) is intuitive for data management but inadequate for formal modeling
2. **Long format** (one row per occasion) is required for most longitudinal analyses and naturally accommodates unequal spacing and time-varying predictors
3. **Empirical growth plots** are the most important exploratory tool -- always plot individual trajectories before modeling
4. Descriptive statistics by time point reveal trends, group differences, and heteroscedasticity
5. Understanding data structure is a prerequisite for choosing appropriate models

## Original Slides

![[assets/Lecture2.pdf]]
