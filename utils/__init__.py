#!/usr/bin/python
# -*- coding: utf-8 -*-
import babel
import itertools
import re
from babel import Locale
from phonenumbers import COUNTRY_CODE_TO_REGION_CODE, REGION_CODE_FOR_NON_GEO_ENTITY



class CountryInfo(object):
	def __init__(self, country_region_code, region_for_non_geo_entity):
		self._country_region_code = country_region_code
		self._REGION_CODE_TO_COUNTRY_CODE = {}
		for country_code, region_codes in self._country_region_code.items():
			for region_code in region_codes:
				if region_code == region_for_non_geo_entity:
					continue
				if region_code in self._REGION_CODE_TO_COUNTRY_CODE:
					raise ValueError("%r is already in the country code list" % region_code)
				self._REGION_CODE_TO_COUNTRY_CODE[region_code] = str(country_code)


		self._currencies_by_country_code = {
			'BD': ('BDT',),
			'BE': ('EUR',),
			'BF': ('XOF',),
			'BG': ('BGN',),
			'BA': ('BAM',),
			'BB': ('BBD',),
			'WF': ('XPF',),
			'BL': ('EUR',),
			'BM': ('BMD',),
			'BN': ('BND',),
			'BO': ('BOB',),
			'BH': ('BHD',),
			'BI': ('BIF',),
			'BJ': ('XOF',),
			'BT': ('BTN', 'INR'),
			'JM': ('JMD',),
			'BV': ('NOK',),
			'BW': ('BWP',),
			'WS': ('WST',),
			'BQ': ('USD',),
			'BR': ('BRL',),
			'BS': ('BSD',),
			'JE': ('GBP',),
			'BY': ('BYR',),
			'BZ': ('BZD',),
			'RU': ('RUB',),
			'RW': ('RWF',),
			'RS': ('RSD',),
			'TL': ('USD',),
			'RE': ('EUR',),
			'TM': ('TMT',),
			'TJ': ('TJS',),
			'RO': ('RON',),
			'TK': ('NZD',),
			'GW': ('XOF',),
			'GU': ('USD',),
			'GT': ('GTQ',),
			'GS': ('GBP',),
			'GR': ('EUR',),
			'GQ': ('XAF',),
			'GP': ('EUR',),
			'JP': ('JPY',),
			'GY': ('GYD',),
			'GG': ('GBP',),
			'GF': ('EUR',),
			'GE': ('GEL',),
			'GD': ('XCD',),
			'GB': ('GBP',),
			'GA': ('XAF',),
			'SV': ('USD',),
			'GN': ('GNF',),
			'GM': ('GMD',),
			'GL': ('DKK',),
			'GI': ('GIP',),
			'GH': ('GHS',),
			'OM': ('OMR',),
			'TN': ('TND',),
			'IL': ('ILS',),
			'JO': ('JOD',),
			'HR': ('HRK',),
			'HT': ('HTG', 'USD'),
			'HU': ('HUF',),
			'HK': ('HKD',),
			'HN': ('HNL',),
			'HM': ('AUD',),
			'VE': ('VEF',),
			'PR': ('USD',),
			'PS': (),
			'PW': ('USD',),
			'PT': ('EUR',),
			'SJ': ('NOK',),
			'PY': ('PYG',),
			'IQ': ('IQD',),
			'PA': ('PAB', 'USD'),
			'PF': ('XPF',),
			'PG': ('PGK',),
			'PE': ('PEN',),
			'PK': ('PKR',),
			'PH': ('PHP',),
			'PN': ('NZD',),
			'PL': ('PLN',),
			'PM': ('EUR',),
			'ZM': ('ZMW',),
			'EH': ('MAD',),
			'EE': ('EUR',),
			'EG': ('EGP',),
			'ZA': ('ZAR',),
			'EC': ('USD',),
			'IT': ('EUR',),
			'VN': ('VND',),
			'SB': ('SBD',),
			'ET': ('ETB',),
			'SO': ('SOS',),
			'ZW': ('USD', 'ZAR', 'BWP', 'GBP', 'EUR'),
			'SA': ('SAR',),
			'ES': ('EUR',),
			'ER': ('ETB', 'ERN'),
			'ME': ('EUR',),
			'MD': ('MDL',),
			'MG': ('MGA',),
			'MF': ('EUR',),
			'MA': ('MAD',),
			'MC': ('EUR',),
			'UZ': ('UZS',),
			'MM': ('MMK',),
			'ML': ('XOF',),
			'MO': ('MOP',),
			'MN': ('MNT',),
			'MH': ('USD',),
			'MK': ('MKD',),
			'MU': ('MUR',),
			'MT': ('EUR',),
			'MW': ('MWK',),
			'MV': ('MVR',),
			'MQ': ('EUR',),
			'MP': ('USD',),
			'MS': ('XCD',),
			'MR': ('MRO',),
			'IM': ('GBP',),
			'UG': ('UGX',),
			'MY': ('MYR',),
			'MX': ('MXN',),
			'AT': ('EUR',),
			'FR': ('EUR',),
			'IO': ('USD',),
			'SH': ('SHP',),
			'FI': ('EUR',),
			'FJ': ('FJD',),
			'FK': ('FKP',),
			'FM': ('USD',),
			'FO': ('DKK',),
			'NI': ('NIO',),
			'NL': ('EUR',),
			'NO': ('NOK',),
			'NA': ('NAD', 'ZAR'),
			'NC': ('XPF',),
			'NE': ('XOF',),
			'NF': ('AUD',),
			'NG': ('NGN',),
			'NZ': ('NZD',),
			'NP': ('NPR',),
			'NR': ('AUD',),
			'NU': ('NZD',),
			'CK': ('NZD',),
			'CI': ('XOF',),
			'CH': ('CHF',),
			'CO': ('COP',),
			'CN': ('CNY',),
			'CM': ('XAF',),
			'CL': ('CLP',),
			'CC': ('AUD',),
			'CA': ('CAD',),
			'LB': ('LBP',),
			'CG': ('XAF',),
			'CF': ('XAF',),
			'CD': ('CDF',),
			'CZ': ('CZK',),
			'CY': ('EUR',),
			'CX': ('AUD',),
			'CR': ('CRC',),
			'CW': ('ANG',),
			'CV': ('CVE',),
			'CU': ('CUP', 'CUC'),
			'SZ': ('SZL',),
			'SY': ('SYP',),
			'SX': ('ANG',),
			'KG': ('KGS',),
			'KE': ('KES',),
			'SS': ('SSP',),
			'SR': ('SRD',),
			'KI': ('AUD',),
			'KH': ('KHR',),
			'KN': ('XCD',),
			'KM': ('KMF',),
			'ST': ('STD',),
			'SK': ('EUR',),
			'KR': ('KRW',),
			'SI': ('EUR',),
			'KP': ('KPW',),
			'KW': ('KWD',),
			'SN': ('XOF',),
			'SM': ('EUR',),
			'SL': ('SLL',),
			'SC': ('SCR',),
			'KZ': ('KZT',),
			'KY': ('KYD',),
			'SG': ('SGD',),
			'SE': ('SEK',),
			'SD': ('SDG',),
			'DO': ('DOP',),
			'DM': ('XCD',),
			'DJ': ('DJF',),
			'DK': ('DKK',),
			'VG': ('USD',),
			'DE': ('EUR',),
			'YE': ('YER',),
			'DZ': ('DZD',),
			'US': ('USD',),
			'UY': ('UYU',),
			'YT': ('EUR',),
			'UM': ('USD',),
			'TZ': ('TZS',),
			'LC': ('XCD',),
			'LA': ('LAK',),
			'TV': ('TVD', 'AUD'),
			'TW': ('TWD',),
			'TT': ('TTD',),
			'TR': ('TRY',),
			'LK': ('LKR',),
			'LI': ('CHF',),
			'LV': ('EUR',),
			'TO': ('TOP',),
			'LT': ('LTL',),
			'LU': ('EUR',),
			'LR': ('LRD',),
			'LS': ('LSL', 'ZAR'),
			'TH': ('THB',),
			'TF': ('EUR',),
			'TG': ('XOF',),
			'TD': ('XAF',),
			'TC': ('USD',),
			'LY': ('LYD',),
			'VA': ('EUR',),
			'VC': ('XCD',),
			'AE': ('AED',),
			'AD': ('EUR',),
			'AG': ('XCD',),
			'AF': ('AFN',),
			'AI': ('XCD',),
			'VI': ('USD',),
			'IS': ('ISK',),
			'IR': ('IRR',),
			'AM': ('AMD',),
			'AL': ('ALL',),
			'AO': ('AOA',),
			'AN': ('ANG',),
			'AQ': (),
			'AS': ('USD',),
			'AR': ('ARS',),
			'AU': ('AUD',),
			'VU': ('VUV',),
			'AW': ('AWG',),
			'IN': ('INR',),
			'AX': ('EUR',),
			'AZ': ('AZN',),
			'IE': ('EUR',),
			'ID': ('IDR',),
			'UA': ('UAH',),
			'QA': ('QAR',),
			'MZ': ('MZN',),
		}

	def get_calling_code(self, iso):
		for code, isos in self._country_region_code.items():
			if iso.upper() in isos:
				return code
		return None

	def get_curreny_code(self, iso3166_code):
		"""
		Args:
			iso3166_code(str): ISO 3166 的國家代碼 e.g TW, US, CN...
		Returns:
			currency_code(str): ISO 4217 的貨幣代碼
		"""
		if iso3166_code in self._currencies_by_country_code:
			return self._currencies_by_country_code[iso3166_code]
		return None


country_info = CountryInfo(COUNTRY_CODE_TO_REGION_CODE, REGION_CODE_FOR_NON_GEO_ENTITY)




class LanguageInfo(object):
	def __init__(self):
		# 1. 取得語系資料
		self._raw_iso639_locales = babel.localedata.locale_identifiers()
		# 過濾掉所有 _ 尾端不包含國碼的語系
		self._iso639_locales_country_code = self._filter_non_country_code_languge(self._raw_iso639_locales)
		# 過濾掉所有國籍，如果有 Script, 過濾掉 Script 後面的尾碼 (等於有兩個 _ 的需要過濾掉)
		self._iso639_pure_locales = self._get_lang_country_distribution(self._iso639_locales_country_code)

	def _filter_iso369_iso_3166(self, locale):
		"""
		過濾掉所有 ISO 639-2,3 以及只有 語系沒有國家代碼的 ISO 639-1 e,g zh, en
		"""
		return locale if (('_' in locale) and len(locale.split('_')[0]) != 3) else None

	def _filter_region_code(self, locale):
		"""
		過濾掉所有 _001
		"""
		return locale if ('_' in locale) and ('001' not in locale) else None

	def _filter_variant(self, locale):
		"""
		如果有兩個 _ 但是第二個底線的長度不是 2 (代表不是國碼)，則過濾掉
		"""
		return locale if (len(re.findall('_', locale)) == 2 and len(locale[locale.rfind('_')+1:]) == 2) or len(re.findall('_', locale)) != 2 else None
			

	def _filter_non_country_code_languge(self, raw_lang_data):
		"""
		過濾掉 iso639-3 三碼，(如果有 _ 的格式之前是3碼也排除 e.g abq_UN)
		同時過濾掉 iso639-1 二碼，但是沒有結合國家代碼的 ISO 6390-1，但需要包含有 _ 的 language tag e.g zh_TW, en_US, 但排除 en, zh
		過濾掉 region 001
		"""
		meta_lang_codes = filter(self._filter_region_code, filter(self._filter_iso369_iso_3166, raw_lang_data))
		# 過濾掉 variant e.g en_US_POSIX
		meta_lang_codes = filter(self._filter_variant, meta_lang_codes)
		return meta_lang_codes
	
	
	@property
	def iso639_locales(self):
		"""
		取出 ISO 639-1 格式的語系國碼，不包含 Variant, Region 001, 或是 ISO639-2,3
		"""
		return self._iso639_locales_country_code

	@property
	def iso639_pure_locales(self):
		"""
		取出純語系碼 （不包含國碼，但是包含 Script, 並且會帶有所使用該語系的國籍
		e.g: [
			('zh_Hant':[TW, HK, CN, MO]),
			('ja':[JP]),
		]
		"""
		return self._iso639_pure_locales


	def _get_country_code(self, val):
		"""
		過濾出以語系為群集的結果，並且有哪些國家代碼屬於此群集（代表有哪些國家使用此語系）
		如果只有一個  _ 並且 _ 到字尾 為 兩碼，表示可能是 ISO 639-1 e.g zh_CN, ja_JP, en_US 則回傳該值
		如果有兩個 _ 並且 _ 到字尾 為 兩碼，表示可能是含有 Script 的語系 e.g sr_Cyrl_XK, zh_Hant_HK
		"""
		if len(re.findall('_', val)) == 1 and len(val[val.rfind('_')+1:]) == 2:
			return val[:2]
		elif len(re.findall('_', val)) == 2 and len(val[val.rfind('_')+1:]) == 2:
			 return val[:val.rfind('_')]

	def _get_lang_country_distribution(self, iso639_locales_country_code):
		"""
		列出每個語系所包含的國籍，Key 值包含 Script
		"""
		groups = itertools.groupby(iso639_locales_country_code, self._get_country_code)
		lang_countries_mapping = []
		for key, val in groups:
			# 過濾掉所有只包含語系的值
			if key is not None:
				# 對所列出的語系作過濾找出國家代碼
				# 先找出有包含 _ 的 locale_code, 再從最後的 _ 擷取國碼，如果長度為 2 表示為 ISO 639-1 可能最高(會後兩位是國碼)，取得該資料
				country_codes = []
				for locale_code in list(val):
					if '_' in locale_code:
						# 從右邊找到的第一個 _ 抓取到字尾 看是否為國碼 e.g zh_CN, sr_Cyrl_XK，是則拿取此國碼
						candidate_country_code = locale_code[locale_code.rfind('_')+1:]
						if len(candidate_country_code) == 2:
							country_codes.append(candidate_country_code)
				print key, country_codes
				# 使用 tuple
				lang_countries_mapping.append( (key,country_codes) ) 
		return lang_countries_mapping 

	def get_country_all_translation_name(self, country_code):
		"""
		取得該國家名稱的所有翻譯
		Args:
			country_code(str): ISO639-1 的國家代碼
		Returns:
			translation_names(tuple of list):所有語系碼、語系名稱 與 翻譯的名稱
			[
				('English', 'en', 'Japanese'),
				('中文（繁體）', 'zh_Hant', '日本'),
			],
			native_name(unicode): 原生翻譯的語系
			
		"""
		translation_names = []
		native_name = None
		for locale_code in self._iso639_pure_locales:
			try:
				locale_obj = Locale.parse(locale_code[0])
				# 語系碼、語系名稱、國家的翻譯名稱
				transation = (locale_code[0], locale_obj.language_name, locale_obj.territories[country_code])
				translation_names.append(transation)  
				# 找出原生語系的翻譯
				if country_code in locale_code[1]:
					native_name = locale_obj.territories[country_code]
			except:
				pass
		return translation_names, native_name

lang_info = LanguageInfo()


