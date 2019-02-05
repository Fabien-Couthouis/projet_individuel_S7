from django import forms


class PostUrlListForm(forms.Form):
    standards = [
        ('APA', 'APA'),
        ('AFNOR', 'AFNOR'),
    ]

    urlList = forms.CharField(
        widget=forms.Textarea())

    # generated_webography = forms.CharField(
    #     required=False,
    #     widget=forms.Textarea(attrs={'rows': 20, 'cols': 50}),
    #     disabled=True)
    # # initial="Cliquez sur le bouton 'Générer ma webographie' ")

    standard = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect(),
        choices=standards,
        initial=standards[0],
        label='Norme : '
    )
