from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Member, Product, Order, OrderProduct

# 將模型註冊，導入 admin
#admin.site.register(Product)
#admin.site.register(Order)

# 自訂一個新的 User admin
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Member
    
    # 在列表顯示出來的欄位
    list_display = ('id', 'name', 'email', 'password', 'Type', 'phone', 'is_staff', 'is_active',)
    
    # 在 filter 顯示出來的欄位
    list_filter = ('name', 'email', 'password', 'Type', 'phone', 'is_staff', 'is_active',)
    
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password', 'Type', 'phone', 'is_staff', 'is_active',)}),
        #('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2', 'Type', 'phone', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Member, CustomUserAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin): 
    list_display = ('id', 'name', 'description', 'picture', 'inventory', 'price', 'creator', 'startScaleTime', 'endScaleTime')
    list_filter = ('name', 'description', 'picture', 'inventory', 'price','creator', 'startScaleTime', 'endScaleTime')
    
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin): 
    list_display = ('id', 'order_member', 'createTime')
    list_filter = ('order_member', 'createTime')
    inlines = [OrderProductInline]


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin): 
    list_display = ('id', 'order_id', 'item_member', 'item_product', 'amount')
    list_filter = ('order_id', 'item_member', 'item_product', 'amount')

#class OrderInstanceInline(admin.TabularInline):


    
    

    
    
    
    
    
    
    
    
    
    
    
    
    