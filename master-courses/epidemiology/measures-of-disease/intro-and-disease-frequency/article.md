---
title: "Introduction to Epidemiology & Measures of Disease Frequency"
source: "master-2026-spring-intermediate-epidemiology"
platform: "lecture"
author: "Farzana Kapadia"
date: 2026-01-20
ingested: 2026-04-05T00:00:00Z
tags: [epidemiology, disease-frequency, prevalence, incidence, survival-analysis, kaplan-meier, person-time, age-period-cohort]
category: "master-courses/epidemiology/measures-of-disease"
compiled: true
---

# Introduction to Epidemiology & Measures of Disease Frequency

Lectures 1--2 from Intermediate Epidemiology (GPH-GU 2450, NYU School of Global Public Health). Covers course overview, cohort types, prevalence measures, incidence measures, survival analysis, and age-period-cohort effects.

---

## 1. Course Overview

**Objectives for the semester:**

- Build on foundational epidemiology concepts
- Conduct descriptive analyses to investigate an epidemiologic question
- Communicate and interpret epi results in oral and written formats

**Structure:** Weekly lectures (Tuesdays, in-person) + required weekly recitation/lab sessions (Stata exercises). Evaluation via an individual research project (NHANES 2021--2023 data on depression) and a final exam.

---

## 2. Open and Closed Cohorts

A **cohort** is a defined group of individuals followed over time (prospectively or retrospectively).

| Feature | Closed Cohort | Open Cohort |
|---|---|---|
| Membership | Fixed at formation | Can add new members over time |
| Size over time | Same or decreasing (LTFU) | Can increase |
| Synonyms | Fixed cohort | Dynamic cohort |

> This course generally assumes **closed cohorts** unless otherwise noted.

---

## 3. Measures of Prevalence

Prevalence is a **cross-sectional** measure of disease occurrence: the proportion of a population that currently has the outcome over some period of time.

> Must ALWAYS specify the **period of time** over which prevalence is measured.

### 3.1 Prevalence Count

The raw number of existing cases.

- **Pros:** Easy to understand; communicates public health importance with large numbers
- **Cons:** Cannot compare across populations unless denominators are equivalent; can be misleading without context (e.g., "thousands get disease X per year" -- but what is the denominator?)

### 3.2 Prevalence Proportion

$$
\text{Prevalence proportion} = \frac{\text{Number with condition}}{\text{Total population}}
$$

- **Pros:** Communicates public health importance; widely used in epidemiology; similar to incidence if illness duration is very short
- **Cons:** Combines incidence and duration -- a high prevalence could mean high incidence or long duration (or both)

**Example:** "1% of people in the US have type 1 diabetes" is a prevalence proportion statement (cross-sectional). Saying "1% of people *developed* type 1 diabetes" would be an incidence statement -- different meaning.

### 3.3 Prevalence Odds

$$
\text{Prevalence odds} = \frac{P}{1 - P}
$$

where $P$ is the prevalence proportion.

| Proportion | Odds |
|---|---|
| 0.02 | 0.0204 |
| 0.05 | 0.053 |
| 0.10 | 0.11 |
| 0.25 | 0.33 |
| 0.50 | 1.00 |

- When prevalence is low ($< 10\%$), odds $\approx$ proportion
- When prevalence is high ($> 10\%$), odds **overestimates** the proportion
- **Pros:** Ratios of odds (odds ratios) have useful mathematical properties
- **Cons:** Not intuitive; can overstate effects when outcome is common

> **Bottom line:** If you see an odds or odds ratio, try to figure out the underlying proportion/percentage.

**Example:** Study of diabetes among $n = 2000$ adults in West Virginia, 2024. Found 368 cases.
- Prevalence proportion: $368 / 2000 = 18.4\%$
- Prevalence odds: $368 / 1632 = 0.22$

The proportion (18.4%) is more interpretable than the odds (0.22).

---

## 4. Measures of Incidence

Incidence measures **new** events occurring over time. Four standard measures:

### 4.1 Incidence Count

Simply the number of new events in a given period.

### 4.2 Incidence Proportion (Risk)

$$
\text{Risk} = \frac{\text{Number of new events}}{\text{Population at risk at start}} = \frac{A}{N}
$$

- AKA **cumulative incidence** or **incidence proportion**
- Is a probability: range $[0, 1]$, dimensionless
- **Requires a fixed time period** -- must always state it (e.g., "5-year risk of lung cancer")
- Risk is just a summary of the survival curve at a particular time: $\text{Risk}_t = 1 - S(t)$

**Pros:**
- Intuitive -- it is a probability

**Cons:**
- Interpretation is conditional for recurrent (non-terminal) outcomes
- Does not account for variable follow-up lengths between subjects (incidence rate addresses this)
- Loses information compared to a full survival curve

### 4.3 Incidence Odds

$$
\text{Incidence odds} = \frac{R}{1 - R}
$$

where $R$ is the risk. Same relationship as prevalence odds to prevalence proportion.

- Range: $[0, \infty)$
- Rule of thumb: if risk $\leq 10\%$, then odds $\approx$ risk
- Otherwise, odds will be more extreme and likely misinterpreted as risk

### 4.4 Incidence Rate (Incidence Density)

$$
\text{Incidence rate} = \frac{A}{\text{Person-time}} = \frac{\text{Number of events}}{\sum_i t_i}
$$

- Dimension: $\text{time}^{-1}$ (inverse time)
- Range: $[0, \infty)$ -- can exceed 1
- Inverse of incidence rate = average time to event (under a steady-state assumption)

**Pros:**
- Uses virtually all available information
- Allows comparison across populations/studies with different follow-up periods
- Handles recurrent outcomes naturally

**Cons:**
- Less intuitive than risk
- Strong assumption that each unit of person-time is interchangeable

### Incidence Proportion vs. Incidence Rate

| Feature | Risk (IP) | Rate (IR) |
|---|---|---|
| Can exceed 1? | No | Yes |
| Units | Dimensionless (%) | Inverse person-time |
| Requires fixed time period? | Yes | No |
| Handles recurrent events? | Poorly | Well |

---

## 5. Person-Time

$$
\text{Person-time} = \sum_i t_i
$$

where $t_i$ is the time each individual $i$ was at risk.

**Important considerations:**
- Person-time observed after a hysterectomy should not count as "at risk" for uterine cancer
- For infectious diseases with partial immunity, person-time at risk may vary
- Denominator need not be time -- e.g., vehicle-miles driven (motor vehicle studies), pack-years smoked (cigarette studies)

**Caution:** Person-time estimates can be misleading -- 1000 people followed 5 years = 5000 person-years, but so does 5000 people followed 1 year. These may not be equivalent.

**Example with recurring events:**
Six individuals (A--F) followed over 5 years for disease D. Some experience D multiple times, some are censored. After first diagnosis, 1-year immunity, then at-risk again.
- Total person-time at risk: 20 person-years
- Total events: 6
- Incidence rate: $6/20 = 30$ per 100 person-years

---

## 6. Survival Analysis

### 6.1 Survival Probability $S(t)$

The probability that an individual survives from origin time (e.g., diagnosis) to a specified future time $t$.

$$
S(0) = 1, \quad S(\text{lifetime}) = 0
$$

$S(t)$ is **non-increasing** (decreases or stays constant, never increases).

$$
\text{Risk}_t = 1 - S(t)
$$

### 6.2 Survival Curves

- Theoretically smooth, but in practice appear as **step functions** (updated only when events occur)
- Begin at 100% and move downward over time
- Powerful tool for understanding time-dependent effects
- Risk at any time point is just a "slice" of the survival curve

### 6.3 Kaplan-Meier Method

A non-parametric method for estimating survival probabilities. Survival probability changes only at event times.

**Three key assumptions:**
1. Censored patients have the same survival probability as those who continue to be followed
2. Survival probabilities are the same for early- and late-recruited subjects
3. Events happen at the specified time

Can determine median survival time, compare survival across groups (e.g., via log-rank test).

---

## 7. Moving Between Risk and Rate

When risk is small ($< 10\%$), the simple approximation holds:

$$
\text{Risk} \approx \text{Incidence rate} \times \text{time}
$$

For larger risks (e.g., lifetime risk estimation), use the exponential formula:

$$
R_t = 1 - e^{-\sum_i IR_i \cdot \Delta t_i}
$$

where $i$ indexes intervals, $IR_i$ is the incidence rate in interval $i$, and $\Delta t_i$ is the interval length.

**Assumptions:** Closed population, no competing risks, risk at any time is small.

**Example:** 5-year lung cancer risk when rate = 8/10,000 person-years:
- Simple: $0.0008 \times 5 = 0.004 = 0.40\%$
- Exponential: $1 - e^{-0.004} = 0.00399 \approx 0.40\%$ (similar because risk is low)

---

## 8. Median Event Time

- At what time have half the people experienced the outcome?
- Read from the survival curve: draw horizontal line at 50%, find where it intersects the curve
- Can estimate **any** percentile, not just the median
- Especially useful for inevitable outcomes (e.g., death: lifetime risk = 1, so risk is uninformative, but median time to death is meaningful)
- If fewer than half experience the event, report the 25th percentile time instead
- **Underutilized** measure with good public communication potential

---

## 9. Factors to Consider in Measuring Incidence

- **Competing events:** Events that preclude the event of interest (e.g., death from another cause prevents cancer diagnosis). Theoretical issue for all outcomes except all-cause mortality.
- **Left truncation:** Late entries -- people enrolled at a later point in the study
- **Right censoring:** Loss to follow-up (LTFU)
- Consider whether censoring is independent of the outcome

---

## 10. Defining and Measuring Exposures and Outcomes

- Need clear, precise, unambiguous outcome definitions
- Timeframe matters for survey questions:
  - Cumulative lifetime ("ever" questions) vs. period prevalence (last 30 days, last year) vs. point prevalence (today, this week)
- For biological tests: consider whether a gold standard exists and what the sensitivity/specificity of the available test is

**Choosing between incidence and prevalence:**
- Incidence (risk or rate) requires follow-up -- use for causal/predictive studies
- Prevalence gives information on burden -- more relevant for public health programming and policy

---

## 11. Age, Period, and Cohort Effects

### 11.1 Definitions

- **Age effects:** Variations in outcomes associated with biological, social, or developmental processes of aging, regardless of time period or birth cohort
- **Period effects:** External factors (war, famine, economic crisis, pandemic) that equally affect all age groups at a particular calendar time
- **Cohort effects:** Variations resulting from the unique experience/exposure of a group (birth cohort) as they move through time

### 11.2 APC Analysis

APC analysis aims to disentangle the independent effects of age, period, and cohort on health outcomes.

**Example (Keyes et al., 2010):** Obesity prevalence in the US, 1971--2006 ($N = 91{,}755$). Plotting by age and period shows increasing obesity across all periods. Plotting by age and birth cohort reveals that later-born cohorts have higher obesity at every age -- a cohort effect. APC analysis estimated separate curvature effects for each dimension.

---

## Key Takeaways

1. **Always specify the time period** when reporting prevalence or risk
2. **Prevalence** = cross-sectional snapshot (existing cases); **Incidence** = new events over follow-up
3. **Odds $\approx$ risk** only when the outcome is rare ($< 10\%$); otherwise odds overestimate
4. **Incidence rate** handles variable follow-up and recurrent events better than incidence proportion
5. **Person-time** is not always equivalent across different study designs despite being numerically equal
6. **Risk** is a slice of the survival curve: $R_t = 1 - S(t)$
7. **Kaplan-Meier** estimation assumes independent censoring, uniform recruitment, and exact event timing
8. The simple approximation $\text{Risk} \approx IR \times t$ works only when risk $< 10\%$
9. **Median event time** is an underutilized but highly communicable measure
10. **Age, period, and cohort effects** can confound each other and require careful analytic separation

---

## Original Slides

![[assets/Lecture 1 and 2_Intro and Measures.pdf]]
