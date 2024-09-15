from library.models import Book, Author
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    modified_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    published_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'published_on', 'created_on', 'modified_on')


class AuthorSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    modified_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'name', 'description', 'created_on', 'modified_on')