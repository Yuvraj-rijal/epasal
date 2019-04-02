

# from django.db import models
# from ckeditor.fields import RichTextField
# from sorl.thumbnail import ImageField
# from django.contrib.auth.models import User
#
# # Create your models here.
# class Category(models.Model):
#     title = models.CharField(max_length = 200)
#     image = models.ImageField(varchar = 200)
#     details =models.RichTextfield(maxlength = 250)
#
#
#     # def __str__(self):
#     #     return self.title
#
#
# class Product(models.Model):
#     title = models.CharField(max_length=255)
#     price = models.IntegerField(#max_digits=5)
#     strike_price = models.IntegerField(#max_digits=5)
#     availability =models.BooleanField()
#     brand=models.CharField(max_length=100)
#     short_intro=models.TextField(max_length=250)
#     sizes=RichTextField(max_length=255)
#     colors=models.CharField(max_length=255)
#     description=RichTextField()
#     category_id=models.Foreignkey(Category, on_delete=models.CASCADE)
#     deal_of_the_day=models.BOolean()
#     pub_date=models.DateTimeField(auto_created=True, auto_now=True)
#
# class ProductHasImage(models.Model):
#     image = ImageField()
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     rating = models.IntegerField()
#     comment = models.TextField()
#
# class Cart(models.Model):
#     product = models.ForeignKey(Product, on)
import math

from django.db import models
from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200)
    image = ImageField()
    details = RichTextField()

    class Meta:
        verbose_name_plural = 'Categories'

        def __str__(self):
           return self.title



class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    strike_price = models.IntegerField()
    availability = models.BooleanField()
    brand = models.CharField(max_length=50)
    short_intro = RichTextField()
    sizes = models.CharField(max_length=255)
    colours = models.CharField(max_length=255)
    description = RichTextField()
    deal_of_the_day = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name_plural = 'Product'

    def __str__(self):
            return self.title

    def image(self):
            return self.producthasimage_set.first().image

    def refined_colours(self):
        return self.colours.split(',')

    def refined_size(self):
        return self.size(',')

    def avg_review(self):
        out= math.ceil(self.producthasreview_set.aggregate(models.Avg('rating')).get('rating_avg',0))
        return math.ceil(out if out else 0)


    def star(self):
        return range(int(self.avg_review()))

    def recent_reviews(self):
        return self.producthasreview_set.order_by('-id')[:3]


class ProductHasImage(models.Model):
    image = ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # def image(self):
    #     return self.producthasimage_set.first().image


class ProductHasReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def star(self):
        return range(self.rating)


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qty = models.IntegerField()


