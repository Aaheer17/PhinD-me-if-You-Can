# PhinD me if You Can 🎓  
_Find your perfect PhD advisor match_

## Motivation

Choosing a PhD advisor is one of the most important decisions in a researcher's career - yet the process is often confusing, overwhelming, and based on incomplete information. Students usually spend hours reading Google Scholar profiles, digging through lab websites, and trying to infer work style, expectations, and compatibility on their own. This creates barriers for first-generation students, international students, and applicants without strong mentoring networks.

**PhinD me if You Can** solves this problem by transforming scattered information into a structured, data-driven advisor–student compatibility analysis.

### Why LLMs Are a Perfect Fit

Large Language Models (LLMs) such as **Claude** bring unique strengths that make this application possible:

- **Deep document understanding**  
  LLMs can read CVs, SOPs, lab websites, and publication histories and extract key insights that would take students hours to process manually.

- **Implicit pattern recognition**  
  LLMs can detect advising styles, productivity patterns, research direction drift, and collaboration culture — insights that are not explicitly stated anywhere.

- **Contextual reasoning**  
  Instead of giving only a score, LLMs provide **explanations**, such as:  
  *“Your research interest in generative modeling aligns strongly with the lab’s recent shift toward diffusion-based methods.”*

- **Personalization**  
  Each evaluation is tailored to the student’s preferences, goals, skills, and workstyle — something static ranking systems can't do.

- **Scalability & accessibility**  
  Automating the assessment gives every student access to the kind of guidance usually only available through experienced mentors.

In short, LLMs make advisor–student matching **fairer, more transparent, and more accessible**, helping students make one of the most important decisions of their academic journey with confidence.

This repository contains a Streamlit prototype app that helps prospective PhD students explore how well they might match with a potential advisor, based on:

- Student’s research interests, skills, preferences, CV, and SOP  
- Professor’s Google Scholar and lab website  
- LLM-based qualitative and quantitative reasoning

The app is designed for the **Claude for Good 2025 – Student Track**.

---

## Features

### Student Profile Form
- Research interests  
- Statement of Purpose (SOP) upload (PDF)  
- CV / Resume upload  
- Professional/technical skills  
- Work–life balance preference  
- Preferred advising style  
➡️ **Required fields are marked with `*` and must be completed to proceed.**

### Professor Profile Form
- Professor name  
- Affiliation (optional)  
- Google Scholar profile URL  
- Lab / personal website URL  
➡️ **Required fields are marked with `*`.**

### Match Evaluation (Results Page)
- Overall match score  
- Research fit, workstyle fit, and advising skill confidence  
- Professor publication rate (last few years)  
- Typical student publication output  
- Top target venues (conferences/journals)  
- Narrative explanations for research fit, workstyle, and overall recommendation  

Behind the scenes, the app uses **LLM APIs (such as Claude)** to perform match evaluation and generate detailed reasoning for the advisor–student compatibility.

![System Diagram](sys-diagram.png)
---

### <p align="center"> Pros &  Cons</p>

| **Pros** | **Cons** |
|------------|-------------|
| Evidence-based assessment using concrete data | Lack of contextual nuance |
| Actionable insights for decision-making | Limited workstyle assessment capabilities |
| Time-saving automation for students | Potential biases (productivity, venue, recency) |
| Transparent scoring | Potentially harmful assumptions about work patterns |

---


## 1. Python Version

**Python 3.8 or higher**.

---

## 2. Install required packages

Inside the project folder, run:

```bash
pip install streamlit pandas
```

---

## 3. Run the Streamlit application

Run this from the same directory where `app.py` is located:

```bash
streamlit run app.py
```

---

## 4. For background analysis, our prompt can be found here

```
https://docs.google.com/document/d/1LGRE-jqcXMxs-assE0VZHYdEmGx9yoFK5Ukv6mAB680/edit?usp=sharing
```
