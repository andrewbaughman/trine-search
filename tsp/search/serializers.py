from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class PageSerializer(serializers.ModelSerializer):
	class Meta:
		model = page
		fields = ('id', 'url', 'title', 'description',)

class LinksSerializer(serializers.ModelSerializer):
	class Meta:
		model = links
		fields = ('id', 'destination', 'source', 'isTrine', 'visited',)


class KeywordsSerializer(serializers.ModelSerializer):
	class Meta:
		model = keywords
		fields = ('url', 'keyword', 'times_on_page',)


class PageResultsSerializer(serializers.ModelSerializer):
	class Meta:
		model = page_results
		fields = ('url', 'title', 'description',)
		description = serializers.CharField(required=False, allow_null=True)

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('id', 'username')