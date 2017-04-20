# COMPM052 Spider Scrapy

# Setup

Need sqlite3, python 2.7 and pip

Run `sqlite3 urls.db`, run this query to create the urls table:
```sql
CREATE TABLE urls (url STRING, content TEXT, links STRING, pageRank REAL, amount INTEGER);
CREATE INDEX contentIndex ON urls (content);
CREATE TABLE incomingLinks (urlId INTEGER, incomingLinks STRING);
CREATE INDEX incomingLinksUrlId on incomingLinks (urlId);
```

Run `pip install scrapy`.

To start the spider:
`scrapy runspider scrape.py`

To enable PageRank:
    Generate incoming links for the database: `python makeIncomingLinks.py`
    Run the algorithm: `python pageRank.py`