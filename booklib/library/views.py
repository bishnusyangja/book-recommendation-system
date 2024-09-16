from django.db.models import Q
from rest_framework import status
from library.models import Book, Author, FavoriteBooks
from library.permissions import AdminWritePermission
from library.recommendation import get_recommended_books
from library.serializers import BookSerializer, AuthorSerializer, FavoriteBookSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class BookAPI(ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated, AdminWritePermission)
    queryset = Book.objects.none()
    lookup_field = 'uuid'

    def get_queryset(self):
        qs = Book.objects.filter(is_deleted=False)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(author__name__icontains=search))
        return qs


class AuthorAPI(ModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = (IsAuthenticated, AdminWritePermission)
    queryset = Author.objects.none()
    lookup_field = 'uuid'

    def get_queryset(self):
        qs = Author.objects.filter(is_deleted=False)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(name__icontains=search)
        return qs


class FavoriteBookAPI(ModelViewSet):
    http_method_names = ('get', 'post', 'delete', )
    serializer_class = FavoriteBookSerializer
    permission_classes = (IsAuthenticated, )
    queryset = FavoriteBooks.objects.none()
    lookup_field = 'uuid'

    def get_queryset(self):
        return FavoriteBooks.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx.update({'user': self.request.user})
        return ctx

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status == status.HTTP_201_CREATED:
            response.data['recommended'] = get_recommended_books()
        return response
