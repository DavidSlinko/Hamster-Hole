from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AuthorCategoryViewSet, AuthorViewSet, InstructionViewSet, LetterViewSet

router = DefaultRouter()
router.register(r'categories', AuthorCategoryViewSet)  # Для категорий авторов
router.register(r'authors', AuthorViewSet)  # Для авторов
router.register(r'instructions', InstructionViewSet)  # Для инструкций
router.register(r'letters', LetterViewSet)  # Для букв

urlpatterns = [
    path('api/', include(router.urls)),
]
