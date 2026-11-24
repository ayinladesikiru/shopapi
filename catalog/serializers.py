from django.template.defaultfilters import title
from rest_framework import serializers
from .models import Product, Category, Cart, CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'description', 'sku']



class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'total']

    def get_total(self, item: CartItem):
        return item.product.price * item.quantity


class CartSerializer(serializers.ModelSerializer):
    cart_id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['cart_id', 'items', 'total_price']

    def get_total_price(self, cart: Cart):
        return sum(item.product.price * item.quantity for item in cart.items.all())




