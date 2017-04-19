import scrapy, sqlite3, re, sys
conn = sqlite3.connect('urls.db')

c = conn.cursor()
query = c.execute("SELECT rowid, url FROM urls")
urls = query.fetchall()
urlCount = len(urls)
print "Got " + str(urlCount) + " urls"
for idx, url in enumerate(urls):
    if (idx + 1) % 50 == 0:
        print str(idx + 1) + " / " + str(urlCount)
    if url[1] is not None:
        q = c.execute("SELECT rowid FROM urls WHERE links LIKE ?", ('%' + url[1] + '%',))
        incomingLinks = map(lambda x: str(x[0]), q.fetchall())
        incomingLinksString = " ".join(incomingLinks)
        c.execute("INSERT INTO incomingLinks (urlId, incomingLinks) VALUES (?, ?)", [ url[0], incomingLinksString ])
        conn.commit()