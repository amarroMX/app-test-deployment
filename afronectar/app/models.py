from django.db.models import F
from django.db import models
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator


class Category(MPTTModel):
    """ Product's category"""
    parent = TreeForeignKey("self", verbose_name='parent', help_text='select parent\'s category' , on_delete=models.PROTECT)
    title = models.CharField(max_length=50, verbose_name='title', help_text='category\'s title' , unique=True, db_index=True)
    slug = models.GeneratedField(
        expression=F("parent") +'-'+  F("title"),
        unique=True,
        output_field=models.FloatField(),
        db_persist=True,
    )
    description = models.CharField(max_length=500, verbose_name='description', help_text='category\'s description', db_index=True)
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Category< title:{self.title}, parent:{self.parent.title}, created:{self.created}, level:{self.get_level}>"

    def __repr__(self) -> str:
        return f"Category< title:{self.title}, parent:{self.parent.title}, created:{self.created}, level:{self.get_level}>"

class Product(models.Model):
    """ Product"""
    title = title = models.CharField(max_length=50, verbose_name='title', help_text='product\'s title', unique=True, db_index=True)
    description = models.TextField(unique=True, verbose_name='description', help_text='product\'s description', db_index=True)
    slug = models.GeneratedField(
        expression=F("title") +'-'+ F("origin"),
        output_field=models.FloatField(),
        unique=True,
        db_persist=True,
    )
    origin = models.CharField(max_length=20, unique=True, db_index=True)
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Product< title:{self.title}, origin:{self.origin}, created:{self.created}>"

    def __repr__(self) -> str:
        return f"Product< title:{self.title}, origin:{self.origin}, created:{self.created}>"

class Item(models.Model):
    """Product's variant item"""
    product = models.ForeignKey('Product', on_delete=models.PROTECT, related_name='items')
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=0, 
                message="minimum value for item's price is 0"
            ), 
            MaxValueValidator(
                limit_value=1000.00,
                message="maximum value for item's price is 1000.00"
            )
        ],
    )
    sku = models.CharField(max_length=15, unique=True, db_index=True)
    slug = slug = models.GeneratedField(
            expression=F("title") +'-'+ F("origin"),
            output_field=models.FloatField(),
            unique=True,
            db_persist=True,
    )
    manufactured = models.BooleanField(default=False)
    barcode = models.PositiveBigIntegerField(
            validators=MaxLengthValidator(
                limit_value=13,
                message="maximum length for item's barcode is 13"
            ))
    stars = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=0, 
                message="minimum value for item's rating is 0"
            ), 
            MaxValueValidator(
                limit_value=5,
                message="maximum value for item's rating is 5"
            )
        ],
    )
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)

class Property(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        help_text=_("few product's properties are already defined! Select as you whishe or add new ones."),
        max_length=50,
    )
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_("product's property value should be unique."), 
        max_length=50, 
        unique=True
    )
    items = models.ManyToManyField( Item,
                                    verbose_name='item', 
                                    help_text='product\'s items',
                                    related_name="properties")
    add_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class Sale(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='sales')
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='items_sales')
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)

class Batch(models.Model):
    """Production batch for coffee items"""
    Item = models.ForeignKey('Item', on_delete=models.CASCADE)
    created_by = models.ForeignKey('Users.user', on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    available_quantity = models.PositiveBigIntegerField(default=F('quantiy'))
    sold = models.BooleanField(default=False)
    expire_on = models.DateTimeField()
    manufactured_on = models.DateTimeField()
    created = models.DateTimeField(auto_now=True)

