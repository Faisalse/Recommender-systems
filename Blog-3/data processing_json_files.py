# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:28:38 2023

@author: shefai
"""

import pandas as pd
import os.path
import json 

folderpath = r"ml_latest/"    
filepaths  = [os.path.join(folderpath, name) for name in os.listdir(folderpath)]
df = pd.DataFrame()
counter  = 1
for path in filepaths:
    with open(path, encoding="utf8") as json_file:
        data = json.load(json_file)    
    tempDict = dict()  
    # MovieLens
    if "movielens" in data:
        
        #1
        if "actors" in data["movielens"]:
            actors = data["movielens"]["actors"]
            tempAct = ""
            for act in actors:
                tempAct = tempAct+","+act
            tempDict["actors"] = tempAct
        else:
            tempDict["actors"] = None
        
        #2
        if "directors" in data["movielens"]:
            directors = data["movielens"]["directors"]
            
            if len(directors) > 0:
                tempDict["directors"] = directors[0]
            else: 
                tempDict["directors"] = directors
        else:
            tempDict["directors"] = None      
        #3
        tempDict["Id"] = data["movielensId"]
        #4
        tempDict["summary"] = data["movielens"]["plotSummary"]
        #5
        tempDict["date"] = data["movielens"]["releaseDate"]
        #6
        tempDict["year"] = data["movielens"]["releaseYear"]
        if "imdb" in data:
            #7
            if "reviews" in data["imdb"]:
                reviews = data["imdb"]["reviews"]
                if reviews is None:
                    tempDict["reviews"] = None
                else:
                    
                    tempRev = ""
                    if type(reviews) == str:
                        tempDict = reviews
                    else:
                        for rev in reviews:
                            tempRev = tempRev +","+rev   
                        tempDict["reviews"] = tempRev    
            else:
                tempDict["reviews"] = None
            
            #8
            if "synopsis" in data["imdb"]:
                synop = data["imdb"]["synopsis"]
                
                if synop is None:
                    tempDict["synopsis"] = None
                else:
                    
                    if type(synop) is list:
                        temp = ""
                        for sy in synop:
                           temp = temp+","+sy
                    if type(synop) is str:
                        tempDict["synopsis"] = synop 
            else:
                tempDict["synopsis"] = None
            #9
            if "adult" in data["imdb"]:
                tempDict["adult"] = data["tmdb"]["adult"] 
            else:
                tempDict["adult"] = None
            
        #10    
        if "tmdb" in data:
            if "keywords" in data["tmdb"]:
                
                keyword = data["tmdb"]["keywords"]
                
                if keyword is None:
                    tempDict["keyword"] = None
                else:
                    if type(keyword) is list:
                        temp = ""
                        for sy in keyword:
                           temp = temp+","+sy["name"]
                         
                        tempDict["keyword"] = temp  
                    if type(keyword) is str:
                        tempDict["keyword"] = keyword 
            else:
                tempDict["keyword"] = None
        else:
            tempDict["keyword"] = None
        frame = [df, pd.DataFrame(tempDict, index =[0])]
        df = pd.concat(frame)
        counter +=1
        if counter == 22000:
            break

data = df
data.info()

del data["synopsis"]
del data["adult"]
data.dropna(inplace = True)

## add.......
# title and rating to datasets
movie = pd.read_csv("MovieLens/movies.csv")
rating = pd.read_csv("MovieLens/ratings.csv")
movieId_genre = dict(zip(movie.movieId, movie.genres))
movieId_title = dict(zip(movie.movieId, movie.title))
movieId_rating = dict(zip(rating.movieId, rating.rating))

deletedList = list()
for id in list(data['Id']):
    if id in movieId_genre and id in movieId_title and id in movieId_rating:
        pass
    else: 
        deletedList.append(id)
for delete in deletedList:
    data = data[data["Id"] != delete]
temp1 = list()
temp2 = list()
temp3 = list()
for id in list(data['Id']):
        temp1.append(movieId_genre[id])
        temp2.append(movieId_title[id])
        temp3.append(movieId_rating[id])

data["genres"] = temp1
data["title"] = temp2
data["rating"] = temp3
# finally save dataset to conduct further tasks...
data.to_csv("data.txt", sep = "\t", index = False)        
    
    
    
    
    
    
    
    
    
 
    
        


     
     
    
    
