from search.models import *

import networkx
import scipy
import numpy


def PR(_edges, _links):
	PageRanks = {}
	
	A = make_A(_edges, _links)
	T = make_T(A)
	eigenvector = find_vector(T)
	
	for x in range(0, len(_links)):
		PageRanks[_links[x].id] = eigenvector[x]
	return PageRanks


def make_A(_edges, _links):
	### Reference for zero'd array: https://thispointer.com/create-an-empty-2d-numpy-array-matrix-and-append-rows-or-columns-in-python/
	A = numpy.zeros((len(_links),len(_links)), float)
	# Populate the adjacency matrix
	for edge in _edges:
		### Reference for finding index given value: https://www.tutorialspoint.com/accessing-index-and-value-in-a-python-list
		pointA = _links.index(edge.pointA)
		pointB = _links.index(edge.pointB)
		A[pointA][pointB] = 1
	print(A)
	### Reference for transpose function: https://numpy.org/doc/stable/reference/generated/numpy.matrix.transpose.html
	return A.transpose()

def make_T(A):
	### Reference for finding sum of all columns: https://www.geeksforgeeks.org/calculating-the-sum-of-all-columns-of-a-2d-numpy-array/
	sums = A.sum(axis=0)
	
	# Convert the adjacency matrix into a stochastic matrix(all column values add up to 1)
	for row in range(0, len(A)):
		for column in range(0,len(A)):
			if sums[column] != 0:
				A[row][column] = A[row][column] / sums[column]
			else:
				A[row][column] = A[row][column]
	print(A)

	# Create Square Matrix with all 1's
	I = numpy.zeros((len(A),len(A)), float)
	for row in range(0, len(I)):
		for column in range(0,len(I)):
			I[row][column] = 1

	### Reference for composing T matrix: https://www.youtube.com/watch?v=uDphHCgpDro
	T = ((0.15 / len(A)) * I) + (0.85 * A)
	print(T)
	return T


def find_vector(T):
	### Reference for finding eigenvector associated with eigenvalue of 1: https://stackoverflow.com/questions/11953867/how-do-i-find-out-eigenvectors-corresponding-to-a-particular-eigenvalue-of-a-mat
	values, vector = scipy.sparse.linalg.eigs(T, k=1, sigma=1)
	
	# Divide every entry by the sum of the vector to make a probability.
	sum_of_vector = vector.sum(axis=0)
	for x in range(0, len(vector)):
		vector[x] = (vector[x] / sum_of_vector)
	### Reference for converting list to list of real numbers: http://www.trytoprogram.com/python-programming/python-numbers/
	eigenvector = vector.real

	# Reformat the list so that it's easier to use and read.
	pageranks = []
	for rank in eigenvector:
		pageranks.append(rank[0].round(4))

	# Here is your probability vector. Aka PageRank vector.
	print(pageranks)
	return pageranks
