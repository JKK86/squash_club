from django.contrib import admin

from courts.models import Category, Court, Reservation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug', ]


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ['category', 'number', 'air_condition', 'lighting', ]
    list_filter = ['category', ]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['court', 'user', 'date', 'time', 'duration', 'paid', 'status', 'comments', 'created']
    list_filter = ['court', 'date', 'paid', 'status']
    search_fields = ['user']
    exclude = ['paid', 'created']
