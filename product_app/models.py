from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
            
    def __str__(self):
        return self.name

class product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=400)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0, blank=False, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="products")
    slug = models.SlugField(unique=True, null = True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name