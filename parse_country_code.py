# -*- coding: utf-8 -*-

import os
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

def main():
	resp = requests.get('http://www.nationsonline.org/oneworld/country_code_list.htm')
	soup = BeautifulSoup(resp.content, 'html.parser')
	table_rows = soup.find('table',id='codelist').find_all('tr')
	country_list = []
	country_key = []
	cols_header = table_rows[0].find_all('th')

	for col_header in cols_header[1:4]:
		country_key.append(col_header.text)
		key_size = len(country_key)

	for row in table_rows[1:]:
		table_cols = row.find_all('td')
		size = len(table_cols)

		country_list.append({
			'Country': (table_cols[size-4].text).strip(),
			country_key[1]: (table_cols[size-3].text).strip(),
			country_key[2]: (table_cols[size-2].text).strip(),
		})

	basepath = os.path.dirname(__file__)
	reader_filepath = os.path.abspath(os.path.join(basepath, 'countries_data.csv'))
	writer_filepath = os.path.abspath(os.path.join(basepath, 'countries_code_out.csv'))

	# output = open('test2.csv','wb')
	# csvfile = open(reader_filepath)

	read_df = pd.read_csv(reader_filepath)
	print read_df
	import pdb; pdb.set_trace()
	country_code_df = pd.DataFrame(country_list)
	print country_code_df
	result_df = pd.merge(read_df, country_code_df, on='Country',how='left')
	print result_df
	result_df.to_csv(writer_filepath, sep=',', encoding='utf-8')
	# reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
	# ori_fieldnames = reader.fieldnames
	# ori_fieldnames.extend(country_key[1:])
	# import pdb; pdb.set_trace()
	# csvwriter = csv.DictWriter(output, delimiter=',', fieldnames=ori_fieldnames)

	# for row in UnicodeReader(fcsv, delimiter=',', quotechar='"'): # 2

if __name__ == '__main__':
	main()