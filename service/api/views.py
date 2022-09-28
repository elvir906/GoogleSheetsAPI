from app.models import Orders
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import OrdersSerializer


@api_view()
def get_chunk(request):
    entries = Orders.objects.all()
    return Response(OrdersSerializer(entries, many=True).data)
