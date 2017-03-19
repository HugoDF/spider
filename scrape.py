import scrapy
import sqlite3
import re
conn = sqlite3.connect('urls.db')

from w3lib.html import remove_tags, remove_tags_with_content, replace_escape_chars

c = conn.cursor()
c.execute('DELETE FROM urls')
#c.execute('SELECT * FROM urls')
#url = c.fetchone()

class UclSpider(scrapy.Spider):
	name = 'Ucl Spider'
	start_urls = [ 'https://ucl.ac.uk' ]

	def parse(self, response):
		for html in response.css('body'):
			content = html.extract()

		text = replace_escape_chars(remove_tags(remove_tags_with_content(content, ('script', ))))
		# text = text.replace("'", r"")
		# text = text.replace(".", r"")
		# text = text.replace(",", r"")
		# text = text.replace(":", r"")
		# text = text.replace("-", r"")
		words = ["ABORT", 
		"ACTION", 
		"ADD", 
		"AFTER", 
		"ALL", 
		"ALTER", 
		"ANALYZE", 
		"AND", 
		"AS", 
		"ASC", 
		"ATTACH", 
		"AUTOINCREMENT", 
		"BEFORE", 
		"BEGIN", 
		"BETWEEN", 
		"BY", 
		"CASCADE", 
		"CASE", 
		"CAST", 
		"CHECK", 
		"COLLATE", 
		"COLUMN", 
		"COMMIT", 
		"CONFLICT", 
		"CONSTRAINT", 
		"CREATE", 
		"CROSS", 
		"CURRENT_DATE", 
		"CURRENT_TIME", 
		"CURRENT_TIMESTAMP", 
		"DATABASE", 
		"DEFAULT", 
		"DEFERRABLE", 
		"DEFERRED", 
		"DELETE", 
		"DESC", 
		"DETACH", 
		"DISTINCT", 
		"DROP", 
		"EACH", 
		"ELSE", 
		"END", 
		"ESCAPE", 
		"EXCEPT", 
		"EXCLUSIVE", 
		"EXISTS", 
		"EXPLAIN", 
		"FAIL", 
		"FOR", 
		"FOREIGN", 
		"FROM", 
		"FULL", 
		"GLOB", 
		"GROUP", 
		"HAVING", 
		"IF", 
		"IGNORE", 
		"IMMEDIATE", 
		"IN", 
		"INDEX", 
		"INDEXED", 
		"INITIALLY", 
		"INNER", 
		"INSERT", 
		"INSTEAD", 
		"INTERSECT", 
		"INTO", 
		"IS", 
		"ISNULL", 
		"JOIN", 
		"KEY", 
		"LEFT", 
		"LIKE", 
		"LIMIT", 
		"MATCH", 
		"NATURAL", 
		"NO", 
		"NOT", 
		"NOTNULL", 
		"NULL", 
		"OF", 
		"OFFSET", 
		"ON", 
		"OR", 
		"ORDER", 
		"OUTER", 
		"PLAN", 
		"PRAGMA", 
		"PRIMARY", 
		"QUERY", 
		"RAISE", 
		"RECURSIVE", 
		"REFERENCES", 
		"REGEXP", 
		"REINDEX", 
		"RELEASE", 
		"RENAME", 
		"REPLACE", 
		"RESTRICT", 
		"RIGHT", 
		"ROLLBACK", 
		"ROW", 
		"SAVEPOINT", 
		"SELECT", 
		"SET", 
		"TABLE", 
		"TEMP", 
		"TEMPORARY", 
		"THEN", 
		"TO", 
		"TRANSACTION", 
		"TRIGGER", 
		"UNION", 
		"UNIQUE", 
		"UPDATE", 
		"USING", 
		"VACUUM", 
		"VALUES", 
		"VIEW", 
		"VIRTUAL", 
		"WHEN", 
		"WHERE", 
		"WITH", 
		"WITHOUT"]
		for word in words:
			text = text.replace(word, r"")
			text = text.replace(word.lower(), r"")
			text = text.replace(word.title(), r"")
		# text = text.replace("and", r"")
		# text = text.replace("on", r"")
		# text = text.replace("to", r"")
		# text = text.replace("in", r"")
		# text = text.replace("is", r"")
		# text = text.replace("when", r"")
		# text = text.replace("from", r"")
		# text = text.replace("All", r"")
		# text = text.replace("Add", r"")
		# text = text.replace("In", r"")
		# text = text.replace("all", r"")
		# text = text.replace("Values", r"")
		# text = text.replace("values", r"")
		text = text.replace(u'\xa0', u' ')
		text = text.replace(u'\xa9', u' ')
		text = text.replace(u'\\u"\d+"', u' ')
		text = re.sub('[^a-zA-Z]+', ' ', text)

		c.execute('INSERT INTO urls (url, content) VALUES (?, ?)', [ response.url, text ])
		conn.commit()

		next_page = response.css('a ::attr(href)').extract()
		for page in next_page:
			if "ucl.ac.uk" in page:
				c.execute('SELECT COUNT(*) FROM urls WHERE url = ?', [ page ])
				urlCount = c.fetchone()
	     		if urlCount != 0:
	     			yield scrapy.Request(response.urljoin(page), callback=self.parse)