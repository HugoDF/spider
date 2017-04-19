from whoosh import scoring
from whoosh.qparser import QueryParser
from whoosh.fields import *
from whoosh.index import open_dir
import os

def searchTerm(list):
	connector = list[2]
	term = ''

	for i in range (3, len(list) - 1):
		term += list[i] + ' ' + connector + ' '

	term += list[-1]

	print term

	return term

def index():
	print "Opening Index"
	ix = open_dir("indexdir")

	return ix

def search(ix, term):
	bm25f = {}
	print "BM25F"
	with ix.searcher() as searcher:
		query = QueryParser('content', ix.schema).parse(term)
		results = searcher.search(query, limit = 25)
		index = 1

		for r in results:
			print r['title']
			bm25f[r['title']] = index
			index += 1

	freq = {}
	print "\nFrequency"
	with ix.searcher(weighting = scoring.Frequency()) as searcher:
		query = QueryParser('content', ix.schema).parse(term)
		results = searcher.search(query, limit = 25)
		index = 1

		for r in results:
			print r['title']
			freq[r['title']] = index
			index += 1

	tf_idf = {}
	print "\nTF_IDF"
	with ix.searcher(weighting = scoring.TF_IDF()) as searcher:
	    query = QueryParser('content', ix.schema).parse(term)
	    results = searcher.search(query, limit = 25)
	    index = 1

	    for r in results:
	    	print r['title']
	    	tf_idf[r['title']] = index
	    	index += 1

	print '\nBM25F vs Frequency'
	difference = 0
	for page in bm25f:
		if page in freq:
			difference += abs(bm25f[page] - freq[page])
	print difference

	print '\nBM25F vs TF_IDF'
	difference = 0
	for page in bm25f:
		if page in tf_idf:
			difference += abs(bm25f[page] - tf_idf[page])
	print difference

	print '\nTF_IDF vs Frequency'
	difference = 0
	for page in tf_idf:
		if page in freq:
			difference += abs(tf_idf[page] - freq[page])
	print difference

def searchInit(list):
	if list[1] == 'OR' or list[1] == 'AND':
		print "Query Collected"
		search(index(database()), searchTerm(list))
		return
	print 'Incorrect Connector'

if __name__ == '__main__':
	os.system('clear')

	if len(sys.argv) < 3:
		print 'Insufficient Arguments'
	else:
		searchInit(sys.argv)
