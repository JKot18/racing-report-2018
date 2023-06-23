from flask import render_template, abort, request, Response, make_response
from flask_api import FlaskAPI
from flask_swagger_ui import get_swaggerui_blueprint
import json
from report.data.database_sqlite import get_report, get_list, get_racer
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

bread_crumbs = ["report", "list"]


@app.route("/")
@app.route("/report/")
def report() -> Response:
    """
    '/' and '/report/' handler. Takes order argument.
    """
    order = request.args.get('order')
    sorted_report = get_report()
    return render_template('report.html', title='Report', bread_crumbs=bread_crumbs, sorted_report=sorted_report,
                           order=order)


@app.route("/list")
def list_racers() -> Response:
    """
    '/list' handler.
    """
    list_of_racers = get_list()
    return render_template('list.html', title='List of Racers', bread_crumbs=bread_crumbs,
                           list_of_racers=list_of_racers)


@app.route("/list/<driver_code>")
def racer(driver_code: str) -> Response:
    """
    '/list/*' uri handler. Only existing in list_of_racers code can be an ending of uri
    """
    racer = get_racer(driver_code)
    for info in racer:
        if driver_code in info:
            return render_template('racer.html', title='Racer Info', bread_crumbs=bread_crumbs,
                                   racer=racer, driver_code=driver_code)
    abort(404)


@app.errorhandler(404)
def notFound(error) -> Response:
    """
    404 page handler, returns 404 status code
    """
    return render_template('page404.html', title='Page Not Found', bread_crumbs=bread_crumbs), 404


@app.get("/api/v1/drivers/")
def drivers_api() -> Response:
    racers = get_list()
    racers_dict = [{'code': racer[0], 'name': racer[1]} for racer in racers]
    format = request.args.get('format')
    json_drivers = make_response(json.dumps(racers_dict))
    if format == 'xml':
        xml_data = xmltodict.unparse({'drivers': {'driver': racers_dict}}, pretty=True)
        return xml_data
    else:
        json_drivers.headers['Content-Type'] = 'application/json'
        return json_drivers


@app.get("/api/v1/drivers/<driver_code>/")
def driver_api(driver_code: str) -> Response:
    driver = get_racer(driver_code)
    driver_dict = [{'code': racer[0], 'name': racer[1], 'team': racer[2], 'time_start': racer[3], 'time_end': racer[4], 'time_diff': racer[5], 'valid': racer[6]} for racer in driver]
    format = request.args.get('format')
    for info in driver:
        if driver_code in info:
            if format == 'xml':
                xml_data = xmltodict.unparse({'driver': driver_dict}, pretty=True)
                return xml_data
            else:
                response = make_response(json.dumps(driver_dict))
                response.headers['Content-Type'] = 'application/json'
                return response
    abort(404)


@app.get("/api/v1/report/")
def report_api() -> Response:
    results = get_report()
    results_dict = [{'code': racer[0], 'time': str(racer[1]), 'name': racer[2], 'team': racer[3]} for racer in results]
    format = request.args.get('format')
    if format == 'xml':
        xml_data = xmltodict.unparse({'drivers': {'driver': results_dict}}, pretty=True)
        return xml_data
    else:
        json_report = make_response(json.dumps(results_dict))
        json_report.headers['Content-Type'] = 'application/json'
        return json_report


if __name__ == "__main__":
    app.run(debug=True)
