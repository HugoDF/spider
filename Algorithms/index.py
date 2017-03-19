import sqlite3
conn = sqlite3.connect('urls.db')

c = conn.cursor()

def index():
	c.execute("SELECT * FROM urls")
	result = c.fetchall()
	urls = result
	
	for i in range (0, len(result) - 1):
	 	for word in result[i][1].split():
	 		print word
	 	 	inputWord = word.lower()
	 	 	c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (inputWord,))
	 	 	exist = c.fetchall()
	 	 	if exist == []:
	 	 		c.execute("CREATE TABLE " + inputWord + " (url string, count int)")
	 	 		conn.commit()
			 	c.execute("INSERT INTO " + inputWord + " VALUES (?,?)", (urls[i][0], 1))
	 	 		conn.commit()
			else:
			 	c.execute("SELECT count FROM " + inputWord + " WHERE url=?", (urls[i][0], ))
			 	count = c.fetchone();
			 	if count is None:
			 		c.execute("INSERT INTO " + inputWord + " VALUES (?,?)", (urls[i][0], 1))
			 		conn.commit()
			 	else:
			 		count = count[0] + 1
			 		c.execute("UPDATE " + inputWord + " SET count = ? WHERE url = ?", (count, urls[i][0], ))
	 	 			conn.commit()

	return

index()