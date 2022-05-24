from django.urls import path
from .views import ListUser, DetailUser, ListProduct, DetailProduct, ListOrder, DetailOrder, UserMe

urlpatterns = [
    path('Product', ListProduct.as_view(), name = 'product'), 
    path('Product/<int:pk>', DetailProduct().as_view(), name = 'singleproduct'),
    
    path('Order', ListOrder.as_view(), name = 'order'), 
    path('Order/<int:pk>', DetailOrder.as_view(), name = 'singleorder'), 
    
    path('User/me', UserMe.as_view(), name='userMe'),
    path('User/<int:pk>', DetailUser.as_view(), name='singleuser'),
    
]


