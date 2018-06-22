from elasticsearch_dsl.connections import connections
from django_elasticsearch_dsl import DocType, Index
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from .models import Newspaper
from elasticsearch_dsl import Q


CLIENT = Elasticsearch([{'host' : '210.125.96.107', 'port' : 9200}])


# @newspaper.doc_type
class NewsDocument(DocType):

    class Meta:
        model = Newspaper
        fields = ['code', 'date', 'imagelink', 'keywords', 'major', 'middle', 'publisher', 'title_hangul', 'title_hanja']


# define simple search here
# Simple search function
def search(keyword):
	S = Search(using=CLIENT, index="test")
	q = Q("match", title_hangul=keyword) & Q("match", keywords=keyword)

	query = S.query(q)
	count = query.count()
	response = query[0:count].execute()
	return response


# def connection():
# 	CLIENT = Elasticsearch([{'host' : '210.125.96.107', 'port' : 9200}])
# 	S = Search(using=CLIENT, index="test")
# 	return S 
	
	