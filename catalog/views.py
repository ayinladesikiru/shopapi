from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from rest_framework.generics import ListAPIView, RetrieveAPIView


class ProductListView(ListAPIView):
    queryset = Product.objects.all().filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    serializer = CategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)

