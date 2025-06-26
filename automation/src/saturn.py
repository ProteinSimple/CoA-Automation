import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode
from datetime import datetime, timedelta
import pandas as pd

BASE_URL = "https://saturn.proteinsimple.com/api/1/cartridges/"


class CartridgeData:
    code_map: dict[int, str] = {
        1: 'cIEF 200',
        2: 'cIEF 200',
        8: 'SDSTurbo',
        6: 'SDS+',
        5: 'Flex',
    } # TODO: change this to accomodate for future additions!
    
    def __init__(self, sat_data: pd.DataFrame =None):
        self.id : int = None
        self.build_date: str = None
        self.build_time: str = None
        self.exp_date: str = None
        self.class_name: str = None
        self.class_code: int = None
        self.batch_num: int = None

        if sat_data is not None:
            d = sat_data
            self.id = int(d["_id"])
            self.build_date = f"{d['b_date'].month}/{d['b_date'].day}/{d['b_date'].year}"
            self.build_time = f"{d['b_date'].minute}:{d['b_date'].hour}"
            self.exp_date = f"{d['exp_date'].month}/{d['exp_date'].day}/{d['exp_date'].year}"
            self.class_name = d["_cls"]
            self.class_code = int(d["cartridge_type"])
            if self.class_code in [1, 2, 5]:
                self.batch_num = d["membrane_lot"]
            if self.class_code == 6:
                self.batch_num = d["size_insert_lot"]
            if self.class_code == 8:
                self.batch_num = d["pn702_0013_lot"]
            

    def to_dict(self):
        return {
            "id" : self.id,
            "build_date": self.build_date,
            "build_time": self.build_time,
            "exp_date": self.exp_date,
            "class_name": self.class_name,
            "class_code": self.class_code,
            "batch_num": self.batch_num
        }
    
    
    def model_name(self) -> str:
        return CartridgeData.code_map[self.class_code]
        


def build_saturn_url(startdate=None, enddate=None, **extra_params):
    params = {}

    if startdate:
        params["startdate"] = startdate
    if enddate:
        params["enddate"] = enddate

    # Add any other params dynamically
    params.update(extra_params)

    return BASE_URL + "?" + urlencode(params)

def saturn_get_cartridge_data_range(length, limit, username, passkey):


    end_dt = datetime.today() + timedelta(days=1)
    start_dt = end_dt - timedelta(days=length)

    startdate = start_dt.strftime("%Y-%m-%d")
    enddate = end_dt.strftime("%Y-%m-%d")
    url = build_saturn_url(startdate=startdate, enddate=enddate)
    response = requests.get(url, auth=HTTPBasicAuth(username, passkey))


    if response.status_code == 200:
        data = pd.DataFrame(response.json())
        data.to_csv("out.csv")
        if limit == -1:
            limit = len(data)
        for _, d in data.iloc[::-1].head(limit).iterrows():
            val = {
                "id": d["_id"],
                "b_date": datetime.fromtimestamp(int(d["build_completion_date"]["$date"]) / 1000).strftime("%Y-%m-%d %H:%M:%S")
            }
            yield val
            
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None

def saturn_get_cartridge_data(id, username, passkey) -> CartridgeData | None:
    end_dt = datetime.today() + timedelta(days=1)
    start_dt = end_dt - timedelta(days=5) # TODO: change this to search cartridges form previous days as well!

    startdate = start_dt.strftime("%Y-%m-%d")
    enddate = end_dt.strftime("%Y-%m-%d")
    url = build_saturn_url(startdate=startdate, enddate=enddate)
    response = requests.get(url, auth=HTTPBasicAuth(username, passkey))

    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        df["b_date_ts"] = df["build_completion_date"].apply(lambda x: x["$date"])
        df["b_date"] = pd.to_datetime(df["b_date_ts"], unit="ms")
        df["exp_date"] = (df["b_date"] + pd.DateOffset(months=12)).dt.to_period("M").dt.to_timestamp("M")
        df.to_csv("out.csv")
        for _, d in df.iloc[::-1].iterrows():
            if int(d["_id"]) == id:
                return CartridgeData(d)
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None

def saturn_get_cartridge_data_bundle(ids, username, passkey) -> list[CartridgeData] | None:
    end_dt = datetime.today() + timedelta(days=1)
    start_dt = end_dt - timedelta(days=5) # TODO: change this to search cartridges form previous days as well!
    ids_s = set(ids)
    startdate = start_dt.strftime("%Y-%m-%d")
    enddate = end_dt.strftime("%Y-%m-%d")
    url = build_saturn_url(startdate=startdate, enddate=enddate)
    response = requests.get(url, auth=HTTPBasicAuth(username, passkey))

    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        df["b_date_ts"] = df["build_completion_date"].apply(lambda x: x["$date"])
        df["b_date"] = pd.to_datetime(df["b_date_ts"], unit="ms")
        df["exp_date"] = (df["b_date"] + pd.DateOffset(months=12)).dt.to_period("M").dt.to_timestamp("M")
        df.to_csv("out.csv")
        retVal = []
        for _, d in df.iloc[::-1].iterrows():
            if int(d["_id"]) in ids_s:
                retVal.append(CartridgeData(d))
        return retVal
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
