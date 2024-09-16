from rest_framework import serializers
from library.models import Book, Author


class BookSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(read_only=True)
    created_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    modified_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    published_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Book
        fields = ('uuid', 'title', 'author', 'description', 'published_on', 'created_on', 'modified_on')


class AuthorSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(read_only=True)
    created_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    modified_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Author
        fields = ('uuid', 'name', 'description', 'created_on', 'modified_on')