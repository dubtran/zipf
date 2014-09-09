import json, pdb
import numpy as np
import distance
import pandas as pd


class Recommender:

	def __init__(self, products_file):
		self.users = set()
		columns=['user_id', 'movie_id', 'rating', 'timestamp']
		self.data = self.pandaData('../data/u.data', '\t', columns)
		columns=['user_id', 'age', 'gender', 'occupation', 'zip code']
		self.user = self.pandaData('../data/u.user', columns = columns)
		columns=['movie_id', 'movie_title', 'release date', 'video release date',
              'IMDb URL', 'unknown', 'Action', 'Adventure', 'Animation',
              "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
              'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
              'Thriller', 'War', 'Western']
		self.item = self.pandaData('../data/u.item',columns = columns)
		self.genre = self.pandaData('../data/u.genre')
		self.main = self.build_feature_matrix()

		self.main = self.main.iloc[:10,:10]
		self.rows, self.cols = self.main.shape
		self.sim = self.compute_similarity()
		self.personal = {i+1:self.build_personal_matrix(i+1) for i in xrange(self.rows)}
		self.personalsum = {i+1:self.normalized_sum(i+1) for i in xrange(self.rows)}

	
	def build_feature_matrix(self):
		main = pd.merge(self.data, self.item, how='inner', on='movie_id')
		main = pd.pivot_table(main, values=['rating'], cols=['user_id'], rows=['movie_id'])
		main = main.fillna(-1)
		return main

	def compute_similarity(self):
		sim_matrix = np.zeros((self.rows, self.rows))
		for i in xrange(self.rows):
			for j in xrange(i+1,self.rows):
				vec1 = self.main.iloc[i,:][self.main.iloc[i,:] != -1]
				vec2 = self.main.iloc[j,:][self.main.iloc[j,:] != -1]
				sim_matrix[i,j] = distance.euclidean(vec1,vec2)
		sim_matrix = sim_matrix.T + sim_matrix

		return sim_matrix

	def normalized_sum(self):
		return self.personal[user].iloc[:,np.arange(2,self.personal[user].shape[1],2)].mean()		

	def get_top_n_recommendations(self, user, n):
		inds = np.argsort(self.personalsum[user].values)[:-n-1:-1]
 		print 'Top ' + str(n) + ' Recommended Movies for User ' + str(user) + ':\t'
 		for ind in inds:
 			num = int(self.personalsum[user].keys()[ind].split('_')[1])
 			title = self.item[self.item['movie_id'] == num]['movie_title'].values[0]
 			print '\tMovie: ' + title
 			print '\tPredicted rating: ' + str(self.personalsum[user].values[ind]) + '\n'
	#get top ten according to weight

	def pandaData(self, filex, delim = '|', columns =[]):
		data = pd.read_csv(filex, delimiter = delim, header = None)
		if columns != []:
			data.columns = columns
		return data

	def build_personal_matrix(self,user):
		#movies seen x (rating, unseen sim, unseen weighted)
		personal = pd.DataFrame(self.main[self.main['rating'][user] != -1]['rating'][user])
		personal.columns = ['rating']
		print personal
		unseen = np.array(self.main['rating'][2][self.main['rating'][2] ==-1].reset_index()['movie_id'])
		seen = np.array(self.main['rating'][2][self.main['rating'][2] !=-1].reset_index()['movie_id'])
		print unseen
		print seen
		for movie in unseen:
			colsim = str(movie) +' sim'
			personal[colsim] = self.sim[movie-1,:][seen-1]
			colw = str(movie)+ ' weight'
			personal[colw] = np.multiply(personal[colsim], personal['rating'])

		return personal
		
			






