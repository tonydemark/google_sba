#!/usr/bin/python2.4

import pprint
import csv
import re
import sys
import json
import Levenshtein
from apiclient.discovery import build

f = {
    'id': 0,
    'location': 7,
    'first-name': 3,
    'last-name': 4,
    'department': 7,
    'title': 9,
    'company': 6,
    'industry': 5,
    'li-public-profile': 8,
}

def main():

	service = build("customsearch", "v1",
		developerKey="AIzaSyB9iBLJG4eWe2W3pwj7u72sxYqYWtrSCCI")

	outfile = open('output.csv','wb')
	csvwriter = csv.writer(outfile)


	with open('input.csv', 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		csvreader.next()

		for row in csvreader:
			print ' '.join((row[f['id']],row[f['last-name']],row[f['first-name']]))
			compareName = ' '.join([row[f['first-name']],row[f['last-name']]])
			items = [ '"' + compareName + '"', '"' + row[f['title']] + '"', '"' + row[f['company']] + '"' ]
			for key in ('location','department','industry'):
				if row[f[key]] != 'NULL':
					items.append('"' + row[f[key]] + '"')
			items.append('site:linkedin.com')
			query = ' '.join(items).decode('UTF-8','ignore').encode('UTF-8')
			res = service.cse().list(
		      q=query,
		      cx='004456612287487030855:s6r07ulnhms',
		    ).execute()
			numResults = int(res['searchInformation']['totalResults'])
			row.append(numResults)
			row.append(query)
			if numResults > 0:
				gather = []
				for result in res['items']:
					if result['link'].find('/pub/dir') != -1:
						continue
					gather.append(result)
				row.append(len(gather))
				matches = 0
				if len(gather) > 0:
					max_ratio = 0
					min_distance = 1000
					closest_result = gather[0] 
					for result in gather:
						resultName = linkedin_title_to_compare_name(result['title'].encode("UTF-8",'ignore'))
						print resultName
						ratio = Levenshtein.ratio(compareName.encode("UTF-8",'ignore'),resultName.encode("UTF-8",'ignore'))
						distance = Levenshtein.distance(compareName.encode("UTF-8",'ignore'),resultName.encode("UTF-8",'ignore'))
						if (ratio > max_ratio and distance < min_distance):
							max_ratio = ratio
							min_distance = distance
							closest_result = result
							if max_ratio >= 0:
								matches += 1
					row.append(matches)
					if max_ratio >= 0:
						row.append(max_ratio)
						row.append(min_distance)
						row.append(closest_result['title'].encode("UTF-8",'ignore'))
						row.append(closest_result['link'])
			else:
				row.append(0)
				row.append(0)
			csvwriter.writerow(row)

def linkedin_title_to_compare_name(str):
	regex = re.compile(r'[\s\,\.]')
	name = str.split(' - ',1)
	return regex.sub('',''.join(name[0])).lower().decode('UTF-8','ignore')

if __name__ == '__main__':
  main()
