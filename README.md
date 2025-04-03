```mermaid
flowchart TD
    subgraph "Data Sources"
        DS1["Leads.csv"]:::data
        DS2["Leads Data Dictionary.xlsx"]:::data
    end

    DS1 -->|"feeds"| P1["Data Cleaning/Preprocessing"]:::process
    DS2 -->|"feeds"| P1

    P1 -->|"passes clean data to"| P2["Exploratory Data Analysis"]:::process

    P2 -->|"sends insights to"| P3["Model Building & Evaluation"]:::process

    subgraph "Output & Reporting"
        R1["Lead Scoring Case Study.ipynb"]:::report
        R2["Assignment Subjective Questions.docx"]:::report
        R3["Executive Summary of Lead Scoring Case Study.pdf"]:::report
        R4["Presentation.pdf"]:::report
        R5["README.md"]:::report
    end

    P3 -->|"generates results for"| R1

    PL["Python Libraries: Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, Statsmodels"]:::lib
    PL ---|"supports"| P2
    PL ---|"supports"| P3

    click DS1 "https://github.com/geethasagarb/lead_scoring_case_study/blob/master/Leads.csv"
    click DS2 "https://github.com/geethasagarb/lead_scoring_case_study/blob/master/Leads%20Data%20Dictionary.xlsx"
    click P1 "https://github.com/geethasagarb/lead_scoring_case_study/blob/master/Lead%20Scoring%20Case%20Study.ipynb"
    click P2 "https://github.com/geethasagarb/lead_scoring_case_study/blob/master/Lead%20Scoring%20Case%20Study.ipynb"
    click P3 "https://github.com/geethasagarb/lead_scoring_case_study/blob/master/Lead%20Scoring%20Case%20Study.ipynb"
    click R1 "https://github.com/geethasagarb/lead_scoring_case_study/blob/master/Lead%20Scoring%20Case%20Study.ipynb"
    click R2 "https://github.com/geethasagarb/lead_scoring_case_study/blob/master/Assignment%20Subjective%20Questions.docx"
    click R3 "https://github.com/geethasagarb/lead_scoring_case_study/blob/master/Executive%20Summary%20of%20Lead%20Scoring%20Case%20Study.pdf"
    click R4 "https://github.com/geethasagarb/lead_scoring_case_study/blob/master/Presentation.pdf"
    click R5 "https://github.com/geethasagarb/lead_scoring_case_study/blob/master/README.md"

    classDef data fill:#f9c,stroke:#333,stroke-width:2px,color:#000;
    classDef process fill:#bbf,stroke:#333,stroke-width:2px,font-weight:bold;
    classDef report fill:#cfc,stroke:#333,stroke-width:2px,color:#000;
    classDef lib fill:#ffc,stroke:#333,stroke-width:2px,color:#000;
```


# Lead Scoring Case Study

This repository contains a case study focused on lead scoring using machine learning techniques. The goal is to predict the likelihood of leads converting into customers based on historical data.


## Problem Statement
Businesses often receive numerous leads, but not all of them convert into customers. Efficiently categorizing these leads based on their likelihood to convert helps in prioritizing follow-ups and optimizing marketing efforts. This project aims to develop a predictive model that scores leads to identify the most promising ones.


## Dataset
The dataset `Leads.csv` contains various attributes of leads such as:
- **Prospect ID**
- **Lead Number**
- **Lead Origin**
- **Lead Source**
- **Do Not Email**
- **Do Not Call**
- **Converted**
- **Total Visits**
- **Total Time Spent on Website**
- **Page Views Per Visit**
- **Last Activity**
- **Country**
- **Specialization**
- **Current Occupation**
- **Tags**, etc.

## Libraries Used
- **Pandas**: Data manipulation
- **NumPy**: Numerical computations
- **Matplotlib**, **Seaborn**: Data visualization
- **Scikit-learn**: Machine learning
- **Statsmodels**: Statistical modeling

## Exploratory Data Analysis
- Load the dataset and inspect basic statistics.
- Check for duplicate values in key columns (`Prospect ID` and `Lead Number`).
- Display the first few rows and overall shape of the dataset.
- Generate descriptive statistics and data types information.

## Data Cleaning
- Replace 'Select' values with NaN to handle unanswered questions.
- Drop columns with more than 40% missing values to ensure data quality.
- Handle remaining missing values appropriately.

## Model Building
1. **Data Splitting**: Split the data into training and testing sets.
2. **Feature Scaling**: Standardize numerical features.
3. **Model Selection**: Use algorithms like Logistic Regression.
4. **Evaluation**: Assess models using metrics like Confusion Matrix, Precision, Recall, and F1 Score.

## Results
### Training Dataset
- **Accuracy**: 80.57%
- **Sensitivity**: 79.72%
- **Specificity**: 81.08%

### Test Dataset
- **Accuracy**: 80.34%
- **Sensitivity**: 79.27%
- **Specificity**: 81.04%

## Conclusion
The model demonstrates strong performance in predicting lead conversions with accuracy, sensitivity, and specificity above 80% for both training and test datasets. Key factors influencing higher conversion rates include:
- Using the 'Lead Add Form'
- Being a 'Working Professional'
- Spending more time on the website
- Referral leads from existing customers
- Channels like Google and Direct Traffic
- Engagement through 'SMS Sent' or 'Email Opened'

The most common specialization categories are 'Others', followed by Finance Management, HR Management, and Marketing Management.

## How to Use
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/geethasagarb/lead_scoring_case_study.git
   cd lead_scoring_case_study
   ```

2. **Install Required Libraries**:
   Make sure you have the required libraries installed. You can install them using:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Jupyter Notebook**:
   Open the Jupyter Notebook to explore and run the analysis:
   ```bash
   jupyter notebook Lead\ Scoring\ Case\ Study.ipynb
   ```

## References
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Seaborn Documentation](https://seaborn.pydata.org/)
- [Statsmodels Documentation](https://www.statsmodels.org/stable/index.html)

---

