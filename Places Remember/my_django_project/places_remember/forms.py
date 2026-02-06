"""Forms for places_remember app."""

from django import forms


class MemoryForm(forms.Form):
    """Form for adding a memory: title, comment, coordinates."""

    title = forms.CharField(
        max_length=200,
        label="Название места",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Название"}),
    )
    comment = forms.CharField(
        max_length=1000,
        label="Комментарий",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 4, "placeholder": "Ваши впечатления"}
        ),
    )
    lat = forms.FloatField(widget=forms.HiddenInput(), required=True)
    lng = forms.FloatField(widget=forms.HiddenInput(), required=True)
