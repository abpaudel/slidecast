from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import PresentationForm, SlideForm, UserForm
from .models import Presentation, Slide, GoLive
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GoLiveSerializer


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
LOGIN_URL = '/cast/login/'
  
    
class SlideData(APIView):

    def get(self, request):
        slide = get_object_or_404(GoLive)
        serializer = GoLiveSerializer(slide, many = False)
        return Response(serializer.data)

    def post(self, request):
        slide = get_object_or_404(GoLive)
        slide.current_slide = request.data.get("current_slide")
        slide.save()
        serializer = GoLiveSerializer(slide, many = False)
        return Response(serializer.data)
  

@login_required(login_url=LOGIN_URL)
def create_presentation(request):
    form = PresentationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        presentation = form.save(commit=False)
        presentation.user = request.user
        presentation.save()
        return render(request, 'presenter/detail.html', {'presentation': presentation})
    context = {
        "form": form,
    }
    return render(request, 'presenter/create_presentation.html', context)


@login_required(login_url=LOGIN_URL)
def create_slide(request, presentation_id):
    form = SlideForm(request.POST or None, request.FILES or None)
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    if form.is_valid():
        files = request.FILES.getlist('image_file')
        for file in files:
            file_type = file.name.split('.')[-1]
            file_type = file_type.lower()
            if file_type in IMAGE_FILE_TYPES:
                slide = Slide()
                slide.image_file = file
                slide.presentation = presentation
                slide.save()
        context = {
            'presentation': presentation,
            'form': form,
       }
        return render(request, 'presenter/detail.html', {'presentation': presentation})
    else:
        context = {
            'presentation': presentation,
            'form': form,
        }
    return render(request, 'presenter/create_slide.html', context)


@login_required(login_url=LOGIN_URL)
def delete_presentation(request, presentation_id):
    presentation = Presentation.objects.get(pk=presentation_id)
    presentation.delete()
    presentations = Presentation.objects.filter(user=request.user)
    return render(request, 'presenter/index.html', {'presentations': presentations})


@login_required(login_url=LOGIN_URL)
def delete_slide(request, presentation_id, slide_id):
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    slide = Slide.objects.get(pk=slide_id)
    slide.delete()
    return render(request, 'presenter/detail.html', {'presentation': presentation})


@login_required(login_url=LOGIN_URL)
def detail(request, presentation_id):
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    context = {
        'presentation': presentation,
        'slidecount': presentation.slide_set.count()
    }
    return render(request, 'presenter/detail.html', context)



@login_required(login_url=LOGIN_URL)
def golive(request, presentation_id, current_slide=1):
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    try:
        golive = GoLive.objects.get()
    except GoLive.DoesNotExist:
        golive = GoLive()
    golive.current_presentation = presentation
    golive.current_slide = current_slide
    golive.save()
    rng = range(1, golive.current_presentation.slide_set.count()+1)
    return render(request, 'presenter/presenter.html', {'golive': golive, 'range': rng})
            

def golive_viewer(request):
    golive = get_object_or_404(GoLive)
    try:
        rng = range(1, golive.current_presentation.slide_set.count()+1)
        context = {
            'golive': golive,
            'range': rng
        }
    except AttributeError:
        context = {'golive': golive }
    return render(request, 'presenter/viewer.html', context)


@login_required(login_url=LOGIN_URL)
def onair(request):
    try:
        onair = GoLive.objects.get()
    except GoLive.DoesNotExist:
        onair = GoLive()
        onair.save()
    return render(request, 'presenter/onair.html', {'onair': onair})


@login_required(login_url=LOGIN_URL)
def stoplive(request):
    onair = get_object_or_404(GoLive)
    onair.current_presentation = None
    onair.save()
    return render(request, 'presenter/onair.html', {'presentation': onair.current_presentation})


@login_required(login_url=LOGIN_URL)
def index(request):
    presentations = Presentation.objects.filter(user=request.user)
    slide_results = Slide.objects.all()
    query = request.GET.get("q")
    if query:
        presentations = presentations.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
        return render(request, 'presenter/index.html', {
            'presentations': presentations,
        })
    else:
        return render(request, 'presenter/index.html', {'presentations': presentations})


def logout(request):
    auth_logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'presenter/login.html', context)



def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                presentations = Presentation.objects.filter(user=request.user)
                return render(request, 'presenter/index.html', {'presentations': presentations})
            else:
                return render(request, 'presenter/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'presenter/login.html', {'error_message': 'Invalid login'})
    return render(request, 'presenter/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                presentations = Presentation.objects.filter(user=request.user)
                return render(request, 'presenter/index.html', {'presentations': presentations})
    context = {
        "form": form,
    }
    return render(request, 'presenter/register.html', context)