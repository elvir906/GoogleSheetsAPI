from app.models import Orders
from rest_framework import serializers


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = [
            'table_row_index',
            'table_row_number',
            'order_number',
            'cost_usd',
            'cost_rub',
            'delivery_date',
            'created_at',
            'updated_at',
        ]
