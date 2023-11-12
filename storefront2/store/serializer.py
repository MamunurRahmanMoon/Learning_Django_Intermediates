from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection, Reviews


class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price')
    # price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name = 'collection_details'
    # )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "unit_price",
            "inventory",
            "collection",
            "price_with_tax",
            "last_update"
        ]

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)


# def validate(self, data):
#     if data['password'] != data['confirm_password']:
#         return serializers.ValidationError('Passwords do not match')
#     return data


class CollectionSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)

    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    products_count = serializers.IntegerField(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ["id", "date", "name", "description"]

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Reviews.objects.create(product_id = product_id, **validated_data)