from django.db import models
from django.urls import reverse

# Create your models here.





class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="items/images", default="")
    number = models.IntegerField(default=0)
    category = models.CharField(max_length=100, default='Default Category')

    def get_url(self):
        return reverse('product_detail', args=[self.number])


    def __str__(self):
        return self.product_name










