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
	












'''
def update_graph_g():

	for entity in keywords.objects.all():
		os.system('clear')
		print(entity.id)
		print(entity)
		if (entity.keyword not in G):
			G.add_node(entity.keyword)
			#print("added node")
		else:
			#print("node already present")
			pass
		
		


def adjust_edges():
	for entity in keywords.objects.all():
		os.system('clear')
		print(entity.id)
		print(entity)
		### https://stackoverflow.com/questions/687295/how-do-i-do-a-not-equal-in-django-queryset-filtering
		for other_entity in keywords.objects.filter(~Q(keyword=entity.keyword)):
			#print(other_entity.keyword)
			try:
				if (entity.keyword in G.neighbors(other_entity.keyword)):
					G[entity.keyword][other_entity.keyword]['weight'] += 1
					#print('no new node')
				else:
					G.add_edge(entity.keyword, other_entity.keyword)
					G[entity.keyword][other_entity.keyword]['weight'] = 1
					#print('new node')
			except Exception as e:
				print(str(e))
	pos = nx.spring_layout(G)
	nx.draw_networkx(G, pos)
	plt.show()
	plt.savefig('graph.png')
		
		


def update_graph_c():
	for page in links.objects.all():
		os.system('clear')
		print(page.id)
		if (page.destination not in C):
			C.add_node(page.destination, weight = 0)
		for link in links.objects.filter(source=page.destination):
			if (C.has_edge(page.destination, link.destination)):
				C[page.destination][link.destination]['weight'] = 0
			else:
				if (C.has_node(link.destination) == False):
					C.add_node(link.destination, weight = 0)
				C.add_edge(page.destination, link.destination)
				C[page.destination][link.destination]['weight'] = 0
		neighbors = C.neighbors(page.destination)
		for neighbor in neighbors:
			pass
			#for entity in entities:
				#add code to increase edge weight when
				#Pseudocode
				# if neighbor.has_word(entity):
				#		weight += 1
	
	return "Status: Finished"

	

def load_graph(graph, filepath):
	graph = nx.read_gml(filepath)
	return graph

def save_graph(graph, filepath):
	nx.write_gml(graph, filepath)

def retrieve_topic(query):
	topic = {}
	for word in query:
		print(word)
		if G.has_node(word):
			topic[word] = 100
			neighbors = G.neighbors(word)
			print(neighbors)
			for neighbor in neighbors:
				if neighbor in topic:
					topic[neighbor] += G[word][neighbor]['weight']
				else:
					topic[neighbor] = G[word][neighbor]['weight']
		else:
			print('Nothing here')
	return topic		



def get_ranked_list(entity_list):
	print(entity_list)
	ranked_list = {}
	for entity in entity_list:
		try:
			kwobjects = keywords.objects.filter(keyword=entity)
			for kwobject in kwobjects:
				link = links.objects.get(destination=kwobject.url.destination)
				ranked_list[link.destination] = kwobject.times_on_page
		except Exception as e:
			print(str(e))
	ranked_list = dict(sorted(ranked_list.items(), key=lambda item: item[1], reverse=True))
	return ranked_list
	
	pages = C.nodes()
	for page in pages:
		for entity in entity_list:
			try:
				link = links.objects.get(destination=page)
				print(link)
				kwobject = keywords.objects.get(url=link, keyword=entity)
				print(kwobject)
				C.nodes[page]['weight'] = entity_list[entity] * kwobject.times_on_page
				print(C.nodes[page]['weight'])
			except Exception as e:
				print(str(e))
	results = {}
	pages = list(C.nodes(data=True))
	for page in pages:
		if page[1]['weight'] > 0:
			results[page[0]] = page[1]['weight']
	results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
	print(results)
	save_graph(G, "graphG")
	save_graph(C, "graphC")
	return results

		




parser:

	when done parsing,
	socket signal to graphmanager(message=add to entitygraph)
	socket signal to graphmanager(message=add to connectivitygraph)


view:
	when user enters query,
	socket signal to graphmanager(message=get ranked list)



while True:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		conn, addr = s.accept()
		with conn:
			print('Connected by', addr)
			while True:
				data = str(conn.recv(8192).decode("utf-8"))
				
				if (data[:14] == 'update_graph_g'):
					print(data[16:])
					ret = {}
					ret = update_graph_g(ast.literal_eval(data[16:]))
					print('finished')
					conn.sendall(ret.encode('utf-8'))
				elif (data[:14] == 'retrieve_topic'):
					print(data[16:])
					ret = {}
					ret = json.dumps(retrieve_topic(ast.literal_eval(data[16:])))
					print('finished')
					conn.sendall(ret.encode('utf-8'))
				elif (data[:14] == 'update_graph_c'):
					print(data[16:])
					params = ast.literal_eval(data[16:])
					ret = {}
					ret = json.dumps(update_graph_c(params))
					print('finished')
					conn.sendall(ret.encode('utf-8'))
				elif (data[:15] == 'get_ranked_list'):
					print(data[17:])
					ret = {}
					ret = json.dumps(get_ranked_list(ast.literal_eval(data[17:])))
					print('finished')
					conn.sendall(ret.encode('utf-8'))
				
				if not data:
					break
'''