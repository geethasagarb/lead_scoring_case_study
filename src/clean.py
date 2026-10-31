"""Data cleaning steps for the X Education leads dataset.

Each function mirrors one step of notebooks/lead_scoring_case_study.ipynb, so the
cleaning can be tested and reused outside the notebook.
"""

import numpy as np
import pandas as pd


def replace_select(df: pd.DataFrame) -> pd.DataFrame:
    """Treat the form placeholder 'Select' as a missing value."""
    return df.replace('Select', np.nan)
