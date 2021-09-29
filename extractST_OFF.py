import sys
import operator
import pickle

class recursionlimit:
    def __init__(self, limit):
        self.limit = limit
        self.old_limit = sys.getrecursionlimit()

    def __enter__(self):
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)

def extractST(fileName,rgFile,partFile):
	f = fileName.split(".")
	dataFile=""
	for i in range(len(f)-1):
		if (i < len(f)-2):
			dataFile += f[i]+"."
		else:
			dataFile += f[i]
	# print("something")
	
	# rgfile=open(dataFile + '.rg.txt','r')
	rgfile=open(rgFile,'r')
	lines = rgfile.readlines()
	rgfile.close()

	treenodes=int(lines[0].split(" ")[0])
	edges=int(lines[0].split(" ")[1])
	# print treenodes
	# print edges

	#adjacency list for reeb graph
	adjlist={}
	for i in range(edges):
		tmp=lines[i+treenodes+1].split(" ")
		a=int(tmp[0])
		b=int(tmp[1])
		if a in adjlist:
			adjlist[a].append(b)
		else:
			adjlist[a]=[b]

		if b in adjlist:
			adjlist[b].append(a)
		else:
			adjlist[b]=[a]

	#For reeb graph
	isodict={}
	visiteddict={}
	for i in range(treenodes):
		tmp=lines[i+1].split(" ")
		a=int(tmp[0])
		v=float(tmp[1])
		isodict[a]=v
		visiteddict[a]=False

	# print adjlist
	# print isodict

	firstminima=True
	minima = lines[1].split(" ")[0]
	value  = float(lines[1].split(" ")[1])
	for i in range(treenodes):
		if (lines[i+1].split(" ")[2].rstrip() == "MIN"):
			if firstminima:
				minima = lines[i+1].split(" ")[0]
				value  = float(lines[i+1].split(" ")[1])
				firstminima=False

			elif float(lines[i+1].split(" ")[1])<value:
				minima = lines[i+1].split(" ")[0]
				value  = float(lines[i+1].split(" ")[1])

	# print minima
	# print value

	splitTreeNodes=[]
	splitTreeEdges=[]

	def createSplitTree(node,isoval):
		#print("processing node: "+ str(node))
		splitTreeNodes.append((node,isodict[node]))
		visiteddict[node]=True
		adjnodes=adjlist[node]

		for i in range(len(adjnodes)):
			if ( isodict[adjnodes[i]] < isoval):
				continue
			else:
				if (not visiteddict[adjnodes[i]]):
					splitTreeEdges.append((node,adjnodes[i]))
					createSplitTree(adjnodes[i],isodict[adjnodes[i]])
		return

	with recursionlimit(120000):
		createSplitTree(int(minima),float(value))

	# print str(len(splitTreeNodes))+" "+str(len(splitTreeEdges))+"\n"

	# for i in range(len(splitTreeNodes)):
	# 	print splitTreeNodes[i]

	# i=0
	# while i<len(splitTreeEdges):
	# 	print str(splitTreeEdges[i])+" "+str(splitTreeEdges[i+1])
	# 	i=i+2

	#To draw split Tree
	visualizetree=open(dataFile+'_treenodes','wb')
	s=""
	s=s+"["
	for i in range(len(splitTreeNodes)):
		# print splitTreeNodes[i]
		s=s+"["
		#tmp=splitTreeNodes[i]
		s=s+str(splitTreeNodes[i][0])+", "+str(splitTreeNodes[i][1])
		if i < len(splitTreeNodes)-1:
			s=s+"],"
		else:
			s=s+"]"

	s=s+"]"
	# print s
	visualizetree.write(s)
	visualizetree.close()

	visualizetree=open(dataFile+'_treeedges','wb')
	t="["
	i=0
	while i<len(splitTreeEdges):
		t=t+"["
		t=t+str(splitTreeEdges[i][0])+", "+str(splitTreeEdges[i][1])
		if i==(len(splitTreeEdges)-1):
			t=t+"]"
		else:
			t=t+"],"
		i=i+1
	t=t+"]"
	# print t
	visualizetree.write(t)
	visualizetree.close()


	unaugST=open(dataFile + ".splittree",'w')
	unaugST.write(str(len(splitTreeNodes))+" "+str(len(splitTreeEdges))+"\n")

	Vertex=[]
	for i in range(len(splitTreeNodes)):
		Vertex.append(splitTreeNodes[i][0])
		unaugST.write(str(splitTreeNodes[i][0])+" "+str(splitTreeNodes[i][1])+"\n")

	i=0
	edgelist=[]
	while i<len(splitTreeEdges):
		unaugST.write(str(Vertex.index(splitTreeEdges[i][0]))+" "+str(Vertex.index(splitTreeEdges[i][1]))+"\n")
		edgelist.append( (Vertex.index(splitTreeEdges[i][0]), Vertex.index(splitTreeEdges[i][1]) ) )
		# unaugST.write(str(splitTreeEdges[i][0])+" "+str(splitTreeEdges[i][1])+"\n")
		i=i+1

	offfile=open(dataFile + ".off",'r') #pot file doesn't contain dimx,dimy,dimz, origin and delta
	olines=offfile.readlines()
	offfile.close()

	isoallvertexlist=[]
	num_nodes=int(olines[1].rstrip().split(" ")[0])
	for i in range(num_nodes):
		tmp=float(olines[i+2].rstrip().split(" ")[3])
		isoallvertexlist.append(tmp)

	augfile=open(partFile,'r')
	alines=augfile.readlines()
	augfile.close()

	#arcnodes store augmented grid point numbers for each edge in split tree
	arcnodes=[[] for i in range(len(splitTreeEdges))]

	for i in range(len(alines)):
		#print(i)
		edgeno=int(alines[i].rstrip())
		edge=lines[edgeno+treenodes+1].rstrip()
		a=int(edge.split(" ")[0])
		b=int(edge.split(" ")[1])
		if (i != a and i != b):
			try:
				idx1 = splitTreeEdges.index((a,b))
			except ValueError:
				idx1 = -1 
			try:
				idx2 = splitTreeEdges.index((b,a))
			except ValueError:
				idx2 =  -1

			if ( idx1 == -1 and idx2 == -1 ):
				continue
			else:
				if idx1 != -1:
					arcnodes[idx1].append((i,isoallvertexlist[i]))
				else:
					arcnodes[idx2].append((i,isoallvertexlist[i]))

	for i in range(len(arcnodes)):
		arcnodes[i].sort(key=operator.itemgetter(1),reverse=True)

	f=open(dataFile + '_arcnodes.pkl','wb')
	pickle.dump(arcnodes,f)
	f.close()

	f=open(dataFile + '_edgelist.pkl','wb')
	pickle.dump(edgelist,f)
	f.close()

	# print(arcnodes)
	# print(splitTreeEdges)
	