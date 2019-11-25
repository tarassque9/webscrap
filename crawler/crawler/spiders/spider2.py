import scrapy
import csv
import random
import json


class ReadSpider(scrapy.Spider):
    name = 'readspider'

    def start_requests(self):
        with open('urls.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            spamreader = random.sample(list(spamreader), 250)
            random_urls = []
            for url in spamreader:
                url = url[0].split('/')[4]
                random_urls.append(''.join(url))
        
        
        for slug in random_urls:
            new_url = 'https://e27.co/api/startups/get/?slug={}&data_type=general'.format(slug)
            yield scrapy.Request(url=new_url, callback=self.parse)
    
    
    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        list_startups = []
        company_name = jsonresponse['data']['name']
        slug = jsonresponse['data']['slug']
        profile_url = 'https://e27.co/{}'.format(slug)
        company_website_url = jsonresponse['data']['metas']['website']
        location = jsonresponse['data']['location'][0]['text']
        tags = jsonresponse['data']['market']
        short_description = jsonresponse['data']['metas']['short_description']
        description = jsonresponse['data']['metas']['description']
        founding_month = jsonresponse['data']['metas']['found_month']
        founding_year = jsonresponse['data']['metas']['found_year']
        founding_date = (founding_month, founding_year)
        founders = []
        employee_range = []
        email = jsonresponse['data']['metas']['email']
        linkedin = jsonresponse['data']['metas']['linkedin']
        twitter = jsonresponse['data']['metas']['twitter']
        facebook = jsonresponse['data']['metas']['facebook']
        urls = (linkedin, twitter, facebook)
        phones = []
        information = {'company_name': company_name, 'profile_url': profile_url,
        'company_web_site_url': company_website_url, 'location': location, 'tags': tags,
        'short_description': short_description, 'description': description,
        'founding_date': founding_date, 'founders': founders,
        'employee_range': employee_range, 'urls': urls,
        'email': email, 'phones': phones, }

        
        list_startups.append(information)

        # key = list_startups[0].keys()
        # with open('profiles_info2.csv', 'w') as myfile:
        #     dict_writer = csv.DictWriter(myfile, keys)
        #     dict_writer.writeheader()
        #     dict_writer.writerows(list_startups)