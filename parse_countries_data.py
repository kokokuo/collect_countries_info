#!/usr/bin/python
# -*- coding: utf-8 -*-
import babel
import os
from babel import Locale
from utils import country_info, lang_info
import pandas as pd
import re
import pycountry
import pytz
import json
import io

basepath = os.path.dirname(__file__)

"""
找出該國家的所有資料 (ISO 3166) #################################################################
ISO 3166 包含獨立與為獨立的國家地區 - 目前全世界有195個國家。 主要政治實體為249個(不含爭議地區)
參考：http://www.global-elements.com/wp/alexandroslee/195countries_249entities_unn_countrycode/
在 WIKI 中就是列表 Independant 為 No 的 https://en.wikipedia.org/wiki/ISO_3166-1
""" 
# 找出國家 iso 3166 代碼
iso3166_countries = pycountry.countries
countries_info = []
for country in iso3166_countries:
    # 找出手機號碼
    phone = country_info.get_calling_code(country.alpha_2)
    # 找出幣別
    curreny_code = country_info.get_curreny_code(country.alpha_2)
    # 取得國家的時區
    if country.alpha_2 in pytz.country_timezones:
        timezones = pytz.country_timezones[country.alpha_2]

    print country.alpha_2, country.alpha_3, country.name, phone, curreny_code, timezones
    # 提供給 DataFrame 用的 Header
    headers = ['name', 'native_name', 'abbr_iso', 'abbr3_iso', 'country_code', 'currencies_code', 'timezones']
    # 如果有該國碼出現，才會加入至國家中
    if country.alpha_2:
        country_data = {
            'name': country.common_name if hasattr(country, 'common_name') else country.name,
            'abbr_iso': country.alpha_2,
            'abbr3_iso': country.alpha_3,
            'country_code': phone,
            'currencies_code': curreny_code if curreny_code else None,
            'timezones': timezones
        }
        # 取得該國家名稱的所有翻譯語言
        translation_names, native_name = lang_info.get_country_all_translation_name(country.alpha_2)
        country_data['native_name'] = native_name
        for country_translation_info in translation_names:
            langauge_title = u"{name} ({code})".format(name=country_translation_info.lang_name, code=country_translation_info.locale_code)
            country_data[langauge_title] = country_translation_info.native_name
            headers.append(langauge_title)
        countries_info.append(country_data)
    print country_data


# 寫入檔案
csv_writer_fp = os.path.abspath(os.path.join(basepath, 'country_info_out.csv'))
json_writer_fp = os.path.abspath(os.path.join(basepath, 'country_info_out.json'))
df = pd.DataFrame(countries_info, columns=headers)
df.to_csv(csv_writer_fp, sep=',', encoding='utf-8')

# 產生 json 檔案 （utf-8）
with io.open(json_writer_fp, 'w', encoding='utf-8') as fp:
    json_data = json.dumps(countries_info, indent=4, ensure_ascii=False)
    fp.write(unicode(json_data))
