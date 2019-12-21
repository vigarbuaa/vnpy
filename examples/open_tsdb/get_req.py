from datetime import datetime
import warnings

# coding:utf-8
import requests

# -*- coding: utf-8 -*-
import requests


def get_data_by_get(query):
    r = requests.get("http://119.27.160.141:4242/api/query?" + query)
    if len(r.json()) > 0:
        dps = r.json()[0]['dps']
        return dps
    else:
        return None

if __name__ == "__main__":
    print(get_data_by_get('start=1490586530&m=sum:sys.cpu.data'))