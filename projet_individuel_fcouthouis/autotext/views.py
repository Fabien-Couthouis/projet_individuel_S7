from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .forms import PostUrlListForm
from .models.webography import Webography

# from .models import Choice, Question


# def index(request):
#     return render(request, 'autotext/index.html', {''})


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostUrlListForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = form.cleaned_data
            webographie = Webography(data['urlList'])
            webography_output = webographie.generate(data['standard'])
            return render(request, 'autotext/index.html', {'form': form, 'webography_output': webography_output})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PostUrlListForm()

    return render(request, 'autotext/index.html', {'form': form})
