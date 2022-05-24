from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import Product, Order, OrderProduct

from django.contrib.auth import get_user_model
User = get_user_model()

# 會員 因為是既定的模板 所以不能用 models.Model
class RegisterSerializers(serializers.ModelSerializer):
    '''
    Type_choice = (
    ('buyer', 'buyer'), ('seller', 'seller')
    )
    '''
    
    # 會員姓名 透過一對一關係將 User Model 欄位做延伸
    name = serializers.CharField(max_length = 50)
    # 類型
    Type = serializers.ChoiceField(
        choices = [('b', '買家'), ('s', '賣家')], 
        write_only = True
    )
    # Type = serializers.CharField(choices = Type_choice, default = 'buyer')
    # email
    email = serializers.EmailField(max_length = 50)
    # 密碼
    password = serializers.CharField(max_length = 50)
    # 電話
    phone = serializers.CharField(max_length = 50)
    
    
    class Meta : 
        model = User
        fields = ('id', 'name', 'email', 'password', 'Type', 'phone')

    def validate(self, args):
        email = args.get('email', None)
        # name = args.get('name', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('email already exists')})
        '''    
        if User.objects.filter(name=name).exists():
            raise serializers.ValidationError({'name': ('name already exists')})
        '''
        return super().validate(args)
  

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
    
class ProductSerializers(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta :
        fields = (
            'id', 
            'name',
            'description',
            'picture', 
            'creator',
            'price', 
            'inventory', 
            'startScaleTime', 
            'endScaleTime', 
        )
        model = Product
    

class UserSerializers(serializers.ModelSerializer):
    #my_id = serializers.SerializerMethodField()
    products = serializers.PrimaryKeyRelatedField(many = True, queryset = Product.objects.all())
    orders = serializers.PrimaryKeyRelatedField(many = True, queryset = Order.objects.all())
    
    class Meta:
        model = User
        fields = (
            'id', 
            'name', 
            'email', 
            'Type',
            'phone', 
            'products', 
            'orders', 
        )
     

class UserSerializers1(serializers.ModelSerializer):
    #my_id = serializers.SerializerMethodField()
    #products = serializers.PrimaryKeyRelatedField(many = True, queryset = Product.objects.all())
    #orders = serializers.PrimaryKeyRelatedField(many = True, queryset = Order.objects.all())
    
    class Meta:
        model = User
        fields = (
            'id', 
            'name', 
            'email', 
            'Type',
            'phone', 
        )
        
class UserSerializers2(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'name', 
            'email', 
            'is_staff', 
            'is_active'
        )

class OrderProductSerializers(serializers.ModelSerializer):
    item_member = serializers.HiddenField(default=serializers.CurrentUserDefault())
    #order_id = serializers.HiddenField(default = Order.objects.latest('id'))
    
    class Meta : 
        fields = (
            #'id', 
            #'order_id', 
            'item_member', 
            'item_product', 
            'amount',  
        )
        model = OrderProduct


class OrderSerializers(serializers.ModelSerializer):
    order_member = serializers.HiddenField(default=serializers.CurrentUserDefault())  
    order_products = OrderProductSerializers(many = True)
    
    class Meta : 
        fields = (
            'id', 
            'order_member',
            'createTime', 
            'order_products', 
        )
        model = Order
       

    def create(self, validated_data):      
        orderproduct_data = validated_data.pop('order_products')     
        order_instance = Order.objects.create(**validated_data) 
        
        for order_data in orderproduct_data:
            OrderProduct.objects.create(order_id = order_instance, **order_data)
            
        return order_instance


'''
class OrderProductSerializers(serializers.ModelSerializer):
    item_member = serializers.HiddenField(default=serializers.CurrentUserDefault())
    #order_id = serializers.HiddenField(default = Order.objects.latest('id'))
    
    class Meta : 
        fields = (
            #'id', 
            #'order_id', 
            'item_member', 
            'item_product', 
            'amount',  
        )
        model = OrderProduct


class OrderSerializers(serializers.ModelSerializer):
    order_member = serializers.HiddenField(default=serializers.CurrentUserDefault())  
    order_products = OrderProductSerializers(many = True)
    
    class Meta : 
        fields = (
            'id', 
            'order_member',
            'createTime', 
            'order_products', 
        )
        model = Order
       
    def create(self, validated_data):      
        orderproduct_data = validated_data.pop('order_products')     
        order = Order.objects.create(**validated_data)
        for order_data in orderproduct_data:
            OrderProduct.objects.create(**order_data)
        return Order.objects.all().order_by("-id")[1] 

'''








