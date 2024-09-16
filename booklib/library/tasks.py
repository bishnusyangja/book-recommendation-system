from celery import shared_task
import logging
from library.models import Book, SimilarityMatrix
from library.recommendation import find_similarity

logger = logging.getLogger('celery')

BULK_UPDATE_MAX_SIZE = 100

@shared_task
def cosine_similarity(id):
    logger.info("***** Calculating cosine similarity ********")
    new_book = Book.objecs.get(id=id)
    existing = Book.objects.exclude(id=id)

    counter = 0
    bulk_obj = []
    for book in existing:
        similarity = find_similarity(book.title, new_book.title)
        dict = {'similarity': similarity}
        if book.id < new_book.id:
            dict['small_book_id'] = book.id
            dict['large_book_id'] = new_book.id
        else:
            dict['small_book_id'] = new_book.id
            dict['large_book_id'] = book.id
        bulk_obj.append(SimilarityMatrix(**dict))
        counter += 1
        if counter >= BULK_UPDATE_MAX_SIZE:
            SimilarityMatrix.objects.bulk_create(bulk_obj)
            # reset bulk_obj and counter
            bulk_obj = []
            counter = 0
    return True