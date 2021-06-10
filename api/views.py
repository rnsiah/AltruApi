from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from Alt.models import Shirt, NonProfit, Atrocity, Category, Rating, User
from api.models import User, UserProfile
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ShirtSerializer, NonProfitSerializer, AtrocitySerializer,  CategorySerializer, RatingSerializer, UserProfileSerializer
from api.serializers import UserSerializer
from api.permissions import IsLoggedInUserOrAdmin, IsAdminUser
from django.shortcuts import get_object_or_404
from django.http.response import Http404
from django.http import HttpResponse




class UserProfileFinder(generics.RetrieveUpdateDestroyAPIView):
  serializer_class= UserProfileSerializer
  queryset= UserProfile.objects.all()



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
    

class UserDetail(APIView):
  permission_classes = (IsAuthenticated, )
  



class UserProfileDetail(APIView):
   permission_classes = (IsAuthenticated, )

   def get_object(self, pk):
    try:
      return UserProfile.objects.get(pk = pk)
    except UserProfile.DoesNotExist:
      raise Http404

    def get(self, request, pk, format=None):
      userprofile = self.get_object(pk)
      serializer = UserProfileSerializer(userprofile)
      return Response(serializer.data)

   def patch(self, request, pk, format=None):
      userprofile = self.get_object(pk)
      serializer = UserProfileSerializer(userprofile, data=request.data, partial=True)
      if serializer.is_valid():
        
        serializer.save()
        return HttpResponse(status=200)
      return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


   def delete(self, request, pk, format=None):
       userprofile = self.get_object(pk)
       userprofile.delete()
       return Response(status = status.HTTP_204_NO_CONTENT)

  

  






class ShirtList(viewsets.ModelViewSet):
  authentication_classes = ()

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
  
class UserProfileView(viewsets.ModelViewSet):
  queryset=UserProfile.objects.all()
  serializer_class = UserProfileSerializer
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



     
  




  
  
  

  
   

  