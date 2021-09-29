import pickle
import json
import sys
import operator
import pprint

class recursionlimit:
    def __init__(self, limit):
        self.limit = limit
        self.old_limit = sys.getrecursionlimit()

    def __enter__(self):
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)

def calc(fileName):
	f = fileName.split(".")
	dataFile=""
	for i in range(len(f)-1):
		if (i < len(f)-2):
			dataFile += f[i]+"."
		else:
			dataFile += f[i]

	l=open(dataFile + '_arcnodes.pkl','rb')
	arcnodes=pickle.load(l)
	# print(arcnodes)

	m=open(dataFile + '_edgelist.pkl','rb')
	edgelist=pickle.load(m)
	# print(edgelist)

	st=open(dataFile + '.splittree','rb')
	stlines=st.readlines()
	st.close()

	num_treenodes=int(stlines[0].split(" ")[0])
	num_edges=int(stlines[0].split(" ")[1])
	root = int(stlines[1].split(" ")[0])


	adjlistLeft={} # [(0,1),(0,2),(4,0)] adjLeft[0]=[1,2]
	adjlistRight={} # adjRight[0]=[4]

	#creating empty adjacency list for each node
	for i in range(num_treenodes):
		# t=stlines[i+1].rstrip()
		# a=int(t.split(" ")[0])
		adjlistLeft[i] = []
		adjlistRight[i] = []

	#creating left and right adjacenecy lists
	for i in range(num_edges):
		t=stlines[i+num_treenodes+1].rstrip()
		a=int(t.split(" ")[0])
		b=int(t.split(" ")[1])
		adjlistLeft[a].append(b)
		adjlistRight[b].append(a)

	potfile=open(dataFile + ".raw",'r') #pot file doesn't contain dimx,dimy,dimz, origin and delta
	plines=potfile.readlines()
	potfile.close()

	#Iso value list for Grid points
	isoallvertexlist=[]
	for i in range(len(plines)):
		tmp=plines[i].rstrip().split(" ")
		for j in range(len(tmp)):
			isoallvertexlist.append(float(tmp[j]))

	#computing childlists
	childlist=[[] for i in range(num_treenodes)]
	visited={}
	def bfs(node):
		visited[node] = 1
		# childlist[node]=[]
		for e in adjlistLeft[node]:
			if e not in visited:
				childlist[node].append(e)
				bfs(e)

		for e in adjlistRight[node]:
			if e not in visited:
				childlist[node].append(e)
				bfs(e)

	# bfs(root)
	# bfs(0) #root is at index 0


	with recursionlimit(120000):
		bfs(0)

	isotreenodes=[]
	for i in range(num_treenodes):
		isotreenodes.append(float(stlines[i+1].rstrip().split(" ")[1]))

	def orderchildlist(node):
		if len(childlist[node]) == 0:
			return isotreenodes[node]

		tmpchildlist=[]
		for child in childlist[node]:
			tmpchildlist.append((child,orderchildlist(child)))

		tmpchildlist.sort(key=operator.itemgetter(1),reverse=True)
		
		childlist[node]=[] 
		for i in range(len(tmpchildlist)):
			childlist[node].append(tmpchildlist[i][0])

		return tmpchildlist[0][1]

	with recursionlimit(120000):
		orderchildlist(0)

	Treenodewidth = [0]*num_treenodes
	pedge = [[] for i in range(num_treenodes)]


	def calc_numofpoints(node, parent):
		sum = 0
		for child in childlist[node]:
			sum += calc_numofpoints(child, node)
		sum += 1

		Treenodewidth[node] = sum

		if(parent == -1):
			return 

		#search for edge(node, parent) in edgelist
		try:
			idx1 = edgelist.index((node,parent))
		except ValueError:
			idx1 = -1
		try:
			idx2 = edgelist.index((parent,node))
		except ValueError:
			idx2 = -1

		if idx1 == -1 and idx2 == -1:
			print("You made some errors. Debug it")
			quit()

		index = 0
		if idx1 != -1:
			index = idx1
		else:
			index = idx2

		arcgp = arcnodes[index]
		# arciso=[]
		arcisodict={}
		for i in range(len(arcgp)): #changed this
			# arciso.append(isoallvertexlist[arcgp[i]])
			if isoallvertexlist[arcgp[i][0]] in arcisodict:
				arcisodict[isoallvertexlist[arcgp[i][0]]] += 1
			else:
				arcisodict[isoallvertexlist[arcgp[i][0]]] = 1

		sortedarcisodict=sorted(arcisodict.items(),key=operator.itemgetter(0),reverse=True)	

		internaliso=[]
		internalwidth=[]
		for k in sortedarcisodict:
			sum += k[1]
			internalwidth.append(sum)
			internaliso.append(k[0])	
		pedge[node]=[{"i":val, "w":w} for val, w in zip(internaliso,internalwidth)]
			
		return sum


	with recursionlimit(120000):
		calc_numofpoints(0, -1) #root is at index 0

	#JSON

	jsonlist =  [ {"i":v, "w":w, "c":c, "p":p } for v,w,c,p in zip(isotreenodes,Treenodewidth,childlist,pedge) ]

	print(json.dumps(jsonlist))

	# iso_width_childlist_pedge=[{"iso":val, "width":w, "childlist":c, "pedge":p } for val, w, c, p in zip(Uisoval,Uwidth,childList,pedge)]