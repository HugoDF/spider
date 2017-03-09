import urllib
import os, os.path
rootDir = "Python"
searchTerm = "news"
fileList = []
for root, dirs, files in os.walk(rootDir):
	for file in files:
		if file.endswith(".html"):
			sock = urllib.urlopen(os.path.join(root, file))
			htmlSource = sock.read()
			sock.close()
			searchIndex = int(htmlSource.find(searchTerm, 0))
			searchTotal = int(0)
			while searchIndex != -1:
				searchIndex = int(htmlSource.find(searchTerm, searchIndex + len(searchTerm)))
				searchTotal += 1
			for listIndex in range(0, len(fileList) + 1):
				if listIndex == len(fileList):
					fileList.insert(listIndex, (searchTotal, os.path.join(root, file)))
					break
				elif searchTotal > fileList[listIndex][0]:
					fileList.insert(listIndex, (searchTotal, os.path.join(root, file)))
					break
					
print fileList