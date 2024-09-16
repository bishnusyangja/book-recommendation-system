from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_similarity(title_1, title_2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([title_1, title_2])
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return "{:.2f}".format(cosine_sim[0][0])
