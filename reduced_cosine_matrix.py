
'''
    Reducing the size of cosine matrix , so that it will be easy for main code to open file

    given the file name , we read the pickle file which contains 
    the cosine matrix in a dataframe format (which was generated through kaggle kernel),
    as it is a large file , we will sort the values for each row in 
    descneding order and store only top 50 (per rows or movie).
'''


import pandas as pd


def generate_top_50(file_name,cnt):
    try:
        df=pd.read_pickle('./data/'+file_name)
        print(df.shape)
        l={}
        for i in range(df.shape[0]):
            sorted_row = df[i].sort_values(ascending=False)
            sorted_row = sorted_row[:50]
            final_row = [(v[0],v[1]) for v in sorted_row.iteritems()]
            l[i]=final_row
        temp_df = pd.DataFrame.from_dict(l,orient='index')
        print(temp_df.shape)
        #temp_df.head()
        if cnt==1:
            temp_df.to_csv('./data/top_50_cosine_values_list1.csv')
        else:
            temp_df.to_csv('./data/top_50_cosine_values_list2.csv')

        if cnt==1:
            df12 = pd.read_csv('./data/top_50_cosine_values_list1.csv')
            df12.rename(columns={'Unnamed: 0':'movie_id'},inplace=True)
            df12.to_csv('./data/top_50_cosine_values_list1.csv',index=False)
        elif cnt==2:
            df12 = pd.read_csv('./data/top_50_cosine_values_list2.csv')
            df12.rename(columns={'Unnamed: 0':'movie_id'},inplace=True)
            df12.to_csv('./data/top_50_cosine_values_list2.csv',index=False)
    
    except Exception as e:
        print(str(e))

'''
    cosine_matrix_list1.pkl (file size :4gb)
    cosine_matrix_list2.pkl (file size : 2.1gb)

    cause they had 2d matrix dataframe of size (28k,28k) and (19k,19k)  respectively.
    so we reduced it to store only top 50 (28k,50) and (19k,50) respectively.
    
'''

generate_top_50('cosine_matrix_list1.pkl',1)
generate_top_50('cosine_matrix_list2.pkl',2)  # cnt=1 for list1 , cnt=2 for list2