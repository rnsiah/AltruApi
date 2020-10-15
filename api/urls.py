from django.conf.urls import url, include
from rest_framework import routers
from api.views import UserViewSet
from django.urls import path
from . import views



router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),
    path('shirts', views.ShirtList.as_view()),
    path('atrocities', views.AtrocityList.as_view()),
    path('nonprofits', views.NonProfitList.as_view()),
    path('categories', views.CategoryList.as_view()),
    path('featuredshirts', views.FeaturedShirts.as_view()),
    path('featuredatrocities', views.FeaturedAtrocities.as_view()),
    path('featurednonprofits', views.FeaturedNonProfits.as_view()),
    
]