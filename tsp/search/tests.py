from django.test import TestCase
from search.models import *
from search.pagerank import *
from decimal import Decimal

# Create your tests here.

class PageRankTestCase(TestCase):
	def setUp(self):
		n1 = links.objects.create(destination="http://www.1.com")
		n2 = links.objects.create(destination="http://www.2.com")
		n3 = links.objects.create(destination="http://www.3.com")
		n4 = links.objects.create(destination="http://www.4.com")

		edges.objects.create(pointA=n1, pointB=n2)
		edges.objects.create(pointA=n1, pointB=n3)
		edges.objects.create(pointA=n2, pointB=n3)
		edges.objects.create(pointA=n3, pointB=n4)
		edges.objects.create(pointA=n4, pointB=n3)
		
	def test_pagerank_returns_correct_ranks(self):
		"""PageRank should be {1: 0.0375, 2: 0.0534, 3: 0.4711, 4: 0.4379}"""
		pageranks = PR_from_db(list(edges.objects.all()), list(links.objects.all()), len(links.objects.all()))
		for key in pageranks:
				link = links.objects.get(id=key)
				link.pagerank = pageranks[key]
				link.save()

		self.assertEqual(links.objects.get(id=1).pagerank, round(Decimal(0.0375), 4))
		self.assertEqual(links.objects.get(id=2).pagerank, round(Decimal(0.0534), 4))
		self.assertEqual(links.objects.get(id=3).pagerank, round(Decimal(0.4711), 4))
		self.assertEqual(links.objects.get(id=4).pagerank, round(Decimal(0.4379), 4))
		

	def test_make_A_returns_correct_matrix(self):
		"""A should be [[0. 1. 1. 0.], [0. 0. 1. 0.], [0. 0. 0. 1.], [0. 0. 1. 0.]]"""
		expected_A = [[0., 0., 0., 0.], [1., 0., 0., 0.], [1., 1., 0., 1.], [0., 0., 1., 0.]]
		print(len(links.objects.all()))
		A = make_A(list(edges.objects.all()), list(links.objects.all()), len(links.objects.all()))
		print(expected_A)
		print(A)
		for x in range(0,len(A)):
			for y in range(0, len(A)):
				self.assertEqual(A[x][y], expected_A[x][y])
		print("Passed make_A")
