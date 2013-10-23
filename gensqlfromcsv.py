#!/usr/bin/python2.4

import csv

def main():
	with open('output.csv', 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in csvreader:
			try:
				if row[16] > 0.3:
					print "update assessment_profile set linkedin_public_profile_url = '%s', status = 1 where id = %s;" % (row[19],row[0])
			except:
				pass
if __name__ == '__main__':
  main()
