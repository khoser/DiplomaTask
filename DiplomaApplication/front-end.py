from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import date as dt
import requests

URL_BACKEND = "http://localhost:8000"

app = FastAPI()


def prepare_table(rec, date):
    html = f"""
    <html>
    <head><title>Devops school - weather in Moscow</title></head>
    <body>
    <center><b>Devops school - weather in Moscow at {date}</b></center>
    <hr>
        <table align="center" valign="center" border="1" cellspacing="0" cellpadding="5">
            <tr>
                <!--td><b>applicable_date</b></td-->
                <td><b>created</b></td>
                <td><b>weather_state_name</b></td>
                <td><b>wind_direction_compass</b></td>
                <td><b>min_temp</b></td>
                <td><b>max_temp</b></td>
                <td><b>the_temp</b></td>
            </tr>
    """
    for row in rec:
        html += "<tr>\n"
        for col in row:
            html = html + f"<td>{col}</td>\n"
        html += "</tr>\n"
    html += "</table></body></html>"
    return html


@app.get("/")
async def main():
    # resp = requests.get(f"{URL_BACKEND}/date/{dt.today()}")
    # return prepare_table(resp.json(), dt.today())
    return {'use': '/date/...'}


@app.get("/date", response_class=HTMLResponse)
async def main():
    resp = requests.get(f"{URL_BACKEND}/date/{dt.today()}")
    return prepare_table(resp.json(), dt.today())


@app.get("/date/{date}", response_class=HTMLResponse)
async def get_by_date(date):
    resp = requests.get(f"{URL_BACKEND}/date/{date}")
    return prepare_table(resp.json(), date)


@app.get("/reload/", response_class=HTMLResponse)
async def call_backend():
    resp = requests.get(f"{URL_BACKEND}/reload/{dt.today().isoformat()}")
    return prepare_table(resp.json(), dt.today().isoformat())


@app.get("/reload/{date}", response_class=HTMLResponse)
async def call_backend(date):
    resp = requests.get(f"{URL_BACKEND}/reload/{date}")
    return prepare_table(resp.json(), date)
