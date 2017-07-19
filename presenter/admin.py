from django.contrib import admin
from .models import Presentation, Slide, GoLive

admin.site.register(Presentation)
admin.site.register(Slide)
admin.site.register(GoLive)
