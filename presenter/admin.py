from django.contrib import admin
from .models import Slide

class SlideAdmin(admin.ModelAdmin):
	list_display = ('numberofslides','currentslide')

admin.site.register(Slide, SlideAdmin)