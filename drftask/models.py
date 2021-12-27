from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    submdate = models.DateTimeField()
    marks = models.IntegerField()

    def __str__(self):
     return str(self.title)

    @property
    def get_task(self):
        task = self.task_set.all()
        return task


class Task(models.Model):
    name = models.CharField(max_length=200)
    completed = models.BooleanField(default=False, blank=True, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='task', blank=True, null=True)

    def __str__(self):
        return str(self.name)


# class Task(models.Model):
#     title = models.CharField(max_length=200)
#     completed = models.BooleanField(default=False,blank=True,null=True)
#     def __str__(self):
#         return self.title


class Category(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=100)

    def __str__(self):
        return str(self.title)


class Subcategory(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory')

    def __str__(self):
        return str(self.title)


class Subsubcategory(models.Model):
    title = models.CharField(max_length=200)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='subsubcategory')

    def __str__(self):
        return str(self.title)


class Product(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Favourite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product)


class Customer(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=250, null=True)

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    total_quantity = models.IntegerField()
    grand_total = models.IntegerField()
    customorder = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='customorder')

    def __str__(self):
        return str(self.id)


class Orderitem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='orderitems')
    
    def __str__(self):
        return str(self.order)


class Rproducts(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100)
    most_fav = models.BooleanField(blank=True, null=True)
    fav = models.BooleanField(blank=True, null=True)
    least = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Review(models.Model):
    rating = models.IntegerField()
    product = models.ForeignKey(Rproducts, on_delete=models.CASCADE, blank=True, null=True,related_name='product')
    
    def __str__(self):
        return str(self.rating)


class Post(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.title)


class Postmedia(models.Model):
    picture = models.ImageField(null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='post')
    
    def __str__(self):
        return str(self.post.title)


class Productthumbnail(models.Model):
    picture = models.ImageField(null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return str(self.picture)
