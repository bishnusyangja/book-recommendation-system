from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Q

from library.models import FavoriteBooks, SimilarityMatrix, Book


def calculate_similarity(title_1, title_2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([title_1, title_2])
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return "{:.2f}".format(cosine_sim[0][0])


def get_recommended_book_ids(user_id, num):
    book_ids = list(FavoriteBooks.objects.filter(user_id=user_id).values_list('book_id', flat=True))
    result_query = SimilarityMatrix.objects.filter(Q(small_book_id__in=book_ids) | Q(large_book_id__in=book_ids)).exclude(
        Q(small_book_id__in=book_ids) & Q(large_book_id__in=book_ids)).order_by('-similarity')[:num]

    recommended_book_ids = []
    for item in result_query:
        if item.small_book_id in book_ids:
            recommended_book_ids.append(item.large_book_id)
        else:
            recommended_book_ids.append(item.small_book_id)
    return recommended_book_ids


def get_recommended_book_query(user_id, num):
    recommended_book_ids = get_recommended_book_ids(user_id, num)
    return Book.objects.filter(id__in=recommended_book_ids)