'''

    This contains code for predicting simillar movies given the  movie name.

    TO DO :
      - write a main function to deal with main values
      - request lib to fetch additional movie details from imdb website
    
'''
import argparse
from numpy.testing._private.utils import break_cycles
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-m','--movie',help='movie name',type=str)

args = parser.parse_args()
movie_name = args.movie


def read_csv_files():
    try:
        id_list1 = pd.read_csv('./data/id_to_title_list1.csv')
        id_list2 = pd.read_csv('./data/id_to_title_list2.csv')
        cosine_list1 = pd.read_csv('./data/top_50_cosine_values_list1.csv')
        cosine_list2 = pd.read_csv('./data/top_50_cosine_values_list2.csv')

        return cosine_list1,cosine_list2,id_list1,id_list2,True
    except FileNotFoundError:
        print(' Csv Files not found !!')
        return {},{},{},{},False
    except Exception as e:
        print(str(e))
        return {},{},{},{},False


def id_to_title(m_id,id_list1,id_list2):
    try:
        title1 = id_list1[id_list1['movie_id']==m_id]
        title2 = id_list2[id_list2['movie_id']==m_id]
        if not title1.empty:
            return title1['title'].to_dict()
        elif not title2.empty:
            return title2['title'].to_dict()
        return ''
    except Exception as e:
        print(str(e))



def title_to_id(name,id_list1,id_list2):
    try:
        id1 = id_list1[id_list1['title'].str.lower()==name.lower()]
        id2 = id_list2[id_list2['title'].str.lower()==name.lower()]
        movie_id,imdb_id,title='','',''
        flag=False
        if not id1.empty:
            movie_id,imdb_id,title,flag = id1['movie_id'][0],id1['imdb_id'][0],id1['title'][0],True
        elif not id2.empty:
            movie_id,imdb_id,title,flag = id2['movie_id'][0],id2['imdb_id'][0],id2['title'][0],True
    
        return movie_id,imdb_id,title,flag
    except Exception as e:
        print(str(e))
        return '','','',False

def get_cosine_matrix(id,cosine_list1,cosine_list2):
    try:
        val1 = cosine_list1[cosine_list1['movie_id']==id]
        val2 = cosine_list2[cosine_list2['movie_id']==id]
        l={}
        flag=False
        if not val1.empty:
            l = val1.to_dict('index')
            flag=True
        elif not val2.empty:
            l = val2.to_dict('index')
            flag=True
        return l[0],flag
    except Exception as e:
        print(str(e))
        return {},False



cosine_list1,cosine_list2,id_list1,id_list2,file_found = read_csv_files()

movie_id,imdb_id,title,id_found = title_to_id(movie_name,id_list1,id_list2)
print(id_found)
print('Movie Name : ',title)
cosine_matrix,matrix_found = get_cosine_matrix(movie_id,cosine_list1,cosine_list2)
#print(cosine_matrix)
result=[]
for idx in range(1,50):
    temp = cosine_matrix[str(idx)]
    #print('1st: ',temp)
    temp = temp.replace('(','').replace(')','').split(',')
    #print('2nd: ',temp)
    temp = [round(float(j.strip()),2) for j in temp]
    m_name = id_to_title(int(temp[0]),id_list1,id_list2)
    result.append([list(m_name.values())[0],temp[1]])

for i in result[:20]:
    print(i[0])