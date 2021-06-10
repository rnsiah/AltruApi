from django.conf.urls import url, include
from rest_framework import routers
from api.views import UserViewSet,RatingViewSet, ShirtList, UserProfileView
from django.urls import path
from . import views



router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register('ratings', RatingViewSet)
router.register('shirts', ShirtList )
router.register('userprofile', UserProfileView)




urlpatterns = [
    url(r'^', include(router.urls)),
    path('userprofiles/<int:pk>/', views.UserProfileDetail.as_view()),
    path('atrocities', views.AtrocityList.as_view()),
    path('nonprofits', views.NonProfitList.as_view()),
    path('categories', views.CategoryList.as_view()),
    path('featuredshirts', views.FeaturedShirts.as_view()),
    path('featuredatrocities', views.FeaturedAtrocities.as_view()),
    path('featurednonprofits', views.FeaturedNonProfits.as_view()),
    path('userdetails/<int:pk>', views.UserProfileDetail.as_view()),
   

    
    
]