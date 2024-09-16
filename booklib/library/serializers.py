from rest_framework import serializers
from library.models import Book, Author, FavoriteBooks

MAX_FAV_LIST = 20


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


class FavoriteBookSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(read_only=True)
    created_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    modified_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    book = BookSerializer(read_only=True)

    book_uuid = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.user = context.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = FavoriteBooks
        fields = ('uuid', 'book_uuid', 'book', 'created_on', 'modified_on', )

    def validate_book_uuid(self, value):
        if not value:
            raise serializers.ValidationError('Not a valid book')
        if Book.objects.filter(uuid=value).count() == 0:
            raise serializers.ValidationError('Not a valid book')
        book_pk = Book.objects.get(uuid=value).pk
        if FavoriteBooks.objects.filter(user=self.user, book_id=book_pk).count() > 0:
            raise serializers.ValidationError('The book is already in your favorite list.')
        return book_pk

    def validate(self, attrs):
        if FavoriteBooks.objects.filter(user=self.user).count() >= MAX_FAV_LIST:
            raise serializers.ValidationError(
                {'book': 'You cannot add more than {} books in your favorite list.'.format(MAX_FAV_LIST)})
        return attrs

    def create(self, validated_data):
        validated_data['book_id'] = validated_data.pop('book_uuid')
        validated_data['user_id'] = self.user.id
        return super().create(validated_data)