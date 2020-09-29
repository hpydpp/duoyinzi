import requests, time, codecs


BAIDU_DICT_URL = "https://dict.baidu.com/s?wd="

inputFile  = "./words.txt"

outputFile = "./wordContents.txt"


def queryWord(url, word):

	uri = url + word + "&ptype=zici"
	r = requests.get(uri)
	if r.status_code != 200:
		print("word %s not found\n", word)
		return ""
	return r.text

f = open(inputFile, 'r')

output = codecs.open(outputFile, 'w+', 'utf-8')

for line in f:
#	print("query the word = %s \n", line.rstrip())
	text = queryWord(BAIDU_DICT_URL, line.rstrip())
	output.write(text+"\r\n\r\n")
	print("word get = %s\n", line.rstrip())
#	time.sleep(1)

f.close()

output.close()
