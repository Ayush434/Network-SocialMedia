from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Followers(models.Model):
    user = models.CharField(max_length=50,blank=True, null=True)
    follower = models.CharField(max_length=50,blank=True, null=True)
    
    def __str__(self):
        return f"user: {self.user} have a new follower - > {self.follower}"
    
    def serialize(self):
        return {
            "user": self.user,
            "follower": self.follower
        }
    
class Following(models.Model):
    user = models.CharField(max_length=50,blank=True, null=True)
    following = models.CharField(max_length=50,blank=True, null=True)
    
    def __str__(self):
        return f"user: {self.user} wants to follow {self.following}"
    
    def serialize(self):
        return {
            "user": self.user,
            "following": self.following
        }
    

class Posts(models.Model):
    user = models.CharField(max_length=50,blank=True, null=True)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)
    num_of_likes = models.IntegerField(default = '0')
    
    def __str__(self):
        return f"user: {self.user}, num_of_likes {self.num_of_likes}, description: {self.description}, id: {self.id}"
    
    def serialize(self):
        return {
            "user": self.user,
            "description": self.description,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "id": self.id,
            "likes": self.num_of_likes
        }
        
class Likes(models.Model):
    user = models.ManyToManyField(User, blank=True)
    post =  models.ForeignKey(Posts, on_delete= models.CASCADE, blank=True, null=True)
    
    
    def __str__(self):
        return f"user: {self.user} Liked {self.post}"
    
    # def serialize(self):
    #     return {
    #         "user": self.user,
    #         "post": self.post,
    #         "like": self.like,
    #         "id": self.id
    #     }