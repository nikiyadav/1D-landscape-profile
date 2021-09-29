import sys
import extractST_OFF
import calHillWidth_OFF
import extractST_RAW
import calcHillWidth_RAW

fileName=sys.argv[1]
fileType=fileName.split(".")[-1]

jointreeFile=sys.argv[2]
augFile=sys.argv[3]

# use output redirection to store json file.
if (fileType == 'off' or fileType == "OFF"):
	# takes input (off file, join tree file, augmentation file)
	# Generates files : .splittree, _arcnodes.pkl, _edgelist.pkl, _treenodes, _treeedges 
	extractST_OFF.extractST(fileName,jointreeFile,augFile)
	calHillWidth_OFF.calc(fileName) 

elif (fileType == 'raw' or fileType == "RAW"):
	# raw file doesn't contain dimx,dimy,dimz, origin and delta information
	# takes input (raw file, join tree file, augmentation file)
	# Generates files : .splittree, _arcnodes.pkl, _edgelist.pkl, _treenodes, _treeedges 
	extractST_RAW.extractST(fileName,jointreeFile,augFile)
	calcHillWidth_RAW.calc(fileName) 