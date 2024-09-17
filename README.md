# Book Recommendation System

## To run the project
- make sure you have python 3.10 or higher and poetry 1.1.12 or higher installed in your machine
- navigate to booklib folder and install dependencies using `poetry install`
- Now you are on the file with manage.py, to dive into virtualenv run the command `poetry shell`
- Now run the command `python manage.py migrate` to propagate the database schema
- For ease of use, I have used sqlite as relational database, we can also use postgresql and mysql if needed
- To run the test cases just run `python manage.py test`
- To run the backend server `python manage.py runserver`

- Cosine Similarity are calculated while a new book is added. So to run that background task, run `bash run_celery.sh`, make sure you have installed `redis-server` in your machine
