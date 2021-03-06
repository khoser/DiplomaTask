"""
1. Retrieve a portion of data from API (Variant 7) and store it in a database
2. Update data on demand
3. Update DB schema if needed on app’s update

Variant 7. Using API https://www.metaweather.com/api/ get data about weather in Moscow for current month
and store it into your DB
(id, weather_state_name, wind_direction_compass, created, applicable_date, min_temp, max_temp, the_temp).
Output the data by date (the date is set) in form of a table and sort them by created in ascending order.
"""

import sys
from calendar import monthrange
import datetime
from db import Database
import asyncio
import aiohttp
from fastapi import FastAPI
from datetime import date as dt

URL_API = 'https://www.metaweather.com/api/location/2122265'  # Moscow
attrs = {
    'id': 'bigint',
    'weather_state_name': 'varchar',
    'wind_direction_compass': 'varchar',
    'created': 'timestamp',
    'applicable_date': 'date',
    'min_temp': 'float',
    'max_temp': 'float',
    'the_temp': 'float'
}
db = Database()
app = FastAPI()


class AsyncWeatherCall(object):
    def __init__(self, urls, ids):
        self.stri = []
        self.urls = urls
        self.ids = ids

    async def call_url(self, url):
        session = aiohttp.ClientSession()
        response = await session.get(url)
        data = await response.json()
        result = ',\n'.join('(' + ','.join(f"'{(item[index])}'" for index in attrs.keys()) + ')' for item in data
                            if item['id'] not in self.ids)
        if result:
            self.stri.append(result.replace('None', 'Null'))
        await session.close()

    def do_async(self):
        futures = [self.call_url(url) for url in self.urls]
        loop = asyncio.new_event_loop()
        loop.run_until_complete(asyncio.wait(futures))
        return ',\n'.join(self.stri)


def recreate_tables():
    sql_cmd = f'''
        CREATE table if not exists public.weather({', '.join(f'{key} {value} NULL' for key, value in attrs.items())});
    '''
    db.execute(sql_cmd)


def get_ids(date):
    sql_cmd = f"""select id from public.weather
    where applicable_date between
        '{date.strftime('%Y-%m')}-01' and '{date.strftime('%Y-%m')}-{monthrange(date.year, date.month)[1]}'
    """
    ids = db.select(sql_cmd)
    return [i[0] for i in ids if i is not None]


@app.get("/reload/{date}")
def backend(date):
    call_date = dt.fromisoformat(date)
    year = int(call_date.year)
    month = int(call_date.month)
    day = int(call_date.day)
    recreate_tables()
    gen_ids = get_ids(datetime.date(year, month, day))
    urls = [f'{URL_API}/{year}/{month}/{cur_day + 1}' for cur_day in range(monthrange(year, month)[1])]
    day_val = AsyncWeatherCall(urls, gen_ids).do_async()
    sql_cmd = ''
    if day_val:
        sql_cmd += f'''
        insert into public.weather({','.join(f'"{index}"' for index in attrs.keys())}) values {day_val};
        '''
    if sql_cmd:
        db.execute(sql_cmd)
    return front_data_by_date(date)


def usage():
    print(f'usage: {sys.argv[0]} year month day')


@app.get("/date/{date}")
def front_data_by_date(date):
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
    return db.select(sql_cmd)


@app.get("/")
def hello():
    return {'use': '/date/...'}


# if __name__ == '__main__':
#     try:
#         backend(*sys.argv[1:4])
#     except TypeError as e:
#         usage()
