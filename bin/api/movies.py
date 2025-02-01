import pandas as pd
import numpy as np
import ast
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.stem import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

ps = PorterStemmer()


def process_dataset():
    movies=pd.read_csv('../../data/tmdb_5000_movies.csv')
    credits = pd.read_csv('../../data/tmdb_5000_credits.csv')
    movies = movies.merge(credits, on='title')
    movies = pd.DataFrame(movies[['movie_id', 'title', 'overview','genres', 'keywords', 'cast','crew']])
    movies.dropna(inplace=True)
    return(movies)


def stems(text):
    l=[]
    for i in text.split():
        l.append(ps.stem(i))
    return(" ".join(l))


def get_similar():
    movies = process_dataset()
    movies['genres'] = movies['genres'].apply(lambda x: [i['name'] for i in ast.literal_eval(x)])
    movies['keywords'] = movies['keywords'].apply(lambda x: [i['name'] for i in ast.literal_eval(x)])
    movies['cast'] = movies['cast'].apply(lambda x: [i['name'] for i in ast.literal_eval(x)])
    movies['crew'] = movies['crew'].apply(lambda x: [i['name'] for i in ast.literal_eval(x)])
    movies['overview'] = movies['overview'].apply(lambda x: x.split())
    movies['overview'] = movies['overview'].apply(lambda x: [ps.stem(i) for i in x])
    movies['genres'] = movies['genres'].apply(lambda x: [ps.stem(i) for i in x])
    movies['keywords'] = movies['keywords'].apply(lambda x: [ps.stem(i) for i in x])
    movies['cast'] = movies['cast'].apply(lambda x: [ps.stem(i) for i in x])
    movies['crew'] = movies['crew'].apply(lambda x: [ps.stem(i) for i in x])

    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    movies = movies.drop('overview', axis=1)
    movies = movies.drop('genres', axis=1)
    movies = movies.drop('keywords', axis=1)
    movies = movies.drop('cast', axis=1)
    movies = movies.drop('crew', axis=1)

    movies ['tags'] = movies ['tags'].apply(lambda x: " ".join(x))
    movies['tags'] = movies['tags'].apply(stems)
    
    count = CountVectorizer(max_features=5000, stop_words='english')
    count_matrix = count.fit_transform(movies['tags']).toarray()
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    np.save('../../data/cosine_sim.npy', cosine_sim)
    return cosine_sim


def get_recommendations(title):
    movies = process_dataset()
    cosine_sim = np.load('../../data/cosine_sim.npy')
    indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices]


def main():
    # cosine_sim = get_similar()
    print(get_recommendations('The Dark Knight Rises'))
    
if __name__ == '__main__':
    main()
