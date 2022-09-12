from django.urls import path
from . import views



urlpatterns = [
path('stores', views.GetCreateStores.as_view()),
path('stores/<str:pk>', views.RetrieveDeleteUpdateStore.as_view()),

path('products', views.GetCreateProducts.as_view()),
path('products/<int:id>', views.RetrieveDeleteUpdateProduct.as_view()),
]