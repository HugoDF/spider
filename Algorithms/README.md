# Running

## Requires Scraper

Install scraper dependencies and run.

## Installation

`pip install whoosh`

Create dir `indexdir`

## Running

For one Algorithm `python search.py ALG (PageRank) CON TERMS`

ALG = BM25F || TF_IDF || Frequency
CON = OR || AND

For all Algorithms `python searchCompare.py CON TERMS`

ALG = BM25F, Frequency, TF_IDF

PagaRank = Optional, default as False. If 'PageRank' is included, results would be return based on the ranking of the pages in descending order.

CON = OR, AND

TERMS = *anything*
