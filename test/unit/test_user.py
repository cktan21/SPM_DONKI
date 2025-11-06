import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.services.atomic.user.supabaseClient import SupabaseClient


# -------------------------------
# Fixtures
# -------------------------------
@pytest.fixture
def mock_client():
    """Patch create_client and return a mocked Supabase client."""
    with patch("backend.services.atomic.user.supabaseClient.create_client") as mock_create_client:
        client = MagicMock()
        mock_create_client.return_value = client
        yield client


@pytest.fixture
def supabase_client(mock_client):
    """Return SupabaseClient with mocked client."""
    return SupabaseClient()


# -------------------------------
# Authentication Methods Tests
# -------------------------------
def test_sign_in_with_password_success(mock_client, supabase_client):
    """Test successful user sign in with email and password"""
    email = "test@example.com"
    password = "password123"
    expected_response = {
        "user": {"id": "user123", "email": email},
        "session": {"access_token": "token123", "refresh_token": "refresh123"}
    }
    
    mock_client.auth.sign_in_with_password.return_value = expected_response
    
    result = supabase_client.sign_in_with_password(email, password)
    
    mock_client.auth.sign_in_with_password.assert_called_once_with({
        "email": email,
        "password": password
    })
    assert result == expected_response


def test_sign_up_success(mock_client, supabase_client):
    """Test successful user sign up"""
    email = "newuser@example.com"
    password = "password123"
    role = "admin"
    name = "John Doe"
    department = "Engineering"
    
    expected_response = {
        "user": {"id": "user123", "email": email},
        "session": {"access_token": "token123"}
    }
    
    mock_client.auth.sign_up.return_value = expected_response
    
    result = supabase_client.sign_up(email, password, role, name, department)
    
    mock_client.auth.sign_up.assert_called_once_with({
        "email": email,
        "password": password,
        "options": {
            "data": {
                "role": role,
                "name": name,
                "department": department,
            }
        }
    })
    assert result == expected_response


def test_sign_up_with_defaults(mock_client, supabase_client):
    """Test user sign up with default parameters"""
    email = "user@example.com"
    password = "password123"
    
    expected_response = {"user": {"id": "user123"}}
    mock_client.auth.sign_up.return_value = expected_response
    
    result = supabase_client.sign_up(email, password)
    
    mock_client.auth.sign_up.assert_called_once_with({
        "email": email,
        "password": password,
        "options": {
            "data": {
                "role": "user",
                "name": "New User",
                "department": "General",
            }
        }
    })
    assert result == expected_response


def test_set_session_success(mock_client, supabase_client):
    """Test setting session with tokens"""
    access_token = "access_token_123"
    refresh_token = "refresh_token_123"
    expected_response = {"session": {"access_token": access_token}}
    
    mock_client.auth.set_session.return_value = expected_response
    
    result = supabase_client.set_session(access_token, refresh_token)
    
    mock_client.auth.set_session.assert_called_once_with(access_token, refresh_token)
    assert result == expected_response


def test_sign_out_success(mock_client, supabase_client):
    """Test user sign out"""
    scope = "local"
    expected_response = {"message": "Signed out successfully"}
    
    mock_client.auth.sign_out.return_value = expected_response
    
    result = supabase_client.sign_out(scope)
    
    mock_client.auth.sign_out.assert_called_once_with(scope=scope)
    assert result == expected_response


def test_sign_out_default_scope(mock_client, supabase_client):
    """Test user sign out with default scope"""
    expected_response = {"message": "Signed out successfully"}
    mock_client.auth.sign_out.return_value = expected_response
    
    result = supabase_client.sign_out()
    
    mock_client.auth.sign_out.assert_called_once_with(scope='local')
    assert result == expected_response


def test_refresh_session_success(mock_client, supabase_client):
    """Test refreshing session with refresh token"""
    refresh_token = "refresh_token_123"
    expected_response = {
        "session": {"access_token": "new_access_token", "refresh_token": "new_refresh_token"}
    }
    
    mock_client.auth.refresh_session.return_value = expected_response
    
    result = supabase_client.refresh_session(refresh_token)
    
    mock_client.auth.refresh_session.assert_called_once_with(refresh_token)
    assert result == expected_response


# -------------------------------
# User Data Methods Tests
# -------------------------------
def test_get_user_by_auth_id_success(mock_client, supabase_client):
    """Test getting user by auth ID"""
    auth_id = "auth123"
    expected_user = {
        "id": "user123",
        "email": "test@example.com",
        "role": "user",
        "name": "Test User",
        "department": "Engineering"
    }
    
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value = expected_user
    
    result = supabase_client.get_user_by_auth_id(auth_id)
    
    mock_client.table.assert_called_once_with("USER")
    mock_table.select.assert_called_once_with("id, email, role, name", "department")
    mock_table.select.return_value.eq.assert_called_once_with("auth_id", auth_id)
    assert result == expected_user


def test_get_user_by_id_success(mock_client, supabase_client):
    """Test getting user by user ID"""
    user_id = "user123"
    expected_user = {
        "id": user_id,
        "auth_id": "auth123",
        "email": "test@example.com",
        "role": "user",
        "name": "Test User",
        "created_at": "2023-01-01T00:00:00Z",
        "department": "Engineering"
    }
    
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value = expected_user
    
    result = supabase_client.get_user_by_id(user_id)
    
    mock_client.table.assert_called_once_with("USER")
    mock_table.select.assert_called_once_with("*")
    mock_table.select.return_value.eq.assert_called_once_with("id", user_id)
    assert result == expected_user


def test_get_all_users_success(mock_client, supabase_client):
    """Test getting all users"""
    expected_users = [
        {"id": "user1", "email": "user1@example.com", "role": "user"},
        {"id": "user2", "email": "user2@example.com", "role": "admin"}
    ]
    
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.execute.return_value.data = expected_users
    
    result = supabase_client.get_all_users()
    
    mock_client.table.assert_called_once_with("USER")
    mock_table.select.assert_called_once_with("*")
    assert result == expected_users


def test_get_all_users_empty(mock_client, supabase_client):
    """Test getting all users when no users exist"""
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.execute.return_value.data = None
    
    result = supabase_client.get_all_users()
    
    assert result == []


def test_get_all_users_none_data(mock_client, supabase_client):
    """Test getting all users when data is None"""
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.execute.return_value.data = None
    
    result = supabase_client.get_all_users()
    
    assert result == []


# -------------------------------
# Audit Logs Tests
# -------------------------------
def test_get_all_logs_success(mock_client, supabase_client):
    """Test getting all audit logs"""
    expected_logs = [
        {"id": "log1", "table_name": "USER", "action": "INSERT", "record_id": "user123"},
        {"id": "log2", "table_name": "USER", "action": "UPDATE", "record_id": "user456"}
    ]
    
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = expected_logs
    
    result = supabase_client.get_all_logs()
    
    mock_client.table.assert_called_once_with("AUDIT_TRAIL")
    mock_table.select.assert_called_once_with("*")
    mock_table.select.return_value.eq.assert_called_once_with("table_name", "USER")
    assert result == expected_logs


def test_get_all_logs_with_filter(mock_client, supabase_client):
    """Test getting audit logs with filter"""
    filter_by = "user123"
    expected_logs = [
        {"id": "log1", "table_name": "USER", "action": "INSERT", "record_id": "user123"}
    ]
    
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = expected_logs
    
    result = supabase_client.get_all_logs(filter_by)
    
    # Verify the method was called and returned expected result
    mock_client.table.assert_called_once_with("AUDIT_TRAIL")
    mock_table.select.assert_called_once_with("*")
    assert result == expected_logs


def test_get_all_logs_empty(mock_client, supabase_client):
    """Test getting audit logs when no logs exist"""
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = None
    
    result = supabase_client.get_all_logs()
    
    assert result == []


def test_get_all_logs_none_data(mock_client, supabase_client):
    """Test getting audit logs when data attribute is None"""
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = None
    
    result = supabase_client.get_all_logs()
    
    assert result == []


# -------------------------------
# Error Handling Tests
# -------------------------------
def test_sign_in_with_password_failure(mock_client, supabase_client):
    """Test sign in failure handling"""
    email = "test@example.com"
    password = "wrongpassword"
    
    mock_client.auth.sign_in_with_password.side_effect = Exception("Invalid credentials")
    
    with pytest.raises(Exception, match="Invalid credentials"):
        supabase_client.sign_in_with_password(email, password)


def test_sign_up_failure(mock_client, supabase_client):
    """Test sign up failure handling"""
    email = "test@example.com"
    password = "password123"
    
    mock_client.auth.sign_up.side_effect = Exception("Email already exists")
    
    with pytest.raises(Exception, match="Email already exists"):
        supabase_client.sign_up(email, password)


def test_get_user_by_auth_id_failure(mock_client, supabase_client):
    """Test get user by auth ID failure handling"""
    auth_id = "auth123"
    
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.side_effect = Exception("Database error")
    
    with pytest.raises(Exception, match="Database error"):
        supabase_client.get_user_by_auth_id(auth_id)


def test_get_all_users_failure(mock_client, supabase_client):
    """Test get all users failure handling"""
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.execute.side_effect = Exception("Database error")
    
    with pytest.raises(Exception, match="Database error"):
        supabase_client.get_all_users()

# -------------------------------
# Additional column & edge coverage
# -------------------------------

def test_sign_up_custom_fields_forwarded(mock_client, supabase_client):
    """role/name/department should be forwarded when provided."""
    email, pwd = "hr@ex.com", "pw"
    out = {"user": {"id": "u1"}, "session": None}
    mock_client.auth.sign_up.return_value = out

    res = supabase_client.sign_up(email, pwd, role="manager", name="Alice", department="HR")
    mock_client.auth.sign_up.assert_called_once_with({
        "email": email,
        "password": pwd,
        "options": {"data": {"role": "manager", "name": "Alice", "department": "HR"}}
    })
    assert res == out


def test_get_user_by_auth_id_column_list(mock_client, supabase_client):
    """Covers exact columns (including department)."""
    mock_table = mock_client.table.return_value
    expected = {"data": [{"id": "1", "email": "a@b.c", "role": "user", "name": "A", "department": "Ops"}]}
    mock_table.select.return_value.eq.return_value.execute.return_value = expected

    result = supabase_client.get_user_by_auth_id("auth-1")
    mock_client.table.assert_called_once_with("USER")
    mock_table.select.assert_called_once_with("id, email, role, name", "department")
    assert result == expected


def test_get_user_by_id_column_list(mock_client, supabase_client):
    """Covers created_at and department selection."""
    mock_table = mock_client.table.return_value
    expected = {"data": [{"id": "1", "auth_id": "auth", "email": "e", "role": "r",
                          "name": "n", "created_at": "t", "department": "d"}]}
    mock_table.select.return_value.eq.return_value.execute.return_value = expected

    result = supabase_client.get_user_by_id("1")
    mock_table.select.assert_called_once_with(
        "id, auth_id, email, role, name, created_at", "department"
    )
    assert result == expected


def test_get_all_users_normalizes_none(mock_client, supabase_client):
    """get_all_users should normalize None to [] (newer client behavior)."""
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.execute.return_value.data = None
    assert supabase_client.get_all_users() == []


def test_get_all_logs_normalizes_none(mock_client, supabase_client):
    """get_all_logs should normalize None to [] as well."""
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = None
    assert supabase_client.get_all_logs() == []

