import csv
import sys


if __name__ == "__main__":

	if len(sys.argv) != 2:
		print("USAGE: python count_positives.py <file>")
		exit()

	with open(sys.argv[1]) as f:
		reader = csv.reader(f)
		items = list(reader)
		pos = 0
		for item in items:
			if item[-1] == "1":
				pos += 1
		print(str(pos) + "/" + str(len(items)))
		print(pos/(len(items)*1.0))