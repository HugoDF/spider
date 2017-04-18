import scrapy, sqlite3, re, sys
conn = sqlite3.connect('urls.db')

c = conn.cursor()
query = c.execute("SELECT rowid, url FROM urls")
urls = query.fetchall()
print "Got " + str(len(urls)) + " urls"
for url in urls:
    if url[1] is not None:
        q = c.execute("SELECT url FROM urls WHERE links LIKE '%" + url[1] + "%'")
        incomingLinks = map(lambda x: x[0], q.fetchall())
        incomingLinksString = " ".join(incomingLinks)
        c.execute("INSERT INTO incomingLinks (urlId, incomingLinks) VALUES (?, ?)", [ url[0], incomingLinksString ])
        conn.commit()