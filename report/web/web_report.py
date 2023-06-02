from flask import Flask, render_template, abort, request, Response
from pathlib import Path
from typing import List, Dict, Tuple
from report.src._.main import build_report

app = Flask(__name__)


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
    return render_template('report.html', title='Report', bread_crumbs=bread_crumbs, sorted_report=sorted_report, order=order)


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
def notFound(error):
    """
    404 page handler, returns 404 status code
    """
    bread_crumbs = content()[0]
    return render_template('page404.html', title='Page Not Found', bread_crumbs=bread_crumbs), 404


if __name__ == "__main__":
    app.run(debug=True)
