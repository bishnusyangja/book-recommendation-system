from rest_framework import serializers
from library.models import Book, Author


class BookSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(read_only=True)
    created_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    modified_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    published_on = serializers.DateField(format='%Y-%m-%d')
    author = serializers.ListField(child=serializers.CharField(), write_only=True)
    author_list = serializers.CharField(read_only=True)

    class Meta:
        model = Book
        fields = ('uuid', 'title', 'author', 'author_list', 'description', 'published_on', 'created_on', 'modified_on')

    def validate_author(self, value):
        if not value:
            raise serializers.ValidationError('authors are required')
        if not isinstance(value, list):
            raise serializers.ValidationError('List of uuid for authors are required')
        if not len(value) == Author.objects.filter(uuid__in=value).count():
            raise serializers.ValidationError('Some of your uuid does not match with author')
        return list(Author.objects.filter(uuid__in=value).values_list('pk', flat=True))

    def validate_title(self, value):
        if Book.objects.filter(title=value.strip(), is_deleted=False).count() > 0:
            raise serializers.ValidationError('The book you want to enter was already in list')
        return value.strip()


class AuthorSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(read_only=True)
    created_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    modified_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Author
        fields = ('uuid', 'name', 'description', 'created_on', 'modified_on')

    def validate_name(self, value):
        if Author.objects.filter(name=value.strip(), is_deleted=False).count() > 0:
            raise serializers.ValidationError('The book you want to enter was already in list')
        return value.strip()