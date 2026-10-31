"""Data cleaning steps for the X Education leads dataset.

Each function mirrors one step of notebooks/lead_scoring_case_study.ipynb, so the
cleaning can be tested and reused outside the notebook.
"""

import numpy as np
import pandas as pd


def replace_select(df: pd.DataFrame) -> pd.DataFrame:
    """Treat the form placeholder 'Select' as a missing value."""
    return df.replace('Select', np.nan)


def drop_high_missing(df: pd.DataFrame, threshold: float = 0.4) -> pd.DataFrame:
    """Drop columns where the share of missing values is at or above `threshold`."""
    return df.loc[:, df.isnull().mean() < threshold]


# Most common value used to fill blanks in each categorical column
CATEGORICAL_FILL = {
    'Specialization': 'Others',
    'What is your current occupation': 'Unemployed',
    'Last Activity': 'Email Opened',
    'Lead Source': 'Google',
}


def impute_categoricals(df: pd.DataFrame, fill: dict = CATEGORICAL_FILL) -> pd.DataFrame:
    """Fill missing categorical values with a fixed value per column."""
    return df.fillna({col: value for col, value in fill.items() if col in df.columns})


def impute_mode(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Fill missing values in numeric columns with each column's mode."""
    return df.fillna({col: df[col].mode()[0] for col in columns})


def drop_single_value_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drop text columns that hold only one distinct value."""
    text_cols = df.select_dtypes(include='object').columns
    single = [col for col in text_cols if df[col].nunique() == 1]
    return df.drop(columns=single)


RARE_LEAD_SOURCES = [
    'bing', 'Click2call', 'Press_Release', 'Social Media', 'Live Chat',
    'youtubechannel', 'testone', 'Pay per Click Ads', 'welearnblog_Home',
    'WeLearn', 'blog', 'NC_EDM',
]

RARE_LAST_ACTIVITIES = [
    'Unreachable', 'Unsubscribed', 'Had a Phone Conversation',
    'Approached upfront', 'View in browser link Clicked', 'Email Marked Spam',
    'Email Received', 'Visited Booth in Tradeshow', 'Resubscribed to emails',
]


def group_rare(series: pd.Series, rare_values: list, label: str = 'Others') -> pd.Series:
    """Replace each value in `rare_values` with a single `label`."""
    return series.replace({value: label for value in rare_values})


def cap_outliers_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    """Cap and floor values outside [Q1 - k*IQR, Q3 + k*IQR]."""
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    return series.clip(lower=q1 - k * iqr, upper=q3 + k * iqr).astype(float)


# Columns dropped for reasons explained in the notebook
LOW_VALUE_COLUMNS = ['City', 'Tags', 'Country', 'What matters most to you in choosing a course']
ID_COLUMNS = ['Prospect ID', 'Lead Number', 'Last Notable Activity']
SKEWED_COLUMNS = [
    'Do Not Call', 'Search', 'Newspaper Article', 'X Education Forums',
    'Newspaper', 'Digital Advertisement', 'Through Recommendations',
]
NUMERIC_COLUMNS = ['TotalVisits', 'Total Time Spent on Website', 'Page Views Per Visit']
RENAMES = {
    'A free copy of Mastering The Interview': 'Free_Copy',
    'What is your current occupation': 'Current_Occupation',
}
BINARY_COLUMNS = ['Do Not Email', 'Free_Copy']


def clean_leads(raw: pd.DataFrame) -> pd.DataFrame:
    """Run every cleaning step from the notebook, in the same order."""
    df = replace_select(raw)
    df = drop_high_missing(df)
    df = df.drop(columns=LOW_VALUE_COLUMNS)
    df = impute_categoricals(df)
    df = impute_mode(df, ['TotalVisits', 'Page Views Per Visit'])
    df = drop_single_value_columns(df)
    df = df.drop(columns=ID_COLUMNS + SKEWED_COLUMNS)

    for col in NUMERIC_COLUMNS:
        df[col] = cap_outliers_iqr(df[col])

    df['Lead Source'] = group_rare(df['Lead Source'], RARE_LEAD_SOURCES).str.capitalize()
    df['Last Activity'] = group_rare(df['Last Activity'], RARE_LAST_ACTIVITIES)

    df = df.rename(columns=RENAMES)
    df[BINARY_COLUMNS] = df[BINARY_COLUMNS].apply(lambda col: col.map({'Yes': 1, 'No': 0}))
    return df
