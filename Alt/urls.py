from django.urls import path
from .views import home, ShirtList, view_shirt, NonProfitList, view_nonProfit

app_name= 'Alt'

urlpatterns = [
    path('', home, name='landing'),
    path('allshirts', ShirtList.as_view(), name = 'allshirts_list'),
    path('shirt/<slug>/', view_shirt, name = 'shirts' ),
    path('all_nonprofits', NonProfitList.as_view(), name='nonprofit_list'),
    path('nonprofit/<slug>', view_nonProfit, name='nonprofit' )
    
    
   
]



