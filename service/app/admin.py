from django.contrib import admin

from .models import Orders


class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'table_row_index',
        'table_row_number',
        'order_number',
        'cost_usd',
        'cost_rub',
        'delivery_date',
        'created_at',
        'updated_at'
    )


admin.site.register(Orders, OrdersAdmin)
