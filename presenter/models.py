from django.contrib.auth.models import Permission, User
from django.db import models


class Presentation(models.Model):
    user = models.ForeignKey(User, default=1)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank = True, null = True)
    pdf_file = models.FileField()


    def __str__(self):
        return self.title


class Slide(models.Model):
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE)
    image_file = models.ImageField()
    order = models.IntegerField(default = 0)

class GoLive(models.Model):
	current_presentation = models.ForeignKey(Presentation, blank = True, null = True)
	current_slide = models.IntegerField(default = 1)