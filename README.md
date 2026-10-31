# Lead Scoring: Which Leads Should Sales Call First?

X Education, an online course company, gets thousands of leads, but only **38.5% convert**. Sales was calling everyone. I built a logistic regression model that gives every lead a **0–100 score**, so the team can focus on the leads most likely to buy.

## Result
At the chosen cutoff, **73% of the leads the model flags actually convert**, almost double the 38.5% baseline. It still catches **~79% of all real conversions**.

| | Accuracy | Sensitivity | Specificity | Precision |
|---|---|---|---|---|
| Train (6,468 leads) | 80.8% | 79.9% | 81.3% | 72.4% |
| Test (2,772 leads) | 80.3% | 79.4% | 80.9% | 73.1% |

Train and test scores are nearly identical, so the model generalizes well rather than memorizing.

## What drives conversion
- **Working professionals** convert at **91.6%**, vs 33.9% for unemployed leads.
- **Time spent on the website** has a strong positive relationship with conversion.
- **Landing Page Submission** is the top lead origin (52.9% of leads, 36.2% conversion).
- Recent activity like **SMS Sent** and **Email Opened**, plus **referral** leads, also feature in the final model.

## How I built it
**Data:** 9,240 leads × 37 columns (web behavior, lead source, occupation, last activity).

**Cleaning**
- Treated "Select" (unanswered form fields) as missing.
- Dropped 7 columns with more than 40% missing values.
- Grouped rare categories into "Others".
- Capped outliers using the IQR method.
- Dropped near-constant columns, going from 37 to 11 features before encoding.

**Modeling**
- One-hot encoded the categoricals and split 70/30.
- Standardized the numeric features.
- Dropped 2 features with correlation above 0.85 to the lead source.
- Used RFE to pick 15 features, then ran a backward-elimination loop: refit, drop the least significant feature (p ≥ 0.05), otherwise drop any feature with VIF above 5, and repeat. That left **11 features, all with VIF under 2.2**.

**Choosing the cutoff:** I plotted accuracy, sensitivity and specificity across cutoffs from 0 to 0.9 and picked **0.35**, where all three balance. That favors catching real buyers over avoiding false alarms, which is the right trade-off for a sales team.

**Stack:** Python · pandas · scikit-learn (RFE, LogisticRegression) · statsmodels (GLM, VIF) · Matplotlib / Seaborn

## Repository structure
| Path | What's in it |
|---|---|
| `notebooks/lead_scoring_case_study.ipynb` | Full analysis and model, with comments |
| `data/leads.csv` / `data/leads_data_dictionary.xlsx` | Raw data and column definitions |
| `reports/presentation.pdf` | Slide summary for business stakeholders |
| `reports/executive_summary.pdf` | One-page summary |
| `reports/subjective_questions.docx` | Written answers on model use |

## How to run
```bash
pip install -r requirements.txt
cd notebooks
jupyter notebook lead_scoring_case_study.ipynb
```
