from django.db import models

# auto_now_add adds date upon row creation
# auto_now adds date upon row modification

# Create your models here.
# Equivalent to a table called Users of type models with rows: id, username, and password.
class Users(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    date_joined = models.DateTimeField(auto_now_add=True)

class Posts(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=20000)
    poster = models.ForeignKey(Users, on_delete=models.CASCADE)

class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment_title = models.CharField(max_length=100)
    comment_text = models.TextField(max_length=5000)
    commenter = models.ForeignKey(Users, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)