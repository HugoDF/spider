import sqlite3
import numpy as np
conn = sqlite3.connect('urls.db')
c = conn.cursor()

def count():
    # Get total number of pages
    c.execute('SELECT COUNT(*) FROM urls')
    total_pages = c.fetchall()[0][0]

    for i in range(0,total_pages):
        print(str(i+1) + '/' + str(total_pages))
        c.execute('SELECT links FROM urls WHERE rowid = ?', [ i+1 ])
        outlinks = c.fetchall()[0][0].split()
        c.execute('UPDATE urls SET amount = ? WHERE rowid = ?', [ len(outlinks), i+1 ])
        conn.commit()

if __name__=='__main__':
    count();
