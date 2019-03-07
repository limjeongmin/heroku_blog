from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Photo
from .forms import PhotoForm
from photos.forms import CreateUserForm
from django.contrib import messages

def detail(requset, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    context = dict()
    context['photo'] = photo
    return render(requset, 'photos/detail.html', context)


def create(request):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    if request.method == 'GET':
        form = PhotoForm()
    elif request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('photos:detail', photo_id=photo.pk)

    context = {
        'form': form
    }
    return render(request, 'photos/edit.html', context)


def index(request):
    photos = Photo.objects.all()
    context = dict()
    context['photos'] = photos
    return render(request, 'photos/list.html', context)


def delete(request):
    # 1. POST요청으로온 pk를 받아서 photo모델이 맞는지 찾는다.
    # 2. 틀릴경우 , 다시 해당 페이지/   맞을경우 , photo를 삭제하고 , list 페이지를 보여준다.
    if request.method == 'POST':
        photo_id = request.POST['photo_id']
        try:
            photo = Photo.objects.get(pk=photo_id, user=request.user)
        except :

            return redirect('photos:detail', pk=photo_id)
        photo.delete()
    return redirect('photos:list')


def signup(request):
    if request.method == "POST":
        createuserform = CreateUserForm(request.POST)
        if createuserform.is_valid():
            user = createuserform.save(commit=False)
            user.save()

            return HttpResponseRedirect(reverse("signup_ok"))
    elif request.method == "GET":
        createuserform = CreateUserForm()
    return render(request, "registration/signup.html", {
        "createuserform": createuserform,

    })
