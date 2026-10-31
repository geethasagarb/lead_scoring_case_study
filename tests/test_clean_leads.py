from pathlib import Path

import pandas as pd
import pytest

from src.clean import clean_leads

DATA = Path(__file__).resolve().parents[1] / 'data' / 'leads.csv'


@pytest.fixture(scope='module')
def cleaned():
    return clean_leads(pd.read_csv(DATA))


def test_keeps_every_lead_and_the_expected_columns(cleaned):
    assert cleaned.shape == (9240, 11)
    assert list(cleaned.columns) == [
        'Lead Origin', 'Lead Source', 'Do Not Email', 'Converted', 'TotalVisits',
        'Total Time Spent on Website', 'Page Views Per Visit', 'Last Activity',
        'Specialization', 'Current_Occupation', 'Free_Copy',
    ]


def test_has_no_missing_values_or_placeholders(cleaned):
    assert cleaned.isna().sum().sum() == 0
    assert not (cleaned == 'Select').any().any()


def test_binary_columns_are_zero_or_one(cleaned):
    for col in ['Do Not Email', 'Free_Copy', 'Converted']:
        assert set(cleaned[col].unique()) <= {0, 1}


def test_lead_source_is_grouped_and_capitalized(cleaned):
    sources = set(cleaned['Lead Source'])
    assert 'google' not in sources and 'bing' not in sources
    assert {'Google', 'Olark chat', 'Reference', 'Welingak website', 'Others'} <= sources


def test_conversion_rate_is_unchanged(cleaned):
    assert cleaned['Converted'].mean() == pytest.approx(0.3854, abs=1e-4)
