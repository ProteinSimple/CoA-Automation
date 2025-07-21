from datetime import datetime, timedelta
from urllib.parse import urlencode

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

from keyToken import add_token, load_token
from log import get_logger

logger = get_logger(__name__)
BASE_URL = "https://saturn.proteinsimple.com/api/1/cartridges/"


class CartridgeData:
    code_map: dict[int, str] = {
        1: "cIEF 200",
        2: "cIEF 400",
        8: "SDSTurbo",
        6: "SDS+",
        5: "Flex",
    }

    def __init__(self, sat_data: pd.DataFrame = None):
        self.id: int = None
        self.build_date: str = None
        self.build_time: str = None
        self.exp_date: str = None
        self.class_name: str = None
        self.class_code: int = None
        self.batch_num: int = None
        self.qc_status: bool = None

        if sat_data is not None:
            d = sat_data
            self.id = int(d["_id"])
            self.build_date = "%s/%s/%s" % (
                d["b_date"].month,
                d["b_date"].day,
                d["b_date"].year,
            )
            self.build_time = "%d:%02d" % (
                d["b_date"].hour,
                d["b_date"].minute,
            )
            self.exp_date = "%s/%s/%s" % (
                d["exp_date"].month,
                d["exp_date"].day,
                d["exp_date"].year,
            )
            self.class_name = d["_cls"]
            self.class_code = int(d["cartridge_type"])
            if self.class_code == 1:
                self.batch_num = d["membrane_lot"]
            if self.class_code == 6:
                self.batch_num = d["size_insert_lot"]
            if self.class_code == 8:
                self.batch_num = d["pn702_0013_lot"]
            if self.class_code in set([2, 5]):
                self.batch_num = d["center_cap_lot"]
            pass_fail = str(d.get("latest_assay_analysis_pass_fail", "")).strip().lower()
            self.qc_status = "P" if pass_fail == "pass" else "F" if pass_fail == "fail" else "NA"

    def to_dict(self):
        return {
            "id": self.id,
            "build_date": self.build_date,
            "build_time": self.build_time,
            "exp_date": self.exp_date,
            "class_name": self.class_name,
            "class_code": self.class_code,
            "batch_num": self.batch_num,
        }

    def model_name(self) -> str:
        return CartridgeData.code_map[self.class_code]


def build_saturn_url(startdate=None, enddate=None, **extra_params) -> str:
    params = {}

    if startdate:
        params["startdate"] = startdate
    if enddate:
        params["enddate"] = enddate

    params.update(extra_params)

    return BASE_URL + "?" + urlencode(params)


def _saturn_get_response(start, end, username, passkey):
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    end_dt = end_dt + timedelta(days=1)
    end = end_dt.strftime("%Y-%m-%d")
    url = build_saturn_url(startdate=start, enddate=end)
    response = requests.get(url, auth=HTTPBasicAuth(username, passkey))

    if response.status_code == 200:
        return response
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None


def saturn_get_bundle(username, passkey,
                      start=None, end=None) -> list[CartridgeData]:
    if start is None or end is None:
        # THIS SHOULD NEVER HAPPEN AND IS A BAD IMPLEMENTATION
        end_dt = datetime.today() + timedelta(days=1)
        start_dt = end_dt - timedelta(
            days=5
        )  # TODO: change this to search cartridges form previous days as well!

        start = start_dt.strftime("%Y-%m-%d")
        end = end_dt.strftime("%Y-%m-%d")

    response = _saturn_get_response(start, end, username, passkey)

    df = pd.DataFrame(response.json())
    df["b_date_ts"] = df["build_completion_date"].apply(lambda x: x["$date"])
    df["b_date"] = pd.to_datetime(df["b_date_ts"], unit="ms")
    df["exp_date"] = (
        (df["b_date"] + 
         pd.DateOffset(months=12))
            .dt.to_period("M")
            .dt.to_timestamp("M")
    )

    retVal = []
    for _, d in df.iloc[::-1].iterrows():
        retVal.append(CartridgeData(d))
    return retVal


def saturn_check(username, passkey) -> bool:
    # TODO: add comments here ?!
    end_dt = datetime.today()
    enddate = end_dt.strftime("%Y-%m-%d")
    url = build_saturn_url(startdate=enddate, enddate=enddate)
    logger.debug("Sending an basic request to check connection: %s", url)
    response = requests.get(url, auth=HTTPBasicAuth(username, passkey))
    logger.debug(str(response))
    if response.status_code == 200:
        return True
    else:
        return False


def auth(args):
    logger.info("trying to authenticate to saturn API")
    if (
        hasattr(args, "user")
        and hasattr(args, "passkey")
        and args.user
        and args.passkey
    ):
        logger.debug("New credentials given for saturn authentication")
        add_token(args.user, args.passkey)

    else:
        logger.debug(
            "Creadentials not given in the arguments." +
            " trying to load from cache"
        )
    user, passkey = None, None
    try:
        logger.debug("Loading user/passkey to auth into staurn")
        user, passkey = load_token()
        assert saturn_check(user, passkey)
        logger.info("Saturn auth was succesful !")
        return user, passkey
    except Exception as e:
        raise Exception("Couldn't load saturn API key correctly: " + str(e))
