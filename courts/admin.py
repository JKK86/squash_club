from django.contrib import admin

from courts.models import Category, Court, Reservation, PriceList, Discount


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug', ]


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ['category', 'order', 'air_condition', 'lighting', ]
    list_filter = ['category', ]


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ['category', 'weekend', 'time', 'price']
    list_filter = ['category', 'weekend']
    list_editable = ['price']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['court', 'user', 'date', 'time', 'duration', 'paid', 'status', 'comment', 'created']
    list_filter = ['court', 'date', 'paid', 'status']
    search_fields = ['user']
    exclude = ['paid', 'created']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'discount']
    list_filter = ['category']
    list_editable = ['discount']
