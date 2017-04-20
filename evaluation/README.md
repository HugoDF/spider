# Evaluation

The evaluation module is run from `evaluate.py` (which is in the root of the project).

There are two metrics to evaluate relevance of results:
- precision: fraction of retrieved instances that are relevant
- recall: fraction of relevant instances that are retrieved

Relevant paper for definitions: [http://www.webology.org/2005/v2n2/a12.html](http://www.webology.org/2005/v2n2/a12.html)

## Method

[Search Engines for the World Wide Web: A Comparative Study and Evaluation Methodology](https://www.learntechlib.org/p/83947)

see also [https://www.las.org.sg/sjlim/SJLIM20094Sampath.pdf](https://www.las.org.sg/sjlim/SJLIM20094Sampath.pdf)

and [https://arxiv.org/pdf/1302.2318.pdf](https://arxiv.org/pdf/1302.2318.pdf) "Slightly better correlation between precision and user satisfaction was shown by Kelly, Fu and Shah (2007)" [Kelly, D., X. Fu and C. Shah (2007). Effects of Rank and Precision of Search Results on Users'
Evaluations of System Performance, University of North Carolina.]

### Queries

We created X queries to mimic things people coming the UCL CS website may be looking for.

> Insert queries

The queries are then run against our algorithms (BM25F, Frequency, TF_IDF) both with and without PageRank enabled to see how they perform.

### Manual Relevance rating of query results

Assign it manually according to stuff found in [http://www.aitel.hist.no/~mildrid/dring/paper/SIGIR.html](http://www.aitel.hist.no/~mildrid/dring/paper/SIGIR.html).

Relevance rating: 
- 1: information is found on the page
- 0.5: the page has a link to a page where the information can be found
- 0: neither the information or a link to it is present on the page.


We then run through Normalized Discounted Cumulative Gain [http://www.ebaytechblog.com/2010/11/10/measuring-search-relevance/](http://www.ebaytechblog.com/2010/11/10/measuring-search-relevance/)

Rough working implementations of different rank/relevance metrics: [https://gist.github.com/bwhite/3726239](https://gist.github.com/bwhite/3726239).

### Further work

- we could write more queries to test
- we could measure recall (this would require manually tagging a large set of documents): recall: fraction of relevant instances that are retrieved vs precision: fraction of retrieved instances that are relevant
- if we had users we could use click and query logs to improve performance
- removal of "/mobile" urls, cons: some pages for mobile/desktop have difference content
- deduplication of URLs that are the same different case eg. "http://www0.cs.ucl.ac.uk/staff/y.jia/publications.html" and "http://www0.cs.ucl.ac.uk/staff/Y.Jia/publications.html", cons: see removal of "/mobile" links
- to create an automatic relevance rating system we could use the CS Search as an oracle for relevance. IE if a result for a query is returned by the CS Search, then it is relevant. This is a binary relevance measure, as opposed to our manual approach.
