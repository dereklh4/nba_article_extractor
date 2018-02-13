from goose import Goose
import os
import string

i = 0
for filename in os.listdir(os.getcwd() + "/articles"):
	f = open("articles/" + filename)
	html = f.read()
	#print(html)
	f.close()
	
	#remove everything before 'comment' to aid goose extractor
	idx = html.find("comment")
	html = html[idx:]

	#use goose to extract raw_text
	extractor = Goose()
	article = extractor.extract(raw_html=html)
	text = article.cleaned_text
	print(text)

	#remove non ascii
	printable = set(string.printable)
	text = filter(lambda x: x in printable, text)

	#save text to raw article
	f2 = open("raw_text/" + str(i) + ". [raw] " + filename,"w+")
	f2.write(text)
	f2.close()
	i += 1