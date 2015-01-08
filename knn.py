#!/usr/bin/python
#!/usr/bin/env python
import sys
import random
from operator import itemgetter

input_pos = file(sys.argv[1])
input_neg = file(sys.argv[2])
k = int(sys.argv[3]) #k neighbours
p = float(sys.argv[4]) #minimum fraction of neighbors needed in order to classify a sample as positive
n = int(sys.argv[5]) #number of folds for cross-validation
#Create Data Matrices------------------------------------------------------------------------------------
#create positive data matrix where last feature is actually output (1 = positive)
pos = []
pos_original = []
for line in input_pos:
	row = line.strip().split("\t")
	pos.append(row)
	pos_original.append(row)
num_ft = len(pos) #number of features in each training example
pos_result = []
for i in range(num_ft):
	pos_result += [1]
pos.append(pos_result)
pos_original.append(pos_result)
pos = zip(*pos) #transposes matrix so first index is in to a training example
pos_original = zip(*pos_original)

#create negative data matrix where last feature is actually output (0 = negative)
neg = []
neg_original = []
for line in input_neg:
	row = line.strip().split("\t")
	neg.append(row)
	neg_original.append(row)
neg_result = []
for i in range(num_ft):
	neg_result += [0]
neg.append(neg_result)
neg_original.append(neg_result)
neg = zip(*neg) #transposes matrix so first index is in to a training example
neg_original = zip(*neg_original)

#find euclidean distance between two lists, with input on number of elements to compare
def euclidean(x,y,num_ft):
	sumSq=0.0
	#add up the squared differences
	for i in range(num_ft):
		sumSq+=(float(x[i])-float(y[i]))**2#take the square root of the result
	return (sumSq**0.5)

#Perform Cross-Validation------------------------------------------------------------------------------
num_pos = len(pos) #number of positive training examples
num_neg = len(neg) #number of negative training examples
random.shuffle(pos) #shuffles order of positive training examples
random.shuffle(neg) #shuffles order of negative training examples
tp = 0;
fp = 0;
tn = 0;
fn = 0;
for i in range(n):#Create test and training groups
	test = pos[(i*num_pos/n):((i+1)*num_pos/n)] + neg[(i*num_neg/n):((i+1)*num_neg/n)]
	train = []
	for j in range(n):
		if i != j:
			train += pos[(j*num_pos/n):((j+1)*num_pos/n)] + neg[(j*num_neg/n):((j+1)*num_neg/n)]
	#Run the test samples against the training samples
	for j in range(len(test)):
		distances = []
		for l in range(len(train)): #calculate distance from every training example
			distances.append([euclidean(test[j],train[l],num_ft),train[l][num_ft]])
		#take top k neighbors and look at their classification
		sorted_distances = sorted(distances, key=itemgetter(0))
		neighbors = []
		for l in range(k):
			neighbors += [sorted_distances[l][1]]
		if (float(neighbors.count(1))/k >= p):
			#Test example classified as positive...
			if test[j][num_ft] == 1:
				tp += 1
			else:
				fp += 1
		else:
			#Test example classified as negative...
			if test[j][num_ft] == 0:
				tn += 1
			else:
				fn += 1
				# print str(pos_original.index(test[j]))


#Output Results----------------------------------------------------------------------------------------
accuracy = float(tp+tn)/(tp+tn+fp+fn)
sensitivity = float(tp)/(tp+fn)
specificity = float(tn)/(tn+fp)

print "TP: " + str(tp)
print "TN: " + str(tn)
print "FP: " + str(fp)
print "FN: " + str(fn)
print "accuracy: " + str(round(accuracy,2))
print "sensitivity: " + str(round(sensitivity,2))
print "specificity: " + str(round(specificity,2)) 

out = open('knn.out', 'w+')
out.write("k: " + str(k) + '\n')
out.write("p: " + str(p) + '\n')
out.write("n: " + str(n) + '\n')
out.write("accuracy: " + str(round(accuracy,2)) + '\n')
out.write("sensitivity: " + str(round(sensitivity,2)) + '\n')
out.write("specificity: " + str(round(specificity,2)) + '\n')
