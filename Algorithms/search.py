from whoosh import scoring
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from whoosh.fields import *
import os, sys

def searchTerm(list):
	connector = list[2]
	term = ''

	for i in range (3, len(list) - 1):
		term += list[i] + ' ' + connector + ' '

	term += list[-1]

	return term

def index():
	print "Index Opening"
	ix = open_dir("indexdir")

	return ix

def search(ix, term, algorithm):
	if algorithm == 'BM25F':
		print "BM25F Search"
		with ix.searcher() as searcher:
			query = QueryParser('content', ix.schema).parse(term)
			results = searcher.search(query, limit=25)

			for r in results:
				print r['title']
			
			return map(lambda r: r['title'], results)

	if algorithm == 'Frequency':
		print "Frequency Search"
		with ix.searcher(weighting = scoring.Frequency()) as searcher:
			query = QueryParser('content', ix.schema).parse(term)
			results = searcher.search(query, limit=25)

			for r in results:
				print r['title']

			
			return map(lambda r: r['title'], results)

	if algorithm == 'TF_IDF':
		print "TF_IDF Search"
		with ix.searcher(weighting = scoring.TF_IDF()) as searcher:
		    query = QueryParser('content', ix.schema).parse(term)
		    results = searcher.search(query, limit=25)

		    for r in results:
		    	print r['title']
			
			return map(lambda r: r['title'], results)

	print 'Incorrect Alogrithm'

def searchInit(list):
	algorithm = list[1]
	if list[2] == 'OR' or list[2] == 'AND':
		print "Query Collected"
		return search(index(), searchTerm(list), algorithm)
	print 'Incorrect Connector'

if __name__ == '__main__':
	os.system('clear')

	if len(sys.argv) < 4:
		print 'Insufficient Arguments'
	else:
		print "Starting Query"
		searchInit(sys.argv)