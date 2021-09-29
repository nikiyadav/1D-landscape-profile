dataFile = '../data/1grm'

f=open(dataFile + '.rg.txt','rb')
lines=f.readlines()
f.close()


num_nodes=int(lines[0].rstrip().split(" ")[0])
maxper=float(lines[1].rstrip().split(" ")[1])
l=1
for i in range(num_nodes):
	t=float(lines[i+1].rstrip().split(" ")[1])
	if t>maxper:
		maxper =  t
		l=i+1

print(maxper)
print(i)
