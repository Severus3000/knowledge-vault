---
title: "Cohort Studies: Design, Sampling, and Exchangeability"
source: "master-2026-spring-intermediate-epidemiology"
platform: "lecture"
author: "Farzana Kapadia"
date: 2026-03-09
ingested: 2026-04-05T00:00:00Z
tags: [epidemiology, study-design, cohort-study, prospective, retrospective, confounding, exchangeability, exposure-measurement]
category: "master-courses/epidemiology/study-designs"
compiled: true
---

# Cohort Studies: Design, Sampling, and Exchangeability

## Overview

Cohort studies are **observational analytic** studies in which exposure is **not assigned** by the investigator. They sit on the observational branch of analytic epidemiology, contrasting with experimental designs like RCTs.

Traditionally, a group of **disease-free** people is identified and followed over time to ascertain the occurrence of health-related events. Exposure status is identified at baseline and reassessed at follow-up visits.

### Descriptive vs. Analytic Epidemiology

- **Descriptive epidemiology**: Describes differences in disease distribution across populations; identifies associations over which disease distribution varies
  - Example: *"What is the prevalence of lung cancer among smokers?"*
- **Analytic epidemiology**: Causal research to understand the extent to which changes in exposure cause changes in outcome on average in a population
  - Example: *"Does smoking increase the risk of developing lung cancer?"*
  - Requires appropriate confounder control and causal diagram (DAG) specification

### Attributes of Cohort Studies

- Permit calculation of **incidence** (risk, rates, survival)
- Move from **association** to **effect** estimation
- Individuals typically form the unit of observation and analysis
- Involve collection of primary data, though secondary data sources are sometimes used

## Design Types

### Prospective Cohort

Study begins in the present and follows participants **forward in time**. Exposure and outcome data are collected as events occur.

### Retrospective Cohort

Uses **historical data** -- the cohort was assembled in the past, and both exposure and outcome have already occurred. Researchers look back through existing records.

### Mixed (Ambidirectional) Cohort

Combines retrospective and prospective elements. A cohort assembled in the past is followed forward from the present into the future.

## From Research Question to Study Design

The study design flows from the research question through a structured pipeline:

1. **Study Question**: Evaluate incidence and risk factors for outcomes
2. **Study Design**: Identify sampling strategy; determine best measures for exposures, covariates, and outcomes at multiple time points
3. **Study Implementation**: Implement sampling technique and data collection methods
4. **Data Management**: Create codebooks and systems; enter, clean, and check all data
5. **Data Analysis**: Identify analytic sample; estimate incidence and evaluate risk factors
6. **Reporting Results**: Explain findings; describe strengths, limitations, and recommendations

### Contrasting Descriptive and Analytic Approaches

For the same topic (smoking and lung cancer):

| | Descriptive (Cross-sectional) | Analytic (Cohort) |
|---|---|---|
| **Research question** | "What is prevalence of LC among SMK and ~SMK?" | "Does smoking increase the risk of developing lung cancer?" |
| **Measures** | Self-reported LC, prevalence of smoking | Packs/day, years smoking (time-dependent), incident LC diagnosis |
| **Target population** | Does sampling reflect true population? No counterfactual | Is there a target population? Are exposed and unexposed exchangeable? |
| **Analysis** | Descriptive stats; bivariable stratified analyses | Multivariable models controlling for covariates identified via DAG |

## Deciding on the Study Population

### Population Characteristics

- **Defined**: By age, sex, location, exposure, etc.
- **Fixed**: No participants added after initial enrollment
- **Dynamic**: Cohort varies over follow-up; can be reopened if sample size decreases due to mortality/attrition

### Cohort Population Considerations

**Overall**: Identify a relevant population -- what makes a population relevant for the study?

**Exposure opportunity**: People should be included who could get the exposure, at least in theory. Do not study hysterectomy effects in people who have never had (and cannot have) a uterus -- their probability of exposure is zero. This parallels the **positivity** requirement in RCTs.

**Outcome risk**: 
- Include people **free of the outcome** at baseline
- Only include people **at risk** of the outcome (e.g., do not study uterine cancer among women who have had hysterectomy)
- Avoid introducing **"immortal person-time"**
- Need sufficient outcome frequency for adequate statistical **power**

### Assembling the Cohort

**Population-based**:
- Entire population or representative sample
- Exposures unknown until first observation when exposure data is collected

**Exposure-based**:
- Find subjects with a common exposure (e.g., asbestos workers)
- Identify a comparison group of similar unexposed individuals
- Risk of **selection bias** (e.g., healthy worker effect) if groups are not comparable
- Useful for **rare exposures**

## Participant Enrollment

- **Finding participants**: Where and how are they selected?
- **Ethical issues**: Still exist even though exposure is not assigned. Notable historical case: **Tuskegee Syphilis Study (1932-1972)**
- **Obtaining consent**: Can be complicated; may not be necessary if data are already collected and de-identified

## Measuring Exposures, Covariates, and Outcomes

### Fixed vs. Time-Dependent Variables

- **Fixed variables**: Do not vary over time (e.g., sex [not gender], blood type)
- **Time-dependent variables**:
  - Outcome status (yes/no) or level
  - Exposure status or level
  - Confounders and effect modifiers may also be time-dependent

### Defining Exposure and Covariates

**Exposures**:
- Require a well-defined study question
- Must consider whether exposure is **measured well**
- The observational nature affects consistency in ascertainment and collection

**Covariates**:
- How do we decide which covariates are worth collecting? Use a **causal diagram** (DAG)
- Measurement of covariates is vital, not just exposure and outcome

### Assessment of Exposure and Covariates

- Often assessed at baseline (cohort entry)
- Questionnaires should be "exhaustive but not exhausting"
- Minimize missing data to avoid bias and power loss
- When exposures change over time (e.g., antiretroviral therapy use in an HIV cohort), continued assessment is necessary and **greatly complicates analysis**

## Measuring Outcomes

### Types of Outcomes

- **Single event/discrete outcome**: Follow-up ends at the event; can only happen once (e.g., death)
- **Multiple events/discrete outcome**: Follow-up continues after first event; accrual of person-time restarts (e.g., recurrent infections)
- **Intermediate markers**: Rate of change in a measure predictive of outcome; represents an intermediate step in the disease process

### Defining and Assessing Outcomes

- A well-articulated study question makes outcome definition easier
- **Constant monitoring** is desirable but not always possible (depends on cohort type)
- Planned interval cohorts (e.g., visits every 6 months) will miss actual event dates
  - Leads to **interval censoring** and potential misclassification of outcome timing, number, and severity
  - More frequent follow-up may be needed for less-critical events

## Participant Follow-Up and Retention

### Follow-Up

- Track all participants forward in time
- Consider: How often? Will events or exposures be missed? What are the cost-effort tradeoffs?

### Retention

- **Good retention is critical** to study validity
- Strategies: multiple mailings, phone calls at varying times, home visits, smartphone reminders
- Providing benefits to participants may help retention, but raises **ethical concerns** (remuneration vs. coercion)

## Exchangeability in Cohort Studies

The central challenge: we want exposed and unexposed persons to be as comparable as possible -- we want them to be **exchangeable**.

- Exposure is **self-determined** -- no randomization
- Selection into the study can vary by exposure group, so the unexposed group **may not** be a good proxy for what would have happened to the exposed group had they not been exposed (the **counterfactual**)
- To achieve exchangeability and approximate the ideal, we **must deal with confounding**

### Contrast with RCTs

In RCTs, randomization achieves exchangeability by design (in expectation). In cohort studies, exchangeability must be **approximated** through:
- Careful selection of comparison groups
- Comprehensive measurement of confounders
- Appropriate statistical adjustment (multivariable models guided by DAGs)

## Loss to Follow-Up in Cohort Studies

LTFU prevents outcome assessment and creates **missing data** with potential for **selection bias**.

### Why People Are Lost

- Subject withdraws from study
- Subject cannot be located (emigration, changed contact information, changed phone numbers)

### Consequences

- Missing outcome data
- Potential selection bias if LTFU is related to the outcome
- For certain outcomes, **external data sources** (death registry, cancer registry) can supplement follow-up and reduce these problems

## Key Takeaways

1. Cohort studies are observational analytic designs that follow participants over time to estimate **incidence** and evaluate exposure-outcome relationships
2. Three temporal designs exist: **prospective** (forward from now), **retrospective** (historical data), and **mixed** (past to future)
3. Population selection must consider exposure **opportunity**, outcome **risk** (at-risk and disease-free at baseline), and sufficient outcome frequency for **power**
4. Exposures and covariates can be **fixed** or **time-dependent**; time-varying variables substantially complicate analysis
5. **Exchangeability** is the central challenge -- without randomization, confounding must be addressed through DAG-guided covariate adjustment
6. **LTFU** creates missing data and selection bias; retention strategies and external data linkage help mitigate these problems
7. Outcome assessment timing matters: interval cohorts introduce **interval censoring** and potential misclassification that continuous monitoring avoids

## Original Slides

![[assets/Lecture 7_Cohort Intro.pdf]]
