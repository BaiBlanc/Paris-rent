
import re
import scrapy

from spider_demo.items import SpiderDemoItem

class SelogerSpider(scrapy.Spider):

    name = 'seloger'

    # Urls needed for the first round
    start_urls = ['https://www.seloger.com/list_beta.htm?projects=1&types=2%2C1'
                  '&natures=1&places=%5B%7Bci%3A750056%7D%5D&price=NaN%2F1400&qsVersion=1.0&LISTING-LISTpg=1']
    current_page = 1
    has_page = True

    def parse(self, response):
        '''
        :param response: The page of the site
        :return: generator of items
        '''
        if not response:
            self.has_page = False
        node_list = response.xpath('//div[@class="Card__ContentZone-sc-7insep-3 ihomVp"]')
        for node in node_list:
            item = SpiderDemoItem()
            # extract() will change xpath Objects to unicode strings
            # normalize-space() remove all the useless space and \n
            price = node.xpath('normalize-space(.//div[@class="Price__Label-sc-1g9fitq-1 jGOFou"]/text())').extract()

            code_post = node.xpath('.//div[@class="Card__LabelGap-sc-7insep-5 jyylUg"]/text()').extract()
            info = node.xpath('.//ul[@class="ContentZone__Tags-wghbmy-6 cjYXjZ"]/li/text()').extract()

            # Some reconstrustions and stocking into the fields of items
            price_match = re.match(r'\d+', re.sub(r'\s*', '', price[0]))
            item['price'] = int(price_match.group())
            code_post_match = re.search(r'\d+', code_post[1])
            item['code_post'] = int(code_post_match.group())+75000
            size, type= self.typeSizeControl(info)
            item['type'] = type
            # extract 54.3 from '54,3 m2' the size of the appartement
            size_match = re.match(r'\d*(\.\d+)?', re.sub(",", ".", size))
            item['size'] = float(size_match.group())
            # The generator of the items
            yield item
        current_page = int(re.search(r'LISTpg=(\d+)', self.start_urls[0]).group(1))
        if self.has_page:
            self.current_page+=1
            next_page = self.current_page
            next_url = 'https://www.seloger.com/list_beta.htm?projects=1&types=2%2C1'+\
                       '&natures=1&places=%5B%7Bci%3A750056%7D%5D&price=NaN%2F1400&qsVersion=1.0&LISTING-LISTpg='+str(next_page)
            yield scrapy.Request(
                next_url,
                callback = self.parse,
                dont_filter = True
            )

    def typeSizeControl(self, info:[]):
        '''
        Destructure the array of info and obtain the value of size and type
        :param info: Info contains the number of rooms, potentially the number of living-room, the area and dispose an elevator
        :return: (size, type): the area of the appartement, and the type(Studio, F1~F4)
        '''
        # extract 2 from '2 p' the number of the rooms
        nb_piece = int(re.match(r'\d+',info[0]).group())
        nb_chambre = 0
        size = 0
        if len(info)>1:
            if re.search(r'(.+)\sch',info[1]):
                nb_chambre = int(re.search(r'(.+)\sch',info[1]).group(1))
                if len(info)>2:
                    size = info[2]
                else:
                    size = "0,0"
            else:
                nb_chambre = 0
                size = info[1]
        else:
            nb_chambre = 0
            size = "0,0"

        if (nb_piece == 1) & (nb_chambre == 0):
            type = 'Studio'
        elif (nb_piece == 1) & (nb_chambre == 1):
            type = 'Appartement F2'
        elif (nb_piece == 2) & (nb_chambre == 1):
            type = 'Appartement F3'
        else:
            type = 'Appartement F4'
        return (size,type)

