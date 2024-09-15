from django.db import models


# Категория автора (зарубежный или российский)
class AuthorCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название для категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории автора'
        verbose_name_plural = 'Категории авторов'


# Модель букв
class Letter(models.Model):
    symbol = models.CharField(max_length=1, unique=True, verbose_name='Буква')  # Символ буквы

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name = 'Буква'
        verbose_name_plural = 'Буквы'


# Автор с привязкой к категории и букве
class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя и Фамилия автора')  # Имя и фамилия автора
    letter = models.ForeignKey(Letter, related_name='authors', on_delete=models.CASCADE, verbose_name='Буква для автора')
    category = models.ForeignKey(AuthorCategory, related_name='authors', on_delete=models.CASCADE,
                                 verbose_name='Категория автора')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


# Инструкция с привязкой к автору
class Instruction(models.Model):
    author = models.ForeignKey(Author, related_name='instructions', on_delete=models.CASCADE, verbose_name='Автор')
    image = models.ImageField(upload_to='instructions/images/', blank=True, null=True, verbose_name='Фото')
    description = models.TextField(verbose_name='Описание')
    file = models.FileField(upload_to='instructions/files/', blank=True, null=True, verbose_name='Файл')

    def __str__(self):
        return f"Инструкция от {self.author.name}"

    class Meta:
        verbose_name = 'Инструкция'
        verbose_name_plural = 'Инструкции'
