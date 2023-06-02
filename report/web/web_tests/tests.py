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

    def test_racer_route_nonexistent_driver(self, client) -> None:
        '''
        Test if route returns status code 404
        :param client: FlaskClient
        :return: None
        '''
        response = client.get("/list/wrong_path")
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main()
