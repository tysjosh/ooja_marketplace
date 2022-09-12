from django.contrib import admin
from .models import ProductInventory, Store, StoreCategory
from leaflet.admin import LeafletGeoAdmin

# # Register your models here.


# class ProductInventoryAdmin(admin.ModelAdmin):

#     list_display = [
#         'name',
#         'store_price',
#         'sale_price',
#         'store',
#         'created_at',
#         'last_modified'
#     ]

@admin.register(Store)
class StoreAdmin(LeafletGeoAdmin):
    list_display = ['id','name', 'owner', 'description', 'created_at', 'last_modified', 'street_1',
                    'street_2','city','state','zip_code','country','location',]


class StoreCategoryAdmin(admin.ModelAdmin):

    list_display = [field.name for field in
        StoreCategory._meta.get_fields() if not field.many_to_many]

# admin.site.register(ProductInventory, ProductInventoryAdmin)
admin.site.register(StoreCategory, StoreCategoryAdmin)