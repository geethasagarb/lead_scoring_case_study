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


def test_impute_categoricals_fills_only_known_columns():
    df = pd.DataFrame({
        'Specialization': [np.nan, 'Finance Management'],
        'Lead Source': [np.nan, 'Reference'],
        'Other': [np.nan, 'x'],
    })
    out = impute_categoricals(df)
    assert out['Specialization'].tolist() == ['Others', 'Finance Management']
    assert out['Lead Source'].tolist() == ['Google', 'Reference']
    assert out['Other'].isna().iloc[0]


def test_impute_mode_uses_most_common_value():
    df = pd.DataFrame({'TotalVisits': [0.0, 2.0, 2.0, np.nan]})
    assert impute_mode(df, ['TotalVisits'])['TotalVisits'].tolist() == [0.0, 2.0, 2.0, 2.0]


def test_drop_single_value_columns_only_drops_constant_text():
    df = pd.DataFrame({
        'constant_text': ['No', 'No', 'No'],
        'varied_text': ['a', 'b', 'a'],
        'constant_number': [1, 1, 1],
    })
    assert list(drop_single_value_columns(df).columns) == ['varied_text', 'constant_number']


def test_group_rare_maps_listed_values_and_keeps_others():
    s = pd.Series(['bing', 'Google', 'blog', 'Reference'])
    assert group_rare(s, ['bing', 'blog']).tolist() == ['Others', 'Google', 'Others', 'Reference']


def test_cap_outliers_iqr_caps_and_floors():
    # Q1 = 2, Q3 = 4, IQR = 2 -> bounds [-1, 7]
    s = pd.Series([-10, 2, 3, 4, 100])
    assert cap_outliers_iqr(s).tolist() == [-1.0, 2.0, 3.0, 4.0, 7.0]


def test_cap_outliers_iqr_leaves_values_inside_bounds():
    s = pd.Series([1, 2, 3, 4, 5])
    pd.testing.assert_series_equal(cap_outliers_iqr(s), s.astype(float))
