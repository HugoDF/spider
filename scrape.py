import scrapy
import sqlite3
conn = sqlite3.connect('urls.db')

from w3lib.html import remove_tags, remove_tags_with_content

c = conn.cursor()
c.execute('SELECT * FROM urls')
url = c.fetchone()

class UclSpider(scrapy.Spider):
    name = 'Ucl Spider'
    start_urls = [ 'https://ucl.ac.uk' ]

    def parse(self, response):
        for html in response.css('body'):
            content = html.extract()

        text = remove_tags(remove_tags_with_content(content, ('script', )))

        print text
        
        c.execute('INSERT INTO urls (url, content) VALUES (?, ?)', [ response.url, text ])
        conn.commit()
        
        next_page = response.css('a ::attr(href)').extract()
        for page in next_page:
            if "ucl.ac.uk" in page:
                c.execute('SELECT COUNT(*) FROM urls WHERE url = ?', [ page ])
                urlCount = c.fetchone()
                if urlCount != 0:
                    yield scrapy.Request(response.urljoin(page), callback=self.parse)