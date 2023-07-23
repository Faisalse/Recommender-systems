# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 18:07:02 2023

@author: shefai
"""

# import required packages
import pandas as pd
import numpy as np
import math
class UserBasedColl:
    def __init__(self, k = 20, similarity = "cosine", recommendation = 15):
        self.k = k
        self.similarity = similarity
        self.recommendation = recommendation
        self.userToEncoding = dict()    
        self.encodingToUser = dict()    
        self.itemToEncoding = dict()
        self.encodingToItem = dict()
        self.userid_similarity_dic = dict()       
    def user_item_dic(self, movie_rating):        
        # movie_rating is a dataframe that contains userId, itemId and rating.. 
        userid_itemid_dic = dict()        
        for index, row in movie_rating.iterrows():
            if row["userId"] not in userid_itemid_dic:
                userid_itemid_dic[int(row["userId"])] = {int(row["movieId"]): row["rating"]}
            else:
                userid_itemid_dic[row["userId"]][int(row["movieId"])] = row["rating"]
        # encoding     
        itemCounter = 0
        userCounter = 0
        userToEncoding = dict()    
        encodingToUser = dict()    
        itemToEncoding = dict()
        encodingToItem = dict()
        userid_itemid_dic_temp = userid_itemid_dic.copy()

        for key in userid_itemid_dic:
            if key not in userToEncoding:
                userToEncoding[key] = userCounter
                encodingToUser[userCounter] = key
                userid_itemid_dic_temp[userCounter] = userid_itemid_dic_temp.pop(key)
                userCounter +=1        
        userid_itemid_dic = userid_itemid_dic_temp.copy()
        userid_itemid_dic_temp = userid_itemid_dic.copy()

        
        for key in userid_itemid_dic:
            temp = userid_itemid_dic[key].copy()
            
            for key2 in userid_itemid_dic[key]:
                if key2 not in itemToEncoding:
                    itemToEncoding[key2] = itemCounter
                    encodingToItem[itemCounter] = key2
                    temp[itemCounter] = temp.pop(key2)
                    itemCounter +=1    
                else:
                    temp[itemToEncoding[key2]] = temp.pop(key2)
            
            userid_itemid_dic_temp[key] = temp  

        userid_itemid_dic = userid_itemid_dic_temp.copy()
        
        
        numberOfitem = len(movie_rating["movieId"].unique())
        numberOfuser = len(movie_rating["userId"].unique())
        
        matrix = np.zeros((numberOfuser, numberOfitem))
        
        for key in userid_itemid_dic:
            for key2 in userid_itemid_dic[key]:
                matrix[key][key2] = userid_itemid_dic[key][key2]
        
        return matrix, userToEncoding, encodingToUser, itemToEncoding, encodingToItem
    
    def fit(self, train):
        self.userid_itemid_rating_matrix, self.userToEncoding, self.encodingToUser, self.itemToEncoding, self.encodingToItem = self.user_item_dic(train)
        self.userid_similarity_dic = self.user_simi_dic(self.userid_itemid_rating_matrix)
    
    def cosine(self, u1, u2):
        # u1 and u2 are two vectors..
        sumtotal = 0
        u1Sum = 0
        u2Sum = 0
        for i in range(len(u1)):
            
            sumtotal += u1[i] * u2[i]
            u1Sum += math.pow(u1[i], 2)
            u2Sum += math.pow(u2[i], 2)
            
        # to avoid division from zero.... 
        if u1Sum ==0 or u2Sum == 0:
            return 0
        return sumtotal  / (math.sqrt(u1Sum) * math.sqrt(u2Sum) ) 
    
    def user_simi_dic(self, matrix):
        user_simi_d = dict()
        for user in range(matrix.shape[0]):
            
            scoreList = list()
            first = matrix[user]
            for user1 in range(matrix.shape[0]):
                second = matrix[user1]
                score = getattr(self, self.similarity)( first, second)
                scoreList.append(score)
             
            temp = list(np.argpartition(np.array(scoreList), -self.k)[-self.k:])
            
            tempDic = dict()

            for i in temp:
                tempDic[i] = scoreList[i]
            user_simi_d.update({user : tempDic})
        return user_simi_d
    
    def getUser(self, movieRating, movieGenre):
        loopChecking = True
        while loopChecking:
            print("Enter the UserId")
            input1 = input()
            
            print("Users already seen movies"+"\n")
            moviesWatchUsers = movieRating[movieRating["userId"] == int(input1)]
            
            moviesWatchUsers = list(moviesWatchUsers["movieId"])
            
           
            dataframe = pd.DataFrame()
            
            for i in moviesWatchUsers:
                frame1 = [dataframe, movieGenre[movieGenre["movieId"] == i] ]
                dataframe = pd.concat(frame1)
            
            del dataframe["movieId"]
            
            print(dataframe.iloc[:10])
            
            print("----------------------------------------------------------------------"+"\n")
            print("----------------------------------------------------------------------"+"\n")
            
            print("TopK recommendations"+"\n")
            
            if input1.isdigit():
                
                userId = self.userToEncoding[int(input1)]
                similarUsers = self.getSimilarUsers(userId)
                
                del similarUsers[userId]
                getUserMoviesWithRatingss = self.getUserMoviesWithRatings(similarUsers, userId)
                
                
                # multiply the movie rating of each user with similarity score.....
                
                for key in similarUsers:
                    for key2 in getUserMoviesWithRatingss[key]:
                        getUserMoviesWithRatingss[key][key2] = getUserMoviesWithRatingss[key][key2] * similarUsers[key]
                        
                
                # if it is possible that some users may be watch similar types of movies. If users have similar types of movies
                # then add thier weitage score....
                tempdict = dict()
                for values in getUserMoviesWithRatingss.values():
                    
                    for i in values:
                        if i not in tempdict.keys():
                            tempdict[i] = values[i] 
                        else:
                            tempdict[i] = tempdict[i] + values[i]
                tempdict = sorted(tempdict.items(), key=lambda x: x[1], reverse=True)
                temp = list()
                
                for i in tempdict:
                    temp.append(i[0])
                recommenderMovies = self.recommendations(temp, movieGenre)
                print(recommenderMovies)
                loopChecking = False
            else:
                print("Please, enter valid User Id")
    def getSimilarUsers(self, user1):
        return self.userid_similarity_dic[user1]
    
    def getUserMoviesWithRatings(self, similarUsers, userId):
        temp1 = dict()
        
        for key in similarUsers.keys():
            temp1[key] = self.userid_similarity_dic[key]
            
        temp2 = self.userid_similarity_dic[userId]
        for key in temp1.keys():
            for key2 in temp2.keys():
                if key2 in temp1[key]:
                    del temp1[key][key2]       
        return temp1    
    def recommendations(self, user1, recommendation):
        encodingToItem = list()
        
        for i in user1:
            encodingToItem.append(self.encodingToUser[i])    
        encodingToItem = encodingToItem[:self.recommendation]        
        dataframe = pd.DataFrame()        
        for i in encodingToItem:
            frame1 = [dataframe, recommendation[recommendation["movieId"] ==i] ]
            dataframe = pd.concat(frame1)
        
        del dataframe["movieId"]
        return dataframe            
#%%
p1 = UserBasedColl(20, "cosine")  
movie_rating = pd.read_csv("movieLens/ratings.csv")
movie_rating = movie_rating.iloc[:5000, :]
movie_genre = pd.read_csv("movieLens/movies.csv")
# call fiting function....
p1.fit(movie_rating)
#%%
p1.getUser(movie_rating, movie_genre)
