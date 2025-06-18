import requests, os
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode

from datetime import datetime, timedelta

BASE_URL = "https://saturn.proteinsimple.com/api/1/cartridges/"

def build_saturn_url(startdate=None, enddate=None, **extra_params):
    params = {}

    if startdate:
        params["startdate"] = startdate
    if enddate:
        params["enddate"] = enddate

    # Add any other params dynamically
    params.update(extra_params)

    return BASE_URL + "?" + urlencode(params)

def saturn_get_cartridge_data(length, limit, username, passkey):


    end_dt = datetime.today()
    start_dt = end_dt - timedelta(days=length)

    startdate = start_dt.strftime("%Y-%m-%d")
    enddate = end_dt.strftime("%Y-%m-%d")
    url = build_saturn_url(startdate=startdate, enddate=enddate)
    response = requests.get(url, auth=HTTPBasicAuth(username, passkey))


    if response.status_code == 200:
        data = response.json()
        for d in list(reversed(data))[:limit]:
            val = {
                "id": d["_id"],
                "b_date": datetime.fromtimestamp(int(d["build_completion_date"]["$date"]) / 1000).strftime("%Y-%m-%d %H:%M:%S")    
            }
            yield val
            
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None


def saturn_check_connection(username, passkey) -> bool:
    end_dt = datetime.today()
    enddate = end_dt.strftime("%Y-%m-%d")
    url = build_saturn_url(startdate=enddate, enddate=enddate)
    response = requests.get(url, auth=HTTPBasicAuth(username, passkey))
    if response.status_code == 200:
        return True
    else:
        return False
