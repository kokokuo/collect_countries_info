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

basepath = os.path.dirname(__file__)
# 取得所有語系以及語系代碼 #################################################################

# 1.取得所有 iso 639-1 語系資料 (各種語系與該語系被使用的國籍)
pure_locales = lang_info.iso639_pure_locales

# 2. 找出各個語言的 native_name
language_locale_info = []
for pure_locale in pure_locales:
	locale_lang = Locale.parse(pure_locale[0])
	language_locale_info.append({
		'native_name': locale_lang.display_name,
		'eng_name': locale_lang.english_name,
		'locale_lang_code': pure_locale[0],
		'countries': json.dumps(pure_locale[1])
	})
	print locale_lang.display_name, locale_lang.english_name, pure_locale[1]


# 寫入檔案
writer_filepath = os.path.abspath(os.path.join(basepath, 'lang_locale_info_out.csv'))
df = pd.DataFrame(language_locale_info)
df.to_csv(writer_filepath, sep=',', encoding='utf-8')


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
	headers = ['name', 'native_name', 'alpha2_code', 'alpha3_code', 'country_code', 'currency_code', 'timezones']
	country_data = {
		'name': country.name,
		'alpha2_code': country.alpha_2,
		'alpha3_code': country.alpha_3,
		'country_code': phone,
		'currency_code': json.dumps(curreny_code) if curreny_code else None,
		'timezones': json.dumps(timezones)
		
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
writer_filepath = os.path.abspath(os.path.join(basepath, 'country_info_out.csv'))
df = pd.DataFrame(countries_info, columns=headers)
df.to_csv(writer_filepath, sep=',', encoding='utf-8')