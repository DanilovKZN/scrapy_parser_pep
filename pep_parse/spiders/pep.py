from urllib.parse import urljoin

import scrapy

from pep_parse.items import PepParseItem


TABLE_WITH_NUMERICAL_PEP = 'section#numerical-index'
PEP_CONTENT_IN_NUMERICAL_PEP = 'section#pep-content'

BASE_URL = 'http://peps.python.org'

PEP_STATUS = [
    'Active',
    'Accepted',
    'Deferred',
    'Final',
    'Provisional',
    'Rejected',
    'Superseded',
    'Withdrawn',
    'Draft',
]


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        numerical_index_table = response.css(TABLE_WITH_NUMERICAL_PEP)
        tbody = numerical_index_table.css('tbody')
        all_peps = tbody.css('a::attr(href)').getall()

        for pep in all_peps:
            pep_url = urljoin(BASE_URL, pep)
            yield response.follow(pep_url, callback=self.parse_pep)

    def parse_pep(self, responce):
        pep_content = responce.css(PEP_CONTENT_IN_NUMERICAL_PEP)
        name_pip_list = pep_content.css('h1::text').get().strip().split()
        dl_tags = responce.css('dl')
        dt_text = dl_tags.css('dt::text').getall()
        dd_text = dl_tags.css('dd::text').getall()
        return_status = ''
        for status in PEP_STATUS:
            if status in dt_text or status in dd_text:
                return_status = status
                break
        date_to_output = {
            'number': name_pip_list[1],
            'name': ' '.join(map(str, name_pip_list[3:])),
            'status': return_status
        }
        yield PepParseItem(date_to_output)
