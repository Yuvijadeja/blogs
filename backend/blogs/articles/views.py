from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article
from .serializer import ArticleSerializer
from .permissions import IsAuthorOrReadOnly

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by("-created_at")
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author']
    ordering_fields = ['id', 'title', 'created_at']
    search_fields = ['id', 'title']
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # Auto-assign logged-in user as author
        serializer.save(author=self.request.user)
