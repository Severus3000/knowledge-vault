---
title: "Measures of Association"
source: "master-2026-spring-intermediate-epidemiology"
platform: "lecture"
author: "Farzana Kapadia"
date: 2026-03-09
ingested: 2026-04-05T00:00:00Z
tags: [epidemiology, measures-of-association, risk-difference, risk-ratio, rate-ratio, odds-ratio, confidence-intervals, p-values, risk-communication]
category: "master-courses/epidemiology/measures-of-disease"
compiled: true
---

# Measures of Association

Lecture 3 from Intermediate Epidemiology (GPH-GU 2450, NYU School of Global Public Health). Covers the 2x2 table, risk/rate/odds contrasts, the relationship between OR and RR, bias vs. variance, confidence intervals, p-values, and risk communication.

---

## 1. The 2x2 Table

The foundational structure for comparing disease frequency across exposure groups:

|  | Outcome | No Outcome | Total | Risk |
|---|---|---|---|---|
| **Exposed** | a | b | a+b | a/(a+b) |
| **Unexposed** | c | d | c+d | c/(c+d) |
| **Total** | a+c | b+d | N | |

**Example:**

|  | Outcome | No Outcome | Total | Risk |
|---|---|---|---|---|
| Exposed | 60 | 140 | 200 | **0.30** |
| Unexposed | 15 | 85 | 100 | **0.15** |

- Risk Ratio = $0.30 / 0.15 = 2.0$
- Risk Difference = $0.30 - 0.15 = 0.15$ (or 15 per 100)

**Reminders:**
1. Row/column labels can be switched
2. Risks require: (a) fixed observation period and (b) complete follow-up without losses
3. A contrast requires **at least two groups**

---

## 2. Identifying Comparison Groups

- Must have at least two groups to estimate a contrast
- With more than 2 groups: choose a reference, or compute pairwise contrasts
- With continuous exposures: categorize or model directly
- Contrasts require **assignment to group**, which requires **measurement of group membership**
  - Poor exposure measurement affects both "exposed" and "unexposed" groups
  - This links to measurement bias and misclassification

**Example:** RCT examining whether injectable hormonal contraception DMPA (Depo-Provera) increases HIV vulnerability. Key design questions: What is the study population? Treatment arm? Control arm? Each choice of comparison group asks a slightly different scientific question.

---

## 3. Measures of Association I: Risk Contrasts

Let $P(Y|X=1)$ = risk among exposed, $P(Y|X=0)$ = risk among unexposed.

### 3.1 Risk Difference (RD)

$$
RD = P(Y|X=1) - P(Y|X=0)
$$

- The **absolute** difference in risks between exposed and unexposed
- Range: $[-1, 1]$
- **Null value: 0** (no difference)

### 3.2 Risk Ratio (RR)

$$
RR = \frac{P(Y|X=1)}{P(Y|X=0)}
$$

- The **relative** comparison of risks
- Range: $[0, \infty)$ (or undefined if denominator = 0)
- **Null value: 1** (equal risks)

---

## 4. Measures of Association II: Rate Contrasts

Let $IR(Y|X=1)$ = incidence rate among exposed, $IR(Y|X=0)$ = incidence rate among unexposed.

### 4.1 Rate Difference (RaD)

$$
RaD = IR(Y|X=1) - IR(Y|X=0)
$$

- Range: $(-\infty, \infty)$
- **Null value: 0**

### 4.2 Rate Ratio (RaR)

$$
RaR = \frac{IR(Y|X=1)}{IR(Y|X=0)}
$$

- Range: $[0, \infty)$
- **Null value: 1**

---

## 5. Measures of Association III: Odds Contrasts

Let $\text{Odds}(Y|X=1) = P(Y|X=1) / P(\bar{Y}|X=1)$ and similarly for $X=0$.

### 5.1 Odds Difference

> **Does not exist.** An odds difference does not make sense and should not be computed.

### 5.2 Odds Ratio (OR)

$$
OR = \frac{\text{Odds}(Y|X=1)}{\text{Odds}(Y|X=0)} = \frac{a \cdot d}{b \cdot c}
$$

- Range: $[0, \infty)$
- **Null value: 1**
- Equivalent to the cross-product ratio in the 2x2 table

---

## 6. Summary of All Contrasts

| Measure | Formula | Range | Null Value | Scale |
|---|---|---|---|---|
| Risk Difference | $P_1 - P_0$ | $[-1, 1]$ | 0 | Absolute |
| Risk Ratio | $P_1 / P_0$ | $[0, \infty)$ | 1 | Relative |
| Rate Difference | $IR_1 - IR_0$ | $(-\infty, \infty)$ | 0 | Absolute |
| Rate Ratio | $IR_1 / IR_0$ | $[0, \infty)$ | 1 | Relative |
| Odds Ratio | $O_1 / O_0$ | $[0, \infty)$ | 1 | Relative |

---

## 7. Differences vs. Ratios in Public Health

Ratio measures are **independent of absolute risk** levels. This creates an important interpretive gap.

**Example:**
- Compare 20% vs. 10%: $RR = 2.0$, $RD = 10\%$
- Compare 4% vs. 2%: $RR = 2.0$, $RD = 2\%$
- Same ratio, very different absolute differences

**Which is "right"?** Depends on the purpose:
- For **public health interventions** -- the RD (absolute scale) tells you the number of lives saved / cases prevented and informs NNT (number needed to treat)
- For **etiological research** -- the RR (relative scale) characterizes the strength of the exposure-outcome relationship

> A risk ratio alone cannot tell you how many cases to expect -- you also need the baseline risk.

---

## 8. Risk Ratio vs. Odds Ratio

### 8.1 When OR Approximates RR

- OR $\approx$ RR when the **outcome is rare** (risk $< 10\%$) or when $RR = 1$ (null)
- When risks are large and non-null, OR **overestimates** RR

**Example:**
- 20% vs. 10%: $RR = 2.00$, $OR = 2.25$
- 4% vs. 2%: $RR = 2.00$, $OR = 2.04$

### 8.2 Why Odds Overstate Risk

Recall: $\text{odds} = P / (1 - P)$.

- When $P > 0$, the denominator $(1 - P) < 1$, so odds $>$ risk
- The bigger the risk, the smaller $(1 - P)$, the greater the overestimation
- Therefore the OR will always be farther from 1.0 than the RR (when association exists)

### 8.3 RR Cannot Be Derived from OR Alone

- Given $RR = 2.0$, the OR could be many values depending on baseline risk
- No general correction factor exists to convert between RR and OR without knowing the baseline risks

### 8.4 Advantage of the Odds Ratio

- Risks are bounded to $[0, 1]$, so the RR is constrained by the baseline risk
  - If baseline risk = 50%, max possible $RR = 2.0$
- Odds range $[0, \infty)$ and are not similarly constrained
- OR is the natural parameter in logistic regression and case-control studies

---

## 9. Contrasts Are Averages

**Critical point:** All contrast measures are **population averages**. They cannot be assumed to apply to any individual. In fact, sometimes they apply to **no** individuals.

**Example:** A drug lowers LDL cholesterol by 10 points in people with XX chromosomes but raises it by 10 points in people with other sex chromosomes. In a 50/50 population, the average association is **0 points** -- yet no individual experiences zero change.

---

## 10. Bias and Variance

### 10.1 Bias (Systematic Error)

- Due to confounding, selection bias, information bias
- **Does not decrease** with increasing sample size
- Affects validity (accuracy of the estimate)

### 10.2 Variance (Random Error)

- Due to sampling error
- **Does decrease** as sample size increases
- Affects precision (consistency of the estimate)

> The bias-variance distinction maps onto a target analogy: **validity** = closeness to the bullseye; **precision** = tightness of the cluster.

---

## 11. Understanding Variance: P-Values

**Definition:** The probability, given that the null hypothesis is true, of observing results as extreme or more extreme than the observed data by chance alone.

- Null hypothesis: typically $RD = 0$, $RR = 1$, or $OR = 1$
- Convention: reject $H_0$ if $p \leq 0.05$ (but this threshold is arbitrary)

**Limitations of p-values:**
- Conflate effect size with sample size
- Binary "significant/not significant" thinking loses nuance
- Do not tell you the probability that $H_0$ is true

---

## 12. Understanding Variance: Confidence Intervals

### 12.1 Correct Interpretation

A 95% CI is a range of **plausible values** for the population parameter. It depends on:
1. The **point estimate** (RD, RR, or OR)
2. The **variability** of the estimate
3. The **sample size**

**Formal definition:** If the study were repeated infinitely, 95% of the CIs would contain the true parameter.

### 12.2 Common Misinterpretation

It is **NOT** "we are 95% sure the true parameter is in this range." That would require a **Bayesian credible interval**.

### 12.3 Standard Error

A calculation based on the data that quantifies the precision of the estimate. The CI is built from the point estimate $\pm$ a multiple of the SE.

---

## 13. Risk Communication

### 13.1 Principles

- Be **super, super obvious** -- way more obvious than you think is necessary
- Always state the **time period** associated with the risk (without it, risks are uninterpretable)
- Always include a **comparison group** -- a contrast requires two groups
- Know your **audience**

### 13.2 Language Precision

Ambiguous: "Risk of death among the exposed was 10% higher than among the unexposed."

- Could mean $RD = 10\%$ (10 percentage points higher) **or** $RR = 1.10$ (1.1 times the risk)

**Better:**
- For absolute differences: "10 **percentage points** higher" or "on the absolute scale"
- For relative differences: "1.1 **times** the risk" or "10% higher on the relative scale"

### 13.3 Examples of Clear Communication

- "The 3-year risk of death among the exposed was **1.5 times** the risk among the unexposed."
- "The 5-year risk of death among the exposed was **10 percentage points higher** than the risk among the unexposed."
- "The one-month risk of recurrent heart attack among the exposed was **five times** the one-month risk among the unexposed."
- "The incidence **rate** of serious injury among the exposed was **1.5 times** that among the unexposed."

### 13.4 Common Pitfalls

- Failing to state the time period
- Failing to include a comparison group (a single risk is not a contrast)
- Ambiguous language around "higher" (absolute vs. relative)

### 13.5 Headline Example

Headline: "Eating Yogurt Could Cut Diabetes Risk by 28 Percent"

The actual study (O'Connor et al., EPIC-Norfolk): HR 0.72 [95% CI 0.55, 0.95] for low-fat fermented dairy (yoghurt) intake on incident type 2 diabetes. The "28%" is $1 - 0.72 = 0.28$, a relative reduction. Without knowing the baseline risk, you cannot determine how many cases this prevents.

---

## Key Takeaways

1. **Risk Difference** (absolute) tells you the public health impact; **Risk Ratio** (relative) tells you the strength of association -- both are needed
2. **OR $\approx$ RR** only when the outcome is rare ($< 10\%$); otherwise OR overestimates RR
3. You **cannot convert** OR to RR (or vice versa) without knowing baseline risks
4. All contrast measures are **population averages** and may not apply to any individual
5. **Bias** (systematic) does not shrink with sample size; **variance** (random) does
6. A 95% CI is a range of plausible values, not a 95% probability statement about the parameter
7. **Always specify:** time period, comparison group, and whether you mean absolute or relative scale
8. The OR has mathematical advantages (logistic regression, case-control studies) despite being less intuitive than RR

---

## Original Slides

![[assets/Lecture 3_Measures of Association.pdf]]
