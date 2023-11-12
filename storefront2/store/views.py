from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status 

from store.filters import ProductFilter
from store.pagination import DefaultPagination

from .models import Product, Collection,OrderItem, Reviews

from .serializer import ProductSerializer, CollectionSerializer, ReviewSerializer


# Create your views here.


# >>>>>>>>> Class Based Views <<<<<<<<<<<<

class ProductViewSet(ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         return Product.objects.filter(collection_id = collection_id)
    #     return queryset
    
    

    def get_serializer_context(self):
        return {"request": self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response({'error' : 'Product can not be deleted'})
        return super().destroy(request, *args, **kwargs)

# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer
    
#     def get_serializer_context(self):
#         return {"request": self.request}
    
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
    # def get(self, request):
    #     queryset = Product.objects.select_related('collection').all()
    #     serializer = ProductSerializer(
    #         queryset, many=True, context={"request": request}
    #     )
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     # print(serializer.validated_data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# class ProductDetails(RetrieveUpdateDestroyAPIView):

#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
#     # def get(self, request, id):
#     #     product = get_object_or_404(Product, pk=id)
#     #     serializer = ProductSerializer(product)
#     #     return Response(serializer.data)

#     # def put(self, request, id):
#     #     product = get_object_or_404(Product, pk=id)
#     #     serializer = ProductSerializer(product, data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data)

#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# >>>>>>>>> Function Based Views <<<<<<<<<<<<

# @api_view(["GET", "POST"])
# def product_list(request):
#     if request.method == "GET":
#         queryset = Product.objects.all()
#         serializer = ProductSerializer(
#             queryset, many=True, context={"request": request}
#         )
#         return Response(serializer.data)

#     elif request.method == "POST":
#         # serializer = ProductSerializer(data=request.data)
#         # if serializer.is_valid():
#         #     serializer.validated_data
#         #     return Response("ok")
#         # else:
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # print(serializer.validated_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["GET", "PUT", "DELETE"])
# def product_details(request, id):
#     product = get_object_or_404(Product, pk=id)

#     if request.method == "GET":
#         ##### If I pass any product id that does not exists in Product model,
#         ##### then it will return error saying "Does not exist"
#         #
#         ##### Approach-1: Thats why we provide a TRY block for excption handling

#         # try:
#         #     product = Product.objects.get(pk=id)
#         #     serializer = ProductSerializer(product)
#         #     return Response(serializer.data)
#         # except Product.DoesNotExist:
#         #     return Response(status = status.HTTP_404_NOT_FOUND)

#         ###### Approach-2: Repeating {TRY EXCEPT} block is time consuming thats why we use a SHORTCUT >> get_object_or_404

#         serializer = ProductSerializer(product)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     elif request.method == "DELETE":
#         if product.orderitems.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# >>>>>>>>> Class Based Views <<<<<<<<<<<<

class CollectionViewSet(ModelViewSet):
    queryset =  Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):

        if Product.objects.filter(collection_id = kwargs['pk']).count() > 0:
            return Response({'error' : 'Collection can not be deleted'})
        return super().destroy(request, *args, **kwargs)
    
    # def delete(self, request, pk):
    #     collection = get_object_or_404(Product, pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error': 'Collection cannot be deleted'})
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# class CollectionList(ListCreateAPIView):
#     queryset =  Collection.objects.annotate(products_count=Count("products")).all()
#     serializer_class = CollectionSerializer

# class CollectionDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count("products"))

#     serializer_class = CollectionSerializer

#     def delete(self, request, pk):
#         collection = get_object_or_404(Product, pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted'})
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# >>>>>>>>> Function Based Views <<<<<<<<<<<<

# @api_view(["GET", "POST"])
# def collection_list(request):
#     if request.method == "GET":
#         queryset = Collection.objects.annotate(products_count=Count("products")).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     elif request.method == "POST":
#         serializer = CollectionSerializer(Collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(["GET", "PUT", "DELETE"])
# def collection_details(request, pk):
#     collection = get_object_or_404(
#         Collection.objects.annotate(products_count=Count("products")), pk=pk
#     )

#     if request.method == "GET":
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid()
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == "DELETE":
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# in the 'collection_list' function if the request method is 'POST' then it will create an object to the 'Collection' model. But when I type " { 'title': 'video games', "




class ReviewViewSet(ModelViewSet):
    
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Reviews.objects.filter(product_id = self.kwargs['product_pk'])
    def get_serializer_context(self):
        print(self.kwargs)
        return {'product_id': self.kwargs['product_pk']}


