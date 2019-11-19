import scrapy
import json
import csv


class StartupsSpider(scrapy.Spider):
    name = "startups"
    start_urls = ['https://e27.co/api/startups/?tab_name=recentlyupdated']
    

    def parse(self, response):
        request_body = '&length=20' # here must be variable: totalstartupcount from json file but i don't know how do it right, and i get random number
        url = response.url + request_body
        yield scrapy.Request(url=url, body=request_body, callback=self.get_page)

       
    def get_page(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        list_urls = []
        for el in jsonresponse['data']['list']:
            profile_url = 'https://e27.co/%s' % el['slug'] 
            list_urls.append(profile_url)
        with open('urls.csv', 'w') as myfile:
            write = csv.writer(myfile)
            for item in list_urls:
                write.writerow([item])
        