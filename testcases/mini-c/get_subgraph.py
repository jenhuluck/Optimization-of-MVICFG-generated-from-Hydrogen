import os
import sys
#generate the subgraph dot file for simple MVICFG
def get_nodes(nodes_array,nodes):
	for ele in nodes_array:
		if "[label" in ele:
			sp = ele.split('"')
			nodes.append(int(sp[1]))	


if __name__ == '__main__':
	argc = len(sys.argv)
	# the format of the command should be like #python get_subgraph.py 1010
	assert argc > 1, "Please provide a subgraph cluster number"

	subcluster_number = sys.argv[-1]
	cluster_name = "subgraph cluster_"+subcluster_number+" {"
	
	writeFile = open("MVICFG_subcluster.dot","w")

	readFile = open('MVICFG.dot', 'r')
	header = 'digraph "MVICFG" \n{ label="MVICFG"; \n'
	writeFile.write(header)

	nodes_array = [] # for save lines contains nodes
	nodes = [] # for save nodes in array
	readable = False

	line_num = sum(1 for line in readFile)
	counter = line_num
	readFile.seek(0) #reread the file
	while counter > 0:
		counter -= 1
		line = readFile.readline()

		#size -=len(line) + 1
		if cluster_name in line:
			readable = True
		#read nodes part
		if readable:
			nodes_array.append(line)
			writeFile.write(line)
			if "}" in line: #close the nodes part when seeing }
				get_nodes(nodes_array,nodes)
				readable = False
		# read edge part
		if "->" in line:
			sp = line.split('"')
			first_num = int(sp[1])
			second_num = int(sp[3])
			if first_num in nodes and second_num in nodes:
				writeFile.write(line)
				#print(first_num, second_num)
		if counter == 0:
			writeFile.write(line)


	writeFile.close()


	
