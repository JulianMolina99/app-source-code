import pytest
from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv
from unittest.mock import patch
from datetime import datetime, timedelta
from app.services.jwt_handler import verify_jwt
import os
import asyncio

# Load environment variables
load_dotenv()

client = TestClient(app)

# Constants
API_KEY = os.getenv("API_KEY")
VALID_PAYLOAD = {
    "message": "This is a test",
    "to": "Juan Perez",
    "from": "Rita Asturia",
    "timeToLifeSec": 45
}
EXPECTED_RESPONSE = {"message": "Hello Juan Perez your message will be send"}

# Test invalid API key returns 401
def test_invalid_api_key():
    response = client.post(
        "/DevOps",
        headers={
            "X-Parse-REST-API-Key": "wrong-api-key",
            "X-JWT-KWY": "valid-jwt"
        },
        json=VALID_PAYLOAD
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid API Key"}

# Test invalid JWT returns 401
def test_invalid_jwt():
    response = client.post(
        "/DevOps",
        headers={
            "X-Parse-REST-API-Key": API_KEY,
            "X-JWT-KWY": "invalid-jwt"
        },
        json=VALID_PAYLOAD
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid JWT"}

# Test valid request with mocked JWT
def test_valid_request_with_mocking():
    with patch('app.api.endpoints.verify_jwt', return_value={
        "exp": datetime.utcnow().timestamp() + 300
    }):
        response = client.post(
            "/DevOps",
            headers={
                "X-Parse-REST-API-Key": API_KEY,
                "X-JWT-KWY": "valid-jwt"
            },
            json=VALID_PAYLOAD
        )
        assert response.status_code == 200
        assert response.json() == EXPECTED_RESPONSE

# Test expired JWT returns 401
def test_expired_jwt():
    with patch('app.api.endpoints.verify_jwt', return_value=None):  # Simulate expired JWT
        response = client.post(
            "/DevOps",
            headers={
                "X-Parse-REST-API-Key": API_KEY,
                "X-JWT-KWY": "expired-jwt"
            },
            json=VALID_PAYLOAD
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid JWT"}

# Test invalid HTTP methods
@pytest.mark.parametrize("method", ["get", "put", "delete", "patch"])
def test_invalid_methods(method):
    response = getattr(client, method)("/DevOps")
    assert response.status_code == 405
    assert response.json() == {"message": "ERROR"}

# Test missing payload fields
@pytest.mark.parametrize("incomplete_payload", [
    {"message": "This is a test", "from": "Rita Asturia", "timeToLifeSec": 45},  # Missing "to"
    {"to": "Juan Perez", "from": "Rita Asturia", "timeToLifeSec": 45},  # Missing "message"
])
def test_incomplete_payload(incomplete_payload):
    with patch('app.api.endpoints.verify_jwt', return_value={
        "exp": datetime.utcnow().timestamp() + 300
    }):
        response = client.post(
            "/DevOps",
            headers={
                "X-Parse-REST-API-Key": API_KEY,
                "X-JWT-KWY": "valid-jwt"
            },
            json=incomplete_payload
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Incomplete payload"}

# Test concurrency with multiple simultaneous requests
@pytest.mark.asyncio
async def test_concurrent_requests():
    tasks = []
    with patch('app.api.endpoints.verify_jwt', return_value={
        "exp": datetime.utcnow().timestamp() + 300
    }):
        for _ in range(10):
            task = asyncio.ensure_future(
                asyncio.to_thread(
                    client.post,
                    "/DevOps",
                    headers={
                        "X-Parse-REST-API-Key": API_KEY,
                        "X-JWT-KWY": "valid-jwt"
                    },
                    json=VALID_PAYLOAD
                )
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        for response in responses:
            assert response.status_code == 200
            assert response.json() == EXPECTED_RESPONSE
