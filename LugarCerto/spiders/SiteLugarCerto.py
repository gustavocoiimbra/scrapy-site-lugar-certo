from scrapy import Spider
from scrapy import Request
import re


class SiteLugarcertoSpider(Spider):
    name = 'SiteLugarCerto'
    allowed_domains = ['www.lugarcerto.com.br']
    start_urls = ['https://www.lugarcerto.com.br/busca/compra-e-venda/go/apartamento-e-casa']

    def parse(self, response, **kwargs):

        links = response.xpath('/html/body/div/div[5]/section[3]/section/div/a[2]/@href').getall()

        for link in links:
            yield Request(
                url=response.urljoin(link),
                callback=self.extract_data
            )

        number_page = response.xpath('/html/body/div/div[5]/section[3]/section/div[23]/ul/li[2]/input[1]/@value').get()
        number_page = int(number_page)
        next_page = response.xpath('/html/body/div/div[5]/section[3]/section/div[23]/ul/li[3]/a/@href').get()

        if number_page <= 600:
            yield Request(
                url=response.urljoin(next_page),
                callback=self.parse
            )
        else:
            pass

    def extract_data(self, response):

        title = response.css(
            'div [class="col-sxs-12 col-xs-12 margin-bottom-15"] h1::text ').get()
        adress = response.css(
            'div [class="col-sxs-12 col-xs-12 margin-bottom-15"] span::text ').get()
        price = response.css(
            'li.text-gray-dark::text').get()
        advertiser = response.xpath(
            '//*[@id="js-contate-o-anunciante"]/div/div/div/div/div[1]/div/div/p/span/a/@title').get()
        details = response.css(
            'span[class="item-descricao text-bold clearfix"]::text').getall()
        items = response.css(
            'span[class="item-descricao-conteudo margin-right-5"]::text').getall()
        area = [items[i] for i, x in enumerate(details)if re.search('ÁREA', x)]

        yield {
            "Título": title,
            "Endereço": adress,
            "Preço": price,
            "Anunciante": advertiser,
            "Aréa": area
        }
