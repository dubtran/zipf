import graphlab as gl
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist

def getCounts(sFrame):
	numUsers = len(sFrame['userid'].unique())
	numArtist = len(sFrame['artist'].unique())
	songArtist = set(zip(sFrame['artist'], sFrame['track']))

	numSong = len(songArtist)
	print "# of users: " , numUsers
	print "# of artists: ", numArtist
	print "# of songs: ", numSong

	user666 = sFrame[sFrame['userid'] == 'user_000666']
	user666 = user666.groupby(['artist', 'track'], gl.aggregate.COUNT()).topk('Count', 1)
	print "top song for user 666:"
	print user666

	user333 = sFrame[sFrame['userid'] == 'user_000333']
	user333 = user333.groupby(['artist', 'track'], gl.aggregate.COUNT()).topk('Count', 10)
	print "top songs for user 333: " 
	print user333

def recModel(sframe, model, user = None, sim = None):
	print type(sframe)
	(train, test) = sframe.random_split(.8)
	if sim == None:
		recommends = gl.recommender.create(train, user_column = 'userid', item_column='track',
					 target_column='normal_count', method = model)
	else:
		recommends = gl.recommender.create(trainN, user_column="userid",item_column='track', 
					target_column='normal_count', method='item_similarity', similarity_type= sim)
	
	rmse = recommends.evaluate(test)
	print model ," recommender RMSE:"
	print rmse

	rec = recommends.recommend(user)
	print model , " " , user , " recommendations:"
	print rec.topk('track', 10)

def getNormal(main):
	feature = main.groupby(['userid', 'track'], gl.aggregate.COUNT())
	userSum = feature.groupby(['userid'], gl.aggregate.SUM('Count'))

	featDf = feature.to_dataframe()
	sumDf = userSum.to_dataframe()
	df = featDf.merge(sumDf, on = 'userid')

	df['normal_count']=df['Count']/df["Sum of Count"]
	df.pop('Sum of Count')
	
	return gl.SFrame(df), df 

def similarity(df):
	
	df = pd.pivot_table(df, values=['normal_count'], cols=['userid'], rows=['track']).fillna(-1)

	matrix = pdist(np.array(df), 'euclidean')

	# for i in xrange(row):
	# 	for j in xrange(i+1, rows):
	# 		vec1 = df.iloc[i,:][df.iloc[i,:] != -1]
	# 		vec2 = df.iloc[j,:][df.iloc[j,:] != -1]
	# 		matrix[i,j] = (vec1,vec2)
	# sim_matrix = matrix.T + matrix

	return matrix

def signals(sframe):
	# get most recent 
	# get longest streak
	# most consistent song
	pass

def main():

	main = gl.SFrame.read_csv('/Users/dubT/Documents/Zipfian/recommendation-systems/lastfm-dataset-1K/sample.csv')
	old = main.column_names()
	new = ['userid', 'timestamp', 'artid', 'artist', 'trackid', 'track']
	names = dict(zip(old,new))
	main.rename(names)

	getCounts(main)

	main, maindf = getNormal(main)
	subs = main[main['Count'] >= 25]
	subdf = maindf[maindf['Count'] >= 25]

	recModel(subs, model = 'item_means')
	recModel(subs, sim = 'cosine')
	recModel(subs, model = 'matrix_factorization')
	recModel(subs, model = 'linear_model')

	sims = similarity(subdf)



if __name__ == '__main__':
	main()
	