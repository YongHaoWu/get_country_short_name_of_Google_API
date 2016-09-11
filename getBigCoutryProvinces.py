import csv
import requests
import urllib.request
import re
big_countries = [
'CN',
'JP',
'FR',#France
'US',#United States
'RU',#Russia
'DE',#Germany
'GB',#United Kingdom
]
for big_country in big_countries:
    tmp_countries = []
    EN_list = []
    EN_longname_list = []
    ZH_longname_list = []
    url = "http://www.geodatasource.com/breakdown/"+big_country
    page = urllib.request.urlopen(url)
    page_str = page.read().decode('utf-8')
    content = re.findall(r'<div class="content-page">.*?</div>', page_str, re.DOTALL)
    # print(content)
    string = re.findall(r'<li>(.*?)\(', content[0], re.MULTILINE)
    print(big_country+" is ")
    for single_province in string:
        # print(single_province)
        url = 'http://maps.google.cn/maps/api/geocode/json'
        params = {'language': 'en', 'address': single_province}
        response = requests.get(url, params=params)
        json_data = response.json()

        if json_data['results'][0]['types'][0] == 'administrative_area_level_1':
            print("origin is "+single_province+" short name: "+json_data['results'][0]['address_components'][0]['short_name'])
            EN_list.append(json_data['results'][0]['address_components'][0]['short_name'])
            EN_longname_list.append(json_data['results'][0]['address_components'][0]['long_name'])

            url = 'http://maps.google.cn/maps/api/geocode/json'
            params = {'language': 'zh-CN', 'address': single_province}
            response = requests.get(url, params=params)
            json_data = response.json()
            ZH_longname_list.append(json_data['results'][0]['address_components'][0]['long_name'])
            with open(big_country+'.csv', 'w') as csvfile:
                fieldnames = ['short_name', 'EN_longname', 'ZH_longname']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for k in range(0, len(EN_list)):
                    writer.writerow({'short_name': EN_list[k], 'EN_longname': EN_longname_list[k], 'ZH_longname': ZH_longname_list[k]})
