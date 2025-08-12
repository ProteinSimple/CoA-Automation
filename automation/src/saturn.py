from datetime import datetime, timedelta
from urllib.parse import urlencode
import json
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from keyToken import add_token, load_token
from log import get_logger
logger = get_logger(__name__)
BASE_URL = "https://saturn.proteinsimple.com/api/1/cartridges/"

QC_RUN_URL = "https://saturn.proteinsimple.com/api/1/mauriceqcruns/"


class CartridgeData:
    code_map: dict[int, str] = None

    def __init__(self, sat_data: pd.DataFrame = None):
        self.id: int = None
        self.build_date: str = None
        self.build_time: str = None
        self.exp_date: str = None
        self.class_name: str = None
        self.class_code: int = None
        self.batch_num: int = None
        self.qc_status: bool = None
        self.qc_date: str = None
        self.qc_time: str = None
        self.qc_user: str = None

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
            if pd.notna(d.get("qc_user")):
                self.qc_user = d.get("qc_user")
            qc_data = d.get("qc_results")
            if pd.isna(qc_data) is not True:
                data = qc_data[-1]
                # QC time
                qc_time_dt = data["analysis_timestamp"]
                qc_timestampt = pd.to_datetime(qc_time_dt, unit="s")
                self.qc_date = "%s/%s/%s" % (
                    qc_timestampt.month,
                    qc_timestampt.day,
                    qc_timestampt.year,
                )
                self.qc_time = "%d:%02d" % (
                    qc_timestampt.hour,
                    qc_timestampt.minute,
                )

    @staticmethod
    def load_code_map(path: str):
        with open(path) as f:
            res = json.load(f)
            CartridgeData.code_map = {int(k): v for k, v in res.items()}

    @staticmethod
    def add_code2map(path: str, code: int, val: str):
        CartridgeData.code_map[code] = val
        with open(path, mode="w+") as f:
            json.dump(CartridgeData.code_map, f)

    def to_dict(self):
        return {
            "id": self.id,
            "build_date": self.build_date,
            "build_time": self.build_time,
            "exp_date": self.exp_date,
            "class_name": self.class_name,
            "class_code": self.class_code,
            "batch_num": self.batch_num,
            "qc_date": self.qc_date,
            "qc_time": self.qc_time,
            "qc_status": self.qc_status,
            "qc_user": self.qc_user
        }

    def model_name(self) -> str:
        return CartridgeData.code_map[self.class_code]


def build_saturn_url(base_url, startdate=None, enddate=None, **extra_params) -> str:
    params = {}

    if startdate:
        params["startdate"] = startdate
    if enddate:
        params["enddate"] = enddate

    params.update(extra_params)

    return base_url + "?" + urlencode(params)


def _saturn_get_cartridge_data(start, end, username, passkey):
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    end_dt = end_dt + timedelta(days=1)
    end = end_dt.strftime("%Y-%m-%d")
    url = build_saturn_url(BASE_URL, startdate=start, enddate=end)
    response = requests.get(url, auth=HTTPBasicAuth(username, passkey))

    if response.status_code == 200:
        return response
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None


def _preprocess_cartridge_data(df: pd.DataFrame):
    df["b_date_ts"] = df["build_completion_date"].apply(lambda x: x["$date"])
    df["b_date"] = pd.to_datetime(df["b_date_ts"], unit="ms")
    df["exp_date"] = (
        (df["b_date"] +
            pd.DateOffset(months=12))
                .dt.to_period("M")
                .dt.to_timestamp("M")
    )


def _saturn_get_prod_data(username, passkey,
                          start, end) -> pd.DataFrame:
    response = _saturn_get_cartridge_data(start, end, username, passkey)
    _preprocess_cartridge_data(df := pd.DataFrame(response.json()))
    return df


def saturn_check(username, passkey) -> bool:
    # TODO: add comments here ?!
    end_dt = datetime.today()
    enddate = end_dt.strftime("%Y-%m-%d")
    url = build_saturn_url(BASE_URL, startdate=enddate, enddate=enddate)
    logger.debug("Sending an basic request to check connection: %s", url)
    response = requests.get(url, auth=HTTPBasicAuth(username, passkey))
    logger.debug(str(response))
    if response.status_code == 200:
        return True
    else:
        return False


def _saturn_get_qc_results(start, end, user, passkey):
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    end_dt = end_dt + timedelta(days=1)
    end = end_dt.strftime("%Y-%m-%d")
    url = build_saturn_url(QC_RUN_URL, startdate=start, enddate=end)
    response = requests.get(url, auth=HTTPBasicAuth(user, passkey))

    if response.status_code == 200:
        return response
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None


def _extract_info(id: int | str) -> dict:
    if isinstance(id, int):
        id = str(id)

    class_code = int(id[0])
    year = 2000 + int(id[1:3])
    month = int(id[3:5])
    day = int(id[5:7])

    build_date = f"{year:04d}-{month:02d}-{day:02d}"

    return {
        "class_code": class_code,
        "build_date": build_date
    }


def _saturn_get_qc_data(username, passkey,
                        start, end):
    qc_data = _saturn_get_qc_results(start, end, username, passkey).json()
    info_set = {}
    for data in qc_data:
        id = int(data['cartridge_serial'])
        info_set[id] = data  # always keep the latest QC test results

    values = []
    earliest_date = None
    latest_date = None

    for id, data in info_set.items():
        values.append({
            "_id": str(id),
            "qc_user": data["analyst"].split("@")[0]
        })

        extracted = _extract_info(id)
        build_date = extracted["build_date"]
        if earliest_date is None or build_date < earliest_date:
            earliest_date = build_date
        if latest_date is None or build_date > latest_date:
            latest_date = build_date

    retVal = {
        "start": earliest_date,
        "end": latest_date,
        "values": pd.DataFrame(values)
    }

    return retVal


def saturn_bundle_data(username, passkey, start, end):
    res = _saturn_get_qc_data(username, passkey, start, end)
    qc_df: pd.DataFrame = res['values']
    prod_start = res["start"]
    prod_end = res["end"]
    prod_df = _saturn_get_prod_data(username, passkey, prod_start, prod_end)
    prod_df["_id"] = prod_df["_id"].astype(str)
    qc_df["_id"] = qc_df["_id"].astype(str)
    joined = qc_df.join(prod_df.set_index("_id"), on="_id", how='inner')
    saturn_bundle_data.prod_start = prod_start
    saturn_bundle_data.prod_end = prod_end
    return [CartridgeData(d) for _, d in joined.iloc[::-1].iterrows()]


def saturn_bundle_prod_data(username, passkey,
                            start, end):
    prod_df = _saturn_get_prod_data(username, passkey, start, end)

    def is_valid_int(val):
        try:
            return float(val).is_integer()
        except Exception:
            return False
    prod_df = prod_df[prod_df["_id"].apply(is_valid_int)]
    prod_df["_id"] = prod_df["_id"].astype(str)
    return [CartridgeData(d) for _, d in prod_df.iloc[::-1].iterrows()]


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
        raise Exception(
            "Couldn't load saturn API key correctly: " + str(e)
        )
