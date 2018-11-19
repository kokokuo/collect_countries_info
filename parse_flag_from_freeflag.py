# -*- coding: utf-8 -*-

import os
import csv
from
import requests
from lxml import etree
from bs4 import BeautifulSoup
import pandas as pd

basepath = os.path.dirname(__file__)
site = "http://www.freeflagicons.com"
save_folder = "Flags"
"""
找出該國家的國旗圖示 #################################################################
參考來源：http://www.freeflagicons.com/list/
"""


def save_flag_to_file(flag_url, filename):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    folder_path = os.path.join(basepath, save_folder)
    abs_file_path = os.path.abspath(os.path.join(folder_path, filename))

    with open(abs_file_path, 'wb') as f:
        if 'http:' not in flag_url:
            flag_url = '{}{}'.format('http:', flag_url)
            
        resp = requests.get(flag_url)
        f.write(resp.content)


def grab_country_data(code_row):
    data = code_row.find_all('td')
    INTRO_LINK_IDX = 0
    COUNTRY_LTD_IDX = 5
    import pdb; pdb.set_trace()
    flag_url = site + data[INTRO_LINK_IDX].find('a').get('href')
    tld = data[COUNTRY_LTD_IDX].text
    abbr2_iso = tld[1:].upper()
    print("導向的網址: {}, LTD 碼: {}, Abbr2 iSO: {} ".format(flag_url, tld, abbr2_iso))
    flag_path = save_flag_to_file(flag_url, abbr2_iso + '.png')

    return {
        'flag_url': flag_url,
        'file_path': flag_path,
        'tld': tld,
        'abbr2_iso': abbr2_iso
    }


def main():
    CODES_TABLE = 1
    DATA_START_ROW = 1
    FLAG_URL_IDX = 0
    COUNTRY_ABBR3_IDX = 2
    resp = requests.get('http://www.freeflagicons.com/list/')
    soup = BeautifulSoup(resp.content, 'html.parser')
    codes_table = soup.find('table', class_="country-list")
    code_rows = codes_table.find_all("tr")
    rows_size = len(code_rows)
    for code_row in code_rows[DATA_START_ROW:rows_size - DATA_START_ROW]:
        grab_country_data(code_row)
    print('已完成')


if __name__ == '__main__':
    main()
