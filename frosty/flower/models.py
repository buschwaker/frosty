from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class MyUser(AbstractUser):
    """Кастомная модель пользователя"""
    customer = 'customer'
    seller = 'seller'

    ROLE_CHOICES = [
        (customer, 'Покупатель'),
        (seller, 'Продавец'),
    ]

    role = models.CharField(
        choices=ROLE_CHOICES, default=customer,
        max_length=8, verbose_name='Роль'
    )

    is_cleaned = False

    def __str__(self):
        return f'{self.username}'

    def show_spent_by_user(self):
        """Возвращает общую сумму, потраченную пользователем"""
        spent = 0
        for deal in self.deals.all():
            spent += float(deal.spent)
        return int(spent)

    def show_raised_by_user(self):
        """Возвращает общую сумму, заработанную пользователем"""
        raised = 0
        for deal in Deal.objects.filter(lot__seller__exact=self):
            raised += float(deal.spent)
        return int(raised)

    def change_role(self):
        """Позволяет сменить роль пользователю"""
        if self.role == self.customer:
            self.role = self.seller
        else:
            self.role = self.customer
        self.save()

    def clean(self):
        """Поднимает ошибку при попытке поменять роль пользователя
        на покупателя, который будучи продавцом имеет незакрытые лоты
         """
        if self.role == self.customer and self.items.exists():
            raise ValidationError(
                'У пользователя, которому вы хотите'
                ' сменить роль на "клиент" есть активные лоты!'
            )
        self.is_cleaned = True

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.clean()
        super().save(*args, **kwargs)


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания и текст комментария."""
    text = models.TextField(
        'Текст комментария', help_text='Введите текст комментария', )
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    is_cleaned = False

    def __str__(self):
        return self.text[:15]

    class Meta:
        abstract = True
        ordering = ['-created']


class Flower(models.Model):
    """Модель цветка"""
    name = models.CharField(max_length=25, verbose_name='Название')

    white = 'white'
    red = 'red'
    orange = 'orange'
    yellow = 'yellow'
    green = 'green'
    blue = 'blue'
    violet = 'violet'
    pink = 'pink'
    black = 'black'

    COLOUR_CHOICES = [
        (white, 'белый'),
        (red, 'красный'),
        (orange, 'оранжевый'),
        (yellow, 'желтый'),
        (green, 'зеленый'),
        (blue, 'синий/голубой'),
        (violet, 'фиолетовый'),
        (pink, 'розовый'),
        (black, 'черный'),
    ]

    colour = models.CharField(
        choices=COLOUR_CHOICES,
        max_length=6, verbose_name='Цвет', default=white
    )

    def __str__(self):
        return f'{self.name} - {self.colour}'

    class Meta:
        verbose_name_plural = 'Цветы'
        verbose_name = 'Цветок'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'colour'],
                name='unique_name_colour')
        ]
        ordering = ['name']


class Item(models.Model):
    """Модель товара"""
    seller = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        verbose_name='Продавец', related_name='items')
    flower = models.ForeignKey(
        Flower, on_delete=models.CASCADE,
        verbose_name='Товар', related_name='items')
    amount = models.IntegerField(
        validators=[MinValueValidator(0), ], verbose_name='Количество'
    )
    price = models.FloatField(
        validators=[MinValueValidator(0), ], verbose_name='Цена за штуку'
    )
    visible = models.BooleanField(default=True, verbose_name='Показывать?')

    is_cleaned = False

    def __str__(self):
        return f'{self.seller} - {self.flower} - {self.amount}'

    @classmethod
    def show_all_available_items(cls):
        """Метод класса, возвращает список всех нескрытых лотов"""
        return cls.objects.filter(visible=True)

    def clean(self):
        """Проверяет, что лот не создан с пользователем
        в роли покупатель в качестве продавца
        """
        if self.seller.role == 'customer':
            raise ValidationError("Клиент не может продавать товары")
        self.is_cleaned = True

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Лоты'
        verbose_name = 'Лот'
        constraints = [
            models.UniqueConstraint(
                fields=['seller', 'flower'],
                name='unique_seller_flower')
        ]
        ordering = ['seller', 'flower']


class CommentToItem(CreatedModel):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE,
        verbose_name='товар', related_name='comments',
    )
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        verbose_name='Автор', related_name='comments_to_item',
    )

    def clean(self):
        """Проверяет, что комментарий не оставлен на скрытом товаре"""
        if self.item.visible is False:
            raise ValidationError("Нельзя комментировать невидимые товары!")
        self.is_cleaned = True

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Комментарии к товару'
        verbose_name = 'Комментарий к товару'


class CommentToSeller(CreatedModel):
    seller = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        verbose_name='Продавец', related_name='comments',
    )
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        verbose_name='Автор', related_name='comments_to_seller',
    )

    def clean(self):
        """Проверяет, что комментарий не оставлен на покупателе"""
        if self.seller.role == 'customer':
            raise ValidationError("Можно комментировать только продавцов!")
        self.is_cleaned = True

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Комментарии к продавцу'
        verbose_name = 'Комментарий к продавцу'


class Deal(models.Model):
    customer = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        verbose_name='Клиент', related_name='deals',
    )
    lot = models.ForeignKey(
        Item, on_delete=models.CASCADE,
        verbose_name='Товар', related_name='deals',
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(0), ], verbose_name='Количество'
    )

    is_cleaned = False

    @property
    def spent(self):
        """Поле, работающее на чтение, возвращает сумму сделки"""
        return self.amount * self.lot.price

    spent.fget.short_description = 'Потрачено на совершение сделки'

    @staticmethod
    def update_amount_lot(pk, amount):
        """При совершении сделки обновляется
        количество доступных товаров в соответствующем лоте
        """
        instance = Item.objects.get(pk=pk)
        instance.amount -= amount
        instance.save()

    @classmethod
    def full_info(cls):
        """Метод класса, возвращается вся информация о проведенных сделках:
        Для каждого продавца выводится список покупателей
        с суммой потраченной при совершении сделки
        Также выводится общая сумма, заработанная продавцом
        """
        info = 'Информация по сделкам:\n'
        for seller in MyUser.objects.filter(role='seller'):
            info += f'\nКлиенты {seller} потратили каждый:\n'
            for deal in cls.objects.filter(lot__seller=seller):
                info += (f'{deal.customer} - '
                         f'{int(deal.spent)} на {deal.lot.flower}\n')
            info += (f'Итого {seller} заработал'
                     f' {seller.show_raised_by_user()}\n')
        print(info)

    def clean(self):
        """Проверяет, что сделка не совершается в отношении скрытого товара
        или пользователем в роли продавца или не приобретается количество
        товара большее, чем доступно в лоте
        """
        if self.lot.visible is False:
            raise ValidationError("Нельзя покупать скрытые товары!")
        if self.customer.role != 'customer':
            raise ValidationError("Покупать могут только клиенты!")
        if (self.lot.amount - self.amount) < 0:
            raise ValidationError(
                'В лоте недостаточно товаров, купите меньшее количество!'
            )
        else:
            self.update_amount_lot(self.lot.pk, self.amount)
        self.is_cleaned = True

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Сделки'
        verbose_name = 'Сделка'
