import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"YouTube Video Downloader" in response.data

def test_download_invalid_url(client):
    response = client.post('/download', data={'video_url': 'invalid_url'})
    assert response.status_code == 302  # Redirect on error