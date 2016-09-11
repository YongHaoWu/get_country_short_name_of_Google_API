import xlrd
import csv
import requests
# import urllib.request
# import urllib3
# import json

data = xlrd.open_workbook('./Country.xlsx')
table = data.sheets()[0]
country_EN = table.col_values(1)
country_EN = country_EN[2:]
i = 1
EN_list = []
EN_longname_list = []
ZH_longname_list = []
not_use_country = ""
for single_EN in country_EN:
    url = 'http://maps.google.cn/maps/api/geocode/json'
    params = {'language': 'en', 'address': single_EN}
    response = requests.get(url, params=params)
    json_data = response.json()
    if json_data['results'][0]['types'][0] == 'country':
        print("origin is "+single_EN+" short name: "+json_data['results'][0]['address_components'][0]['short_name'])
        EN_list.append(json_data['results'][0]['address_components'][0]['short_name'])
        EN_longname_list.append(json_data['results'][0]['address_components'][0]['long_name'])

        url = 'http://maps.google.cn/maps/api/geocode/json'
        params = {'language': 'zh-CN', 'address': single_EN}
        response = requests.get(url, params=params)
        json_data = response.json()
        ZH_longname_list.append(json_data['results'][0]['address_components'][0]['long_name'])

        if single_EN == 'Zimbabwe':
            break;
    else:
        not_use_country += json_data['results'][0]['address_components'][0]['long_name']
        print("not use: "+json_data['results'][0]['address_components'][0]['long_name'])

with open('short_name.csv', 'w') as csvfile:
    fieldnames = ['short_name', 'EN_longname', 'ZH_longname']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for k in range(0, len(EN_list)):
        writer.writerow({'short_name': EN_list[k], 'EN_longname': EN_longname_list[k], 'ZH_longname': ZH_longname_list[k]})

print(len(EN_list))
print(len(EN_longname_list))
print(len(ZH_longname_list))
print("not use:", not_use_country)
