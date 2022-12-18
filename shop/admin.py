from django.contrib import admin
from .models import Post, Category, Company, Tag, Comment
from markdownx.admin import MarkdownxModelAdmin
# Register your models here.

admin.site.register(Post, MarkdownxModelAdmin)

admin.site.register(Comment)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug1': ('name',)}


admin.site.register(Category, CategoryAdmin)


class CompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Company, CompanyAdmin)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Tag, TagAdmin)
