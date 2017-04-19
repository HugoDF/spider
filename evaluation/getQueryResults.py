from bs4 import BeautifulSoup
import urllib2
import json

def getResultsContainer(soup):
    ols = soup.find_all('ol')
    for ol in ols:
        if ol['id'] == 'fb-results':
            return ol

def transformRawResults(rawResults):
    results = []
    for rawResult in rawResults:
        result = {}
        result['heading'] = rawResult.find('h3').a.text.strip()
        result['summary'] = rawResult.find('p').text.strip()
        result['citeUrl'] = rawResult.find('cite').a.text.strip()
        results.append(result)
    return results

def getResults(query):
    print "Running query: " + query
    url = "http://search2.ucl.ac.uk/s/search.html?Submit=&collection=ucl-public-meta&subsite=cs&query=" + '+'.join(query.split(' '))
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    resultsContainer = getResultsContainer(soup)
    
    rawResults = resultsContainer.find_all('li')
    results = transformRawResults(rawResults)
    return results

queries = [ 'undergraduate curriculum', '2017 PhDs', 'COMPM052', 'information retrieval', '4th year modules', 'master programmes' ]
queryToResults = {}
for query in queries:
    results = getResults(query)
    queryToResults[query] = results

with open('./queryresults/queriesToResults.json', 'w') as outfile:
    json.dump(queryToResults, outfile)