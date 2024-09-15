from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

admin.site.register(AuthorCategory)
admin.site.register(Letter)
admin.site.register(Author)
admin.site.register(Instruction)
#
#
# @admin.register(AuthorCategory)
# class AuthorCategoryAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'name')
#     list_display_links = ('pk', 'name')
#
#
# @admin.register(Letter)
# class LetterAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'symbol')
#     list_display_links = ('pk', 'symbol')
#
#
# @admin.register(Author)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'name', 'category', 'letter')
#     list_display_links = ('pk', 'name', 'category')
#
#
# @admin.register(Instruction)
# class InstructionAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'author', 'description', 'image')
#     list_display_links = ('pk', 'author')
