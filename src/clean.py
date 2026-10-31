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
