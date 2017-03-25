from whoosh import scoring
from whoosh.qparser import QueryParser
from whoosh.index import create_in
from whoosh.fields import *
import sqlite3, os

def searchTerm(list):
	connector = list[2]
	term = ''

	for i in range (3, len(list) - 1):
		term += list[i] + ' ' + connector + ' '

	term += list[-1]

	return term

def database():
	conn = sqlite3.connect('urls.db')
	c = conn.cursor()

	c.execute("SELECT * FROM urls")

	return c.fetchall()

def index(data):
	schema = Schema(title = TEXT(stored = True), content = TEXT)
	ix = create_in("indexdir", schema)
	writer = ix.writer()

	for i in range(0, len(data)):
		writer.add_document(title=data[i][0], content=data[i][1])

	writer.commit()

	return ix

def search(ix, term):
	bm25f = {}
	print "BM25F"
	with ix.searcher() as searcher:
		query = QueryParser('content', ix.schema).parse(term)
		results = searcher.search(query, limit = 100)
		index = 1

		for r in results:
			print r['title']
			bm25f[r['title']] = index
			index += 1

	freq = {}
	print "\nFrequency"
	with ix.searcher(weighting = scoring.Frequency()) as searcher:
		query = QueryParser('content', ix.schema).parse(term)
		results = searcher.search(query, limit = 100)
		index = 1

		for r in results:
			print r['title']
			freq[r['title']] = index
			index += 1

	tf_idf = {}
	print "\nTF_IDF"
	with ix.searcher(weighting = scoring.TF_IDF()) as searcher:
	    query = QueryParser('content', ix.schema).parse(term)
	    results = searcher.search(query, limit = 100)
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
	if sys.argv[1] == 'OR' or sys.argv[1] == 'AND':
		search(index(database()), searchTerm(sys.argv))
		return
	print 'Incorrect Connector'

os.system('clear')

if len(sys.argv) < 3:
	print 'Insufficient Arguments'
else:
	searchInit(sys.argv)