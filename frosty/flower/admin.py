from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import MyUser, Flower, Item, CommentToItem, CommentToSeller, Deal


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'role')}),
        (_('Personal info'),
         {'fields': (
             'first_name', 'last_name', 'email'
         )}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('id', 'username', 'role')


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'colour',
    )
    search_fields = (
        'name',
    )
    list_filter = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'seller',
        'flower',
        'visible',
        'amount',
        'price'
    )
    search_fields = (
        'flower', 'seller'
    )
    list_filter = ('flower', 'seller',)


@admin.register(CommentToItem)
class CommentToItemAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'author',
        'text',
        'created',
    )
    search_fields = (
        'item', 'author'
    )
    list_filter = ('item', 'author',)


@admin.register(CommentToSeller)
class CommentToSellerAdmin(admin.ModelAdmin):
    list_display = (
        'seller',
        'author',
        'text',
        'created',
    )
    search_fields = (
        'seller', 'author'
    )
    list_filter = ('seller', 'author',)


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'lot',
        'amount',
        'spent',
    )
    search_fields = (
        'customer', 'lot'
    )
    list_filter = ('customer', 'lot',)
