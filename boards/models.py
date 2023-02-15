from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name    # Chi hien thi 'name'
    


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True) # Auto lay thoi gian tao moi de gan gia tri
    board = models.ForeignKey(Board, related_name='topics', null=True, on_delete=models.SET_NULL)
    starter = models.ForeignKey(User, related_name='topics', null=True, on_delete=models.SET_NULL)


class Post(models.Model):
    message = models.CharField(max_length=5000)
    topic = models.ForeignKey(Topic, related_name='posts', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='posts', null=True, on_delete=models.SET_NULL)
    update_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    
