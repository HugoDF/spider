from Algorithms.search import searchInit
from evaluation.getQueryResults import getResults

# algorithms are named BM25F, Frequency, TF_IDF
def makeParams(connector, query, algo):
    return [ None, algo, connector ] + query.split(' ')

def printList(ls):
    for x in ls:
        print x

# queries = [ 'undergraduate syllabus', '2017 PhDs', 'COMPM052', 'information retrieval', '4th year modules', 'master programmes', 'software engineering' ]
queries = []
results = {}
for query in queries:
    csResults = map(lambda x: x['citeUrl'], getResults(query))
    bm25F = searchInit(makeParams(connector='AND', query=query, algo='BM25F'))
    freq = searchInit(makeParams(connector='AND', query=query, algo='Frequency'))
    tfIdf = searchInit(makeParams(connector='AND', query=query, algo='TF_IDF'))

    print "====================="
    print "Query: " + query
    print "---------------------"
    
    print "BM25F"
    printList(bm25F)
    print "---------------------"
    
    print "Frequency"
    printList(freq)
    print "---------------------"
    
    print "TF_IDF"
    printList(tfIdf)
    print "---------------------"

    print "CS Search"
    printList(csResults)

    print "====================="
