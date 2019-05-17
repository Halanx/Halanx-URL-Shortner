from django import forms
from .validators import valid_url


class SubmitUrl(forms.Form):
    url = forms.CharField(label="Submit URL",
                          validators=[valid_url],
                          widget=forms.TextInput(attrs={"placeholder": "Long URL",
                                                        "class": "form-control"}))

    short_code = forms.CharField(label="Custom Short Code",
                                 required=False,
                                 widget=forms.TextInput(attrs={"placeholder": "Optional Short Code",
                                                               "class": "form-control"}))
