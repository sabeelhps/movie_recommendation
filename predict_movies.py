import numpy as np
import pandas as pd
import warnings 

warnings.filterwarnings('ignore')

columns_name=["user_id","item_id","rating","timestamp"]

df=pd.read_csv("ml-100k/u.data",sep='\t',names=columns_name)

movie_titles=pd.read_csv("ml-100k/u.item",sep="\|",header=None)

movie_titles=movie_titles[[0,1]]
movie_titles.columns=['item_id','title']

df=pd.merge(df,movie_titles,on="item_id")

ratings=pd.DataFrame(df.groupby('title').mean()['rating'])

ratings['no of ratings']=pd.DataFrame(pd.DataFrame(df.groupby('title').count()['rating']))

ratings=ratings.sort_values(by='rating',ascending=False)

moviemat = df.pivot_table(index="user_id",columns="title",values="rating")

def predictMovies(movie_name):
    
#   finding the ratings given by all the users to that movie  
    movie_user_ratings=moviemat[movie_name]
    
#     find the correlation of given movie with all other movies
    similar_to_movie_name = moviemat.corrwith(movie_user_ratings)
    
#     convert the given correlation into a data frame by giving column name=correlation
    corr_movie_name = pd.DataFrame(similar_to_movie_name,columns=['correlation'])
    
#     we will drop all those values(Nan) i.e user who have not watched given movies and the other movies
    corr_movie_name.dropna(inplace=True)
    
#     we will join the correlation data frame with no.of ratings
    corr_movie_name = corr_movie_name.join(ratings['no of ratings'])
    
#     we will take only those movies which have more than 100 ratings
    predictions=corr_movie_name[corr_movie_name['no of ratings']>100].sort_values('correlation',ascending=False)
    
    return predictions.reset_index().values.tolist()


# predictions=predictMovies("Raiders of the Lost Ark (1981)")
# for i in range(6):
#     print(predictions[i][0])
    