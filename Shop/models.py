from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
#from Shop.models import ProductInstance

from .managers import CustomUserManager

# 會員
class Member(AbstractBaseUser, PermissionsMixin):
    Type_choice = (
    ('b', '買家'), ('s', '賣家')
    )
    
    # 會員姓名 透過一對一關係將 User Model 欄位做延伸
    name = models.CharField(max_length = 50)
    # 類型
    Type = models.CharField(choices = Type_choice, default = 'b', max_length = 5)
    # email
    email = models.EmailField(_('email address'), unique=True)
    # 密碼
    password = models.CharField(max_length = 100)
    # 電話
    phone = models.CharField(max_length = 50)
    # 是否為 superuser
    is_staff = models.BooleanField(default=False)
    # 帳號可用性
    is_active = models.BooleanField(default=True)
    # 加入時間
    date_joined = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    objects = CustomUserManager()

    # 模型方法回傳的值
    def __str__(self):
        return '{}' .format(self.id)
    
from django.contrib.auth import get_user_model
User = get_user_model()


# 產品
class Product(models.Model): 
    # 建立商品會員，取得會員建立的所有產品
    creator = models.ForeignKey(User, related_name = 'products', on_delete = models.CASCADE)
    # 商品名稱
    name = models.TextField(max_length = 20)
    # 商品說明
    description = models.TextField(max_length = 100)
    # 商品圖片
    picture = models.URLField()
    # 存貨
    inventory = models.IntegerField(null=True)
    # 價錢
    price = models.IntegerField()
    # 上架時間
    startScaleTime = models.DateField(default = timezone.now)
    # 下架時間
    endScaleTime = models.DateField(default = '2050-12-31')
    
    class Meta : 
        # 按上架時間降序排列
        ordering = ['-startScaleTime']
    
    # 模型方法回傳的值
    def __str__(self):
        return '{}' .format(self.id)


# 訂單
class Order(models.Model): 
    # 下單會員，取得會員建立的所有訂單
    order_member = models.ForeignKey(User, related_name = 'orders', on_delete = models.CASCADE)
    # 下單時間
    createTime = models.DateTimeField(auto_now_add =True)
    # 訂單商品
    # order_product = models.ManyToManyField(OrderProduct)
    
    class Meta : 
        # 按下單時間降序排列
        ordering = ['id', '-createTime']
        
    # 模型方法回傳的值
    def __str__(self):
        #return f'{self.order_id}' 
        return '{}' .format(self.id)   


# 訂單商品
class OrderProduct(models.Model): 
    # 屬於的訂單編號，取得訂單的所有訂單商品
    order_id = models.ForeignKey(Order, related_name ='order_products', on_delete = models.CASCADE, blank=True, null=True)
    # 下單會員
    item_member = models.ForeignKey(User, related_name = 'order_products', on_delete = models.CASCADE)
    # 訂單商品，取得會員購買的所有商品(不分訂單)
    item_product = models.ForeignKey(Product, on_delete = models.CASCADE)
    # 數量
    amount = models.PositiveIntegerField()
 
    def get_total_price(self):
        return self.amount * self.item.price
    
    def __str__(self):
        #return '商品 : {} , 數量 : {}' .format(self.item_product.name, self.amount)
        return '{}' .format(self.id)
        


    
