from django.contrib import admin

from courts.models import Category, Court


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug', ]


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ['category', 'number', 'air_condition', 'lighting', ]
    list_filter = ['category', ]
