import os
import copy
import re
import sys
import difflib

#find the entry node 
def find_entry(lines):
	for line in lines:
		if "Entry" in line:
			return read_node(line)

#find the exit node
def find_exit(lines):
	for line in lines:
		if "Exit" in line:
			return read_node(line)

#find the node with the largest number
def find_largest_node(lines):
	max = 0
	for line in lines:
		if "->" not in line:
			node = read_node(line)
			if node > max:
				max = node
	return max	

#get line number for each node
def getlabel(lines):
	label_dict = {}
	for line in lines:
		sp = line.split('"')
		if "->" not in line and len(sp)>1 and sp[1].isdigit():
			#print("sp[3]", sp[3])
			key = int(sp[1])
			label = sp[3].split('::')
			label_dict[key] = int(label[0])
	return label_dict

#read the node number
def read_node(line):
	sp = line.split('"')
	if "->" not in line and len(sp)>1 and sp[1].isdigit():
		return int(sp[1])
	return -1

#read the end points of the edge
def read_edge(line):
	if "->" in line:
		sp = line.split('"')
		first_num = int(sp[1])
		second_num = int(sp[3])
		return [first_num, second_num]
	else:
		return [-1, -1]

#construct a adjacent matrix graph with edge weights
#if edge is from 1 -> 2, weight = 3, then adj_matrix[1][2] = 3
# 0 : no edges; 1:V1 ; 2: V2; 3 V1,V2
def construct_graph(num_of_nodes, lines,argc): 
	adj_matrix = [[0 for x in range(num_of_nodes+1)] for y in range(num_of_nodes+1)]
	for line in lines:
		if "->" in line:
			edge = read_edge(line)
			weight = map_to_weight(line,argc)
			add_edge(adj_matrix,edge[0],edge[1],weight)		
	return adj_matrix	

#read dot file and parse edge type to number(weight)
#V1 weight 1, V2 weight 2, Vn weight n, V1V2..Vn weight n+1
def map_to_weight(line,argc):
	if "V1,V2" in line:
		return 3
	elif "V1" in line:
		return 1
	elif "V2" in line:
		return 2
"""
	counter = 0
	num = 0
	for n in range(1,argc):		
		s = "V"+str(n)
		if s in line:
			num = n
			counter += 1
	if counter == argc-1:
		return argc	
	else:
		return num	
"""


#add edges to the adhacent matrix			
def add_edge(matrix,u,v,weight):
	#print(u,v,weight)
	matrix[u][v] = weight

#simplify the graph using dfs
def traverse(matrix, first, second, pred_weight ,exit, label_dict ,pred_label, save_node):
	if matrix[first][second] == 0 or second == exit:
		return 
	current_label = label_dict[second]
	#print("first",first,"second",second,"current_label",current_label,"pred_label",pred_label, "save_node", save_node)
	#current_weight = matrix[first][second]
	temp = matrix[first][second]
	matrix[first][second] = 0 #set to 0 first
	
	neighbors = find_neighbors(matrix,second)
	if len(neighbors) == 0:
		return
	for n in neighbors:
		if temp == pred_weight and current_label == pred_label:
			traverse(matrix,second,n,temp,exit,label_dict,pred_label, save_node)
		else:
			matrix[save_node][second] = temp
			traverse(matrix,second,n,temp,exit,label_dict,current_label, second)

#get nodes and edges with weights from graph
#edges = [[start, end, weight]]
def get_edges_and_nodes(matrix,nodes_set, edges):
	width = len(matrix)
	for i in range(width):
		for j in range(width):
			if matrix[i][j] != 0:
				edges.append([i,j,matrix[i][j]])
				nodes_set.add(i)
				node_set.add(j)

#find the neighbors of a node by a given row
def find_neighbors(matrix, row):
	res = []
	length = len(matrix[row])
	for col in range(length):
		if matrix[row][col] != 0:
			res.append(col)
	return res

#construct a graph dot file of a simplied graph
def print_graph(nodes, edges, label_dict, lines, file, entry, exit, source_dict):
	count = 0
	line_node = {}
	node_node = {}
    #header part
	for line in lines:
		file.write(line)
		if 'label="main"' in line:
			break
	#nodes part
	nodes = sorted(nodes)
	for node in nodes:
		wr = True
		if node == entry:
			node_node[node] = node
			line = f'"{node}" [label="{label_dict[node]}::Entry"]\n'
		elif node == exit:
			node_node[node] = node
			line = f'"{node}" [label="{label_dict[node]}::Exit"]\n'
		else:
			source_line = label_dict[node]
			if source_line in line_node:
				wr = False
				node_node[node] = line_node[source_line]
			#if source_line in source_dict:
			#	line = f'"{node}" [label="{label_dict[node]}:: {source_dict[source_line]}"]\n'
			#else:
			#	line = f'"{node}" [label="{label_dict[node]}"]\n'
			elif source_line in source_dict:
				line_node[source_line] = node
				node_node[node] = node
				updated_line = update_source_line(source_dict[source_line])
				line = f'"{node}" [label="{label_dict[node]}:: {updated_line}"]\n'
			else:
				line_node[source_line] = node
				node_node[node] = node
				#v1line = removed_lines[count]
				v1line = ""
				updated_line = update_source_line(v1line)
				line = f'"{node}" [label="{label_dict[node]}:: {updated_line}"]\n'
				count += 1
		if wr:		
			file.write(line)

	file.write('}\n')

	#edges part
	for edge in edges:
		first = edge[0]
		second = edge[1]
		weight = edge[2]
		#line = f'"{first}" -> "{second}" [arrowhead = normal, penwidth = 1.0, color = black, label="{weight}"];\n'
		edge_label = [None,"V1", "V2", "V1,V2"] # need to change based on input version
		colors = [None, "red", "green","black"]
		first = node_node[first]		
		second = node_node[second]
		if first != second:
			line = f'"{first}" -> "{second}" [arrowhead = normal, penwidth = 1.0, color = {colors[weight]}, label="{edge_label[weight]}"];\n'
			file.write(line)
	file.write('}\n')

# get removed lines from diff between two files
def diffFiles_removedlines(file1name, file2name):
    file1 = open(file1name, "r")
    lines1 = file1.readlines()
    file1.close()
    file2 = open(file2name, "r")
    lines2 = file2.readlines()
    file1.close()
    diff = difflib.unified_diff(lines1, lines2, fromfile=file1name, tofile=file2name, n=0)
    lines = list(diff)[2:]
    #added = [line[1:] for line in lines if line[0] == '+']
    removed = [line[1:].strip() for line in lines if line[0] == '-']
    #print('removes:')
    #for line in removed:
    #    print(line)
    return removed

# update source line to dot file correct version
def update_source_line(source_line):
    updated_line = ""
    for c in source_line:
        if c == "%":
            updated_line += "\\" + c
        elif c == "\"":
            updated_line += "\\" + c
        else:
            updated_line += c
    
    return updated_line

file1name = sys.argv[-2]
file2name = sys.argv[-1]
removed_lines = diffFiles_removedlines(file1name, file2name)

if __name__ == '__main__':

	argc = len(sys.argv)
	# the format of the command should be like #python simply_MVICFG.py sum1.c sum2.c ...
	assert argc > 1, "Please provide source code! For example, prog.c"

	readFile = open('test3/MVICFG.dot', 'r')
	lines = readFile.readlines()

	entry = find_entry(lines)
	exit = find_exit(lines)

	max = find_largest_node(lines)
	label_dict = getlabel(lines)
	graph = construct_graph(max, lines, argc)

	traverse(graph, entry, find_neighbors(graph, entry)[0], None, exit, label_dict, None, entry)
	
	node_set = set()
	edges = []
	get_edges_and_nodes(graph, node_set,edges)

	source_file = sys.argv[-1] # find the last version. If the path label debugged, all versions are required.
	read_source = open(source_file, 'r')
	source_lines = read_source.readlines()

	source_dict = {}
	counter = 1
	for line in source_lines:
		source_dict[counter] = line.strip()
		counter += 1

	writeFile = open("test3/simple.dot","w")
	print_graph(node_set, edges, label_dict, lines, writeFile, entry, exit, source_dict)


	readFile.close()
	writeFile.close()