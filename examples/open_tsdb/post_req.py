from datetime import datetime
import warnings

# coding:utf-8
import requests

def get_data_by_post(cond_dic):
    r = requests.post("http://119.27.160.141:4242/api/query", json=cond_dic)
    if len(r.json()) > 0:
        dps = r.json()[0]['dps']
        return dps
    else:
        return None

def build_post_json():
    cond_dic = {
        "start": 1490586530,
        # "end": 1489836195,
        "queries": [
            {
                "aggregator": "sum",
                "metric": "sys.cpu.data",
                # "tags": {"host": "web01"}
            },
        ]
    }
    return cond_dic

if __name__ == "__main__":
    print(get_data_by_post(build_post_json()))