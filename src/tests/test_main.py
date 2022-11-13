import pytest
import json
from starlette.testclient import TestClient
from copy import copy

from app.main import app


test_request_payload  = {"name": "Mont Blanc", 
                         "alt" : 4808,
                         "lat" : 45.832622,
                         "lon" : 6.865175}

parameters = ("id, payload, status_code", [
                                           [1, {}, 422],
                                           [999, test_request_payload, 404],
                                          ]
             )

@pytest.fixture(scope = 'module')
def client(): 
    with TestClient(app) as client: # context manager will invoke startup event 
        yield client

def test_create_peak(client):
    response = client.post("/peaks/", json = test_request_payload)
    assert response.status_code == 201
    test_request_response = copy(test_request_payload)
    test_request_response.update({"id": 1})
    assert response.json() == test_request_response

def test_create_existing_peak(client):
    response = client.post("/peaks/", json = test_request_payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Peak already exist(s)."}

def test_read_peaks(client):
    response = client.get("/peaks/")
    assert response.status_code == 200

def test_search_peaks_by_name(client):
    response = client.get(f"/peaks/search/?name={test_request_payload['name']}")
    assert response.status_code == 200
    assert response.json()[0]['name'] == test_request_payload['name']

def test_search_peaks_in_bound_box(client):
    response = client.get("/peaks/search/?lat_min=0&lat_max=50&lon_min=-50&lon_max=0")
    assert response.status_code == 200
    assert response.json() == []

def test_update_peak(client):
    test_request_payload.update({"name": "Pic du Mont Blanc"})
    response = client.put("/peaks/1", data = json.dumps(test_request_payload))
    assert response.status_code == 200
    test_request_response = copy(test_request_payload)
    test_request_response.update({"id": 1})
    assert response.json() == test_request_response

@pytest.mark.parametrize(*parameters)
def test_update_peak_invalid(client, id, payload, status_code):
    response = client.put(f"/peaks/{id}", data = json.dumps(payload))
    assert response.status_code == status_code

def test_delete_peak(client):
    response = client.delete("/peaks/1")
    assert response.status_code == 200

def test_delete_incorrect_id(client):
    response = client.delete("/peaks/9999")
    assert response.status_code == 404