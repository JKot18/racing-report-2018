import pytest
from report.web.web_report import app
from flask.testing import FlaskClient


@pytest.fixture()
def client() -> FlaskClient:
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestApp:
    def test_report_route(self, client: FlaskClient) -> None:
        '''
        Test if route returns status code 200
        :param client: FlaskClient
        :return: None
        '''
        response = client.get("/report/")
        assert response.status_code == 200

    def test_list_route(self, client) -> None:
        response = client.get("/list")
        assert response.status_code == 200

    def test_racer_route_existing_driver(self, client) -> None:
        response = client.get("/list/VBM")
        assert response.status_code == 200

    def test_api_route_existing_driver(self, client) -> None:
        response = client.get("/api/v1/drivers/VBM/")
        assert response.status_code == 200

    def test_api_route_drivers(self, client) -> None:
        response = client.get("/api/v1/drivers/")
        assert response.status_code == 200

    def test_racer_route_nonexistent_driver(self, client) -> None:
        '''
        Test if route returns status code 404
        :param client: FlaskClient
        :return: None
        '''
        response = client.get("/list/wrong_path")
        assert response.status_code == 404

    def test_api_route_nonexistent_driver(self, client) -> None:
        response = client.get("/api/v1/drivers/wrong_path/")
        assert response.status_code == 404

    def test_api_get_driver(self, client) -> None:
        response = client.get("/api/v1/drivers/VBM/")
        data = response.json
        assert 'Valtteri Bottas' in data['name']

    def test_api_get_driver_header(self, client) -> None:
        response = client.get("/api/v1/drivers/VBM/")
        data = response.headers
        assert 'application/json' in data['Content-Type']

    def test_api_get_driver_xml(self, client) -> None:
        response = client.get("/api/v1/drivers/VBM/?format=xml")
        xml_data = response.data.decode('utf-8')
        assert '<name>Valtteri Bottas</name>' in xml_data

    def test_api_get_drivers(self, client) -> None:
        response = client.get("/api/v1/drivers/")
        data = response.json
        assert 'SVF' in data.keys()

    def test_api_get_drivers_xml(self, client) -> None:
        response = client.get("/api/v1/drivers/?format=xml")
        xml_data = response.data.decode('utf-8')
        assert '<name>Valtteri Bottas</name>' in xml_data

    def test_api_get_report(self, client) -> None:
        response = client.get("/api/v1/report/")
        data = response.json
        assert 'SVF' in data['1']['code']

    def test_api_get_report_xml(self, client) -> None:
        response = client.get("/api/v1/report/?format=xml")
        xml_data = response.data.decode('utf-8')
        assert '<name>Valtteri Bottas</name>' in xml_data


if __name__ == "__main__":
    pytest.main()
