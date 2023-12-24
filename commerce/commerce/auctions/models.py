from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
# creating table for category#
class Category(models.Model):
    CategoryType = models.CharField(max_length=20)
    image = models.ImageField(blank=True,null=True,upload_to="category")
    overview = models.TextField(max_length=200,null=True)
    status = models.BooleanField(default=True)

    #__str__ : that return a string representation of any object
    def __str__(self):
        return self.CategoryType
    
#--creating table for listing--#
class CreateListing(models.Model):
    #title for received user title input
    title = models.CharField(max_length=24)
    #overview for received user item description input
    overview = models.TextField(max_length=200,null=True)
    #image for uploading user image input
    image = models.ImageField(blank=True,null=True)
    #category with foreignkey for link it with category table
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="category",blank=True,null=False)
    #price for received user item price input
    price = models.FloatField()
    # user variable foreignkey to link user with his data 
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="ListUser",blank=True,null=True)
    #statues of item
    status = models.BooleanField(default=True)
    #time created
    create_date = models.DateTimeField(auto_now_add=True)
    #WatchList
    WatchList = models.ManyToManyField(User,blank=True,null=True,related_name="user_list")
    #status
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title 

#comment model
class UserComment(models.Model):
    post=models.ForeignKey(CreateListing,on_delete=models.CASCADE,related_name="post_Comments")
    name = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_comment",blank=True,null=True)
    content  = models.TextField(max_length=255)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} comment on {self.post}"
    

class UserBid(models.Model):
    bid = models.FloatField()
    bidders  = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,related_name="bidder_user")
    item_price = models.ForeignKey(CreateListing,on_delete=models.CASCADE,related_name='price_old',blank=True,null=True)
    def __str__(self):
        return f"{self.bidders} bid on {self.item_price} with {self.bid}"