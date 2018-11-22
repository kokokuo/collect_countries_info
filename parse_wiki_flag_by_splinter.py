# -*- coding: utf-8 -*-

import os
import csv
from splinter import Browser
from PIL import Image
from StringIO import StringIO
from bs4 import BeautifulSoup


save_folder = "Flags"
basepath = os.path.dirname(__file__)
brower = Browser('chrome', headless=True)

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

    if 'https:' not in flag_url:
        flag_url = '{}{}'.format('https:', flag_url)
    # 調整大小與保存
    resp = requests.get(flag_url)
    im = Image.open(StringIO(resp.content))
    im_width, im_height = im.size
    width = 30
    height = 20
    im = im.resize((width, height), Image.BILINEAR)
    im.save(abs_file_path)


def grab_country_data(code_row, index):
    data = code_row.find_all('td')
    INTRO_LINK_IDX = 0
    COUNTRY_ABBR3_IDX = 2
    flag_url = data[INTRO_LINK_IDX].find('img').get('src')
    abbr3_iso = data[COUNTRY_ABBR3_IDX].text
    print("第 {} 筆：圖片路徑: {}, 3 碼: {} ".format(index, flag_url, abbr3_iso))

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
    brower.visit('https://en.wikipedia.org/wiki/ISO_3166-1')
    codes_table = brower.find_by_xpath('//*[@id="mw-content-text"]/div/table[2]/tbody')[0]


    # //*[@id="mw-content-text"]/div/table[2]/tbody/tr[1]/td[3]/span
    # //*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td[3]/span
    # codes_table = soup.find_all('table', class_="wikitable sortable")[CODES_TABLE]
    # code_rows = codes_table.find_all("tr")
    # rows_size = len(code_rows)
    # index = 1
    # for code_row in code_rows[DATA_START_ROW:rows_size - DATA_START_ROW]:
    #     grab_country_data(code_row, index)
    #     index += 1
    # print('已完成')


if __name__ == '__main__':
    main()
