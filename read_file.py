import numpy as np

f = np.fromfile(open("results"))

#with open("results2", "a") as g:
#	for num in f:
#		g.write(str(num))

#for num in f:
	#if num != 0:
		#print(num)
vector = []
for num in f:
	vector.append(num)

print(vector)
