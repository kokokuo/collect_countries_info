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
# 取得所有語系以及語系代碼 #################################################################

# 1.取得所有 iso 639-1 語系資料 (各種語系與該語系被使用的國籍)
pure_locales = lang_info.iso639_pure_locales

# 2. 找出各個語言的 native_name
language_locale_info = []
for pure_locale in pure_locales:
	locale_lang = Locale.parse(pure_locale[0])
	language_locale_info.append({
		'name': locale_lang.display_name,
		'eng_name': locale_lang.english_name,
		'locale_code': pure_locale[0],
		'using_countries': pure_locale[1]
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

# 找出該國家的所有資料 #################################################################
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
			'name': country.name,
			'abbr_iso': country.alpha_2,
			'abbr3_iso': country.alpha_3,
			'country_code': phone,
			'currencies_code': curreny_code if curreny_code else None,
			'timezones': timezones	
		}
		# 取得該國家名稱的所有翻譯語言
		translation_names , native_name = lang_info.get_country_all_translation_name(country.alpha_2)
		country_data['native_name'] = native_name

		for locale_name in translation_names:
			langauge_title = u"{name} ({code})".format(name=locale_name[0], code=locale_name[1])
			country_data[langauge_title] = locale_name[2]	
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
