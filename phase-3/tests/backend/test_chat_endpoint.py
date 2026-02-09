"""Integration tests for chat endpoints.

Tests the full flow from HTTP request to database changes.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# These tests require the app to be running
# For now, we define the test structure


class TestChatEndpoint:
    """Integration tests for POST /api/chat."""

    @pytest.fixture
    def client(self):
        """Create test client with mocked auth."""
        from main import app
        return TestClient(app)

    @pytest.fixture
    def auth_headers(self):
        """Mock authorization headers."""
        return {"Authorization": "Bearer test-token"}

    def test_add_task_via_chat(self, client, auth_headers):
        """Test adding a task through natural language chat.

        Flow:
        1. Send "add buy groceries" message
        2. Agent should call add_task tool
        3. Response should confirm task creation
        """
        with patch("middleware.jwt_auth.get_current_user_id") as mock_auth:
            mock_auth.return_value = "test-user-123"

            response = client.post(
                "/api/chat",
                json={"message": "add buy groceries"},
                headers=auth_headers,
            )

            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "conversation_id" in data
            # Once agent is wired up:
            # assert "buy groceries" in data["message"].lower()
            # assert len(data["tool_calls"]) > 0
            # assert data["tool_calls"][0]["tool"] == "add_task"

    def test_add_task_with_description(self, client, auth_headers):
        """Test adding a task with description via chat."""
        with patch("middleware.jwt_auth.get_current_user_id") as mock_auth:
            mock_auth.return_value = "test-user-123"

            response = client.post(
                "/api/chat",
                json={"message": "add call mom - ask about weekend plans"},
                headers=auth_headers,
            )

            assert response.status_code == 200

    def test_chat_requires_auth(self, client):
        """Test that chat endpoint requires authentication."""
        response = client.post(
            "/api/chat",
            json={"message": "add test task"},
        )

        assert response.status_code == 401

    def test_chat_empty_message(self, client, auth_headers):
        """Test validation for empty message."""
        with patch("middleware.jwt_auth.get_current_user_id") as mock_auth:
            mock_auth.return_value = "test-user-123"

            response = client.post(
                "/api/chat",
                json={"message": ""},
                headers=auth_headers,
            )

            assert response.status_code == 422  # Validation error

    def test_chat_message_too_long(self, client, auth_headers):
        """Test validation for message exceeding 2000 chars."""
        with patch("middleware.jwt_auth.get_current_user_id") as mock_auth:
            mock_auth.return_value = "test-user-123"

            long_message = "x" * 2001

            response = client.post(
                "/api/chat",
                json={"message": long_message},
                headers=auth_headers,
            )

            assert response.status_code == 422


class TestChatHistory:
    """Integration tests for GET /api/chat/history."""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    @pytest.fixture
    def auth_headers(self):
        return {"Authorization": "Bearer test-token"}

    def test_get_empty_history(self, client, auth_headers):
        """Test getting history when no conversation exists."""
        with patch("middleware.jwt_auth.get_current_user_id") as mock_auth:
            mock_auth.return_value = "new-user-no-history"

            response = client.get(
                "/api/chat/history",
                headers=auth_headers,
            )

            assert response.status_code == 200
            data = response.json()
            assert data["messages"] == []
            assert data["total_count"] == 0

    def test_history_pagination(self, client, auth_headers):
        """Test history pagination with limit and offset."""
        with patch("middleware.jwt_auth.get_current_user_id") as mock_auth:
            mock_auth.return_value = "test-user-123"

            response = client.get(
                "/api/chat/history?limit=10&offset=0",
                headers=auth_headers,
            )

            assert response.status_code == 200


class TestClearHistory:
    """Integration tests for DELETE /api/chat/clear."""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    @pytest.fixture
    def auth_headers(self):
        return {"Authorization": "Bearer test-token"}

    def test_clear_history(self, client, auth_headers):
        """Test clearing conversation history."""
        with patch("middleware.jwt_auth.get_current_user_id") as mock_auth:
            mock_auth.return_value = "test-user-123"

            response = client.delete(
                "/api/chat/clear",
                headers=auth_headers,
            )

            assert response.status_code == 204
