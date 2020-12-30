from elasticsearch import Elasticsearch, helpers
import json
import os
import sys
import requests
import csv  



def load_json(dirpath):

	res = requests.get('http://localhost:9200/liberation/newspaper')
	es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

	for filename in [f for f in os.listdir(dirpath) if f[0]!='.']:
		path = os.path.join(dirpath, filename)
		
		
		with open(path,'r', encoding='utf-8-sig') as open_file:
			docket_content = open_file.read()
			es.index(index='liberation', ignore=400, doc_type='newspaper', body=json.loads(docket_content))
			
def delete_all():
	es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
	es.indices.delete(index='liberation', ignore=[400, 404])


def jsonParser():

  
	# Open the CSV  
	f = open( 'E:/1~20000/result/1-5000.csv', 'r', encoding='utf-8-sig')  
	COLUMNS = ("publisher","title_hangul","date","keywords","major","middle","code","imagelink","title_hanja")
	
	ff = open( 'E:/1~20000/json/1-5000.json', 'w', encoding='utf-8-sig')  
	
	services = csv.DictReader(f, COLUMNS)
	ff.write(json.dumps([row for row in services],ensure_ascii=False))






def main():
	jsonParser()

if __name__ == '__main__':
	main()

