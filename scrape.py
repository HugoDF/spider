import scrapy, sqlite3, re, sys
conn = sqlite3.connect('urls.db')

from w3lib.html import remove_tags, remove_tags_with_content, replace_escape_chars
from bs4 import BeautifulSoup

c = conn.cursor()
c.execute('DELETE FROM urls')
conn.commit()

class UclSpider(scrapy.Spider):
	name = 'Ucl Spider'
	start_urls = [ 'http://www.cs.ucl.ac.uk/home/' ]

	def parse(self, response):
		for html in response.css('body'):
			content = html.extract()
			soup = BeautifulSoup(content, "lxml")

		text = replace_escape_chars(remove_tags(remove_tags_with_content(content, ('script', ))))
		text = text.replace(u'\xa0', u' ')
		text = text.replace(u'\xa9', u' ')
		text = text.replace(u'\\u"\d+"', u' ')

		links = ""
		for link in soup.find_all('a'):
    			link_url = link.get('href')
    			if "cs.ucl.ac.uk" in link_url:
    					links = links + " " + link_url
		
		if "cs.ucl.ac.uk" in response.url:
			c.execute('INSERT INTO urls (url, content, links) VALUES (?, ?, ?)', [ response.url, text.lower(), links ])
			conn.commit()
			print (response.url)

		next_page = response.css('a ::attr(href)').extract()
		for page in next_page:
			if "metalib" in page:
				continue
			if "digital-collections" in page:
				continue
			if "cs.ucl.ac.uk" in page:
				c.execute('SELECT COUNT(*) FROM urls WHERE url = ?', [ page ])
				urlCount = c.fetchone()
				if urlCount != 0:
					yield scrapy.Request(response.urljoin(page), callback=self.parse)