from whoosh import scoring
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from whoosh.fields import *
import os, sys

def searchTerm(list,position):
	connector = list[position]
	term = ''

	for i in range (position+1, len(list) - 1):
		term += list[i] + ' ' + connector + ' '

	term += list[-1]

	return term

def index():
	print ("Index Opening")
	ix = open_dir("indexdir")

	return ix

def search(ix, term, algorithm, pageRank=False):
	if algorithm == 'BM25F':
		print ("BM25F Search")
		with ix.searcher() as searcher:
			query = QueryParser('content', ix.schema).parse(term)
			results = searcher.search(query, limit=1000)

			showResult(results,pageRank,25)
		return

	if algorithm == 'Frequency':
		print ("Frequency Search")
		with ix.searcher(weighting = scoring.Frequency()) as searcher:
			query = QueryParser('content', ix.schema).parse(term)
			results = searcher.search(query, limit=1000)

			showResult(results,pageRank,25)
		return

	if algorithm == 'TF_IDF':
		print ("TF_IDF Search")
		with ix.searcher(weighting = scoring.TF_IDF()) as searcher:
			query = QueryParser('content', ix.schema).parse(term)
			results = searcher.search(query, limit=1000)

			showResult(results,pageRank,25)
		return

	print ('Incorrect Alogrithm')

def searchInit(list):
	algorithm = sys.argv[1]
	if (sys.argv[2] == 'PageRank') and (sys.argv[3] == 'OR' or sys.argv[3] == 'AND'):
					search(index(database()), searchTerm(sys.argv,3), algorithm, True)
	elif sys.argv[2] == 'OR' or sys.argv[2] == 'AND':
			search(index(), searchTerm(sys.argv,2), algorithm, False)
	else:
			print ('Incorrect Connector')

def showResult(results,pageRank,num):
		count = 0;

		if pageRank == False:
				for r in results:
						count += 1;
						print (r['title'])
						if count == num:
								break;
		else:
			lists = ""
			for r in results:
					lists = lists + " " + r['title']
			
			lists = lists.split()
			conn = sqlite3.connect('urls.db')
			c = conn.cursor()

			orders = []
			orders = getPageRank(orders,lists)
			sorted(orders, key=lambda x: x[1])
			for order in orders:
					count += 1;
					print (order[0])
					if count == num:
							break;

def getPageRank(orders,lists):
	if len(links) > 500:
			orders = getPageRank(orders,lists[0:499])
			orders = getPageRank(orders,lists[500:(len(lists)-1)])
	else:
		# Find rowid for each outlink
		query = "SELECT url, pageRank from urls WHERE url IN ({seq}) ORDER BY pageRank DESC".format(seq=','.join(['?']*len(lists)))
		c.execute(query, lists)
		datas = c.fetchall()
		for data in datas:
			orders.append(data)
	
	return orders

os.system('clear')

if len(sys.argv) < 4:
	print ('Insufficient Arguments')
else:
	print ("Starting Query")
	searchInit(sys.argv)