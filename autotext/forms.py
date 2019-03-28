from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .models.reference import Reference
from .models.referencePDF import ReferencePDF

from .models.webography import Webography


class PostUrlListForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

    format_styles = [
        ('APA', 'APA'),
        ('BIB', 'BIBTEX'),
    ]

    urlList = forms.CharField(
        widget=forms.Textarea())

    format_style = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect(),
        choices=format_styles,
        initial=format_styles[0],
        label='Format : '
    )


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

    username = forms.CharField(help_text="Requis. 150 caractères maximum. Uniquement des lettres, nombres et les caractères « @ », « . », « + », « - » et « _ ».",
                               widget=forms.TextInput(
                                   attrs={'placeholder': "Nom d'utilisateur", 'icon': 'fa fa-user'}))

    password1 = forms.CharField(help_text="Minimum 8 caractères.", widget=forms.PasswordInput(
        attrs={'placeholder': 'Mot de passe', 'icon': 'fa fa-lock'}))
    password2 = forms.CharField(help_text="Même mot de passe que précédemment, pour vérification.", widget=forms.PasswordInput(
        attrs={'placeholder': 'Retapez le mot de passe', 'icon': 'fa fa-lock'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


class WebographyForm(ModelForm):
    class Meta:
        model = Webography
        fields = ['raw_urls', 'user']


class ReferenceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

    url = forms.URLField(required=True,
                         max_length=400, widget=forms.Textarea(attrs={'rows': 1, 'placeholder': 'Url'}))
    bibtex_reference = forms.CharField(required=False,
                                       widget=forms.Textarea(attrs={'placeholder': 'Réference bibtex (laisser vide pour une complétion automatique)'}))
    apa_reference = forms.CharField(required=False,
                                    widget=forms.Textarea(attrs={'placeholder': 'Réference apa (laisser vide pour une complétion automatique)'}))
    ref_id = forms.CharField(required=False)
