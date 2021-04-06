# Movie-Recommendation-System

### Datasets Preparations

Movies Data collected from below sources:-
- [the-movies-dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset)   - conatins 45000 movies , used movies released from 1970 to 2012.(file names: movies_metadata.csv , credits.csv) 
- [imdb-extensive-dataset](https://www.kaggle.com/stefanoleone992/imdb-extensive-dataset)  contains 85k movies , used movies released between 2013-2020 . (file name:IMDb_Movies.csv) 

Total Movies count after preprocessing : 47k (approx.)

The final Output (cleaned and preprocessed dataset), i have uploaded it on kaggle , so you can checck it out here [final-datasets](https://www.kaggle.com/himanshubag/movies-dataset-1970-to-2020) , for more details check out the DataPrep ipynb file.

**Movies count (2013-2020)**

![Output](img/Output2.png "Sample Output")


**Movies count (1970-2012)**
![Output1](img/Output1.png "Sample Output1")


### Content Based Filtering
**Example**: if a user likes movies such as ‘The Prestige’ then we can recommend him the movies of ‘Christian Bale’ or movies with the genre ‘Thriller’ or maybe even movies directed by ‘Christopher Nolan’. So what happens here the recommendation system checks the past preferences of the user and find the film “The Prestige”, then tries to find similar movies to that using the information available in the database such as the lead actors, the director, genre of the film, production house, etc and based on this information find movies similar to “The Prestige”.

The filtration strategy is based on the data provided about the items . The algorithm recommends products that are similar to the ones that a user has liked in the past. This similarity (generally cosine similarity) is computed from the data  we have about the items.
