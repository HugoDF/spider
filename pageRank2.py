import sqlite3
import numpy as np
conn = sqlite3.connect('urls.db')
c = conn.cursor()

def pageRank(d = 0.7, max_error = 0.00001):
    # d - damping factor
    # max_error - Acceptable difference between eah iteration

    # Get total number of pages
    c.execute('SELECT COUNT(*) FROM urls')
    total_pages = c.fetchall()[0][0]

    iteration = 0
    list = [0]*total_pages
    while True:
        error = 0
        iteration += 1
        for i in range(0,total_pages):
            print(str(iteration) + ' iteration: ' + str(i+1) + '/' + str(total_pages))
            c.execute('SELECT links,pageRank FROM urls WHERE rowid = ?', [ i+1 ])
            data = c.fetchall()
            outlinks = data[0][0].split()
            old_weighting = data[0][1]

            value = getValue(total_pages,outlinks)
            weighting = (1 - d)/total_pages + d * value
            list[i] = weighting
            error += abs(weighting - old_weighting)
        
        for i in range(0,total_pages):
            c.execute('UPDATE urls SET pageRank = ? WHERE rowid = ?', [ list[i], i+1 ])
            conn.commit()

        if error < max_error:
            break

def getValue(total_pages,links):
    value = 0;
    if len(links) > 500:
        value = getValue(total_pages,links[0:500]) + getValue(total_pages,links[501:(len(links)-1)])
    else:
        # Find rowid for each outlink
        query = "SELECT pageRank, amount from urls WHERE url IN ({seq})".format(seq=','.join(['?']*len(links)))
        c.execute(query, links)
        datas = c.fetchall()
        for data in datas:
            if data[1] == 0:
                value += data[0]/total_pages
            else:
                value += data[0]/data[1]
    
    return value

def resetPageRank():
    c.execute('SELECT COUNT(*) FROM urls')
    total_pages = c.fetchall()[0][0]
    c.execute('UPDATE urls SET pageRank = ?', [ 1/total_pages ])
    conn.commit()

if __name__=='__main__':
    resetPageRank();
    pageRank();