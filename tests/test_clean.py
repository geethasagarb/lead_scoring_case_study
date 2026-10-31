import numpy as np
import pandas as pd
import pytest

from src.clean import (
    cap_outliers_iqr,
    drop_high_missing,
    drop_single_value_columns,
    group_rare,
    impute_categoricals,
    impute_mode,
    replace_select,
)


def test_replace_select_turns_placeholder_into_missing():
    df = pd.DataFrame({'Specialization': ['Select', 'Finance Management'], 'City': ['Mumbai', 'Select']})
    out = replace_select(df)
    assert out['Specialization'].isna().tolist() == [True, False]
    assert out['City'].isna().tolist() == [False, True]


def test_replace_select_does_not_modify_input():
    df = pd.DataFrame({'a': ['Select']})
    replace_select(df)
    assert df.loc[0, 'a'] == 'Select'


def test_drop_high_missing_uses_threshold_inclusively():
    df = pd.DataFrame({
        'keep': [1, 2, 3, 4, 5],
        'drop_exact': [1, 2, 3, np.nan, np.nan],  # 40% missing -> dropped
        'drop_more': [np.nan] * 5,
        'keep_some': [1, 2, 3, 4, np.nan],       # 20% missing -> kept
    })
    assert list(drop_high_missing(df).columns) == ['keep', 'keep_some']
