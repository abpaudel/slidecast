from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SlideSerializer
from .models import Slide
from django.contrib.auth.decorators import login_required


def index(request):
	return render(request, 'presenter/index.html')


@login_required(login_url='/admin/')
def indexadmin(request):
	return render(request, 'presenter/admin.html')
	
	
class SlideData(APIView):

	def get(self, request):
		slides = get_object_or_404(Slide)
		serializer = SlideSerializer(slides, many = False)
		return Response(serializer.data)

	def post(self, request):
		slides = get_object_or_404(Slide)
		slides.currentslide = request.data.get("currentslide")
		slides.save()
		serializer = SlideSerializer(slides, many = False)
		return Response(serializer.data)
		
	