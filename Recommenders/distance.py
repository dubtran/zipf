import numpy as np
def euclidean(vec1, vec2):

	return np.sum((vec2-vec1) ** 2)  ** 0.5
#return np.array((x-y)**y)**0.5	

# Define any other distance metrics here 
#
# Make sure they follow the same API:
#	INPUT: two arrays of numbers (integers or floats)
#	OUTPUT: one float