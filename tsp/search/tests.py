from django.test import TestCase
from search.models import *
from search.pagerank import *
from search.parser import *
from search.crawler import *
from decimal import Decimal

# Create your tests here.

# To run most of the tests, parser.py and crawler.py need to be added on the same level as tests.py,
# but modified to not have the Command class or handle definition.

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

class IsTrineTestCase(TestCase):
	def setUp(self):
		self.u1 = "https://trine.edu/"
		self.u2 = "http://myportal.trine.edu/ics/"
		self.u3 = "https://en.wikipedia.org/wiki/Great_Depression"
		self.u4 = "https://en.wikipedia.org/wiki/TRIN_(finance)"

	def test_finds_trine_urls(self):
		""""u1 and u2 should return true while u3 and u4 should return false"""
		self.assertTrue(trine_url(self.u1))
		self.assertTrue(trine_url(self.u2))
		self.assertFalse(trine_url(self.u3))
		self.assertFalse(trine_url(self.u4))
		print("Passed isTrine")

class LocThirdSlashTestCase(TestCase):
	def setUp(self):
		self.u1 = "https://trine.edu"
		self.u2 = "http://myportal.trine.edu/ics/"
		self.u3 = "https://en.wikipedia.org/wiki/Great_Depression"
		self.u4 = "https://en.wikipedia.org/wiki/TRIN_(finance)"		

	def test_finds_third_slash(self):
		"""u1 should return false. u2, u3, and u4 should return a location in the url before the third slash"""
		self.assertFalse(loc_third_slash(self.u1))
		self.assertEqual(self.u2[:loc_third_slash(self.u2)], "http://myportal.trine.edu")
		self.assertEqual(self.u3[:loc_third_slash(self.u3)], "https://en.wikipedia.org")
		self.assertEqual(self.u4[:loc_third_slash(self.u4)], "https://en.wikipedia.org")
		print("Passed loc third slash")

class IsDuplicatePageTestCase(TestCase):
	def setUp(self):
		#Create link objects for each tested url
		links.objects.create(visited=False, source='', destination='https://trine.edu')
		links.objects.create(visited=False, source='', destination='http://myportal.trine.edu/ics/')
		links.objects.create(visited=False, source='', destination='https://en.wikipedia.org/wiki/Great_Depression')
		links.objects.create(visited=False, source='', destination='https://en.wikipedia.org/wiki/TRIN_(finance)')
		links.objects.create(visited=False, source='', destination='https://en.wikipedia.org/wiki/Macaronesia')
		links.objects.create(visited=False, source='', destination='https://www.trine.edu/academics/majors-degrees/index.aspx')
		
		#Fetch link objects for each tested url
		link_object1 = links.objects.get(destination='https://trine.edu')
		link_object2 = links.objects.get(destination='http://myportal.trine.edu/ics/')
		link_object3 = links.objects.get(destination='https://en.wikipedia.org/wiki/Great_Depression')
		link_object4 = links.objects.get(destination='https://en.wikipedia.org/wiki/TRIN_(finance)')
		
		#Create pages for first 4 urls
		page.objects.create(url=link_object1, title='Trine', description='Trine\'s homepage')
		page.objects.create(url=link_object2, title='Trine MyPortal', description='Trine\'s MyPortal homepage')
		page.objects.create(url=link_object3, title='Wikipedia Great Depression', description='Great Depression | Wikipedia')
		page.objects.create(url=link_object4, title='TRIN_(finance)', description='TRIN_(finance) | Wikipedia')

	def test_duplicate_page(self):
		"""Tests 1-4 should return true, while tests 5 and 6 should return false"""
		self.assertTrue(is_duplicate_page('https://trine.edu'))
		self.assertTrue(is_duplicate_page('http://myportal.trine.edu/ics/'))
		self.assertTrue(is_duplicate_page('https://en.wikipedia.org/wiki/Great_Depression'))
		self.assertTrue(is_duplicate_page('https://en.wikipedia.org/wiki/TRIN_(finance)'))
		self.assertFalse(is_duplicate_page('https://en.wikipedia.org/wiki/Macaronesia'))
		self.assertFalse(is_duplicate_page('https://www.trine.edu/academics/majors-degrees/index.aspx'))
		print("Passed duplicate page")