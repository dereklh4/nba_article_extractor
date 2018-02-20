import os
import numpy as np
import csv

def check_dictionary(dictionary, string,check_partial=False):
	with open(dictionary) as f:
		reader = csv.reader(f)
		items = list(reader)
		for item in items:
			item = item[0]
			if string.lower().find(item.lower()) != -1:
				#print("MATCH: " + string.lower() + " , " + item.lower())
				return 1
			if check_partial:
				for sub_item in item.split(" "):
					if string.lower().find(sub_item.lower()) != -1:
						return 1
	return 0


if __name__ == "__main__":
	
	folder = "test"
	doc_id = 1

	for filename in os.listdir(os.getcwd() + "/" + folder):
		#extract words
		words = []
		with open(folder + "/" + filename) as f:
			for line in f:
				for word in line.split():
					words.append(word)

		#consider possible grams 1,2,3, and 4 grams
		for i in xrange(len(words)):
			for n in xrange(min(4,len(words)-i)):
				
				j = i+1+n #i marks beginning of string, j marks end of string
				marked_string = " ".join(words[i:j])
				example_string = marked_string

				### PREPROCESSING ###

				for c in ["<","/>","[","]","(",")","\"","."]:
					example_string = example_string.replace(c,"")
				
				### PRUNING ###

				#must all start with capital letter
				if not all(x[0].isupper() for x in example_string.split(" ")):
					#print("t: " + example_string)
					continue

				#can't contain numbers
				if any(char.isdigit() for char in example_string):
					#print("n: " + example_string)
					continue

				### FEATURES ###

				#f1: number of words in string
				f1 = len(example_string.split(" "))

				#f2: preceded by word with 's
				f2 = 0
				if i > 0 and words[i-1].find("'s") != -1:
					f2 = 1

				#f3: contains 's
				f3 = 0
				if i > 0 and example_string.find("'s") != -1:
					f3 = 1
				example_string = example_string.replace("'s","") #now can filter out 's

				#f4: preceeded or followed by "said"
				f4 = 0
				if i > 0 and words[i-1].find("said") != -1:
					f4 = 1
				elif j < len(words)-1 and words[j+1].find("said") != -1:
					f4 = 1

				#f5: preceeded by position or title
				positions = ["c","f","g","pg","sg","sf","pf"]
				titles = ["coach","mr","mrs","dr","ms"]
				f5 = 0
				if i > 0 and (words[i-1].lower() in positions or words[i-1].lower() in titles):
					f5 = 1

				#f6: two capitals in same word (i.e more capitals than words)
				f6 = 0
				if sum(1 for c in example_string if c.isupper()) > len(example_string.split(" ")):
					f6 = 1

				#f7: preceeding string starts with capital letter
				f7 = 0
				if i > 0 and words[i-1][0].isupper():
					f7 += 1

				#f8: following string starts with capital letter
				f8 = 0
				if j < len(words)-1 and words[j+1][0].isupper():
					f8 += 1

				
				#f9: contains a first name (taken from https://github.com/hadley/data-baby-names)
				#f10: preceeded by a first name
				#f11: followed by a first name
				f9 = check_dictionary("dictionaries/first_names.csv", example_string)
				f10 = 0
				f11 = 0
				if i > 0:
					f10 = check_dictionary("dictionaries/first_names.csv", words[i-1])
				if j < len(words)-1:
					f11 = check_dictionary("dictionaries/first_names.csv", words[j+1])

				#f12: contains a last name (from http://deron.meranda.us/data/)
				#f13: preceeded by a last name
				#f14: followed by a last name
				f12 = check_dictionary("dictionaries/last_names.csv", example_string)
				f13 = 0
				f14 = 0
				if i > 0:
					f13 = check_dictionary("dictionaries/last_names.csv",words[i-1])
				if j< len(words)-1:
					f14 = check_dictionary("dictionaries/last_names.csv",words[j+1])

				#f15: contains common proper noun (months and days)
				f15 = check_dictionary("dictionaries/proper_nouns.csv",example_string)

				#f16: contains an NBA city,team,state, or arena (https://raw.githubusercontent.com/radavis/gametoday/master/db/teams.csv)
				f16 = check_dictionary("dictionaries/teams_flattened.csv",example_string)

				#f17: contains full name of NBA player (https://www.kaggle.com/drgilermo/nba-players-stats/data) or coach
				f17 = check_dictionary("dictionaries/players.csv",example_string) or check_dictionary("dictionaries/coaches.csv",example_string)

				#f18: contains partial name of NBA player or coach
				f18 = check_dictionary("dictionaries/players.csv",example_string,check_partial=True) or check_dictionary("dictionaries/coaches.csv",example_string,check_partial=True)

				#label: if starts with < and ends with />
				label = 0
				if marked_string[0] == "<" and marked_string[-2:] == "/>":
					label = 1

				output = [example_string,doc_id,i,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,label]

				print(output)

				#save to file


		doc_id += 1


		#exit()

			




