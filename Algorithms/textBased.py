import sqlite3, sys, operator, os

os.system('reset')

conn = sqlite3.connect('urls.db')
c = conn.cursor()

def search(c, terms):
	fileList = {}
	for a in range(0, len(terms)):
		searchTerm = terms[a]
		c.execute("SELECT url, count FROM " + searchTerm)
		results = c.fetchall()
		for b in range(0, len(results)):
			url = results[b][0]
		 	matches = results[b][1]
		 	if url in fileList:
		 		fileList[url] += matches
		 	else:
		 		fileList[url] = matches

	returnList = sorted(fileList.items(), key=operator.itemgetter(1), reverse=True)
	return returnList

terms = []

for i in range (1, len(sys.argv)):
	terms.append(sys.argv[i])

if terms == []:
	print 'No Arguments Applied'
else:
	print search(c, terms)