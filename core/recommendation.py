import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector as connection
from devlog.settings import DATABASES


def recommendation(user_id):

    mydb = connection.connect(host=DATABASES['default']['HOST'], database =DATABASES['default']['NAME'] ,user="root", passwd=DATABASES['default']['PASSWORD'],use_pure=True)


    query = "SELECT * FROM `core_posts_likes`;"

    # load data
    data = pd.read_sql(query,mydb)

    #close the connection
    mydb.close() 

    # create user-item matrix
    user_item_matrix = data.pivot_table(index='user_id', columns='posts_id')

    # set all liked places as 1 
    user_item_matrix = user_item_matrix.where(user_item_matrix.isnull(), other=1);

    # set all unliked as 0
    user_item_matrix.fillna(0,inplace=True);

    # calculate item-item similarity matrix
    item_sim_matrix = pd.DataFrame(cosine_similarity(user_item_matrix.T), index=user_item_matrix.columns, columns=user_item_matrix.columns)



    def get_similar_items(item_id, n_similar=5):
        '''Get top n_similar similar items to item_id'''
        similar_items = item_sim_matrix[item_id].sort_values(ascending=False)[1:n_similar+1]
        return similar_items.index.tolist()
    

    def get_recommendations(user_id, n_recommendations=5):
        '''Get top n_recommendations recommendations for user_id'''
        user_items = user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] != 0].index
        similar_items = []
        for item in user_items:
            similar_items += get_similar_items(item)

        similar_items = [item for item in similar_items if item not in user_items]
        recommended_items = pd.Series(similar_items).value_counts().sort_values(ascending=False).index[:n_recommendations]
        return recommended_items.tolist()

    # usage
    user_id = user_id
    n_recommendations = 5
    recommendations = get_recommendations(user_id, n_recommendations)
    
    l = []
    for item in recommendations:
        l.append(item[1])
    return l


