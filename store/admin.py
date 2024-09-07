from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
# Register your models here.

admin.site.site_header = "FAD Shop"
admin.site.site_title = "FAD Shop"

# @admin.register(Product)

class MyCustomFilter(admin.SimpleListFilter):
    title = _('Custom Filter')  # Use gettext_lazy for translation
    parameter_name = 'custom_filter'

    def lookups(self, request, model_admin):
        # Define the filter options
        return (
            ('option1', _('Contains 55')),
            ('option2', _('Contains 99')),
        )

    def queryset(self, request, queryset):
        # Apply the filter to the queryset
        if self.value() == 'option1':
            return queryset.filter(price__icontains='55')  # Make sure the filter value is correct
        if self.value() == 'option2':
            return queryset.filter(price__icontains='.99')  # Make sure the filter value is correct
        return queryset  # Return the unfiltered queryset if no match

class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name','price','image','is_digital','created_at']
    list_editable = ['is_digital']
    list_filter   = ['is_digital', MyCustomFilter]
    search_fields = ['name','price']

admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)