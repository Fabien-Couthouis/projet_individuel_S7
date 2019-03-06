from django import forms


class PostUrlListForm(forms.Form):
    format_styles = [
        ('APA', 'APA'),
        ('BIB', 'BIBTEX'),
    ]

    urlList = forms.CharField(
        widget=forms.Textarea())

    # generated_webography = forms.CharField(
    #     required=False,
    #     widget=forms.Textarea(attrs={'rows': 20, 'cols': 50}),
    #     disabled=True)
    # # initial="Cliquez sur le bouton 'Générer ma webographie' ")

    format_style = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect(),
        choices=format_styles,
        initial=format_styles[0],
        label='Format : '
    )
