'''

    This contains code for predicting simillar movies by querying the csv data files
    created and stored at ./data/ .

    TO DO :
      - request lib to fetch additional movie details from imdb website
    
'''

from numpy.testing._private.utils import break_cycles
import pandas as pd


def read_csv_files():
    try:
        id_list1 = pd.read_csv('./data/id_to_title_list1.csv')
        id_list2 = pd.read_csv('./data/id_to_title_list2.csv')
        cosine_list1 = pd.read_csv('./data/top_50_cosine_values_list1.csv')
        cosine_list2 = pd.read_csv('./data/top_50_cosine_values_list2.csv')

        return cosine_list1,cosine_list2,id_list1,id_list2
    except FileNotFoundError:
        print('Error in read_csv_files function: '+'Csv Files not found !!')
        return {},{},{},{}
    except Exception as e:
        print('Error in read_csv_files function: '+str(e))
        return {},{},{},{}


def id_to_title(m_id,id_list1,id_list2):
    try:
        title1 = id_list1[id_list1['movie_id']==m_id]
        title2 = id_list2[id_list2['movie_id']==m_id]
        imdb_id,title='',''
        if not title1.empty:
            title1_dict = list(title1.to_dict('index').values())[0]
            imdb_id,title = title1_dict['imdb_id'],title1_dict['title']
        elif not title2.empty:
            title2_dict = list(title2.to_dict('index').values())[0]
            imdb_id,title = title2_dict['imdb_id'],title2_dict['title']
        return imdb_id,title
    except Exception as e:
        print('Error in id_2_title function: '+str(e))
        return '',''



def title_to_id(name,id_list1,id_list2):
    try:
        id1 = id_list1[id_list1['title'].str.lower()==name.lower()]
        id2 = id_list2[id_list2['title'].str.lower()==name.lower()]
        movie_id,imdb_id,title='','',''
        flag=False
        if not id1.empty:
            movie_id,imdb_id,flag = id1['movie_id'][0],id1['imdb_id'][0],True
        elif not id2.empty:
            movie_id,imdb_id,flag = id2['movie_id'][0],id2['imdb_id'][0],True
    
        return movie_id,imdb_id,flag
    except Exception as e:
        print('Error in title_2_id function: '+str(e))
        return '','',False

def get_cosine_matrix(id,cosine_list1,cosine_list2):
    try:
        val1 = cosine_list1[cosine_list1['movie_id']==id]
        val2 = cosine_list2[cosine_list2['movie_id']==id]
        l={}
        if not val1.empty:
            l = val1.to_dict('index')
        elif not val2.empty:
            l = val2.to_dict('index')
        return l[0]
    except Exception as e:
        print('Error in get_cosine_matrix function: '+str(e))
        return {}


def main():
    try:
        movie_name = str(input('Enter your movies : '))
        cosine_list1,cosine_list2,id_list1,id_list2= read_csv_files()
        movie_id,imdb_id,id_found = title_to_id(movie_name,id_list1,id_list2)
        if not id_found:
            print('Movie not found in our DB !!')
            return
        movie_mat= get_cosine_matrix(movie_id,cosine_list1,cosine_list2)
        result = []
        for idx in range(1,50):
            temp = movie_mat[str(idx)].replace('(','').replace(')','').split(',')
            m_score,m_id = round(float(temp[1].strip())*100,2),int(temp[0])
            temp = [round(float(j.strip()),2) for j in temp]
            m_imdbid,m_name = id_to_title(m_id,id_list1,id_list2)
            result.append([m_name,m_score,m_imdbid])
        for m in result:
            print(m[0],m[1],m[2])
    except Exception as e:
        print('Error in Main funtion: '+str(e))
        return





main()
