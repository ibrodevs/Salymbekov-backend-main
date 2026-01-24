import pytest
import requests

def return_base_url():
    return 'http://localhost:8000/api'

def test_success():
    response = requests.get(return_base_url() + '/banners/')
    assert response.status_code == 200
    assert response.json() is not None

def test_second_found():    
    response = requests.get(return_base_url() + '/academic-council/')
    assert response.status_code == 200
    assert response.json() is not None

def test_lang():
    response = requests.get(return_base_url() + '/academic-council/?lang=en')
    assert response.status_code == 200
