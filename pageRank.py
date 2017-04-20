import sqlite3
import numpy
conn = sqlite3.connect('urls.db')
c = conn.cursor()

class graph:
  def __init__(self,n):
    self.size = n
    self.in_links = {}
    self.num_out_links = {}
    self.dead_end = {}

    for j in range(n):
      self.in_links[j] = []
      self.num_out_links[j] = 0
      self.dead_end[j] = True

def updateRanking(graph,r,d = 0.85):
  # graph - graph representing relation between pages
  # r - PageRank
  # d - damping factor

  # Compute the ranking of each page in the graph
  total_pages = graph.size
  v = numpy.matrix(numpy.zeros((total_pages,1)))
  inner_product = sum([r[i] for i in graph.dead_end.keys()])
  for j in range(total_pages):
    a = sum([r[k]/graph.num_out_links[k] for k in graph.in_links[j]])
    v[j] = d*(a+inner_product/total_pages)+(1-d)/total_pages

  return v/numpy.sum(v)

def pagerank(graph, d = 0.85, max_error = 0.00001):
  # graph - graph representing relation between pages
  # d - damping factor
  # max_error - Stop when difference between each iteration less than this value
  
  n = graph.size
  ranking = numpy.matrix(numpy.ones((n,1)))/n
  iteration = 0
  dist = 1
  while dist > max_error:
    iteration += 1
    print ("Iteration: %s" % iteration)
    new_ranking = updateRanking(graph,ranking,d)
    dist = numpy.sum(numpy.abs(ranking-new_ranking))
    print ("Difference: %s" % dist)
    ranking = new_ranking
  return ranking

def graphFromDB():
    # Construct a graph representing the relation between pages in database
    
    c.execute('SELECT COUNT(*) FROM incomingLinks')
    total_pages = c.fetchall()[0][0]

    graphDB = graph(total_pages)

    # Get incoming links of each page
    c.execute('SELECT * FROM incomingLinks')
    datas = c.fetchall()

    count = 0;
    for data in datas:
      count += 1;
      print ("Processing: %s/%s" %(count,total_pages))

      # Database first position is 1, graph first position is 0
      # Shift by -1
      position = data[0] - 1
      if isinstance(data[1],int):
            in_links = [data[1] - 1]
      else:
            in_links = map(int, data[1].split())
            in_links = [x - 1 for x in in_links]

      graphDB.in_links[position] = in_links

      for in_link in in_links:
            if graphDB.num_out_links[in_link] == 0:
                  graphDB.dead_end.pop(in_link)
            
            graphDB.num_out_links[in_link] += 1

    return graphDB

def insertDB(ranking):
      total_pages = len(ranking)
      count = 0

      for i in range(0,total_pages):
            count += 1
            print('Inserting: %s/%s' %(count,total_pages))
            c.execute('UPDATE urls SET pageRank = ? WHERE rowid = ?', [ ranking[i,0], i+1 ])
            conn.commit()

print('Constructing graph...')
graphDB = graphFromDB()
print('Calculating ranking...')
ranking = pagerank(graphDB)
print('Inserting into database...')
insertDB(ranking)
print('Done!')