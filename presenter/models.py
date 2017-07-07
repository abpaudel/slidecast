from django.db import models

class Slide(models.Model):
	numberofslides = models.IntegerField()
	currentslide = models.IntegerField()
