from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.contrib import messages


from elasticsearch_dsl.connections import connections
from django_elasticsearch_dsl import DocType, Index
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from .models import Newspaper
from .elastic_search import search





# Create your views here.
def index(request):


	if request.method == "GET":
		keyword = request.GET.get('keyword')

		if keyword:	
			response = search(keyword)
			return render_to_response('result.html', {'response':response})



	return render(request, 'index.html', {})




# def search(request):
# 	# if request.method == "GET":
		
# 	# 	data = request.GET['key']
# 	# 	print(data)
# 	# 	return render(request, 'result.html', {})
# 	print("fffff")


