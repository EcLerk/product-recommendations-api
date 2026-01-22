from unittest.mock import patch

import pytest
from pandas import DataFrame

from app.services.recommendations import RecommendationsService


@pytest.fixture
def sample_df():
    return DataFrame(
        {
            "uid":    [1, 1, 1, 2, 2, 3],
            "pid":    [101, 102, 103, 101, 104, 105],
            "brand":  ["A", "A", "B", "A", "B", "C"],
            "click":  [5, 2, 1, 3, 4, 10],
            "add_to_cart": [1, 0, 0, 1, 0, 0],
            "purchase":    [0, 1, 0, 0, 0, 1],
        }
    )


@pytest.fixture()
def recommendations_service(sample_df: DataFrame):
    service = RecommendationsService()

    with patch.object(RecommendationsService, "_load_data", return_value=sample_df):
        yield service

