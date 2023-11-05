from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count, Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serializer import ProductSerializer, CollectionSerializer


# Create your views here.


@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        queryset = Product.objects.all()
        serializer = ProductSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    elif request.method == "POST":
        # serializer = ProductSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response("ok")
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # print(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def product_details(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == "GET":
        ##### If I pass any product id that does not exists in Product model,
        ##### then it will return error saying "Does not exist"
        #
        ##### Approach-1: Thats why we provide a TRY block for excption handling

        # try:
        #     product = Product.objects.get(pk=id)
        #     serializer = ProductSerializer(product)
        #     return Response(serializer.data)
        # except Product.DoesNotExist:
        #     return Response(status = status.HTTP_404_NOT_FOUND)

        ###### Approach-2: Repeating {TRY EXCEPT} block is time consuming thats why we use a SHORTCUT >> get_object_or_404

        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == "DELETE":
        if product.orderitems.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "PUT", "DELETE"])
def collection_details(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(products_count=Count("products")), pk=pk
    )

    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def collection_list(request):
    if request.method == "GET":
        queryset = Collection.objects.annotate(products_count=Count("products")).all()
        serializer = CollectionSerializer(queryset, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = CollectionSerializer(Collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# in the 'collection_list' function if the request method is 'POST' then it will create an object to the 'Collection' model. But when I type " { 'title': 'video games', "
