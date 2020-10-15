from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny
from Alt.models import Shirt, NonProfit, Atrocity, Category
from api.models import User
from .serializers import ShirtSerializer, NonProfitSerializer, AtrocitySerializer,  CategorySerializer
from api.serializers import UserSerializer
from api.permissions import IsLoggedInUserOrAdmin, IsAdminUser



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    



class ShirtList(generics.ListCreateAPIView):
  permission_classes = []

  serializer_class = ShirtSerializer
  queryset= Shirt.objects.all()
  
     
class NonProfitList(generics.ListAPIView):
  permission_classes = []
  serializer_class = NonProfitSerializer
  queryset = NonProfit.objects.all()


class AtrocityList(generics.ListAPIView):
  permission_classes = []
  serializer_class = AtrocitySerializer
  queryset= Atrocity.objects.all()

class CategoryList(generics.ListAPIView):
  permission_classes = []
  serializer_class = CategorySerializer
  queryset= Category.objects.all()




class FeaturedShirts(generics.ListAPIView):
  permission_classes = []
  serializer_class = ShirtSerializer
  
  def get_queryset(self):
    return Shirt.objects.filter(featured = True)


class FeaturedAtrocities(generics.ListAPIView):
  permission_classes = []
  serializer_class = AtrocitySerializer
  
  def get_queryset(self):
    return Atrocity.objects.filter(featured = True)



class FeaturedNonProfits(generics.ListAPIView):
  permission_classes = []
  serializer_class = NonProfitSerializer
  
  def get_queryset(self):
    return NonProfit.objects.filter(featured = True)
