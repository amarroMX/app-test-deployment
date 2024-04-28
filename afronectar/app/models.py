from django.db import models
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator


class Category(MPTTModel):
    """ Product's category"""
    parent = TreeForeignKey("self", on_delete=models.PROTECT)
    title = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.CharField(max_length=500, db_index=True)
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Category< title:{self.title}, parent:{self.parent.title}, created:{self.created}, level:{self.get_level}>"

    def __repr__(self) -> str:
        return f"Category< title:{self.title}, parent:{self.parent.title}, created:{self.created}, level:{self.get_level}>"


class Product(models.Model):
    """ Product"""
    title = title = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(unique=True, db_index=True)
    origin = models.CharField(max_length=20, unique=True, db_index=True)
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)


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




class Batch(models.Model):
    """Production batch for coffee items"""
    Item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    expire_on = models.DateTimeField()
    manufactured_on = models.DateTimeField()
    created = models.DateTimeField(auto_now=True)