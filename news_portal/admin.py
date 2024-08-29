from django.contrib import admin
from .models import Category, Author, Post, Comment, PostCategory


def rating_quantity(modeladmin, request, queryset): # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(rating=0)
rating_quantity.short_description = 'Обнулить рейтинг' # описание для более понятного представления в админ панеле задаётся, как будто это объект

class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('id', 'time_in', 'title', 'text', 'rating') # оставляем только имя и цену товара
    list_filter = ('rating', )
    search_fields = ('title', )
    actions = [rating_quantity]

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
