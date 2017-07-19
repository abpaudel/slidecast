from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import PresentationForm, SlideForm, UserForm
from .models import Presentation, Slide, GoLive

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GoLiveSerializer


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
  
    
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
        

def create_presentation(request):
    if not request.user.is_authenticated():
        return render(request, 'presenter/login.html')
    else:
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


def create_slide(request, presentation_id):
    form = SlideForm(request.POST or None, request.FILES or None)
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    if form.is_valid():
        presentation_slides = presentation.slide_set.all()
        slide = form.save(commit=False)
        slide.presentation = presentation
        slide.image_file = request.FILES['image_file']
        file_type = slide.image_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'presentation': presentation,
                'form': form,
                'error_message': 'Image file must be PNG, JPG or JPEG',
            }
            return render(request, 'presenter/create_slide.html', context)

        slide.save()
        return render(request, 'presenter/detail.html', {'presentation': presentation})
    context = {
        'presentation': presentation,
        'form': form,
    }
    return render(request, 'presenter/create_slide.html', context)


def delete_presentation(request, presentation_id):
    presentation = Presentation.objects.get(pk=presentation_id)
    presentation.delete()
    presentations = Presentation.objects.filter(user=request.user)
    return render(request, 'presenter/index.html', {'presentations': presentations})


def delete_slide(request, presentation_id, slide_id):
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    slide = Slide.objects.get(pk=slide_id)
    slide.delete()
    return render(request, 'presenter/detail.html', {'presentation': presentation})


def detail(request, presentation_id):
    if not request.user.is_authenticated():
        return render(request, 'presenter/login.html')
    else:
        user = request.user
        presentation = get_object_or_404(Presentation, pk=presentation_id)
        return render(request, 'presenter/detail.html', {'presentation': presentation, 'user': user, 'slidecount': presentation.slide_set.count()})

def golive(request, presentation_id):
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    golive = get_object_or_404(GoLive)
    golive.current_presentation = presentation
    golive.current_slide = 1
    golive.save()
    return render(request, 'presenter/presenter.html', {'golive': golive, 'range': range(1, golive.current_presentation.slide_set.count()+1)})

def golive_viewer(request):
    golive = get_object_or_404(GoLive)
    return render(request, 'presenter/viewer.html', {'golive': golive, 'range': range(1, golive.current_presentation.slide_set.count()+1)})



def index(request):
    if not request.user.is_authenticated():
        return render(request, 'presenter/login.html')
    else:
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
    logout(request)
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
                login(request, user)
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