'''

    This contains code for predicting simillar movies by querying the csv data files
    created and stored at ./data/ .

    TO DO :
      - request lib to fetch additional movie details from imdb website < done > test.py

      what if 2 movie avengers one in list 1, one in list 2
       ---> improve title_to_id function 
    
'''

from numpy.testing._private.utils import break_cycles
import pandas as pd
import requests
from bs4 import BeautifulSoup



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
        if (not id1.empty) and (not id2.empty):
            # pass
        elif not id1.empty:
            id1_dict = list(id1.to_dict('index').values())
            return id1_dict
        elif not id2.empty:
            id2_dict = list(id2.to_dict('index').values())
            return id2_dict
        return ''
    except Exception as e:
        print('Error in title_2_id function: '+str(e))
        return ''

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


def getMovieDetails(imdb_id):
    try:
        data = {}
        url = 'https://www.imdb.com/title/'+imdb_id
        r = requests.get(url=url)
        soup = BeautifulSoup(r.text, 'html.parser')

        title = soup.find("h1",{"data-testid":"hero-title-block__title"})
        data['title']=title.text

        release_data = soup.find('ul',{'data-testid':'hero-title-block__metadata'})
        temp_data =  release_data.find_all('li')
        data['r_year']=temp_data[0].text[:4]
        data['runtime'] = temp_data[-1].text

        score = soup.find('div',{'data-testid':'hero-rating-bar__aggregate-rating'})
        temp_score = score.find_all('div')[1].text.split('/10')
        data['rating'], data['ratings_count'] = temp_score[0],temp_score[1]

        genres = soup.find('div',{'data-testid':'genres'}).find_all('span')
        genres_list = [i.text for i in genres]
        data['genres']=genres_list

        cast_list = soup.find_all('div',{'data-testid':'title-cast-item'})
        full_cast_list = []
        for i in cast_list :
            real_name = i.find('a',{'data-testid':'title-cast-item__actor'}).text
            stage_name = i.find('span',{'class':'StyledComponents__CharacterNameWithoutAs-y9ygcu-5 iaZZDn'}).text
            full_cast_list.append([real_name,stage_name])
        data['full_cast_names']=full_cast_list

        plot = soup.find('span',{'data-testid':'plot-xs_to_m'}).text
        data['plot'] = plot

        # print('\n')
        # print(data)
        return data
    except Exception as e:
        print('Error in (IMDB fetch)'+str(e))
        return ''
 

def main():
    try:
        movie_name = str(input('Enter your movie : '))
        movie_name = movie_name.strip()
        cosine_list1,cosine_list2,id_list1,id_list2= read_csv_files()
        input_movie_details = title_to_id(movie_name,id_list1,id_list2)
        if input_movie_details=='':
            print('Movie not found in our DB !!')
            return
        if len(input_movie_details)>1:
            print('\tThere are multiple movies with the same title !!')
            print(input_movie_details)
            pass
        else:
            movie_id = input_movie_details[0]['movie_id']
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
