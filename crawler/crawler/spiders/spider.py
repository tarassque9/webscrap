import scrapy
import json
import csv


class StartupsSpider(scrapy.Spider):
    name = "startups"
    start_urls = ['https://e27.co/api/startups/?tab_name=recentlyupdated']


    def parse(self, response):
        request_body = '&length=30000' 
        url = response.url + request_body
        yield scrapy.Request(url=url, body=request_body, callback=self.get_url)


    def get_url(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        for el in jsonresponse['data']['list']:
            profile_url = 'https://e27.co/{}'.format(el['slug'])
            with open('urls.csv', 'a+') as csvfile:
                if [profile_url] not in csvfile:
                    spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow([profile_url])
