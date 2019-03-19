from django.shortcuts import render, redirect
from .forms import PostUrlListForm
from .forms import SignUpForm
from .forms import WebographyForm
from .models.webography import Webography
from django.contrib.auth import login, authenticate
from itertools import chain


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostUrlListForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = form.cleaned_data
            webographie = Webography(raw_urls=data['urlList'])
            webographie.save()
            webographie.generate_articles()

            formatStyle = form.cleaned_data.get('format_style')
            if formatStyle == 'APA':
                webography_output = webographie.get_formatted_webography()
            else:
                webography_output = webographie.get_bibtex_webography()
            return render(request, 'autotext/index.html', {'form': form, 'webography_output': webography_output})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PostUrlListForm()

    return render(request, 'autotext/index.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def myReferences(request):
    # Check if user is logged in
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else:
        if request.method == 'POST':
            form = WebographyForm(request.POST)
            if form.is_valid():
                form.save()

                referencepdf_set = Webography.objects.get(
                    user=request.user).referencepdf_set.all()
                referenceweb_set = Webography.objects.get(
                    user=request.user).referenceweb_set.all()

                reference_set = list(
                    chain(referencepdf_set, referenceweb_set))

                return render(request, 'autotext/myReferences.html', {'form': form, 'reference_set': reference_set})
        else:
            form = WebographyForm()
            return render(request, 'autotext/myReferences.html', {'form': form})
