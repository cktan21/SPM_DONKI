import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.services.atomic.project.supabaseClient import SupabaseClient


# -------------------------------
# Fixtures
# -------------------------------
@pytest.fixture
def mock_client():
    with patch("backend.services.atomic.project.supabaseClient.create_client") as mock_create_client:
        client = MagicMock()
        mock_create_client.return_value = client
        yield client


@pytest.fixture
def supabase_client(mock_client):
    return SupabaseClient()


# -------------------------------
# Insert Recommendation tests
# -------------------------------
def test_insert_recommendation_success(mock_client, supabase_client):
    new_rec = SimpleNamespace(id="rec123", recommendations="My Recommendation")
    expected = {"uuid": "rec123", "recommendation": "My Recommendation"}

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value = expected

    result = supabase_client.insert_recommendation(new_rec)

    mock_client.table.assert_called_once_with("Recommendations")
    mock_table.insert.assert_called_once()
    assert result == expected


def test_insert_recommendation_failure(mock_client, supabase_client):
    new_rec = SimpleNamespace(id="bad", recommendations="Broken")
    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.side_effect = Exception("Insert failed")

    with pytest.raises(Exception):
        supabase_client.insert_recommendation(new_rec)


# -------------------------------
# Fetch Recommendation tests
# -------------------------------
def test_fetch_recommendation_found(mock_client, supabase_client):
    rec_id = "rec123"
    expected = {"uuid": rec_id, "recommendation": "Recommendation"}

    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = [expected]

    result = supabase_client.fetch_recommendation(rec_id)

    mock_client.table.assert_called_once_with("Recommendations")
    assert result == expected  # returns first element


def test_fetch_recommendation_not_found(mock_client, supabase_client):
    rec_id = "doesnotexist"

    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = []

    result = supabase_client.fetch_recommendation(rec_id)

    assert result is None  # returns None when not found


def test_fetch_recommendation_failure(mock_client, supabase_client):
    rec_id = "rec123"
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.side_effect = Exception("DB error")

    with pytest.raises(Exception):
        supabase_client.fetch_recommendation(rec_id)
