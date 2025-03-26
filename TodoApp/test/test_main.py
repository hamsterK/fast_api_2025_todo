from fastapi.testclient import TestClient
import main
from fastapi import status

client = TestClient(main.app)


def test_return_health_check():
    response = client.fet("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}
