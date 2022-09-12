from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Store, ProductImage
from .serializer import ProductSerializer, StoreSerializer, ProductImageSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.gis.geos import Point
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="location")

class GetCreateStores(ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def perform_update(self, serializer):
        street_1 = serializer.initial_data["street_1"]
        address = serializer.initial_data["city"]
        state = serializer.initial_data["state"]
        country = serializer.initial_data["city"]
        data = [street_1, address, state, country]
        " ".join(data)

        g = geolocator.geocode(data)
        lat = g.latitude
        lng = g.longitude
        pnt = Point(lng, lat)
        serializer.save(location=pnt)

class RetrieveDeleteUpdateStore(RetrieveUpdateDestroyAPIView):
    serializer_class = StoreSerializer

    def get_queryset(self, *args,**kwargs):
        store_id = self.kwargs.get('id')
        return Store.objects.get(id=store_id)

    def get(self, request, *args,**kwargs):
        id = self.kwargs.get('id')
        store = self.get_queryset(id)
        serializer = StoreSerializer(store, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args,**kwargs):
        id = self.kwargs.get('id')
        store = self.get_queryset(id)
        serializer = StoreSerializer(store, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args,**kwargs):
        id = self.kwargs.get('id')
        store = self.get_queryset(id)
        store.delete()
        return Response("Deleted", status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        street_1 = serializer.initial_data["street_1"]
        address = serializer.initial_data["city"]
        state = serializer.initial_data["state"]
        country = serializer.initial_data["city"]
        data = [street_1, address, state, country]
        " ".join(data)

        g = geolocator.geocode(data)
        lat = g.latitude
        lng = g.longitude
        pnt = Point(lng, lat)
        serializer.save(location=pnt)

class GetCreateProducts(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class RetrieveDeleteUpdateProduct(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self, *args,**kwargs):
        product_id = self.kwargs.get('id')
        return Product.objects.get(id=product_id)

    def get(self, request, *args,**kwargs):
        id = self.kwargs.get('id')
        product = self.get_queryset(id)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args,**kwargs):
        id = self.kwargs.get('id')
        product = self.get_queryset(id)
        serializer = ProductSerializer(product, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args,**kwargs):
        id = self.kwargs.get('id')
        product = self.get_queryset(id)
        product.delete()
        return Response("Deleted", status=status.HTTP_204_NO_CONTENT)

class SaveImage(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def modify_input_for_multiple_files(self, product_id, image):
        dict = {}
        dict['product'] = product_id
        dict['image'] = image
        return dict

    def get(self, request, *args, **kwargs):
        try:
            id = self.kwargs.get('id')
            images =  ProductImage.objects.filter(project = id)
            serializer = ProductImageSerializer(images, many=True)
        except:
            return Response("404 Not Found")
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def post(self, request, *args, **kwargs):
        project_id = request.data['product']
        images = dict((request.data).lists())['image']

        flag = 1
        arr = []

        for img_name in images:
            modified_data = self.modify_input_for_multiple_files(project_id, img_name)
            file_serializer = ProductImageSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0
        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)

class GetAndDeleteImage(RetrieveDestroyAPIView):
    serializer_class = ProductImageSerializer

    def get_queryset(self,  *args, **kwargs):
        id = self.kwargs.get('id')
        return ProductImage.objects.get(id=id)

    #Get an Image
    def get(self, request,  *args, **kwargs):
        try:
            id = self.kwargs.get('id')
            image = self.get_queryset(id=id)
            serializer = ProductImageSerializer(image, many=False)
        except (ProductImage.DoesNotExist, AttributeError):
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #Delete an Image
    def delete(self, request,  *args, **kwargs):
        id = self.kwargs.get('id')
        image = self.get_queryset(id=id)
        image.delete()
        content = {
        
            'status': 'DELETED'
        }
        return Response(content, status=status.HTTP_204_NO_CONTENT)
