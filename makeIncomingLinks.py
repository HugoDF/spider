import scrapy, sqlite3, re, sys
conn = sqlite3.connect('urls.db')

c = conn.cursor()
query = c.execute("SELECT url FROM urls")
urls = query.fetchall()
print "Got " + str(len(urls)) + " urls"
for url in map(lambda x: x[0], urls):
    q = c.execute("SELECT url FROM urls WHERE links LIKE '%" + url + "%'")
    incomingLinks = map(lambda x: x[0], q.fetchall())
    incomingLinksString = " ".join(incomingLinks)
    c.execute("INSERT INTO urls (incomingLinks) VALUES (?)", [ incomingLinksString ])
    conn.commit()