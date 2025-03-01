from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=200)
    content=models.TextField()
    link=models.CharField(max_length=200)
    summary = models.TextField()
    keywords=models.TextField()
    sentiment=models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    ids=models.IntegerField()

    def __str__(self):
        return self.title
