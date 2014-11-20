import csv


def main():
	
	list_of_dicts = list() #list to store csv in memory, where each row is a dictionary



	keys = get_keys() #set up columns of data

	#Reads CSV file as a dictionary
	with open('calbug_short.csv', 'rwb') as file_obj:
		reader = csv.DictReader(file_obj, delimiter=',')
		for row in reader:
			list_of_dicts.append(row) #copy data into memory

	#Do some processing of data here
	process_country(list_of_dicts)






	#Write processed data to disk
	write_csv(keys,list_of_dicts)


def process_country(list_of_dicts): #standardize notation for countries
	for row in list_of_dicts:
		country = row['Country']
		if country == 'USA' or country == 'United States of America':
			row['Country'] = 'United States'






def get_keys():
	with open('calbug_short.csv', 'rwb') as file_obj:
		reader = csv.DictReader(file_obj, delimiter=',')
		keys = reader.next().keys()
	return keys



def write_csv(fieldnames, data):
	with open("processed_calbug.csv", 'wb') as out_file:
		writer = csv.DictWriter(out_file, delimiter=',', fieldnames = fieldnames)
		writer.writeheader()
		for row in data:
			writer.writerow(row)







	# with open('calbug.csv', 'rb') as csvfile:
	# 	reader = csv.reader(csvfile, delimiter = ',')

if __name__ == "__main__":
	main()

