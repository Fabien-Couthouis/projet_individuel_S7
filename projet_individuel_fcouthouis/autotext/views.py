from django.shortcuts import render
from .forms import PostUrlListForm
from .models.webography import Webography


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostUrlListForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = form.cleaned_data
            webographie = Webography(data['urlList'])
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
