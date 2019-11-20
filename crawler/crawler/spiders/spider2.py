import scrapy
import json
import csv
import random

class StartupsSpider2(scrapy.Spider):
    name = "profileinfo"
    start_urls = ['https://e27.co/api/startups/?tab_name=recentlyupdated']

    def parse(self, response):
        request_body = '&length=30000'
        url = response.url + request_body
        yield scrapy.Request(url=url, body=request_body, callback=self.get_page)

    def get_page(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        result_list = jsonresponse['data']['list']
        result_list = random.sample(result_list, 250)
        list_startups = []
        for el in result_list:
            for k,v in el.items():
                if type(v) == str:
                    if el[k] == '[[]]':
                        el[k] = ' '
        for e in result_list:
            company_name = e['name']
            profile_url = 'https://e27.co/{}'.format(e['slug'])
            company_website_url = e['metas']['website']
            location = e['location'][0]['text']
            tags = e['market']
            totalstartupcount = jsonresponse['data']['totalstartupcount'] #this is number of all profile startups on this site. But i don't know how to convey this value in parce method
            short_description = e['metas']['short_description']
            founding_date = ' '
            founders = ' '
            employee_range = ' '
            emails = ' '
            phones = ' '
            description = ' '
            information = {'company_name': company_name, 'profile_url': profile_url, 
            'company_web_site_url': company_website_url, 'location': location, 'tags': tags, 
            'short_description': short_description, 'founding_date': founding_date, 'founders': founders,
            'employee_range': employee_range, 'emails': emails, 'phones': phones, 'description': description}

            list_startups.append(information)

        keys = list_startups[0].keys()
        with open('profiles_info.csv', 'w') as myfile:
            dict_writer = csv.DictWriter(myfile, keys)
            dict_writer.writeheader()
            dict_writer.writerows(list_startups)