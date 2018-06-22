from django.db import models
from django.utils import timezone
from mysite import settings


class Newspaper(models.Model):
		publisher = models.TextField(max_length=512)
		title_hangul = models.TextField(max_length=512)
		date = models.DateField(null=True, blank=True)
		keywords = models.TextField(max_length=512)
		major = models.TextField(max_length=512)
		middle = models.TextField(max_length=512)
		code = models.TextField(max_length=512)
		imagelink = models.TextField(max_length=512)
		title_hanja = models.TextField(max_length=512)
