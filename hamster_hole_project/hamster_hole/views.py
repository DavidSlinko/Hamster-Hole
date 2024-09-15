from rest_framework import viewsets
from .models import AuthorCategory, Author, Instruction, Letter
from .serializers import AuthorCategorySerializer, AuthorSerializer, InstructionSerializer, LetterSerializer
from django_filters import rest_framework as filters

# Вью для категорий авторов
class AuthorCategoryViewSet(viewsets.ModelViewSet):
    queryset = AuthorCategory.objects.all()
    serializer_class = AuthorCategorySerializer


# Вью для авторов
class AuthorFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    letter = filters.CharFilter(field_name='letter__symbol', lookup_expr='iexact')

    class Meta:
        model = Author
        fields = ['category', 'letter']

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AuthorFilter


# Вью для инструкций
class InstructionViewSet(viewsets.ModelViewSet):
    queryset = Instruction.objects.all()
    serializer_class = InstructionSerializer


# Вью для букв
class LetterViewSet(viewsets.ModelViewSet):
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer
