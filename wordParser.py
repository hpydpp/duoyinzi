# -*- coding: utf-8 -*-

from lxml import etree

import json

import codecs

htmlFile = './wordContents.txt'

gifsFile = './gifs/gifsFile.txt'

wordLists = []

def parse(html, handle):

	wordElements = []
	pinyinVariantsMap  = {}

	wordGifsNode = html.xpath('//img[@id="word_bishun"]')
	
	if not wordGifsNode:
		print("Could not find the corresponding word bishun image, something wrong, exiting...")
		exit()

	handle.write(wordGifsNode[0].attrib['data-gif'] + "\n")

	wordElements.append(wordGifsNode[0].attrib['data-gif'][38:])

	basicMeanNode = html.xpath('//div[@id="basicmean-wrapper"]/div[@class="tab-content"]')

	if not len(basicMeanNode):
		print("Not a valid html for duoyizhi, something wrong, exiting...")
		exit()

	divNode = basicMeanNode[0]

	pinyinVariant = ''

	for it in divNode.iter():
		pinyinVariantsList = []
		if (it.tag == 'dt'):
			pinyinVariant = it.text
		if (it.tag == 'dd'):
			for mean in it.iter('p'):
				combinedMeans = mean.text.strip()
				for child in mean.getchildren():
					if child is not None:
						combinedMeans += child.text
				#print combinedMeans
				if combinedMeans:
					pinyinVariantsList.append(combinedMeans + "<br>")
		
		if pinyinVariant and pinyinVariantsList:
			pinyinVariantsMap[pinyinVariant] = pinyinVariantsList

	wordElements.append(pinyinVariantsMap)

	ciyu_node = html.xpath('//div[@id="zuci-wrapper"]/div[@class="tab-content"]')
	divNode = ciyu_node[0]
	ciyuList = []
	for it in divNode.iter():
		if (it.tag == 'a'):
			ciyuList.append(it.text)

	wordElements.append(ciyuList[:-1])
	
	wordLists.append(wordElements)



def htmlFeeder():
	f = open(htmlFile, 'r')
	htmls = f.read()
	htmlList = htmls.split("\r\n\r\n")

	gifHandle = open(gifsFile, "w+")

	for html in htmlList:
		if html.strip("\r\n\r\n"):
			html = etree.HTML(html)
			parse(html, gifHandle)

	print("There's", len(wordLists))

	return

def wordListEnumerate():
	for word in wordLists:
		print "="*80
		print("bishun ", word[0])
		for key in word[1]:
			print(key)
			print(json.dumps(word[1][key], ensure_ascii=False))
		for ciyu in word[2]:
			print(json.dumps(ciyu, ensure_ascii=False))

def ankiFileFormatter():

	ankiFile = codecs.open("duoyinzi-anki.txt", "w+", "utf-8-sig")

	for word in wordLists:
		ankiString = '<img src="' + word[0] + '" width=100 height=100>' 
		#ankiString = "Placehold"
		#ankiString += '<hr>'
		ankiString += ';'
		ankiString += '<div align="left">'
		#ankiString += '\n'
		for key in word[1]:
			ankiString += '<b>' + key + '</b>'+ '<br>'
			#ankiString += str(word[1][key]) + '<br>'
			for i in range(len(word[1][key])):
				ankiString += word[1][key][i]
			#ankiString += '\n'
		#ankiString += ';'
		#ankiString += '\n'
		
		ankiString += '<hr><b>[ciyu]</b><br>'
		for i in range(len(word[2])):
			ankiString += word[2][i] + ', '

		ankiString = ankiString.rstrip(', ')
		ankiString += '<br>'
		
		ankiString += '</div>\n'
		#print ankiString
		ankiFile.write(ankiString)	

	ankiFile.close()

	return
				
htmlFeeder()

#wordListEnumerate()

ankiFileFormatter()

