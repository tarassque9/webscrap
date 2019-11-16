import scrapy
import json
import csv


class StartupsSpider(scrapy.Spider):
    name = "startups"
    start_urls = ['https://e27.co/api/startups/?tab_name=recentlyupdated']
    

    def parse(self, response):
        request_body = '&length=5' # here must be variable: totalstartupcount from json file but i don't know how do it right, and i get random number
        url = response.url + request_body
        yield scrapy.Request(url=url, body=request_body, callback=self.get_page)

       
    def get_page(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        list_startups = []
        for el in jsonresponse['data']['list']:
            company_name = el['name']
            profile_url = 'https://e27.co/%s/' % el['slug']
            company_website_url = el['metas']['website']
            location = el['location'][0]['text']
            tags = el['market']
            totalstartupcount = jsonresponse['data']['totalstartupcount']
            short_description = el['metas']['short_description']
            information = {'company_name': company_name, 'profile_url': profile_url, 
                    'company_web_site_url': company_website_url, 
                    'location': location, 'tags': tags, 'short_description': short_description}
            list_startups.append(information)
        
        
        #return list_startups
        

    # def write_to_csv(self, list_startups):
    #     keys = list_startups[0].keys()
    #     with open('info.csv', 'wb') as csvfile:
    #         dict_writer = csv.DictWriter(csvfile, keys)
    #         dict_writer.writeheader()
    #         dict_writer.writerows(list_startups)