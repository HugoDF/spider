import numpy as np

def pageRank(graph_matrix, damping_factor = 0.85, max_error = 0.00001):
    M = stochasticMatrix(graph_matrix)

    num_pages = len(graph_matrix)
    ranking = np.ones(num_pages)
    constant = np.repeat((1.0 - damping_factor)/num_pages,num_pages)
    initial = damping_factor * M + constant

    old_ranking = np.zeros(num_pages) + 1.0/num_pages
    while True:
        ranking = np.dot(initial,old_ranking)
        dist = distance(ranking, old_ranking)
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

if __name__=='__main__':

    G = np.array([[0,1,0],[1,1,0],[1,0,0]])
    print (pageRank(G))