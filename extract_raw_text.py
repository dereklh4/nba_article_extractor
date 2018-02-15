from goose import Goose
import os
import string

#make folder if doesn't exist
if not os.path.exists("raw_text"):
	os.makedirs("raw_text")

lengths = {}
print("Extracting text from articles...")
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
	try:
		article = extractor.extract(raw_html=html)
	except:
		print("Unable to extract raw text from " + filename)
	text = article.cleaned_text
	
	if len(text) == 0:
		print("Unable to extract raw text from " + filename)
		continue

	#remove non ascii
	printable = set(string.printable)
	text = filter(lambda x: x in printable, text)

	#save text to raw article
	f2 = open("raw_text/" + "[raw] " + filename,"w+")
	f2.write(text)
	f2.close()
	lengths[filename] = len(text)

print("Sorting articles by length...")
#sort the docs from shortest to longest for convenience of labeling
for i in xrange(len(os.listdir(os.getcwd() + "/raw_text"))):
	#get the next min
	if len(lengths) != 0:
		min_article = min(lengths,key=lengths.get)
		del lengths[min_article]
	else:
		break

	#give it the next number
	os.rename("raw_text/" + "[raw] " + min_article, "raw_text/" + string.zfill(str(i),3) + ". [raw] " + min_article)
	i += 1


