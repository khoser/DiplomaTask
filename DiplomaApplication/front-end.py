from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from db import Database
from datetime import date as dt
import subprocess

db = Database()
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


@app.get("/", response_class=HTMLResponse)
async def main():
    sql_cmd = f"""select
        -- applicable_date,
        created,
        weather_state_name,
        wind_direction_compass,
        min_temp,
        max_temp,
        the_temp
    from public.weather
    where applicable_date = '{dt.today()}'
    order by created asc;"""
    return prepare_table(db.select(sql_cmd), dt.today())


@app.get("/{date}", response_class=HTMLResponse)
async def get_by_date(date):
    sql_cmd = f"""select
       -- applicable_date,
        created,
        weather_state_name,
        wind_direction_compass,
        min_temp,
        max_temp,
        the_temp 
    from public.weather
    where applicable_date = '{date}'
    order by created asc;"""
    return prepare_table(db.select(sql_cmd), date)


@app.get("/reload/{date}")
async def call_backend(date):
    call_date = dt.fromisoformat(date)
    bash_cmd = f"python3 back-end.py {call_date.year} {call_date.month} {call_date.day}"
    p = subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, shell=True)
    return p.communicate()
