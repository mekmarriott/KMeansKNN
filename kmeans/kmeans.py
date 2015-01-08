#!/usr/bin/python
#!/usr/bin/env python

import sys
import random
from operator import itemgetter


if len(sys.argv[0]) < 4:
	print "Not enough arguments"
	print str(sys.argv[0])
	sys.exit()

k = int(sys.argv[1]) #number of centroids
data = file(sys.argv[2]) #cluster assignments
max_it = int(sys.argv[3]) #maximum iterations allowede

#Read in data
dm = []
for line in data:
	row = line.strip().split("\t")
	row = [float(i) for i in row]
	dm.append(row) #add all gene expression levels for that data point
# print dm

dm_t = zip(*dm) #transpose to access by feature first, and then data point
num_ft = len(dm_t) #number of features
num_data = len(dm) #number pf data points

#Initialize centroids
centroids = []
if len(sys.argv) > 4:
	initial = file(sys.argv[4])
	for line in initial:
		row = line.strip().split("\t")
		row = [float(i) for i in row]
		centroids.append(row)
	if k < len(centroids):
		centroids = centroids[:k]
	else:
		k = len(centroids)
else:
	for i in range(num_ft):
		arr = []
		for j in range(k):
			arr.append(random.uniform(min(dm_t[i]),max(dm_t[i]))) #generate coordinate in feature range
		centroids.append(arr)
	centroids = zip(*centroids) #transpose back to access by cluster first, and then feature

#find euclidean distance between two lists, with input on number of elements to compare
def euclidean(x,y,num_ft):
	sumSq=0.0
	#add up the squared differences
	for i in range(num_ft):
		sumSq+=(x[i]-y[i])**2#take the square root of the result
	return (sumSq**0.5)

def assign_clusters():
	assignments = []
	for i in range(num_data):
		results = []
		for j in range(k):
			results.append([euclidean(dm[i],centroids[j],num_ft),j])
		results = zip(*results)
		assignments.append(results[1][results[0].index(min(results[0]))])
	return assignments

#Perform kmeans algorithm
def move_centroids(assignments):
	clusters = []
	for i in range(k):
		cluster_points = []
		#find data points belonging to that cluster
		for j in range(num_data):
			if (assignments[j] == i):
				cluster_points.append(dm[j]) #add data point that belongs to this cluster
		num_cluster_points = len(cluster_points)
		#find new centroid point by averaging each dimension/feature
		if (num_cluster_points > 0):
			cluster_points = zip(*cluster_points) #index by feature/dimension first
			new_centroid = []
			for dim in cluster_points:
				new_centroid.append(sum(dim)/num_cluster_points)
			clusters.append(new_centroid)
		else:
			clusters.append(centroids[i])
	return clusters

#Run KMeans Algorithm and output
it = max_it
for i in range(max_it):
	assignments = assign_clusters()
	clusters = move_centroids(assignments)
	if (centroids == clusters):
		it = i+1
		break
	else:
		centroids = clusters

out = open('sample.out', 'w+')
for j in range(num_data):
	out.write(str(j+1) + '\t' + str(assignments[j]) + '\n')
out.write("iterations: " + str(it))

