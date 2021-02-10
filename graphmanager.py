import networkx as nx
import requests
import socket
import ast
import json


HOST = '127.0.0.2'
PORT = 65432

G = nx.Graph()
C = nx.Graph()





def update_graph_g(entities):
	for entity in entities:
		print(entity)
		if (entity not in G):
			G.add_node(entity)
	adjust_edges(entities)
	return 'Status: Finished'

def adjust_edges(entities):
	for entity in entities:
		for other_entity in entities:
			if other_entity != entity:
				if (entity in G.neighbors(other_entity)):
					G[entity][other_entity]['weight'] += 1
				else:
					G.add_edge(entity, other_entity)
					G[entity][other_entity]['weight'] = 1
	

def load_graph(graph, filepath):
	graph = nx.read_gml(filepath)
	return graph

def save_graph(graph, filepath):
	nx.write_gml(graph, filepath)

def retrieve_topic(query):
	topic = {}
	for word in query:
		if G.has_node(word):
			topic[word] = 100
			neighbors = G.neighbors(word)
			for neighbor in neighbors:
				if neighbor in topic:
					topic[neighbor] += G[word][neighbor]['weight']
				else:
					topic[neighbor] = G[word][neighbor]['weight']
	return topic		


def update_graph_c(parameters):
	url = parameters['url']
	destinations = parameters['destinations']
	entities = parameters['entities']

	if (url not in C):
		C.add_node(url, weight = 0)
	for destination in destinations:
		if (C.has_edge(url, destination)):
			C[url][destination]['weight'] += 1
		else:
			if (C.has_node(destination) == False):
				C.add_node(destination, weight = 0)
			C.add_edge(url, destination)
			C[url][destination]['weight'] = 1
	neighbors = C.neighbors(url)
	for neighbor in neighbors:
		for entity in entities:
		#add code to increase edge weight when
			#Pseudocode
			# if neighbor.has_word(entity):
			#		weight += 1
			pass
	return "Status: Finished"

def get_ranked_list(entity_list):
	print('into function')
	pages = C.nodes()
	for page in pages:
		host = 'http://127.0.0.1:8000/add_page/'
		url_dict = {}
		print(page)
		try:
			url_dict['url'] = page
			url_dict['method'] = 'get_keywords'
			page_entities = requests.post(url=host, data=url_dict)
			print(page_entities.json())
			for entity in entity_list:
				C.nodes[page]['weight'] = 1
				if entity in page_entities:
					C.nodes[page]['weight'] += 1
		except Exception as e:
			print(str(e))
	
	results = {}
	pages = list(C.nodes(data=True))
	for page in pages:
		if page[1]['weight'] > 0:
			results[page[0]] = page[1]['weight']
	print(results)
	return results
	



'''
parser:

	when done parsing,
	socket signal to graphmanager(message=add to entitygraph)
	socket signal to graphmanager(message=add to connectivitygraph)


view:
	when user enters query,
	socket signal to graphmanager(message=get ranked list)
'''


while True:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		conn, addr = s.accept()
		with conn:
			print('Connected by', addr)
			while True:
				data = str(conn.recv(1024).decode("utf-8"))
				
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
