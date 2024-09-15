from rest_framework import serializers
from .models import AuthorCategory, Author, Instruction, Letter


# Сериализатор для инструкции
class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ['id', 'author', 'image', 'description', 'file']


# Сериализатор для авторов
class AuthorSerializer(serializers.ModelSerializer):
    instructions = InstructionSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'letter', 'category', 'instructions']


# Сериализатор для букв
class LetterSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Letter
        fields = ['id', 'symbol', 'authors']


# Сериализатор для категорий авторов
class AuthorCategorySerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = AuthorCategory
        fields = ['id', 'name', 'authors']
