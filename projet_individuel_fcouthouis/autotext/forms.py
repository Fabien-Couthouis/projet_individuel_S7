from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class PostUrlListForm(forms.Form):
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
