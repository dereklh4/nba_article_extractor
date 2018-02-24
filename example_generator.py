import os
import numpy as np
import csv
import sys

saved_dictionaries = {}
def check_dictionary(dictionary, string,check_partial=False):
	if dictionary not in saved_dictionaries:
		f = open(dictionary)
		reader = csv.reader(f)
		saved_dictionaries[dictionary] = list(reader)
		f.close()
	items = saved_dictionaries[dictionary]

	for item in items:
		item = item[0]
		if string.lower().find(item.lower()) != -1:
			return 1
		if check_partial:
			for sub_item in item.split(" "):
				if string.lower().find(sub_item.lower()) != -1:
					return 1
	return 0


if __name__ == "__main__":
	
	if len(sys.argv) != 2:
		print("USAGE: python example_generator.py <source_folder>")
		exit()

	folder = sys.argv[1]
	output_file = folder + "_examples.csv"

	with open(output_file,"w+") as f:
		writer = csv.writer(f)
		headers = ["string","doc_id","word_loc","string_length","number_words","before_'s","contains_'s","before_after_said","position_or_title_before","post_name_after",
		"two_capitals","capital_before","capital_after","contains_first_name","first_name_before","first_name_after","contains_last_name",
		"last_name_before","last_name_after","common_proper_noun","contains_nba_teamcity","contains_nba_person",
		"contains_partial_nba_person","partial_nba_person_before","partial_nba_person_after","label"]
		writer.writerow(headers)

	count = 0
	files = os.listdir(os.getcwd() + "/" + folder)

	f = open(output_file,"a+")
	writer = csv.writer(f)
	
	for filename in files:
		#show progress
		count += 1
		sys.stdout.write('\r')
		sys.stdout.write(str(count) + "/" + str(len(files)))
		sys.stdout.flush()

		#extract words
		marked_words = []
		with open(folder + "/" + filename) as f:
			for line in f:
				for word in line.split():
					marked_words.append(word)

		### PREPROCESSING ###

		for c in ["[","]","(",")","\"",".",","]:
			marked_words = map(lambda x: x.replace(c,""),marked_words)

		words = list(marked_words)
		for c in ["<","/>"]:
			words = map(lambda x: x.replace(c,""),words)

		#consider possible grams 1,2,3, and 4 grams
		for i in xrange(len(words)):
			for n in xrange(min(4,len(words)-i)):
				
				j = i+n #i marks beginning of string, j marks end of string
				marked_string = " ".join(marked_words[i:j+1]).lstrip()
				example_string = " ".join(words[i:j+1]).lstrip()
				
				### PRUNING ###

				if len(marked_string) == 0 or len(example_string) == 0:
					continue

				#must all start with capital letter
				if not all(x[0].isupper() for x in example_string.split(" ") if len(x) > 0):
					continue


				#can't contain numbers
				if any(char.isdigit() for char in example_string):
					#print("n: " + example_string)
					continue

				#ignore if has exactly a transitional, basic word
				skip = False
				with open("dictionaries/basic_transitional.csv") as f:
					reader = csv.reader(f)
					items = list(reader)
					items = map(lambda x: x[0],items)
					items = map(lambda x: x.lower(),items)
					for substring in example_string.split(" "):
						if substring.lower() in items:
							skip = True
				if skip:
					continue

				#check for ESPN words
				if check_dictionary("dictionaries/espn_words.csv",example_string):
					continue

				#contains apostophe that isn't part of 's
				if example_string.find("'s") == -1 and example_string.find("'") != -1:
					continue

				if example_string.find(":") != -1:
					continue

				if example_string.find("?") != -1:
					continue

				### FEATURES ###

				#f0: length of string
				f0 = len(example_string)

				#f1: number of words in string
				f1 = len(example_string.split(" "))

				#f2: preceded by word with 's
				f2 = 0
				if i > 0 and words[i-1].find("'s") != -1:
					f2 = 1

				#f3: contains 's
				f3 = 0
				if example_string.find("'s") != -1:
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

				#f5.5: post-name after
				post_names = ["jr","III"]
				f55 = 0
				if j < len(words)-1 and (words[j+1].lower() in post_names):
					f55 = 1

				#f6: two capitals in same word (i.e more capitals than words)
				f6 = 0
				if sum(1 for c in example_string if c.isupper()) > len(example_string.split(" ")):
					f6 = 1

				#f7: preceeding string starts with capital letter
				f7 = 0
				if i > 0 and len(words[i-1]) > 0 and words[i-1][0].isupper():
					f7 = 1

				#f8: following string starts with capital letter
				f8 = 0
				if j < len(words)-1 and len(words[j+1]) > 0 and words[j+1][0].isupper():
					f8 = 1

				
				#f9: contains a first name (taken from https://github.com/hadley/data-baby-names)
				#f10: preceeded by a first name
				#f11: followed by a first name
				f9 = check_dictionary("dictionaries/first_names.csv", example_string)
				f10 = 0
				f11 = 0
				if i > 0:
					f10 = 1 if check_dictionary("dictionaries/first_names.csv", words[i-1]) and words[i-1][0].isupper() else 0
				if j < len(words)-1:
					f11 = 1 if check_dictionary("dictionaries/first_names.csv", words[j+1]) and words[j+1][0].isupper() else 0

				#f12: contains a last name (from http://deron.meranda.us/data/)
				#f13: preceeded by a last name
				#f14: followed by a last name
				f12 = check_dictionary("dictionaries/last_names.csv", example_string)
				f13 = 0
				f14 = 0
				if i > 0:
					f13 = 1 if check_dictionary("dictionaries/last_names.csv",words[i-1]) and words[i-1][0].isupper() else 0
				if j< len(words)-1:
					f14 = 1 if check_dictionary("dictionaries/last_names.csv",words[j+1]) and words[j+1][0].isupper() else 0

				#f15: contains common proper noun (months and days)
				f15 = check_dictionary("dictionaries/proper_nouns.csv",example_string)

				#f16: contains an NBA city,team,state, or arena (https://raw.githubusercontent.com/radavis/gametoday/master/db/teams.csv)
				f16 = check_dictionary("dictionaries/teams_flattened.csv",example_string)

				#f17: contains full name of NBA player (https://www.kaggle.com/drgilermo/nba-players-stats/data) or coach
				f17 = check_dictionary("dictionaries/players.csv",example_string) or check_dictionary("dictionaries/coaches.csv",example_string)

				#f18: contains partial name of NBA player or coach
				f18 = check_dictionary("dictionaries/players.csv",example_string,check_partial=True) or check_dictionary("dictionaries/coaches.csv",example_string,check_partial=True)

				#f19: preceeded by partial NBA player or coach
				#f20: followed by partial NBA player or coach
				f19 = 0
				f20 = 0
				if i > 0:
					f19 = 1 if check_dictionary("dictionaries/players.csv",words[i-1],check_partial=True) or check_dictionary("dictionaries/coaches.csv",words[i-1],check_partial=True) else 0
				if j< len(words)-1:
					f20 = 1 if check_dictionary("dictionaries/players.csv",words[j+1],check_partial=True) or check_dictionary("dictionaries/coaches.csv",words[j+1],check_partial=True) else 0

				#label: if starts with < and ends with /> and no extras in the middle
				label = 0
				if len(marked_string) > 0:
					if marked_string[0] == "<" and marked_string[-2:] == "/>" and len(marked_string.replace("<","").replace("/>","")) == len(marked_string) - 3:
						label = 1

				doc_id = filename[0:4]

				output = [example_string,doc_id,i,f0, f1,f2,f3,f4,f5,f55,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,f20,label]
				#print(output)
				writer.writerow(output)

			




