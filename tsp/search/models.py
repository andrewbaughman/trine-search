from django.db import models

# Create your models here.

class page(models.Model):
	id = models.AutoField(primary_key=True)
	url = models.ForeignKey('links', on_delete=models.CASCADE, to_field="destination", db_column="url")
	title = models.CharField(max_length=70)
	description = models.TextField(max_length=400)


class keywords(models.Model):
	id = models.AutoField(primary_key=True)
	url = models.ForeignKey('links', on_delete=models.CASCADE)
	keyword = models.CharField(max_length=20)
	times_on_page = models.IntegerField()
	is_substr = models.BooleanField(default=False)


class links(models.Model):
	id = models.AutoField(primary_key=True)
	pagerank = models.DecimalField(max_digits=5, decimal_places=4, null=True)
	destination = models.URLField(max_length=400, unique=True)
	source = models.URLField(max_length=400)
	isTrine = models.BooleanField(default=False)
	visited = models.BooleanField(default=False)


class edges(models.Model):
	id = models.AutoField(primary_key=True)
	pointA = models.ForeignKey('links', related_name="pointA", on_delete=models.CASCADE)
	pointB = models.ForeignKey('links', related_name="pointB", on_delete=models.CASCADE)
