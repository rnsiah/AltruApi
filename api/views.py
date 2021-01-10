from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from Alt.models import Shirt, NonProfit, Atrocity, Category, Rating
from api.models import User, UserProfile
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ShirtSerializer, NonProfitSerializer, AtrocitySerializer,  CategorySerializer, RatingSerializer
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
    




class ShirtList(viewsets.ModelViewSet):
  authentication_classes = (TokenAuthentication, )

  serializer_class = ShirtSerializer
  queryset= Shirt.objects.all()

  @action(detail=True, methods=['POST'])
  def rate_shirt(self,request, pk=None):
    if 'stars' in request.data:
      shirt = Shirt.objects.get(id=pk)
      stars = request.data['stars']
      user = request.user
      


      try:
        rating = Rating.objects.get(user = user.id, shirt = shirt.id)
        rating.stars = stars
        rating.save()
        serializer = RatingSerializer(rating, many =False)
        response = {'message': 'Rating Updated', 'result':serializer.data}
        return Response(response, status=status.HTTP_200_OK)
      except:
        rating = Rating.objects.create(user =user, shirt= shirt)
        serializer =RatingSerializer(rating)
        response = {'message': 'Rating Created', 'result':serializer.data}
        return Response(response, status=status.HTTP_200_OK)
    else:
      response = {'messeage': 'You need to provide a rating'}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)
  
     
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

class RatingViewSet(viewsets.ModelViewSet):
  queryset = Rating.objects.all()
  serializer_class = RatingSerializer
  authentication_classes = (TokenAuthentication, )
  




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



     
  




  
  
  

  
   

  