from django.db.models import Q
from library.models import Book, Author
from library.permissions import AdminWritePermission
from library.serializers import BookSerializer, AuthorSerializer
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