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
取得所有語系以及語系代碼 (ISO-639-1) #################################################################
"""
# 1.取得所有 iso 639-1 語系資料 (各種語系與該語系被使用的國籍)
pure_locales = lang_info.iso639_pure_locales

# 2. 找出各個語言的 native_name
language_locale_info = []
for pure_locale in pure_locales:
    locale_lang = Locale.parse(pure_locale.lang_code)
    language_locale_info.append({
        'name': locale_lang.display_name,
        'eng_name': locale_lang.english_name,
        'locale_code': pure_locale.lang_code,
        'using_countries': pure_locale.countries
    })
    print locale_lang.display_name, locale_lang.english_name, pure_locale[1]


# 寫入檔案
csv_writer_fp = os.path.abspath(os.path.join(basepath, 'lang_locale_info_out.csv'))
json_writer_fp = os.path.abspath(os.path.join(basepath, 'lang_locale_info_out.json'))
df = pd.DataFrame(language_locale_info)
df.to_csv(csv_writer_fp, sep=',', encoding='utf-8')

# 產生 json 檔案 （utf-8）
with io.open(json_writer_fp, 'w', encoding='utf-8') as fp:
    json_data = json.dumps(language_locale_info, indent=4, ensure_ascii=False)
    fp.write(unicode(json_data))
