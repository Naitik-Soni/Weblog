from django.db import models
from datetime import date

# Create your models here.
class UserRegister(models.Model):
    user_name = models.CharField(max_length=50)
    user_mail = models.CharField(max_length=50)
    user_pass = models.CharField(max_length=50)

class BlogContent(models.Model):
    user_mail = models.CharField(max_length=50)
    blog_title = models.CharField(max_length=150)
    blog_image = models.ImageField("BlogImage")
    blog_content = models.TextField()
    blog_date = models.DateField(default=date.today)
