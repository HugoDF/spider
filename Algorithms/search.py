from whoosh import scoring
from whoosh.qparser import QueryParser
from whoosh.index import create_in
from whoosh.fields import *
import sqlite3, os, sys

def searchTerm(list,position):
	connector = list[position]
	term = ''

	for i in range (position+1, len(list) - 1):
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

def search(ix, term, algorithm, pageRank=False):
	if algorithm == 'BM25F':
		with ix.searcher() as searcher:
			query = QueryParser('content', ix.schema).parse(term)
			results = searcher.search(query, limit=100)

			showResult(results,pageRank)
		return

	if algorithm == 'Frequency':
		with ix.searcher(weighting = scoring.Frequency()) as searcher:
			query = QueryParser('content', ix.schema).parse(term)
			results = searcher.search(query, limit=100)

			for r in results:
				print (r['title'])
		return

	if algorithm == 'Frequency':
		with ix.searcher(weighting = scoring.TF_IDF()) as searcher:
		    query = QueryParser('content', ix.schema).parse(term)
		    results = searcher.search(query, limit=100)

		    for r in results:
		    	print (r['title'])
		return

	print ('Incorrect Alogrithm')

def showResult(results,pageRank):
	if pageRank == False:
    		for r in results:
    				print (r['title'])
	else:
			lists = ""
			for r in results:
    				lists = lists + " " + r['title']
			
			lists = lists.split()
			conn = sqlite3.connect('urls.db')
			c = conn.cursor()
			query = "SELECT url from urls WHERE url IN ({seq}) ORDER BY pageRank DESC".format(seq=','.join(['?']*len(lists)))
			c.execute(query,lists)
			orders = c.fetchall()
			for order in orders:
					print(order[0])

def searchInit(list):
	algorithm = sys.argv[1]
	if (sys.argv[2] == 'PageRank') and (sys.argv[3] == 'OR' or sys.argv[3] == 'AND'):
    				search(index(database()), searchTerm(sys.argv,3), algorithm, True)
	elif sys.argv[2] == 'OR' or sys.argv[2] == 'AND':
    		search(index(database()), searchTerm(sys.argv,2), algorithm, False)
	else:
    		print ('Incorrect Connector')

os.system('clear')


if len(sys.argv) < 4:
	print ('Insufficient Arguments')
else:
	searchInit(sys.argv)