from whoosh import scoring
from whoosh.qparser import QueryParser
from whoosh.index import create_in
from whoosh.fields import *
import sqlite3, os, sys

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
	schema = Schema(title=TEXT(stored=True), content=TEXT)
	ix = create_in("indexdir", schema)
	writer = ix.writer()

	for i in range(0, len(data)):
		writer.add_document(title=data[i][0], content=data[i][1])

	writer.commit()

	return ix

def search(ix, term, algorithm):
	if algorithm == 'BM25F':
		with ix.searcher() as searcher:
			query = QueryParser('content', ix.schema).parse(term)
			results = searcher.search(query, limit=100)

			for r in results:
				print r['title']
		return

	if algorithm == 'Frequency':
		with ix.searcher(weighting = scoring.Frequency()) as searcher:
			query = QueryParser('content', ix.schema).parse(term)
			results = searcher.search(query, limit=100)

			for r in results:
				print r['title']
		return

	if algorithm == 'Frequency':
		with ix.searcher(weighting = scoring.TF_IDF()) as searcher:
		    query = QueryParser('content', ix.schema).parse(term)
		    results = searcher.search(query, limit=100)

		    for r in results:
		    	print r['title']
		return

	print 'Incorrect Alogrithm'

def searchInit(list):
	algorithm = sys.argv[1]
	if sys.argv[2] == 'OR' or sys.argv[2] == 'AND':
		search(index(database()), searchTerm(sys.argv), algorithm)
		return
	print 'Incorrect Connector'

os.system('clear')

if len(sys.argv) < 4:
	print 'Insufficient Arguments'
else:
	searchInit(sys.argv)