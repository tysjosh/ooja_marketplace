from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializer import RegisterSerializer


class GetUsers(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

class CreateUser(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

class UpdateUser(RetrieveUpdateDestroyAPIView):
    serializer_class = RegisterSerializer

    def get_queryset(self, *args,**kwargs):
        user_id = self.kwargs.get('id')
        return CustomUser.objects.get(id=user_id)

    def get(self, request, *args,**kwargs):
        id = self.kwargs.get('id')
        user = self.get_queryset(id)
        serializer = RegisterSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args,**kwargs):
        id = self.kwargs.get('id')
        user = self.get_queryset(id)
        serializer = RegisterSerializer(user, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args,**kwargs):
        id = self.kwargs.get('id')
        user = self.get_queryset(id)
        user.delete()
        return Response("Deleted", status=status.HTTP_204_NO_CONTENT)

