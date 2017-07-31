# -*- coding: utf-8 -*-
import os
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

resp = requests.get('http://www.geonames.de/languages.html')
# requests 如果採用 response.text 會取得 Latin-1 編碼的 unicode，所以會導致亂碼，需要採用 content 取得 byte 的原格式才可

# http://xiaorui.cc/2016/02/19/%E4%BB%A3%E7%A0%81%E5%88%86%E6%9E%90python-requests%E5%BA%93%E4%B8%AD%E6%96%87%E7%BC%96%E7%A0%81%E9%97%AE%E9%A2%98/
# https://stackoverflow.com/questions/36833357/python-correct-encoding-of-website-beautiful-soup
soup = BeautifulSoup(resp.content, 'html.parser')
# Select 方法選完後為 list 不是 BeautifulSoup 的類別
lang_table = soup.find('table', class_='unicode')
lang_header_cols = lang_table.find('tr', class_='uniblau').find_all('td')
col_len = len(lang_header_cols)
headers = []
for col in lang_header_cols:
    headers.append(col.text)


lang_rows = lang_table.find_all('tr')
data_rows = []
# 跳過 header
for row in lang_rows[1:]:
    lang_cols = row.find_all('td')
    data_cols = {}
    for index, element in enumerate(headers):
        
        if lang_cols[index].text == u"\xa0" or lang_cols[index].text is None:
            data_cols[element] = lang_cols[col_len -1].text
        else:
            data_cols[element] = lang_cols[index].text
    data_rows.append(data_cols)
# 把此列的資料加入 dataframe
df = pd.DataFrame(data_rows)
basepath = os.path.dirname(__file__)
writer_filepath = os.path.abspath(os.path.join(basepath, 'parse_lang_out.csv'))
df.to_csv(writer_filepath, sep=',', encoding='utf-8')
