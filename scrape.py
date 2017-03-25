import scrapy
import sqlite3
import re
conn = sqlite3.connect('urls.db')

from w3lib.html import remove_tags, remove_tags_with_content, replace_escape_chars

c = conn.cursor()
c.execute('DELETE FROM urls')
conn.commit()

class UclSpider(scrapy.Spider):
	name = 'Ucl Spider'
	start_urls = [ 'https://www.ucl.ac.uk' ]

	def parse(self, response):
		for html in response.css('body'):
			content = html.extract()

		text = replace_escape_chars(remove_tags(remove_tags_with_content(content, ('script', ))))
		text = text.replace(u'\xa0', u' ')
		text = text.replace(u'\xa9', u' ')
		text = text.replace(u'\\u"\d+"', u' ')
		
		if "ucl.ac.uk" in response.url:
			c.execute('INSERT INTO urls (url, content) VALUES (?, ?)', [ response.url, text.lower() ])
		 	conn.commit()
			print response.url

		next_page = response.css('a ::attr(href)').extract()
		for page in next_page:
			if "ucl.ac.uk" in page:
				c.execute('SELECT COUNT(*) FROM urls WHERE url = ?', [ page ])
				urlCount = c.fetchone()
	     		if urlCount != 0:
	     			yield scrapy.Request(response.urljoin(page), callback=self.parse)