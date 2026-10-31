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
