import pytest
import requests

def test_succes():
	res = requests.get('http://localhost:8000/api/partners/?lang=kg')
	assert 'coord1' in res.json()[0]
	assert res.json()[0]['name'] == 'name in kg *'
	assert res.status_code == 200

