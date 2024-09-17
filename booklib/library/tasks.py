from celery import shared_task
import logging
from library.models import Book, SimilarityMatrix
from library.recommendation import calculate_similarity

logger = logging.getLogger('celery')

BULK_UPDATE_MAX_SIZE = 100

@shared_task
def saving_cosine_similarity(new_book_id):
    logger.info("***** Calculating cosine similarity ********")
    new_book = Book.objects.get(id=new_book_id)
    existing = Book.objects.exclude(id=new_book_id)

    counter = 0
    bulk_obj = []
    for book in existing:
        similarity = calculate_similarity(book.title, new_book.title)
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
            logger.info("******** Inserting {} Similarity Matrix records ********* ".format(counter))
            SimilarityMatrix.objects.bulk_create(bulk_obj)
            # reset bulk_obj and counter
            bulk_obj = []
            counter = 0
    if counter:
        logger.info("********** Lastly --> Inserting {} Similarity Matrix records ********* ".format(counter))
        SimilarityMatrix.objects.bulk_create(bulk_obj)

    return True
