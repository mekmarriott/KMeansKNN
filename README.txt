BMI 214
Programming Project 2

Instructions: 
Run the md program with 'python md_em073094.py --iF input_file ###########################

PSEUDOCODE for N-Fold Validation

#where 'positive', 'negative' are the arrays of data points
n_fold_validation(k, p, positive, negative)
	add one more element at the end of every data point indicating whether it is 'positive' or 'negative'
	shuffle data points in positive, negative
	divide positive, negative in to roughly k parts.
	initialize variables 'tp','fp','tn','fn'
	for i from 0 to k-1:
		combine the ith partition of positive, negative into 'test'
		combine everything but the ith partition into 'train'
		for every data point in test:
			create data structure 'distances'
			for every data point in train:
				calculate euclidean distance between test and train data point
				insert (distance, indicator of train data point) into 'distances'
			sort 'distances' by the distance value
			take the first k elements in 'distances'
			count the 'positive' indicators among these elements and divide by k
			if this ratio is greater than p:
				if the indicator of the test data point is positive, increment 'tp'
				else increment 'fp'
			else:
				if the indicator of the test data point is negative, increment 'tn'
				else increment 'fn'
	output accuracy ((tn+tp)/(tn+tp+fn+fp)), sensitivity (tp/(tp+fn)), specificity (tn/(tn+fp))

---------------------------------------------------------------------------------------------------------------

PSEUDOCODE for K-Means

#where 'centroids' is either initialized already or empty
kmeans(k, max, data, centroids)
	if no initial centroids provided:
		for k times:
			create centroid, insert in to 'centroids'
			for each dimension:
				set respective value in centroid as random value within (min,max) of data for that dimension
	initialize 'assignments', 'iterations' = max
	for max times:
		create copy of 'centroids', 'new_centroids'
		for each data point in data:
			create data structure 'distances'
			for each centroid in 'centroids':
				calculate euclidean distance between data point and centroid
				insert distance into 'distances'
			update corresponding value in 'assignments' to index of min value in 'distances' (=index of centroid in 'centroids')
		for each centroid in 'new centroids:
			from 'assignments', find all data points mapping to this centroid's index
			update centroid as average of found data points
		if 'centroid' equals 'new_centroids':
			set 'iterations' to current iteration, and break
		else:
			set 'centroid' to 'new_centroids'
	output 'assignments' and 'iterations'




