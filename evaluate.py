from Algorithms.search import searchInit
from evaluation.getQueryResults import getResults

# algorithms are named BM25F, Frequency, TF_IDF
def makeParams(connector, query, algo, PageRank=False):
    if PageRank:
        configArr = [ None, algo, 'PageRank', connector ]
    else:
        configArr = [ None, algo, connector ]
    return configArr + query.split(' ')

def printList(ls):
    if ls is not None:
        for x in ls:
            print x

queries = [ 'undergraduate syllabus', '2017 PhDs', 'COMPM052', 'information retrieval', '4th year modules', 'master programmes', 'software engineering' ]

results = {}
for query in queries:
    csResults = map(lambda x: x['citeUrl'], getResults(query))
    bm25F = searchInit(makeParams(connector='AND', query=query, algo='BM25F'))
    freq = searchInit(makeParams(connector='AND', query=query, algo='Frequency'))
    tfIdf = searchInit(makeParams(connector='AND', query=query, algo='TF_IDF'))
    bm25FPageRank = searchInit(makeParams(connector='AND', query=query, algo='BM25F', PageRank=True))
    freqPageRank = searchInit(makeParams(connector='AND', query=query, algo='Frequency', PageRank=True))
    tfIdfPageRank = searchInit(makeParams(connector='AND', query=query, algo='TF_IDF', PageRank=True))

    print "====================="
    print "Query: " + query
    print "---------------------"
    
    # print "BM25F"
    # printList(bm25F)
    # print "---------------------"
    
    print "BM25F PageRank"
    printList(bm25FPageRank)
    print "---------------------"
    
    # print "Frequency"
    # printList(freq)
    # print "---------------------"
    
    print "Frequency PageRank"
    printList(freqPageRank)
    print "---------------------"
    
    # print "TF_IDF"
    # printList(tfIdf)
    # print "---------------------"
    
    print "TF_IDF PageRank"
    printList(tfIdfPageRank)
    # print "---------------------"

    # print "CS Search"
    # printList(csResults)

    print "====================="
