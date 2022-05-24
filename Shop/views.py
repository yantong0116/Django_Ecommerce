from django.shortcuts import render
from rest_framework import generics
# from django.contrib.auth.models import User

from .models import Product, Order, OrderProduct
from rest_framework import permissions, status, serializers, authentication
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
import uuid
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from django.http import Http404

from .serializers import UserSerializers, UserSerializers1, UserSerializers2
from .serializers import ProductSerializers, OrderSerializers , RegisterSerializers, OrderProductSerializers


from django.contrib.auth import get_user_model
User = get_user_model()


class RegistrationAPIView(generics.GenericAPIView):

    serializer_class = RegisterSerializers

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        
        if(serializer.is_valid()):
            serializer.save()
            return Response({
                    #"RequestId": str(uuid.uuid4()),
                    "status" : "status.HTTP_201_CREATED", 
                    "message": "User created successfully",
                    "data": serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
        
        return Response({
                    "status" : "status.HTTP_400_BAD_REQUEST", 
                    "message" : "Create user failed. Email is already used.", 
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
    

# 取得與修改自己的資料
class UserMe(generics.RetrieveUpdateDestroyAPIView):
   permission_classes = (permissions.IsAuthenticated,)
   queryset = User.objects.all()
   serializer_class = UserSerializers1
   http_method_names = ['get', 'patch']
   
   '''
   def get_object(self):
       return self.request.user
   '''
   
   def patch(self, request, *args, **kwargs): 
        #if int(kwargs["pk"]) == int(request.user.id) : 
        myself = request.user
        serializer = UserSerializers1(myself, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                    'status': 'status.HTTP_200_OK',
                    'message': 'Update successfully.', 
                    'data':serializer.data
                    },
                    status=status.HTTP_200_OK
                )
        return Response({
                    'status': 'status.HTTP_400_BAD_REQUEST',
                    'message': 'Serializer is not valid.', 
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        
   
   def get(self, request, *args, **kwargs):
        return Response(
                {'status' : 'status.HTTP_200_OK',
                 'message' : 'Successful', 
                 'data' : {
                    'id': request.user.id,
                    'name': request.user.name,
                    'email': request.user.email, 
                    'Type': request.user.Type,
                    'phone': request.user.phone,
                    },
                }, 
                status=status.HTTP_200_OK
            )


    
class ListUser(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializers
    http_method_names = ['get']


class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser, )
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializers2
    http_method_names = ['patch']
    
    # 只要是我們請求後臺時前端請求header頭中攜帶token認證
    # 我們在後臺就可以用request 取到當前的用戶對象
    # kwargs["pk"] 是 url 上的 pk

    '''
    def get(self, request, *args, **kwargs):
        if (kwargs["pk"]) == int(request.user.id) : 
            return Response(
                data={
                    'id': request.user.id,
                    'name': request.user.name,
                    'email': request.user.email, 
                    'Type': request.user.Type,
                    'phone': request.user.phone,
                    #'product': request.user.products,
                },
                status=status.HTTP_200_OK
            )
        else : 
            return Response(
                data={
                    "message": "You didn't have authentication to view user with id: {} ".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            ) 
    '''
         
    def patch(self, request, *args, **kwargs): 
        #if int(kwargs["pk"]) == int(request.user.id) : 
        myself = self.get_object()
        serializer = UserSerializers2(myself, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                    'status': 'status.HTTP_200_OK',
                    'message': 'Update successfully.', 
                    'data':serializer.data
                    },
                    status=status.HTTP_200_OK
                )
        return Response({
                    'status': 'status.HTTP_400_BAD_REQUEST',
                    'message': 'Serializer is not valid.', 
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        #else : 
            #return Response({
                    #"status" : "status.HTTP_403_FORBIDDEN", 
                    #"message" : "You didn't have authentication to visit.", 
                    #}, 
                    #status=status.HTTP_403_FORBIDDEN
                #)
        
class ListProduct(generics.ListCreateAPIView):   
    # 商品的顯示不需要權限
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    http_method_names = ['get', 'post']
    
    def get(self, request):
        return Response({
                "status" : "status.HTTP_200_OK",
                "message" : "Get all product successfully.", 
                "data" : list(Product.objects.all().values())
                },
                status=status.HTTP_200_OK
            )
    
    # POST 只有賣家可以建立商品
    @authentication_classes((SessionAuthentication, ))
    def post(self, request):
        if request.user.Type == 's' :
            serializer = self.get_serializer(data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                        'status': 'status.HTTP_201_CREATED',
                        'message': 'Post the product successfully.', 
                        'data':serializer.data
                        },
                        status=status.HTTP_201_CREATED
                    )
            else : 
                return Response({
                        'status': 'status.HTTP_400_BAD_REQUEST',
                        'message': 'Serializer is not valid.', 
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
        else : 
            return Response({
                    'status': 'status.HTTP_403_FORBIDDEN',
                    'message': 'You did not have authentication to post the product.', 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
 
class DetailProduct(generics.RetrieveUpdateDestroyAPIView):
    
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    http_method_names = ['get', 'patch', 'delete']
    
    
    def get_object(self, pk):
        product = get_object_or_404(Product, pk = pk)
        return product

    # 商品的顯示不需要權限
    def get(self, request, *args, **kwargs):
        product = self.get_object(kwargs["pk"])
        serializer = ProductSerializers(product)
        return Response({
                        'status': 'status.HTTP_200_OK',
                        'message': 'Get the product successfully.', 
                        'data':serializer.data
                        },
                        status=status.HTTP_200_OK
                    )

    
    # 只有建立商品的人可以更改商品內容        
    def patch(self, request, *args, **kwargs):
        queryset = request.user.products.all()
        # 擁有的 product array
        data = list(queryset)
        
        context = {
            "request" : request, 
        }
        
        check = False
        for i in range(len(data)) :
            if str(kwargs["pk"]) == str(data[i]) :
                check = True
        
        if check : 
            product = self.get_object(kwargs["pk"])
            serializer = ProductSerializers(product, data=request.data, context=context)
            if serializer.is_valid():
                serializer.save()
                return Response({
                        'status': 'status.HTTP_200_OK',
                        'message': 'Update the product successfully.', 
                        'data':serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
            else : 
                return Response({
                    'status': 'status.HTTP_400_BAD_REQUEST',
                    'message': 'Serializer is not valid.', 
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else : 
            return Response({
                    'status': 'status.HTTP_403_FORBIDDEN',
                    'message': 'You did not have authentication to update the product.', 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
    
    
    # 只有建立商品的人可以刪除商品   
    @authentication_classes((SessionAuthentication, ))
    def delete(self, request, pk):
        queryset = request.user.products.all()
        # 擁有的 product array
        data = list(queryset)
        
        check = False
        for i in range(len(data)) :
            if str(pk) == str(data[i]) :
                check = True
        
        if check :         
            product = self.get_object(pk)
            product.delete()
            return Response({
                    'status': 'status.HTTP_204_NO_CONTENT',
                    'message': 'Delete the product successfully.', 
                    'data' : 'ID : {} product is deleted.' .format(pk)
                    }, 
                    status=status.HTTP_204_NO_CONTENT
                )
        else : 
            return Response({
                    'status': 'status.HTTP_403_FORBIDDEN',
                    'message': 'You did not have authentication to delete the product.', 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
    
#-----------------------------------------------------------------------------

class ListOrder(generics.ListCreateAPIView):    
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    http_method_names = ['get', 'post']
    

    # 找到登入者下的所有訂單
    def get(self, request, *args, **kwargs):
        if request.user.Type == 'b' :
            order_list =  Order.objects.filter(order_member = int(request.user.id))
            serializer = OrderSerializers(order_list, many = True)
            return Response({
                            'status': 'status.HTTP_200_OK',
                            'message': 'Get orders successfully.', 
                            'buyerID': request.user.id,
                            'buyerName': request.user.name, 
                            'buyerEmail': request.user.email, 
                            'buyerPhone': request.user.phone, 
                            'data':serializer.data
                            }, 
                            status=status.HTTP_200_OK
                        )
        # 考慮做賣家看到自己賣出的商品
        else :
            #queryset = request.user.products.all()
            # 擁有的 product array
            #data = list(queryset)
            
            return Response({
                    'status': 'status.HTTP_403_FORBIDDEN',
                    'message': 'You did not have any order to display.', 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
    
    # 買家下訂單
    def post(self, request):
        
        if request.user.Type == 'b' :
            serializer = self.get_serializer(data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                        'status': 'status.HTTP_201_CREATED',
                        'message': 'Post the order successfully.', 
                        'buyerID': request.user.id,
                        'buyerName': request.user.name, 
                        'buyerEmail': request.user.email, 
                        'buyerPhone': request.user.phone, 
                        'data':serializer.data
                        },
                        status=status.HTTP_201_CREATED
                    )
            else : 
                return Response({
                        'status': 'status.HTTP_400_BAD_REQUEST',
                        'message': 'Serializer is not valid.', 
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
        else : 
            return Response({
                    'status': 'status.HTTP_403_FORBIDDEN',
                    'message': 'You did not have authentication to post the order.', 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
    
    
class DetailOrder(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        
        queryset = request.user.orders.all()
        # 用戶下的所有訂單
        data = list(queryset)
        
        check = False
        for i in range(len(data)) :
            if str(kwargs["pk"]) == str(data[i]) :
                check = True
        
        if check : 
            order = self.get_object()
            
            serializer = OrderSerializers(order)
            return Response({
                        'status': 'status.HTTP_200_OK',
                        'message': 'Get the order successfully.', 
                        'buyerID': request.user.id,
                        'buyerName': request.user.name, 
                        'buyerEmail': request.user.email, 
                        'buyerPhone': request.user.phone, 
                        'data':serializer.data
                        }, 
                        status=status.HTTP_200_OK
                    )
        else : 
            return Response({
                    'status': 'status.HTTP_403_FORBIDDEN',
                    'message': 'You did not have permission to access the detail of the order.', 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )


    