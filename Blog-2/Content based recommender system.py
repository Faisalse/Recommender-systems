# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 18:07:02 2023

@author: shefai
"""

# import required packages
import pandas as pd
import numpy as np
import math
import warnings
warnings.filterwarnings("ignore")
class PopBased:
    def __init__(self, ):
        movie_rating = pd.read_csv("movieLens/ratings.csv")
        movie_rating = movie_rating[movie_rating["rating"] > 3]
        self.movie_rating = movie_rating
        self.movie_genre = pd.read_csv("movieLens/movies.csv")  
    
    def getUserIdTask1(self):
        print("Enter the userId:          ")
        userId  = input()
        if userId.isdigit():
            userId = int(userId)
            dataframe = self.movie_rating[self.movie_rating["userId"] == userId]
            dataframe = dataframe.sort_values(by=['rating'], ascending=False)
            movies = list(dataframe["movieId"])
            df = pd.DataFrame()
            for i in movies:
                frame = [df, self.movie_genre[self.movie_genre["movieId"] == i]]
                df = pd.concat(frame)
        return df                   
    def getUserId(self):
        print("Enter the userId:          ")
        userId  = input()
        if userId.isdigit():
            userId = int(userId)
            dataframe = self.movie_rating[self.movie_rating["userId"] == userId]
            dataframe = dataframe.sort_values(by=['rating'], ascending=False)
            movies = list(dataframe["movieId"])
            df = pd.DataFrame()
            for i in movies:
                frame = [df, self.movie_genre[self.movie_genre["movieId"] == i]]
                df = pd.concat(frame) 
            print("top‐10 recommendations on the console")
            df2  = df.copy()
            df2["movieId"]
            self.analysis = df2.iloc[:20, :]
            print(df2.iloc[:20, :])            
            print("Task from 1 - 4! click desired number to see output:  ----->   ")
            errorChecking = True
            while errorChecking:
                day = int(input())
                if day == 1:
                    print("Create a user profile based on the genres of the movies. Count how often each movie genre appeared in the set of the movies that the user has liked")
                    self.genreDict = self.task1(userId, df)
                    print(self.genreDict)
                    errorChecking = False
                elif day == 2:
                    movieLiknessBasedGenreLikness, self.datafr = self.task2(self.task1(userId, df), self.movie_genre)     
                    print("Determine the similarity of each recommendable movie to this user profile")
                    print(self.datafr)
                    errorChecking = False
                elif day == 3:
                    
                    movieLiknessBasedGenreLikness, t = self.task2(self.task1(userId, df), self.movie_genre)
                    self.series, self.popDataframe = self.task3(movieLiknessBasedGenreLikness, self.movie_rating, self.movie_genre)
                    
                    print("Extend the algorithm as follows. When recommending, remove all movies that have no overlap with the given user profile. Rank the remaining items based on their popularity")
                    print(self.popDataframe)
                    errorChecking = False
                elif day == 4:
                    print("Implement a method that also considers the 'genre count' in the user profile in some form")                    
                    genreDict = self.task1(userId, df)
                    movieLiknessBasedGenreLikness, t = self.task2(genreDict, self.movie_genre)
                    self.series, self.popDataframe = self.task3(movieLiknessBasedGenreLikness, self.movie_rating, self.movie_genre)                    
                    self.mostViewedGenre = self.task4(genreDict, self.popDataframe)
                    errorChecking = False
                else:
                    print("Please, enter the correct number")
            errorChecking = True   
    def task1(self, userID, df):
        genreDict = dict()
        for inderx, row in df.iterrows():
            genreString = row["genres"]
            genreString = genreString.split("|")
            for gen in genreString:
                if gen not in genreDict:
                    genreDict[gen] = 1
            else:
                genreDict[gen] = genreDict[gen] +1
        genreDict = dict(sorted(genreDict.items(), reverse=True, key=lambda item: item[1]))
        return genreDict
     
    def task2(self, genreDict, df):
      currentUserGenderLikness = set()
      movieLiknessBasedGenreLikness = dict()
      for genres in genreDict.keys():
          currentUserGenderLikness.add(genres)
      
      for index, row in df.iterrows():
          movieGenre = set(row["genres"].split("|"))
          overlapping = len(currentUserGenderLikness.intersection(movieGenre))
          movieLiknessBasedGenreLikness[row["movieId"]] = overlapping   
          movie = sorted(movieLiknessBasedGenreLikness.items(), reverse= True, key=lambda x: x[1])
      dataframe = pd.DataFrame()
      for value in movie:
          temp = df[df["movieId"] == value[0]]
          frame = [temp, dataframe]
          dataframe = pd.concat(frame)   
      return movie, dataframe
    def task3(self, genreDict, ratingDataFrame, genredataframe):
       overlapMovies = list()
       for key in genreDict:
           if key[1] == 0:
               pass
           else:
              overlapMovies.append(key[0]) 
       temp = pd.DataFrame()
       
       for i in overlapMovies:
           temp2 = ratingDataFrame[ratingDataFrame["movieId"] == i]
           frame = [temp, temp2]
           temp = pd.concat(frame)
       temp["pop"] = 1
       
       series = temp.groupby(['movieId'])["pop"].sum()
       series = series.sort_values(ascending = False)
       
       temp1 = pd.DataFrame()
       counter = 0
       for index, item in series.items():
           temp5 = genredataframe[genredataframe["movieId"] == index]
           temp5["pop"] = item
           frame = [temp1, temp5]
           temp1 = pd.concat(frame)
           if counter > 100:
               break
           counter+=1
           
       return series, temp1

    def task4(self, genreDict, popDataframe):
        
        for key in genreDict.keys():
            for i in range(len(popDataframe)):
                genreString = popDataframe.iloc[i, 2]
                genreString = genreString.split("|")
                
                if key in genreString: 
                    popDataframe.iloc[i,3] = popDataframe.iloc[i,3] * genreDict[key]                    
        popDataframe.sort_values(by="pop", ascending = False, inplace = True)           
        return popDataframe
#%%
# TASK 1
p1 = PopBased() 
output = p1.getUserIdTask1()
output.head(10)
#%%
# TASK 2
p1 = PopBased() 
p1.getUserId()
    