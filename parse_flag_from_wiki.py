# -*- coding: utf-8 -*-

import os
import csv
import requests
from lxml import etree
from bs4 import BeautifulSoup
import pandas as pd

basepath = os.path.dirname(__file__)
site = "https://en.wikipedia.org"
save_folder = "Flags"
"""
找出該國家的國旗圖示 #################################################################
參考來源：http://www.freeflagicons.com/list/
WIKI : https://en.wikipedia.org/wiki/ISO_3166-1
"""


def grab_flag_url(content):
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find("table", class_="infobox geography vcard")
    flag_url = table.find_all('img')[0].get('src')
    print(" - 圖片路徑: {}".format(flag_url))
    return flag_url


def save_flag_to_file(flag_url, filename): 
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    folder_path = os.path.join(basepath, save_folder)
    abs_file_path = os.path.abspath(os.path.join(folder_path, filename))

    with open(abs_file_path, 'wb') as f:
        if 'https:' not in flag_url:
            flag_url = '{}{}'.format('https:', flag_url)
            resp = requests.get(flag_url)
            f.write(resp.content)


def grab_country_data(code_row):
    data = code_row.find_all('td')
    INTRO_LINK_IDX = 0
    COUNTRY_ABBR3_IDX = 2
    intro_url = site + data[INTRO_LINK_IDX].find('a').get('href')
    abbr3_iso = data[COUNTRY_ABBR3_IDX].text
    print("導向的網址: {}, 3 碼: {} ".format(intro_url, abbr3_iso))
    resp = requests.get(intro_url)
    flag_url = grab_flag_url(resp.content)
    flag_path = save_flag_to_file(flag_url, abbr3_iso + '.png')

    return {
        'flag_url': flag_url,
        'file_path': flag_path,
        'abbr3_iso': abbr3_iso
    }


def main():
    CODES_TABLE = 1
    DATA_START_ROW = 1
    FLAG_URL_IDX = 0
    COUNTRY_ABBR3_IDX = 2
    resp = requests.get('https://en.wikipedia.org/wiki/ISO_3166-1')
    soup = BeautifulSoup(resp.content, 'html.parser')
    codes_table = soup.find_all('table', class_="wikitable sortable")[CODES_TABLE]
    code_rows = codes_table.find_all("tr")
    rows_size = len(code_rows)
    for code_row in code_rows[DATA_START_ROW:rows_size - DATA_START_ROW]:
        grab_country_data(code_row)
    print('已完成')

    # countries_block = table.find("tbody").find_all("tr")
    # country_list = []
    # country_field = []
    # header_columns = table_rows[COLUMN_FIELD_IDX].find_all('td')
    # import pdb; pdb.set_trace()
    # country_field.append("Flag")
    # col_size = len(header_columns)
    # for col_header in header_columns[COLUMN_FIELD_IDX + 1, col_size - 1]:
    #     country_field.append(col_header.text)
    #     key_size = len(country_field)

    # for row in table_rows[1:]:
    #     table_cols = row.find_all('td')
    #     size = len(table_cols)

    #     country_list.append({
    #         'Country': (table_cols[size-4].text).strip(),
    #         country_field[1]: (table_cols[size-3].text).strip(),
    #         country_field[2]: (table_cols[size-2].text).strip(),
    #     })

    # basepath = os.path.dirname(__file__)
    # reader_filepath = os.path.abspath(os.path.join(basepath, 'countries_data.csv'))
    # writer_filepath = os.path.abspath(os.path.join(basepath, 'countries_code_out.csv'))

    # # output = open('test2.csv','wb')
    # # csvfile = open(reader_filepath)

    # read_df = pd.read_csv(reader_filepath)
    # print read_df
    # import pdb; pdb.set_trace()
    # country_code_df = pd.DataFrame(country_list)
    # print country_code_df
    # result_df = pd.merge(read_df, country_code_df, on='Country',how='left')
    # print result_df
    # result_df.to_csv(writer_filepath, sep=',', encoding='utf-8')
    # # reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    # # ori_fieldnames = reader.fieldnames
    # # ori_fieldnames.extend(country_field[1:])
    # # import pdb; pdb.set_trace()
    # # csvwriter = csv.DictWriter(output, delimiter=',', fieldnames=ori_fieldnames)

    # # for row in UnicodeReader(fcsv, delimiter=',', quotechar='"'): # 2

if __name__ == '__main__':
    main()