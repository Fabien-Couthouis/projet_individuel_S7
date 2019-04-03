from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from itertools import chain
from django.template import loader
from django.http import HttpResponse

from .forms import UrlListForm
from .forms import IndexForm

from .forms import SignUpForm
from .forms import ReferenceForm
from .forms import WebographyForm

from .models.webography import Webography
from .models.referencePDF import ReferencePDF
from .models.referenceWeb import ReferenceWeb


def set_to_session(request, webography):
    ''' Set webography info into a session variable'''
    request.session['webography_id'] = webography.id
    request.session['webography_name'] = webography.name


def get_webography_from_session(request):
    webography_id = request.session['webography_id']
    webography = Webography.objects.get(id=webography_id)
    return webography


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = IndexForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = form.cleaned_data
            webography = Webography()
            webography.save()
            set_to_session(request, webography)
            webography.add_refererences_from_urls(
                raw_urls=data['urlList'])

            formatStyle = form.cleaned_data.get('format_style')
            if formatStyle == 'APA':
                webography_output = webography.get_formatted_webography()
            else:
                webography_output = webography.get_bibtex_webography()
            return render(request, 'autotext/index.html', {'form': form, 'webography_output': webography_output})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = IndexForm()

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
        template = loader.get_template('autotext/myReferences.html')

        if not request.session.get('webography_id', None):
            webographies = Webography.objects.filter(user=request.user)
            if webographies:
                # Take first webography
                webography = webographies[0]
                set_to_session(request, webography)
            else:
                context = {
                    'no_webography': 1,
                    'webography_form': WebographyForm(user=request.user),
                    'reference_form': ReferenceForm(),
                    'references_form': UrlListForm()
                }
                return HttpResponse(template.render(context, request))

        else:
            webography = get_webography_from_session(request)

        referencepdf_set = webography.referencepdf_set.all()
        referenceweb_set = webography.referenceweb_set.all()
        # # Chain the sets
        reference_set = list(
            chain(referencepdf_set, referenceweb_set))

        context = {
            'webography_form': WebographyForm(user=request.user),
            'reference_set': reference_set,
            'reference_form': ReferenceForm(),
            'references_form': UrlListForm()
        }
        return HttpResponse(template.render(context, request))


def setWebography(request):
    if request.method == 'POST':
        form = WebographyForm(request.POST, user=request.user)

        if form.is_valid():
            set_to_session(request, form.cleaned_data["webography"])

    return redirect('/myReferences')


def addReference(request):
    if request.method == 'POST':
        form = ReferenceForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            webography = get_webography_from_session(request)
            url = data["url"]
            bibtex_reference = data["bibtex_reference"]
            apa_reference = data["apa_reference"]

            webography.add_reference(
                url=url, apa_reference=apa_reference, bibtex_reference=bibtex_reference)

    return redirect("/myReferences")


def editReference(request):
    if request.method == 'POST':
        form = ReferenceForm(request.POST)

        if form.is_valid():
            reference = get_ref_object(request, "edit_ref")

            data = form.cleaned_data
            reference.url = data["url"]
            reference.bibtex_reference = data["bibtex_reference"]
            reference.apa_reference = data["apa_reference"]

            reference.save()

    return redirect("/myReferences")


def deleteReference(request):
    if request.method == 'POST':
        reference = get_ref_object(request, "delete_ref")
        reference.delete()
    return redirect("/myReferences")


def get_ref_object(request, action):
    ref_data = request.POST.get(action)

    if not ref_data:
        return None

    ref_id = ref_data.split(";")[0]
    ref_classtype = ref_data.split(";")[1]

    if "ReferencePDF" in ref_classtype:
        reference = ReferencePDF.objects.get(id=ref_id)
    elif "ReferenceWeb" in ref_classtype:
        reference = ReferenceWeb.objects.get(id=ref_id)
    else:
        reference = None

    return reference


def addWebography(request):
    if request.method == 'POST':
        form = WebographyForm(request.POST, user=request.user)

        if form.is_valid():
            data = form.cleaned_data
            webography = Webography(name=data['name'], user=request.user)
            webography.save()
            set_to_session(request, webography)

    return redirect("/myReferences")


def editWebography(request):
    if request.method == 'POST':
        form = WebographyForm(request.POST, user=request.user)

        if form.is_valid():
            webography = get_webography_from_session(request)
            data = form.cleaned_data
            webography.name = data["name"]
            webography.save()

    return redirect("/myReferences")


def deleteWebography(request):
    print("o")
    if request.method == 'POST':

        webography_id = request.session.get('webography_id', None)

        webography = Webography.objects.get(id=webography_id)
        webography.delete()
        # Reset session variable
        del request.session['webography_id']
    return redirect("/myReferences")


def addManyReferences(request):
    if request.method == 'POST':
        form = UrlListForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            webography = get_webography_from_session(request)
            webography.add_refererences_from_urls(
                raw_urls=data['urlList'])

    return redirect("/myReferences")
