from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    pdf = models.FileField(upload_to='books/pdf/')

    def __str__(self):
        return self.title
