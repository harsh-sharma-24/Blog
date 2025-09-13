from django.db import models

# Create your models here.

class Post(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.AutoField(primary_key = True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author