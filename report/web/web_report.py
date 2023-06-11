from datetime import timedelta
from flask import render_template, abort, request, Response, make_response
from flask_api import FlaskAPI
from flask_swagger_ui import get_swaggerui_blueprint
import json
from pathlib import Path
from typing import List, Dict, Tuple
from report.src.core.main import build_report
import xmltodict


app = FlaskAPI(__name__)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Report API"
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


def content(order='asc') -> Tuple[List[str], Dict[str, dict], Dict[str, dict]]:
    """
    Creates data for page content: bread crumbs and report's output.
    """
    bread_crumbs = ["report", "list"]
    default_folder = Path(__file__).resolve().parent.parent.parent / 'report' / 'data'
    if order is not None and order == 'desc':
        list_of_racers, report = build_report(default_folder, order)
    else:
        list_of_racers, report = build_report(default_folder, 'asc')
    return bread_crumbs, list_of_racers, report


@app.route("/")
@app.route("/report/")
def report() -> Response:
    """
    '/' and '/report/' handler. Takes order argument.
    """
    order = request.args.get('order')
    bread_crumbs, list_of_racers, sorted_report = content(order)
    return render_template('report.html', title='Report', bread_crumbs=bread_crumbs, sorted_report=sorted_report,
                           order=order)


@app.route("/list")
def list_racers() -> Response:
    """
    '/list' handler.
    """
    bread_crumbs, list_of_racers, report = content('asc')
    return render_template('list.html', title='List of Racers', bread_crumbs=bread_crumbs,
                           list_of_racers=list_of_racers)


@app.route("/list/<driver_code>")
def racer(driver_code: str) -> Response:
    """
    '/list/*' uri handler. Only existing in list_of_racers code can be an ending of uri
    """
    bread_crumbs, list_of_racers, report = content()
    if driver_code in list_of_racers:
        return render_template('racer.html', title='Racer Info', bread_crumbs=bread_crumbs,
                               list_of_racers=list_of_racers, driver_code=driver_code)
    else:
        abort(404)


@app.errorhandler(404)
def notFound(error) -> Response:
    """
    404 page handler, returns 404 status code
    """
    bread_crumbs = content()[0]
    return render_template('page404.html', title='Page Not Found', bread_crumbs=bread_crumbs), 404


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj) -> str:
        if isinstance(obj, timedelta):
            return str(obj)
        return super().default(obj)


@app.get("/api/v1/drivers/")
def drivers_api() -> Response:
    bread_crumbs, list_of_racers, sorted_report = content()
    format = request.args.get('format')
    json_drivers = make_response(json.dumps(list_of_racers, cls=CustomJSONEncoder))
    if format == 'xml':
        xml_data = xmltodict.unparse({'drivers': list_of_racers}, pretty=True)
        return xml_data
    else:
        json_drivers.headers['Content-Type'] = 'application/json'
        return json_drivers


@app.get("/api/v1/drivers/<driver_code>/")
def driver_api(driver_code: str) -> Response:
    bread_crumbs, list_of_racers, sorted_report = content()
    format = request.args.get('format')
    if driver_code in list_of_racers.keys():
        driver = list_of_racers[driver_code]
        if format == 'xml':
            xml_data = xmltodict.unparse({'driver': driver}, pretty=True)
            return xml_data
        else:
            response = make_response(json.dumps(driver, cls=CustomJSONEncoder))
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        abort(404)


@app.get("/api/v1/report/")
def report_api() -> Response:
    bread_crumbs, list_of_racers, sorted_report = content()
    format = request.args.get('format')
    report_lines: dict = {}
    for i, (abbrs, info) in enumerate(sorted_report.items(), start=1):
        name = info['name']
        team = info['team']
        time_diff = info['time_diff']
        line = {'place': i, 'code': abbrs, 'name': name, 'team': team, 'time': time_diff}
        report_lines[i] = line
    if format == 'xml':
        xml_report = {str(key): value for key, value in report_lines.items()}
        xml_data = xmltodict.unparse({'drivers': xml_report}, pretty=True)
        return xml_data
    else:
        json_report = make_response(json.dumps(report_lines, cls=CustomJSONEncoder))
        json_report.headers['Content-Type'] = 'application/json'
        return json_report


if __name__ == "__main__":
    app.run(debug=True)
