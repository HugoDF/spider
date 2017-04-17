import sqlite3
import numpy as np
conn = sqlite3.connect('urls.db')
c = conn.cursor()

def pageRank(graph_matrix, damping_factor = 0.85, max_error = 0.00001):
    M = graph_matrix
    #M = stochasticMatrix(graph_matrix)

    num_pages = len(graph_matrix)
    ranking = np.ones(num_pages)
    constant = np.repeat((1.0 - damping_factor)/num_pages,num_pages)
    initial = damping_factor * M + constant

    old_ranking = np.zeros(num_pages) + 1.0/num_pages
    while True:
        ranking = np.dot(initial,old_ranking)
        dist = distance(ranking, old_ranking)
        print('Difference: ' + str(dist))
        if dist < max_error:
            break
        else:
            old_ranking = ranking

    return ranking

def stochasticMatrix(graph_matrix):
    num_pages = len(graph_matrix)

    # Count number of outlinks for each page
    d = np.zeros(num_pages)
    for i in range(num_pages):
        for j in range(num_pages):
            if (graph_matrix[j, i] == 1):
                d[i] += 1

        if d[i] == 0:   # dead end, assume go to all links
            d[i] = num_pages

    # construct stochastic M
    M = np.zeros((num_pages, num_pages))
    for i in range(num_pages):
        if (d[i] == num_pages):  # dead end
            for j in range(num_pages):
                M[j, i] = 1.0 / d[i]
        else:
            for j in range(num_pages):
                if graph_matrix[j, i] == 1:
                    M[j, i] = 1.0 / d[i]
    
    return M

def distance(v1, v2):
    v = v1 - v2
    v = v * v
    return np.sum(v)

def graphMatrix():
    c.execute('SELECT COUNT(*) FROM urls')
    total_pages = c.fetchall()[0][0]
    matrix = np.zeros((total_pages, total_pages))

    c.execute('SELECT rowid, links FROM urls')
    data = c.fetchall()
    count = 0
    for element in data:
        count += 1
        print("Processing: " + str(count) + "/" + str(total_pages))
        i = element[0] - 1
        outlinks = element[1].split()

        matrix = updateMatrix(matrix,outlinks,i)
    
    return matrix

def updateMatrix(matrix, outlinks, i):
    if len(outlinks) > 500:
        matrix = updateMatrix(matrix,outlinks[0:500],i)
        matrix = updateMatrix(matrix,outlinks[501:(len(outlinks)-1)],i)
    else:
        # Find rowid for each outlink
        query = "SELECT rowid from urls WHERE url IN ({seq})".format(seq=','.join(['?']*len(outlinks)))
        c.execute(query, outlinks)
        positions = c.fetchall()
        for position in positions:
            j = position[0] - 1
            matrix[j][i] = 1
    
    return matrix

def insertPageRankDB(ranking):
    num_pages = len(ranking)
    for i in range(num_pages):
        print("Inserting: " + str(i) + "/" + str(num_pages))
        rank = ranking[i]
        c.execute('UPDATE urls SET pageRank = ? WHERE rowid = ?', [ rank, i+1 ])
        conn.commit()


if __name__=='__main__':    

    print('Constructing matrix from database...')
    matrix = graphMatrix()
    stochasticMatrix(matrix)
    #print('Computing PageRank...')
    #ranking = pageRank(matrix)
    #print('Inserting PageRank into database')
    #insertPageRankDB(ranking)
    print('Done!')