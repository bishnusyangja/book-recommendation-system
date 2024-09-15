from django.db.models import Q
from library.models import Book, Author
from library.serializers import BookSerializer, AuthorSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class BookAPI(ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Book.objects.none()

    def get_queryset(self):
        qs = self.queryset
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(author__icontains=search))
        return qs


class AuthorAPI(ModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Author.objects.none()

    def get_queryset(self):
        qs = Author.objects.all()
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(name__icontains=search)
        return qs