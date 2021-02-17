from django.db import models

# Create your models here.

class page(models.Model):
	id = models.AutoField(primary_key=True)
	url = models.ForeignKey('links', on_delete=models.CASCADE, to_field="destination", db_column="url")
	title = models.CharField(max_length=50)
	description = models.TextField(max_length=400)


class keywords(models.Model):
	id = models.AutoField(primary_key=True)
	url = models.ForeignKey('links', on_delete=models.CASCADE)
	keyword = models.CharField(max_length=50)
	times_on_page = models.IntegerField()


class links(models.Model):
	id = models.AutoField(primary_key=True)
	destination = models.URLField(max_length=200, unique=True)
	source = models.URLField(max_length=200)
	isTrine = models.BooleanField()
	visited = models.BooleanField()


class page_results(models.Model):
	url = models.ForeignKey('links', on_delete=models.CASCADE, to_field="destination", db_column="url")
	title = models.CharField(max_length=50)
	description = models.CharField(max_length=250)