from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class PageSerializer(serializers.ModelSerializer):
	class Meta:
		model = page
		fields = ('id', 'url', 'title', 'description', 'hashId')

class LinksSerializer(serializers.ModelSerializer):
	class Meta:
		model = links
		fields = ('id', 'pagerank', 'destination', 'source', 'isTrine', 'visited', 'parsed')


class EdgesSerializer(serializers.ModelSerializer):
	class Meta:
		model = edges
		fields = ('id', 'pointA', 'pointB',)


class EdgesSerializer(serializers.ModelSerializer):
	class Meta:
		model = edges
		fields = ('id', 'pointA', 'pointB',)


class KeywordsSerializer(serializers.ModelSerializer):
	class Meta:
		model = keywords
		fields = ('id', 'url', 'keyword', 'times_on_page', 'is_substr', 'word_len')


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('id', 'username')